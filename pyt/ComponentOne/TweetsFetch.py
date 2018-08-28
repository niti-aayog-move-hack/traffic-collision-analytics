import os
import tweepy
from tweepy import OAuthHandler
import json
import re
import sys

def already_exists(api,username,last_tid,f_name):
	print("In already exists")
	cnt = 0
	output = ""
	output_line_list = []		
	line_list = []		#list which stores lines of the file before updation

	#-------------------Iterating over all the new tweets--------------------------------------
	for status in tweepy.Cursor(api.user_timeline, id = username).items(30):
		if(int(status.id_str) > last_tid):		#if the tweet is more recent than the most recent tweet in the previous file
			cnt = cnt + 1
			print("Tweet Count : ", cnt)
			message = str(status.text.encode('ascii', 'ignore').decode('ascii'))
			message = re.sub(r"\n", r"\\n", message)
			message = re.sub(r"\t", r"\\t", message)
			if "\t\t" not in message and "\t\n" not in message:
				output_line_list.append("{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}\n".format(status.author._json['id_str'],status.author._json['name'],status.author._json['created_at'],status.id_str,message,str(status.created_at).split(" ")[0].strip(),status.favorite_count,status.retweet_count,status.in_reply_to_status_id,status.in_reply_to_screen_name,status.author._json['screen_name'],status.author._json['statuses_count'],status.author._json['followers_count'],status.author._json['friends_count'])) #add the tweet to the output to be written to the file

		else:		#Tweet is the same as or older than the most recent tweet in the already existing file, i.e, not a new tweet
			print("No tweets beyond this point")
			break


	output_line_list.reverse()
	#--------------------------Write the most recent tweets obtained into the file---------
	f = open(f_name, "a")
	#--------------------------------------------------------------------------------------*

	output = ""
	for line in output_line_list:
		output = output + line

	f.write(output)
	#return True

def first_time(api,username,f_name):

	cnt = 0
	
	output_line_list = []

	f = open(f_name, "w")

	for status in tweepy.Cursor(api.user_timeline, id = username).items(20):		#iterate over all the tweets
		message = str(status.text.encode('ascii', 'ignore').decode('ascii'))		#remove non ascii characters
		message = re.sub("\n", " ", message)		#replace newlines by "\n" string
		message = re.sub("\t", " ", message)		#replace tabs by "\t" string
		if "\t\t" not in message and "\t\n" not in message:
			cnt = cnt + 1
			print("Tweet Count : ", cnt)
			if cnt > 10 :
				print("Appended!")
				output_line_list.append("{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}	{}\n".format(status.author._json['id_str'],status.author._json['name'],status.author._json['created_at'],status.id_str,message,str(status.created_at).split(" ")[0].strip(),status.favorite_count,status.retweet_count,status.in_reply_to_status_id,status.in_reply_to_screen_name,status.author._json['screen_name'],status.author._json['statuses_count'],status.author._json['followers_count'],status.author._json['friends_count']))

	output_line_list.reverse()

	output = ""

	for line in output_line_list:
		output = output + line

	f.write(output)

	return False

def get_last_tid(f_name):
	temp_list = []
	f =  open(f_name, "r")
	for line in f.readlines():
		try:
			temp_list.append(int(line.split("\t")[3]))
		except ValueError:
			continue

	print("Last tid : ", max(temp_list))
	return(max(temp_list))


def fetch(name,username):

	year_list = []
	tweets_count = 0

	consumer_key = 	'eB0hmLCAFEcz9gByv89DoI1HQ'
	consumer_secret = 'P8xZYZXpzAh1BnqWDq6DNQf2Z0WrljTT1tPJ0gC2yZLHowWac7'
	access_token = 	'372788901-cEdjyEE5ON91N5IYQJa2ha1bYMNrMBH8yO4Fe2VG'
	access_secret =	'ThW4N8xCMBpP6ziCXPuwKeJe4hx9SJtUIfs8G9WdePUvd'

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	ft = False

	f_name = ""

	#--------------Getting details of the user-------------------------------------------------------------
	for status in tweepy.Cursor(api.user_timeline, id = username).items(1):
		if(os.path.isfile("../data/" + name + "TwitterData.txt")):	#If the file already exists
			f_name = "../data/" + name + "TwitterData.txt"
			last_tid = get_last_tid(f_name)		#Get id of the last tweet
			already_exists(api,username,last_tid,f_name)

		else:		#If the file doesn't exist, i.e, the user is being searched for the first time
			f_name = "../data/" + name + "TwitterData.txt"
			first_time(api,username,f_name)
			ft = True

	return f_name,ft