from facebook_scraper.facebook_scraper import FacebookScraper
import re
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
from datetime import timedelta
from time import sleep
import pymongo
import json
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
with open(ROOT_DIR+'/config_db.json') as json_file:
    config = json.loads(json_file.read())
# config = json.load(config)

mongoclient = pymongo.MongoClient("mongodb://{}:{}/".format(config["host"], config["port"]))
db = mongoclient[config["db"]]

def get_list_group():
    mycol = db["facebook_groups"]
    groups = []
    for x in mycol.find({}, {"plafform": "facebook"}):
        groups.append(x["_id"])
    print(groups)
    return groups
#
def insert_post_one(post):
    post_dict = post
    # print(post_dict["post_id"])
    post_dict.update({"_id":post_dict["post_id"]})
    mycol = db["facebook_posts"]
    try:
        x = mycol.insert_one(post)
        print(x.inserted_id)
    except Exception as e:
        # print(e)
        pass


def parse(g_id, p_id):
    # url = 'http://m.facebook.com/groups/1000043713742145/permalink/1030776880668828'
    url = 'http://m.facebook.com/groups/{}/permalink/{}'.format(g_id, p_id)
    web_url = 'https://facebook.com/groups/{}/permalink/{}'.format(g_id, p_id)
    data = {}
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    raw = soup.find(id='u_0_4')
    # print(raw)
    story_raw = soup.find(id='m_story_permalink_view')

    # print(story_raw)
    if 'original_content_id' in str(raw):
        try:

            # print('share')
            time = re.findall("publish_time\"\:(.*?)\,\"story_name",str(raw))
            # print(time)
            if len(time) > 1:
                timestamp = time[1]
            else:
                timestamp = time[0]
            # print(timestamp)
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            pubdate = dt.strftime("%Y-%m-%d %H:%M:%S")
            post_date = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            # print(post_date)
            datetime_object = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')


            date_str = dt.strftime("%Y-%m-%d")
            # print(type(date_str))
            # until_obj = datetime.datetime.strptime(until, "%Y-%m-%d")
            # date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # # print(date_obj)
            #
            # d0 = date(date_obj.year, date_obj.month, date_obj.day)
            # d1 = date(until_obj.year, until_obj.month, until_obj.day)
            #
            # #
            # delta = d0 - d1
            # print(delta)
            # #
            # if delta.days >=0:
            #
            #
            ids = re.findall('actor_id\"\:\"(.*?)\"\,\"', str(raw))
            # print(ids)
            if ids is None or ids==[]:
                ids = re.findall('actor_id\"\:(.*?)\,\"dm', str(raw))

            if len(ids) > 1:
                user_id = ids[0]
            else:
                user_id = ids[0]
            usr_name = re.findall('bt"><strong><a href="\/(.*?)\?refid=18&', str(raw))
            # print(usr_name)
            user_raw = re.findall('bt"><strong><a hre(.*?)<\/strong>',str(raw))
            fname = re.findall('tn__=C-R">(.*?)<\/a>',''.join(user_raw))
            # # # print(fname)
            fullname = ''.join(fname)
            username = usr_name[0]
            # # # print(user_id)

            data["post_date"] = post_date
            data["pubdate"] = datetime_object.isoformat()
            data["user_id"] = user_id
            data["username"] = username
            data["fullname"] = fullname
            data["post_url"] = web_url
            # if (bool(BeautifulSoup(data["pubdate"] , "html.parser").find())==True) or(bool(BeautifulSoup(data["user_id"], "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["username"] , "html.parser").find())==True) or (bool(BeautifulSoup(data["fullname"] , "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["post_url"] , "html.parser").find())==True):
            #     return None
            # print(data)
            return data
            # if post_date < last_hour:
            #     return data
            # else:
            #     print(post_date)
        except Exception as e:
            print('Err 1', e)
            # print(str(raw))
            return None

    elif 'originalPostOwnerID' in str(raw):
        try:
            # print('ori')
            # print(raw)
            time = re.findall("publish_time\"\:(.*?)\,\"story_name", str(raw))
            # print(time)
            if len(time) > 1:
                timestamp = time[1]
            else:
                timestamp = time[0]
            # print(timestamp)
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            pubdate = dt.strftime("%Y-%m-%d %H:%M:%S")
            # post_date = datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            post_date = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            datetime_object = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')

            date_str = dt.strftime("%Y-%m-%d")
            # print(type(date_str))
            # until_obj = datetime.datetime.strptime(until, "%Y-%m-%d")
            # date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            # # print(until_obj)
            # # print(date_obj)
            #
            # d0 = date(date_obj.year, date_obj.month, date_obj.day)
            # d1 = date(until_obj.year, until_obj.month, until_obj.day)
            # print(d0)
            # print(d1)
            # #
            # delta = d0 - d1
            # # print(delta)
            # #
            # if delta.days >= 0:
            # print('lanjut')
            # print(raw)
            # print(url)
            ids = re.findall('actor_id\"\:\"(.*?)\"\,\"', str(raw))
            if ids is None or ids==[]:
                ids = re.findall('actor_id\"\:(.*?)\,\"dm', str(raw))
            if len(ids) >0:
                user_id = ids[0]
            else:
                user_id = ids[0]
            usr_name = re.findall('bt"><strong><a href="\/(.*?)\?refid=18&', str(raw))
            if len(usr_name) > 0:
                username = usr_name[0]
            else:
                username = None
            # user_raw = re.findall('bt"><strong><a hre(.*?)<\/strong>', str(raw))
            fname = re.findall('<strong><a>(.*?)<\/a><\/strong><span class="bv"',str(raw))
            # # # print(fname)
            fullname = ''.join(fname)
            # # # print(user_id)
            data["post_date"] = post_date
            data["pubdate"] = datetime_object.isoformat()
            data["user_id"] = user_id
            data["username"] = username
            data["fullname"] = fullname
            data["post_url"] = web_url
            # print(raw)
            # if (bool(BeautifulSoup(data["pubdate"] , "html.parser").find())==True) or(bool(BeautifulSoup(data["user_id"], "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["username"] , "html.parser").find())==True) or (bool(BeautifulSoup(data["fullname"] , "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["post_url"] , "html.parser").find())==True):
            #     return None
            return data
            # if post_date < last_hour:
            #     return data
            # else:
            #     print(post_date)
        except Exception as e:
            print('Err 2', e)
            # print(str(raw))
            return None
    else:
        # print(story_raw)
        # print(url)
        # print("else")
        try:
            time = re.findall("publish_time\"\:(.*?)\,\"story_name", str(story_raw))
            # print(time)
            if len(time) > 1:
                timestamp = time[1]
            else:
                timestamp = time[0]
            # print(timestamp)
            dt = datetime.datetime.fromtimestamp(int(timestamp))
            pubdate = dt.strftime("%Y-%m-%d %H:%M:%S")
            # post_date = datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            post_date = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')
            datetime_object = datetime.datetime.strptime(pubdate, '%Y-%m-%d %H:%M:%S')

            ids = re.findall('actor_id\"\:\"(.*?)\"\,\"', str(story_raw))
            if ids is None or ids==[]:
                ids = re.findall('actor_id\"\:(.*?)\,\"dm', str(story_raw))

            if len(ids) > 0:
                user_id = ids[0]
            else:
                user_id = ids[0]

            usr_name = re.findall('bt"><strong><a href="\/(.*?)\?refid=18&', str(story_raw))
            if usr_name is not None and len(usr_name) > 0:
                username = usr_name[0]
            else:
                username = None

            # user_raw = re.findall('bt"><strong><a hre(.*?)<\/strong>', str(raw))
            fname = re.findall('<strong><a>(.*?)<\/a><\/strong><span class="bv"', str(story_raw))
            fullname = ''.join(fname)
            data["post_date"] = post_date
            data["pubdate"] = datetime_object.isoformat()
            data["user_id"] = user_id
            data["username"] = username
            data["fullname"] = fullname
            data["post_url"] = web_url
            # if (bool(BeautifulSoup(data["pubdate"] , "html.parser").find())==True) or(bool(BeautifulSoup(data["user_id"], "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["username"] , "html.parser").find())==True) or (bool(BeautifulSoup(data["fullname"] , "html.parser").find())==True)\
            #    (bool(BeautifulSoup(data["post_url"] , "html.parser").find())==True):
            #     return None
            return data
            # if post_date < last_hour:
            #     return data
            # else:
            #     print(post_date)

        except Exception as e:
            print('Err 3', e)
            # print(story_raw)
            # print(e)
            return None

