## Edited from https://github.com/acoustid/mbslave

import tarfile
import os
import psycopg2
import logging
import subprocess
from typing import Optional
import configparser as ConfigParser

logger = logging.getLogger(__name__)


class DatabaseConfig(object):

    def __init__(self) -> None:
        self.name = 'musicbrainz'
        self.host: Optional[str] = None
        self.port: Optional[int] = None
        self.user: str = 'musicbrainz'
        self.password: Optional[str] = None
        self.admin_user: str = 'postgres'
        self.admin_password: Optional[str] = None

    def create_psycopg2_kwargs(self, superuser=False, no_db=False):
        kwargs = {}
        if superuser:
            kwargs['user'] = self.admin_user
            if self.admin_password is not None:
                kwargs['password'] = self.admin_password
        else:
            kwargs['user'] = self.user
            if self.password is not None:
                kwargs['password'] = self.password
        if not no_db:
            kwargs['database'] = self.name
        if self.host is not None:
            kwargs['host'] = self.host
        if self.port is not None:
            kwargs['port'] = self.port
        return kwargs

    def read(self, parser, section):
        self.name = parser.get(section, 'name')
        if parser.has_option(section, 'host'):
            self.host = parser.get(section, 'host')
        if parser.has_option(section, 'port'):
            self.port = parser.getint(section, 'port')
        if parser.has_option(section, 'user'):
            self.user = parser.get(section, 'user')
        if parser.has_option(section, 'password'):
            self.password = parser.get(section, 'password')
        if parser.has_option(section, 'admin_user'):
            self.admin_user = parser.get(section, 'admin_user')
        if parser.has_option(section, 'admin_password'):
            self.admin_password = parser.get(section, 'admin_password')

class SchemasConfig(object):

    def __init__(self):
        self.mapping = {}
        self.ignored_schemas = set()

    def name(self, name):
        return self.mapping.get(name, name)

    def read(self, parser, section):
        for name, value in parser.items(section):
            if name == 'ignore':
                self.ignored_schemas = set([s.strip() for s in value.split(',')])
            else:
                self.mapping[name] = value


class TablesConfig(object):

    def __init__(self):
        self.ignored_tables = set()

    def read(self, parser, section):
        for name, value in parser.items(section):
            if name == 'ignore':
                self.ignored_tables = set([s.strip() for s in value.split(',')])

class MusicBrainzConfig(object):

    def __init__(self):
        self.base_url = 'https://metabrainz.org/api/musicbrainz/'
        self.token = ''

    def read(self, parser, section):
        if parser.has_option(section, 'base_url'):
            self.base_url = parser.get(section, 'base_url')
        if parser.has_option(section, 'token'):
            self.token = parser.get(section, 'token')

class Config(object):

    def __init__(self, paths):
        self.cfg = ConfigParser.RawConfigParser()
        for path in paths:
            if os.path.exists(path):
                self.cfg.read(path)
        self.get = self.cfg.get
        self.has_option = self.cfg.has_option

        self.database = DatabaseConfig()
        self.musicbrainz = MusicBrainzConfig()
        self.tables = TablesConfig()
        self.schemas = SchemasConfig()

        if self.cfg.has_section('database'):
            self.database.read(self.cfg, 'database')
        elif self.cfg.has_section('DATABASE'):
            self.database.read(self.cfg, 'DATABASE')

        if self.cfg.has_section('musicbrainz'):
            self.musicbrainz.read(self.cfg, 'musicbrainz')
        elif self.cfg.has_section('MUSICBRAINZ'):
            self.musicbrainz.read(self.cfg, 'MUSICBRAINZ')

        if self.cfg.has_section('tables'):
            self.tables.read(self.cfg, 'tables')
        elif self.cfg.has_section('TABLES'):
            self.tables.read(self.cfg, 'TABLES')

        if self.cfg.has_section('schemas'):
            self.schemas.read(self.cfg, 'schemas')

    def connect_db(self, set_search_path=False, superuser=False, no_db=False):
        db = psycopg2.connect(**self.database.create_psycopg2_kwargs(superuser=superuser, no_db=no_db))
        if set_search_path:
            db.cursor().execute("SET search_path TO %s", (self.schemas.name('musicbrainz'),))
        return db


def connect_db(cfg, set_search_path=False, superuser=False, no_db=False):
    return cfg.connect_db(set_search_path=set_search_path, superuser=superuser, no_db=no_db)


def parse_name(config, table):
    if '.' in table:
        schema, table = table.split('.', 1)
    else:
        schema = 'musicbrainz'
    schema = config.schemas.name(schema.strip('"'))
    table = table.strip('"')
    return schema, table


