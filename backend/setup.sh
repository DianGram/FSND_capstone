source ../udacity_env/bin/activate

DATABASE_URL="postgresql://leegramling@localhost:5432/capstone"
AUTH0_DOMAIN="fsnd-coffeeshop.auth0.com"
ALGORITHMS=['RS256']
API_AUDIENCE="Feed the Kids"
CLIENT_ID="Ml4B4ziACg6qKMsifIL1C7Xit8mnxqfD"
CLIENT_SECRET="VhTXg9ZuuDZf7OswQQJNI6xeGSK9S4aJHgiJNsUo_W9zRAt3frJt1ZRuBZZf55sc"
REDIRECT_URL="http://localhost:5000/callback"
#REDIRECT_URL="http://localhost:5000"
FLASK_APP=app
FLASK_ENV=development
ASSISTANT_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldQZklVRkdNS19KRU9BN0JDUExPZSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY29mZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5MWY4ZmU1NGMzMjIwYzY5NzRjM2FjIiwiYXVkIjoiRmVlZCB0aGUgS2lkcyIsImlhdCI6MTU4ODUyMTgzMywiZXhwIjoxNTg4NjA4MjMyLCJhenAiOiJNbDRCNHppQUNnNnFLTXNpZklMMUM3WGl0OG1ueHFmRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OnZvbHVudGVlciIsInBhdGNoOnRhc2siLCJwYXRjaDp2b2x1bnRlZXIiLCJwb3N0OnZvbHVudGVlciJdfQ.URVi17ZG_iRawdqGhPVovWSl2WdmudAd4WIRUl7EFYwgnWg3Ns6MAnSDppZHVch8ky-TxlnrG4q1Oqlz0FKz10QSN4bmJs8-u1OsfaH1lhgK6PBCt6zoOinf9a_yNPR7seAdiEMcMoL2q94fuwVgphT9tgHb870It4tSwBbfk30FHUFR-hZoCkgpouul_Az0O8WSbEqlwxfCWWEVQpX2zao1E5iV1z6OKIt38jJNj3ogWhPWznjErOebMY_rjWXiOxEs9zvf7tpujrSVIvl4m5Km1-kQ0HABf8VU_rbrMoBJJj8Kwscne6kuNz_t9kW94DSV6yMqG8V5MoT3HglJoQ
DIRECTOR_TOKEN=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldQZklVRkdNS19KRU9BN0JDUExPZSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtY29mZmVlc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5MGU1MTY3YTYxNTIwYzYxZTYxYjE1IiwiYXVkIjoiRmVlZCB0aGUgS2lkcyIsImlhdCI6MTU4ODUyMTk5NywiZXhwIjoxNTg4NjA4Mzk2LCJhenAiOiJNbDRCNHppQUNnNnFLTXNpZklMMUM3WGl0OG1ueHFmRCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2siLCJkZWxldGU6dm9sdW50ZWVyIiwiZ2V0OnZvbHVudGVlciIsInBhdGNoOnRhc2siLCJwYXRjaDp2b2x1bnRlZXIiLCJwb3N0OnRhc2siLCJwb3N0OnZvbHVudGVlciJdfQ.jFD4QQZQe5sK7nep377L8vqVW-ALIqijkDE5JK6VM68a53vxyeK1aHs1NF40f3l00UXa684ZEzD4WAzCkitUmQAAEwp_aDQgJ-N6jFvGbyjJLCfiabTCYJ9AxW0MAraefh9Q9Oydnc3VKotyQ3ybB7-HhLSKi8_YoTMSLXC58scEMRWET7CLNJZ-7tgLhpOisufAWJtw3rA_kswp8Zr9eu2wjhyP6OLnjMexRPlL6vvHoqYOY1ccKZX_TbvpCFZi5-RGWU0PIZO25FCAxC28IacmTg8BPYKOR8EfwqTrP8cK1Dd3vcdbfEAWEYX9xW5p8wBAF6KcjOKWpSm9QJpL5Q

export DATABASE_URL
export FLASK_APP
export FLASK_ENV

export AUTH0_DOMAIN
export ALGORITHMS
export API_AUDIENCE
export CLIENT_ID
export CLIENT_SECRET
export REDIRECT_URL

export ASSISTANT_TOKEN
export DIRECTOR_TOKEN
