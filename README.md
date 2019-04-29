# Set up

Copy settings_example.py into football_stats/.local_settings.py and fill in the database details and
the app secret.


delete from teams_team;
delete from matches_location;
delete from matches_match;
delete from matches_goal;
delete from matches_outcome;
delete from matches_matchday_metadata;

docker run --name my-memcache -d -p 11211:11211 memcached

https://bitbucket.org/anythingabout/openligadb-samples/overview/
python manage.py process_tasks