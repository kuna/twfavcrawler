import tweepy
import private
import csv

# a private function
def CreateBasicAuth():
	auth = tweepy.OAuthHandler(private.consumer_token, private.consumer_secret)
        return auth

def CreateApi(auth, access_token):
        print access_token
	auth.set_access_token(access_token[0], access_token[1])
	api = tweepy.API(auth)
	return api


# TODO: save progress for look at
# TODO: save csv file
status_crawl_twit = {}
def CrawlAllFavorites(api, removefav):
# prepare for party!
	#userid = api.get_user("").id
	userid = api.me().id

	while True:
		results = api.favorites(userid)
		if results:
			for r in results:
				tweetdate = r.created_at
				tweet = r.text
				if (hasattr(r.user, 'screen_name')):
					name = r.user.screen_name
				else:
					name = "Unknown"
				line = [tweetdate.isoformat(), tweet.encode('utf8'), name.encode('utf8')]
				favWriter.writerow(line)
				if (removefav):
					api.destroy_favorite(r.id)
		else:
			print "No more favorites!"
			break

# crawl all images from api, and pack it into zip file.
# you must have crawled csv file.
# TODO
def CrawlAllImages(api):
	userid = api.me().id


"""
public_tweets = api.home_timeline()
for tweet in public_tweets:
	print tweet.text
"""
