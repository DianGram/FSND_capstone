source udacity_env/bin/activate

DATABASE_URL="postgresql://leegramling@localhost:5432/capstone"
AUTH0_DOMAIN="fsnd-coffeeshop.auth0.com"
ALGORITHMS=['RS256']
API_AUDIENCE="Feed the Kids"
FLASK_APP=app
FLASK_ENV=development

export DATABASE_URL
export FLASK_APP
export FLASK_ENV

export AUTH0_DOMAIN
export ALGORITHMS
export API_AUDIENCE