def fqn(schema, table):
    return '%s.%s' % (schema, table)


def check_table_exists(db, schema, table):
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM pg_tables WHERE schemaname=%s AND tablename=%s", (schema, table))
    if not cursor.fetchone():
        return False
    return True


def load_tar(filename: str, db, config, ignored_schemas, ignored_tables):
    tar = tarfile.open(fileobj=filename, mode='r:bz2')
    cursor = db.cursor()
    for member in tar:
        if not member.name.startswith('mbdump/'):
            continue
        name = member.name.split('/')[1].replace('_sanitised', '')
        schema, table = parse_name(config, name)
        fulltable = fqn(schema, table)
        if schema in ignored_schemas:
            logger.info("Ignoring %s", name)
            continue
        if table in ignored_tables:
            logger.info("Ignoring %s", name)
            continue
        if not check_table_exists(db, schema, table):
            logger.info("Skipping %s (table %s does not exist)", name, fulltable)
            continue
        cursor.execute("SELECT 1 FROM %s LIMIT 1" % fulltable)
        if cursor.fetchone():
            logger.info("Skipping %s (table %s already contains data)", name, fulltable)
            continue
        logger.info("Loading %s to %s", name, fulltable)
        print(f"loading {name}")
        cursor.copy_expert('COPY {} FROM STDIN'.format(fulltable), tar.extractfile(member))
        db.commit()

def mbslave_auto_import_main(config: Config) -> None:
    db = connect_db(config)

    files = [
        'mbdump.tar.bz2',
        'mbdump-derived.tar.bz2',
    ]
    for file in files:
        load_tar(file, db, config, config.schemas.ignored_schemas, config.tables.ignored_tables)

def create_user(config: Config) -> None:
    logger.info("Creating user...")
    db = connect_db(config, superuser=True, no_db=True)
    db.autocommit = True
    cursor = db.cursor()
    cursor.execute(f"CREATE USER {config.database.user} PASSWORD %s", (config.database.password,))


def create_database(config: Config) -> None:
    logger.info("Creating database...")
    db = connect_db(config, superuser=True, no_db=True)
    db.autocommit = True
    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE {config.database.name} WITH OWNER {config.database.user}")
    cursor.execute(f"ALTER DATABASE {config.database.name} SET timezone TO 'UTC'")


def create_schemas(config: Config) -> None:
    db = connect_db(config)
    db.autocommit = True
    cursor = db.cursor()
    schemas = [
        'musicbrainz'
    ]
    for schema in schemas:
        if schema in config.schemas.ignored_schemas:
            continue
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {config.schemas.name(schema)}")


def run_script(script: str) -> None:
    subprocess.run(script, check=True, shell=True)


def run_sql_script(name: str, superuser: bool = False) -> None:
    if superuser:
        command = f'mbslave psql --superuser -f {name}'
    else:
        command = f'mbslave psql -f {name}'
    run_script(command)


def mbslave_init_main(config: Config) -> None:
    create_user(config)
    create_database(config)
    create_schemas(config)

    run_sql_script('Extensions.sql', superuser=True)
    run_sql_script('CreateSearchConfiguration.sql', superuser=True)

    sql_scripts = [

        # types
        ('musicbrainz', 'CreateCollations.sql'),
        ('musicbrainz', 'CreateTypes.sql'),

        # tables
        ('musicbrainz', 'CreateTables.sql')

    ]

    for schema, sql_script in sql_scripts:
        if schema in config.schemas.ignored_schemas:
            continue
        run_sql_script(sql_script)

    sql_scripts = [

        # primary keys
        ('musicbrainz', 'CreatePrimaryKeys.sql'),

        # functions
        ('musicbrainz', 'CreateFunctions.sql'),
        ('musicbrainz', 'CreateMirrorOnlyFunctions.sql'),

        # indexes
        ('musicbrainz', 'CreateIndexes.sql'),
        ('musicbrainz', 'CreateMirrorIndexes.sql'),

        # views
        ('musicbrainz', 'CreateViews.sql'),

        # triggers
        ('musicbrainz', 'CreateMirrorOnlyTriggers.sql'),

        # replication
        ('musicbrainz', 'ReplicationSetup.sql'),

    ]

    for schema, sql_script in sql_scripts:
        if schema in config.schemas.ignored_schemas:
            continue
        run_sql_script(sql_script)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    config = Config(['data.conf'])
    mbslave_init_main(config)
    mbslave_auto_import_main(config)
