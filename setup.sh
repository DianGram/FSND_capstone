database_url=postgresql://leegramling@localhost:5432/capstone

source udacity_env/bin/activate
export DATABASE_URL=$database_url
export FLASK_APP=app
export FLASK_ENV=development
