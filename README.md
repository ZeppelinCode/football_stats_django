# Demo Django application 
This application displays the ranking of all
teams in the Bundesliga.

On first startup it pulls all available information from this API: https://www.openligadb.de/ (https://bitbucket.org/anythingabout/openligadb-samples/overview/
). and stores it in a local Postgres database.

It then periodically (every hour) makes requests to the same API in order to pull any additional match updates that might have ocurred.

Presently it only works with one football season - 2018 but its functionality can be extended.

## Demo Set up
In order to run this demo, you need to have docker and docker-compose installed on your machine.

Clone this repo and run `docker-compose up -d`
in the root folder.

The application will start up in a couple of 
minutes after it has:
  - pulled all relevant docker images
  - installed all python dependencies

The application will become available on localhost:8000. If you get a 502 response
from nginx, pip is probably still installing
dependencies.

You can also use the admin console to add new data at localhost:8000/admin using these credentials:

username: superuser

password: very_secure_password

Keep in mind that changes you make might not be immediately visible (there's a 5 minute cache period for team statistics such as wins, losses, points, etc).



# Dev Set Up
If you'd like to work on this app, copy the very_secure_prod_settings.py file into fooball_stats/football_stats/local_settings.py and enter the db credentials.

You also need to have memcached installed and running.

## Future improvements
1. AJAX search bar
2. Improve search by using Unidecode to convert Fortuna Düsseldorf to Fortuna Dusseldorf for easier searching
3. The background API sync task is configured to run every hour. Ideally, it should run every minute if
   a match is in progress in order to display up to date info.
4. Actually store the team images locally.
5. Proper production logging and monitoring
6. The background data sync job should ideally be in a separate container.

## Copy paste database cleanup if needed
```sql
delete from teams_team;
delete from matches_location;
delete from matches_match;
delete from matches_goal;
delete from matches_outcome;
delete from matches_matchday_metadata;
```
