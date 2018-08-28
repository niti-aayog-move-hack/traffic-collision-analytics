import os
import tweepy
from tweepy import OAuthHandler
import json
import re
import sys


def fetch():
	year_list = []
	username = sys.argv[1]
	print("Fetching Tweets...")

	tweets_count = 0

		
	#Variables that contains the user credentials to access Twitter API 
	access_token = "3105037689-DDPtvV3ZhRES0hajaFyOpXTnmyhpw4Hq2B4ajUL"
	access_secret = "Tx5GvdSMZilQ0JllCTcSffudxy8Lt90zV373wZG1WXu0j"
	consumer_key = "mvgXUYsLbRmrlTcvIwprCBpSz"
	consumer_secret = "IV5h6smsEfndxwlw1sqNSFcUFWv0MgFDIXGFzmQImOFHhd3DDh"

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	for status in tweepy.Cursor(api.user_timeline, id = username).items(1):
		if(os.path.isfile("data/" + status.author._json['screen_name'] + "TwitterData.txt")):
			print("Already cached")
			return "data/" + status.author._json['screen_name'] + "TwitterData.txt"
		else:
			f_name = "data/" + status.author._json['screen_name'] + "TwitterData.txt"

	f = open(f_name, "w")

	output = ""

	for status in tweepy.Cursor(api.user_timeline, id = username).items():
		message = str(status.text.encode('ascii', 'ignore').decode('ascii'))
		message = re.sub(r"\n", r"\\n", message)
		message = re.sub(r"\t", r"\\t", message)
		output = output + "{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}\n".format(status.author._json['id_str'],status.author._json['name'],status.author._json['created_at'],status.id_str,message,status.created_at,status.favorite_count,status.retweet_count,status.in_reply_to_status_id,status.in_reply_to_screen_name,status.author._json['screen_name'],status.author._json['statuses_count'],status.author._json['followers_count'],status.author._json['friends_count'])


	f.write(output)

	print("Done!")

	return f_name
fetch()