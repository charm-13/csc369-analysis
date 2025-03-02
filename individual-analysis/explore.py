import json
import sqlalchemy

from database import engine

def map_names():
    map = [
        {"sp_name": 'Nudnik', "mb_name": None},
        {"sp_name": 'DAESUNG', "mb_name": '강대성'},
        {"sp_name": 'SEUNGRI', "mb_name": "이승현"},
        {"sp_name": 'Grant-Lee Phillips', "mb_name": None},
        {"sp_name": 'Iceland Symphony Orchestra', "mb_name": None},
        {"sp_name": 'hey daisy', "mb_name": None},
        {"sp_name": 'WINEHOUSE', "mb_name": None},
        {"sp_name": 'Francois Kevorkian', "mb_name": "François Kevorkian"},
        {"sp_name": 'Lexie Liu', "mb_name": "刘柏辛Lexie"},
        {"sp_name": 'Ryllz', "mb_name": None},
        {"sp_name": 'bunyamiwn', "mb_name": None},
        {"sp_name": '沈以誠', "mb_name": None},
        {"sp_name": 'Hyunjin', "mb_name": "현진"},
        {"sp_name": 'Luis R Conriquez', "mb_name": "Luis R. Conriquez"},
        {"sp_name": 'Taeko Onuki', "mb_name": "大貫妙子"},
        {"sp_name": 'Kidsnot$aints.', "mb_name": None},
        {"sp_name": 'DāM-FunK', "mb_name": None},
        {"sp_name": 'Cise Starr', "mb_name": "Cise Star"},
        {"sp_name": 'xole', "mb_name": None}, # 1,326 monthly listeners
        {"sp_name": 'K-391', "mb_name": None}, # 4.4M montly listeners
        {"sp_name": 'Housing Co.', "mb_name": None},
        {"sp_name": 'Zhang Bichen', "mb_name": None},
        {"sp_name": 'Olivia Herdt', "mb_name": None},
        {"sp_name": 'Skipping Breakfast', "mb_name": None}, # 133 monthly listeners
        {"sp_name": 'Ne-Yo', "mb_name": None}, # 37.8M monthly listeners
        {"sp_name": '妖艶金魚', "mb_name": None},
        {"sp_name": 'ZAYLE', "mb_name": None},
        {"sp_name": 'Gerry Mulligan And His Sextet', "mb_name": "Gerry Mulligan's New Sextet"},
        {"sp_name": 'Jay Jay Pistolet', "mb_name": "Justin Hayward-Young"},
        {"sp_name": 'LCN!', "mb_name": None},
        {"sp_name": 'Miki Matsubara', "mb_name": "松原みき"},
        {"sp_name": '(G)I-DLE', "mb_name": None},
        {"sp_name": 'Lewberger', "mb_name": None},
        {"sp_name": 'G-DRAGON', "mb_name": None},
        {"sp_name": 'Kytoon', "mb_name": None},
        {"sp_name": 'KSLV Noh', "mb_name": "KSLV"},
        {"sp_name": 'Seungmin', "mb_name": "승민"},
        {"sp_name": 'Sarah Maddack', "mb_name": None},
        {"sp_name": 'moonseophwang', "mb_name": None},
        {"sp_name": 'Micah Palace', "mb_name": None}, 
        {"sp_name": 'Eason Chan', "mb_name": "陳奕迅"},
        {"sp_name": 'Francis Nola', "mb_name": None},
        {"sp_name": 'Field Daze', "mb_name": None}, # 380 monthly listeners
        {"sp_name": 'saturn 17', "mb_name": None}, # saturn 15 but no saturn 17 ?
        {"sp_name": 'Garrett.', "mb_name": None},
        {"sp_name": 'Glenn Callin', "mb_name": None},
        {"sp_name": 'Jack Vitek', "mb_name": None}, # 383 monthly listeners
        {"sp_name": 'Lisa Ono', "mb_name": "小野リサ"},
        {"sp_name": '物語シリーズ', "mb_name": None},
        {"sp_name": 'Fujii Kaze', "mb_name": None},
        {"sp_name": "j'san", "mb_name": None},
        {"sp_name": 'Eric Chou', "mb_name": "周興哲"},
        {"sp_name": "Snail's House", "mb_name": None},
        {"sp_name": 'Nam Woo-hyun', "mb_name": "남우현"},
        {"sp_name": 'ziproom', "mb_name": None},
        {"sp_name": 'Dolly Ave', "mb_name": None},
        {"sp_name": 'RANI ADI', "mb_name": None},
        {"sp_name": 'A Si', "mb_name": "阿肆"},
        {"sp_name": 'WayV', "mb_name": "威神V"},
        {"sp_name": 'Feyesal', "mb_name": None},
        {"sp_name": 'Edward Sharpe & The Magnetic Zeros', "mb_name": "Edward Sharpe and the Magnetic Zeros"},
        {"sp_name": 'D.T.E', "mb_name": 'D.T.E.'},
        {"sp_name": 'J.BASS', "mb_name": 'J. Bass'},
        {"sp_name": 'Changbin (Stray Kids)', "mb_name": '창빈'},
        {"sp_name": "Her's", "mb_name": None},
        {"sp_name": "aaron's book club", "mb_name": None},
        {"sp_name": 'cansisco', "mb_name": None},
        {"sp_name": 'Madilyn', "mb_name": None},
        {"sp_name": '江皓南', "mb_name": None},
        {"sp_name": 'U SUNGEUN', "mb_name": '유성은'},
        {"sp_name": 'Circadian Clock', "mb_name": None},
        {"sp_name": 'Kanye West', "mb_name": 'Ye'},
        {"sp_name": 'A-Wall', "mb_name": 'A Wall'},
        {"sp_name": 'Sitting on Saturn', "mb_name": "Sitting On Stacy"},
        {"sp_name": 'Masayuki Suzuki', "mb_name": "鈴木雅之"},
        {"sp_name": 'Feezo', "mb_name": None}, # 1,322 monthly listeners
        {"sp_name": 'risy', "mb_name": None},
        {"sp_name": 'Eslabon Armado', "mb_name": 'Eslabón Armado'},
        {"sp_name": 'Shreea Kaul', "mb_name": None},
        {"sp_name": 'DanielFromSalem', "mb_name": None},
        {"sp_name": 'South Trees', "mb_name": None},
        {"sp_name": 'Shin Yong Jae', "mb_name": "신용재"},
        {"sp_name": '666FUCKTHECOPS', "mb_name": None},
        {"sp_name": 'SxDJI', "mb_name": None},
        {"sp_name": 'Captainsparklez', "mb_name": 'Jordan Maron'},
        {"sp_name": 'Mishaal Tamer', "mb_name": 'Mishaal'},
        {"sp_name": 'Sean Gerty', "mb_name": None},
        {"sp_name": 'Steveruu', "mb_name": None},
        {"sp_name": 'Uriel Barrera', "mb_name": None},
        {"sp_name": 'Zane Rosé', "mb_name": None},
        {"sp_name": 'Crawdads', "mb_name": None}, # 202 monthly listeners
        {"sp_name": 'Box House', "mb_name": None}, # 47 monthly listeners
        {"sp_name": 'Takashi Fujii', "mb_name": "藤井隆"},
        {"sp_name": 'NERONUS', "mb_name": None},
        {"sp_name": 'Billy Vicente', "mb_name": None},
        {"sp_name": 'HyunA&DAWN', "mb_name": None},
        {"sp_name": '11:11 Music Group', "mb_name": None},
        {"sp_name": 'Stage 11', "mb_name": None}, # 31 monthly listeners
        {"sp_name": '진동욱', "mb_name": None},
        {"sp_name": "Destiny's Child", "mb_name": None},
        {"sp_name": 'Lizardsmouth', "mb_name": None}, # 338 monthly listeners
        {"sp_name": 'Lucas Erickson', "mb_name": None}, # 384 monthly listeners
        {"sp_name": 'Mob Rich', "mb_name": None},
        {"sp_name": 'Emmett Mulrooney', "mb_name": None},
        {"sp_name": 'Nat Stephens', "mb_name": None}, # 55 monthly listeners
        {"sp_name": 'Jalen Tyree', "mb_name": "JalenTyree"},
        {"sp_name": 'Los Aptos', "mb_name": None},
        {"sp_name": 'Marc Wavy', "mb_name": None},
        {"sp_name": 'The Honeysticks', "mb_name": "Ricky Montgomery & The Honeysticks"},
        {"sp_name": "Girls' Generation", "mb_name": None}, # has every girls' generation member and a subgroup of gg ??
        {"sp_name": 'alt-J', "mb_name": None}
    ]
    
    with engine.begin() as conn:
        query = """
            CREATE TABLE IF NOT EXISTS musicbrainz.name_map (
                spotify_name        VARCHAR NOT NULL,
                musicbrainz_name    VARCHAR
            );
            
            INSERT INTO musicbrainz.name_map (spotify_name, musicbrainz_name)
            VALUES (:sp_name, :mb_name);
        """
        
        conn.execute(
            sqlalchemy.text(query),
            map
        )
        
        # ensure data was properly inserted
        print(
            conn.execute(
                sqlalchemy.text("""SELECT * FROM musicbrainz.name_map""")
            ).fetchall()
        )
        
def check_artists():
    json_file_path = f"./data/spotify-data/data/liked-artists.json"
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        artists = json.load(json_file)
        
    names = []
    for art in artists:
        print(art["name"])
        names.append(art["name"])
        
    names = list(set(names))
    
    with engine.begin() as conn:
        query = """
            SELECT * 
            FROM unnest(:names) AS n 
            WHERE LOWER(n) NOT IN (
                SELECT LOWER(name) FROM musicbrainz.artist   
            )
        """
        
        print("processing artist query...")
        res = conn.execute(
            sqlalchemy.text(query),
            {"names": names}
        ).fetchall()
        
        print(res)

if __name__ == "__main__":
    check_artists()
    map_names()