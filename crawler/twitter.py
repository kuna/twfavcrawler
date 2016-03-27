import tweepy
import private
import csv
from models import *
import time
import threading
import os
from tweepy.error import *

# a private function
def CreateBasicAuth():
    auth = tweepy.OAuthHandler(private.consumer_token, private.consumer_secret)
    return auth

def CreateApi(access_token):
    auth = CreateBasicAuth()
    auth.set_access_token(access_token[0], access_token[1])
    api = tweepy.API(auth)
    return api

def SafeStr(o):
    if (o == None):
        return None
    else:
        return o





# COMMENT: this thread runs until 
def CrawlFavTweet(api):
    userid = api.me().id
    userobj = User.objects.get(id=userid)
    output_filename = 'fav_' + str(int(time.time())) + '.csv'
    output_dir = '/cdn/tw/archive/' + str(userobj.id) + '/'
    output_path = output_dir + output_filename
    archiveobj = Task(
        output = output_filename,
        user = userobj,
        type = 'fav',
        message = 'Preparing ...',
        total = api.me().favourites_count,
        current = 0,
        status = 0
        )
    archiveobj.save()
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
# task could be stopped in real-time,
# so always refresh object to get current task status
        archiveobj.refresh_from_db()
        if (archiveobj.status != 0):
            break

        try:
            # first try test
            results = api.favorites()
            if results:
                for r in results:
                    print '[TEST] ' + str(r.id) + ' - ' + r.text.encode('utf8')
                    #print(dir(r))
                    ret_stat_id = ''
                    ret_stat_user_id = ''
                    if (hasattr(r, 'retweeted_status')):
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
                archiveobj.message = str(archiveobj.current) + ' / ' + str(archiveobj.total)
            else:
                archiveobj.message = "No more favorites! parsing end!"
                break
            archiveobj.save()
        except RateLimitError:
            archiveobj.message = 'Api limit, rest for a while ...'
            archiveobj.save()
            time.sleep(600)  # about 10min
        except TweepError as e:
            print e.response
            break

    archiveobj.status = 1   # finished successfully
    archiveobj.save()


# crawl all images from api, and pack it into zip file.
# you must have crawled csv file.
def CrawlImages(api):
    userid = api.me().id


"""
public_tweets = api.home_timeline()
for tweet in public_tweets:
	print tweet.text
"""

def Task_CrawlFavTweet(api):
    t = threading.Thread(target=CrawlFavTweet, args=[api])
    t.start()
    return True