def run():
    fb = FacebookScraper()
    list_group = get_list_group()
    last_hour_datetime = datetime.datetime.now() - timedelta(hours=12)
    last_hour_datetime = last_hour_datetime.strftime('%Y-%m-%d %H:%M:%S')
    last_hour = datetime.datetime.strptime(last_hour_datetime, '%Y-%m-%d %H:%M:%S')
    print(last_hour)
    for group_id in list_group:
        for post in fb.get_group_posts(group=group_id ,page_limit=100):
            # print(post)
            if (post["post_id"] is not None) and (post["text"] is not None) and (post["text"] !=''):
                # print(post["post_id"])
                detail = parse(group_id, post["post_id"])
                if detail is not None and detail["post_date"] >= last_hour:
                    del detail["post_date"]
                    del post['time']
                    del post['shared_text']
                    del post['post_text']
                    # print(post["text"])
                    # post.update({"text":str(post["text"].encode())})
                    post.update({"group_id":group_id})
                    post.update({"type": "post"})
                    post.update({"platform": "facebook"})
                    post.update(detail)
                    # print(str(post["text"]))
                    # print(type(post["text"]))
                    # print(post["text"].decode('ascii'))
                    # a = post["text"].encode('utf-8')
                    # print(a)

                    if (post["username"] is not None and '</' not in post["username"]) or (post["username"] is not None and '<a href=' in post["username"])\
                        or (post["fullname"] is not None and '</' not in post["fullname"]) or (post["fullname"] is not None and'<a href=' in post["fullname"])\
                        or (post["user_id"] is not None and '</' not in post["user_id"]) or (post["user_id"] is not None and '<a href=' in post["user_id"]):
                        print(post)
                        insert_post_one(post)
                        sleep(2)
                else:
                    # print('fuck')
                    print(detail)

if __name__ == '__main__':
    run()


