import os
import json
import pymongo
import datetime
from datetime import timedelta
from time import sleep
from threading import Thread
from facebook_scraper import get_posts
from flask import Flask, request
from flask.json import jsonify

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(ROOT_DIR+'/config_db.json') as json_file:
    config = json.loads(json_file.read())
# config = json.load(config)

mongoclient = pymongo.MongoClient("mongodb://{}:{}/".format(config["host"], config["port"]))
db = mongoclient[config["db"]]

class FbCrawl(Thread):
    def __init__(self, until):
        Thread.__init__(self)
        self.until = until
    def run(self):
        run_crawler(self.until)
def insert_post_one(post):
    post_dict = post
    # print(post_dict["post_id"])
    post_dict.update({"_id":post_dict["post_id"]})
    mycol = db["facebook_page_posts"]
    try:
        x = mycol.insert_one(post)
        print(x.inserted_id)
    except Exception as e:
        # print('Mongo Err',e)
        pass

def run_crawler(backtrack_hour):
    list_pages = ["ShopeeID", "detikcom", "KOMPAScom", "gojekindonesia", "GrabID", "OVOIDN", "linkaja.indonesia",
                  "TravelokaID", "gopayindonesia","homecreditid", "kredivo", "tokopedia", "bukalapak", "AkuLakuIndonesia",
                  "TempoMedia","jpnncom","suaradotcom","GrabFoodID"]

    i = 0
    n = len(list_pages)
    last_hour_datetime = datetime.datetime.now() - timedelta(hours=int(backtrack_hour))
    last_hour_datetime = last_hour_datetime.strftime('%Y-%m-%d %H:%M:%S')
    last_hour = datetime.datetime.strptime(last_hour_datetime, '%Y-%m-%d %H:%M:%S')
    while i <= n:
        endDate = 0
        if i == n:
            print('close bos')
            break
        for post in get_posts(list_pages[i], pages=50):
            pubdate = post["time"].strftime("%Y-%m-%d %H:%M:%S")
            post_date = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            # print(post_date)
            if post["post_url"] is not None and post_date >= last_hour:
                del post["shared_text"]
                post.update({"source": "page"})
                post.update({"type": "post"})
                post.update({"pubdate": post["time"]})
                post.update({"platform": "facebook"})
                post.update({"page_source": list_pages[i]})
                post.update({"page_id": post["actor_id"]})
                del post["time"]
                del post["actor_id"]
                del post["post_text"]
                print(post)
                insert_post_one(post)
                sleep(3)
            elif post_date <= last_hour:
                print(post["time"])
                endDate += 1
                if endDate >= 10:
                    i += 1
                    break

@app.route("/fb/pages", methods=['GET'])
def fb_pages():
    b_hour = request.args.get('b_hour')
    thread_fb = FbCrawl(b_hour)
    thread_fb.start()
    resp = {'running': True}
    return jsonify(resp)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8083, debug=False, threaded=True)





