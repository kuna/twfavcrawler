import tweepy
import private
import csv
import models
import time
import threading
import os
from tweepy.error import *

# a private function
def CreateBasicAuth():
    auth = tweepy.OAuthHandler(private.consumer_token, private.consumer_secret)
    return auth

def CreateApi(auth, access_token):
    print access_token
    auth.set_access_token(access_token[0], access_token[1])
    api = tweepy.API(auth)
    return api

def SafeStr(o):
    if (o == None):
        return None
    else:
        return o





def CrawlFavTweet(api):
    userid = api.me().id
    userobj = User.objects.get(id=userid)
    output_filename = fav + '_' + str(userobj.id) + '_' + str(int(time.time())) + '.csv'
    output_dir = '/cdn/tw/tweet/'
    output_path = output_dir + output_filename
    archiveobj = Archive.objects.create(
        output = output_filename,
        user = userobj,
        archivetype = 'fav',
        status = 'Preparing ...',
        total = api.me().favourites_count,
        current = 0
        )
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    csvfile = csv.writer(open(output_path, 'wb'), delimiter=',')
    csvfile.writerow([
        'tweet_id',
        'in_reply_to_status_id',
        'in_reply_to_user_id',
        'retweeted_status_id',
        'retweeted_status_user_id',
        'timestamp',
        'source',
        'text'
        ])

    while True:
        try:
            results = api.favorites(userid)
            if results:
                for r in results:
                    tweetdate = r.created_at
                    ret_stat_id = ''
                    ret_stat_user_id = ''
                    if (r.retweeted_status):
                        ret_stat_id = r.retweeted_status.id
                        ret_stat_user_id = r.retweeted_status.user.id
                    line = [
                        r.id,
                        SafeStr(r.in_reply_to_status_id),
                        SafeStr(r.in_reply_to_user_id),
                        ret_stat_id,
                        ret_stat_user_id,
                        r.created_at.isoformat(),
                        r.source.encode('utf8'),
                        r.text.encode('utf8'),
                    ]
                    csvfile.writerow(line)
                    api.destroy_favorite(r.id)
# update db
                archiveobj.current += 1
                archiveobj.status = str(archiveobj.current) + ' / ' + str(archiveobj.total)
            else:
                print "No more favorites! parsing end!"
                break
        except RateLimitError:
            archiveobj.status = 'Api limit, rest for a while ...'
            time.sleep(600)  # about 10min






# crawl all images from api, and pack it into zip file.
# you must have crawled csv file.
# TODO
def CrawlImages(api):
    userid = api.me().id


"""
public_tweets = api.home_timeline()
for tweet in public_tweets:
	print tweet.text
"""

# workers here!
task_workers = {}
def Task_CrawlFavTweet(name, api):
    if (task_workers[name] == None or
        not task_workers[name].isAlive()):
        task_workers[name] = threading.Thread(target=CrawlFavTweet, args=[api])
        task_workers[name].start()
        return True
    else:
        return False
