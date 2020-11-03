# fb-scraper

NGINX Proxy for fb-scraper app
## Database
* MongoDB >=4.4.1 https://docs.mongodb.com
## Requirements
* Python >=3.6
* Pip3
## Usage
* apt-install libxml2-dev libxslt1-dev zlib1g-dev
* pip install -r requirements.txt
* pip install -r requirements-dev.txt
* python3 group_search.py (Banned)
* python3 page_search (Running)

### Postman ###
* url : ip-addr:8082/fb/group (GET)
* url : ip-addr:8083/fb/pages?b_hour=hour (GET)
* Example : ip-addr:8083/fb/pages?b_hour=6

### Curl ###
* curl --location --request GET 'ip-addr:8082/fb/group'
* curl --location --request GET '127.0.0.1:8083/fb/pages?b_hour=6'

### Environment Variables

The API will then be available at http://127.0.0.1:8000
