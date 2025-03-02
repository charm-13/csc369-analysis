# Data Cleaning and Exploration on Music Data

### Loading MusicBrainz PostgreSQL Data
When loading the MusicBrainz data into a postgres db;
* One row in `musicbrainz.label` failed a check constraint thus causing a partially built database, and
* The file with the `musicbrainz.artist` contents was missing an entire column defined in the schema.

To fix these errors, I removed the constraint on `musicbrainz.label` as it did not have a foreign key relation and was otherwise not applicable to my analysis.
I also removed the missing column from the schema for `musicbrainz.artist` since the data did not exist.

## Possible Gaps with MusicBrainz's Dataset
After getting everything set up properly, I wanted to see some possible gaps in MusicBrainz data.<br>
Though the dataset is large, I wanted to take a look at some of the major tables that I would be querying.

#### Artists
First, I checked to see if any of my liked artists did not appear in MusicBrainz' database. I did expect some smaller artists to not be in there, but quite a few known celebrities and popular bands seemed to not be in MusicBrainz database such as Grant-Lee Phillips, Destiny's Child, and (G)-IDLE.<br> 
Some surprisingly very popular names appeared in the list, too, including 'A-Wall', 'Kanye West', and 'JAY-Z'. However, after a quick search, some of those larger names appeared with a different spelling. 'A-Wall' appeared as 'A Wall', 'Kanye West' appeared as 'Ye', and 'JAY-Z' appeared on the list as 'Jay Z'. 

The discrpency in naming between Spotify and MusicBrainz could cause a few quality issues since some very big names do not appear and any normalization within those discrepencies would need to be done manually. Even so, for each Spotify artist that did not appear in the MusicBrainz dataset I manually searched for different spellings and other aliases to create a table with mappings from the Spotify name to the MusicBrainz name. Some artists, mostly smaller bands, did not appear in the MusicBrainz dataset at all. <br>
The smaller artists not being in the MusicBrainz dataset is not concerning. Rather, it can help answer my research questions.

However, there still were quite a few larger artists and bands not listed in the dataset. While it is extremely concering that MusicBrainz did not include icons like Destiny's Child in their dataset, those missing artists do not make up enough of my Spotify listening data for that lack of information to be a major concern.

#### Genres, Labels, and More
Data on music labels, genres, languages, and artist credit were up to the standard required to answer my research questions.
