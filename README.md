# API documentation
https://bitbucket.org/anythingabout/openligadb-samples/overview/

# Set up
Copy settings_example.py into football_stats/.local_settings.py and fill in the database details and
the app secret.


# Copy paste database cleanup if needed
delete from teams_team;
delete from matches_location;
delete from matches_match;
delete from matches_goal;
delete from matches_outcome;
delete from matches_matchday_metadata;

docker run --name my-memcache -d -p 11211:11211 memcached
python manage.py process_tasks

# Future improvements
1. AJAX search bar
2. Improve search by using Unidecode to convert Fortuna Düsseldorf to Fortuna Dusseldorf for easier searching
3. The background API sync task is configured to run every hour. Ideally, it should run every minute if
   a match is in progress in order to display up to date info.
4. Actually store the team images locally.