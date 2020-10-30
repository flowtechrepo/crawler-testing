# fb-scraper

NGINX Proxy for fb-scraper app
## Database
* MongoDB >=4.4.1 https://docs.mongodb.com
## Requirements
* Python >=3.6
* Pip3
## Usage

* pip install -r requirements.txt
* export FLASK_APP=group_search.py
* python3 -m flask run --host=0.0.0.0 --port=8082

### Postman ###
* url : ip-addr:8082/fb/group
* Method : GET

### Curl ###
* curl --location --request GET 'localhost:8082/fb/group'

### Environment Variables

The API will then be available at http://127.0.0.1:8000
