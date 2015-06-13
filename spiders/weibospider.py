#-*- coding=utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from ScrapyWeiboByAPI.items import UserItem,WeiboItem
import time
import json
import base62

class WeiboSpider(CrawlSpider):
	name = 'weibospider'
	allowed_domains = ['weibo.cn']

	
	def __init__(self):
		super(WeiboSpider,self).__init__()
		self.access_token = "xxxx"
		#start time or end time of an event
		self.start_time = time.mktime(time.strptime("2012-11-20","%Y-%m-%d"))
		self.end_time = time.mktime(time.strptime("2013-12-20","%Y-%m-%d"))
		self.base_url = "https://api.weibo.com/2/comments/show.json?"

	def start_requests(self):
		fp = open("/home/owen/workspace/ScrapyByAPI/ScrapyWeiboByAPI/spiders/weibo_id_of_leader_not_clean",'r')

		line = fp.readline()

		while "" != line:
			if not line.startswith("#"):
				req_url = self.mk_request(base62.url_to_mid(line.strip()),0)
				yield Request(url=req_url,callback=self.parse_weibo)
			line = fp.readline()
		fp.close()

	def mk_request(self,mid,max_id):
		req_url = self.base_url + "access_token=" + self.access_token + "&"
		req_url += "id=" + str(mid) + "&count=200&"
		req_url += "max_id=" + str(max_id)
		self.log(req_url)
		return req_url 

    #parse status of the original weibo
    #decide whether we need to further parse it comment

	def parse_status(self,status):
		try:
			#Sun May 13 00:56:44 +0800 2012
			u_time = time.mktime(time.strptime(status["created_at"],"%a %b %d %H:%M:%S +0800 %Y"))
			#if the users is created later than the event start later
			if u_time < self.start_time or u_time > self.end_time:
				return False,0
		except:
			return False,0
			self.log(status["created_at"])

		try:
			if status.has_key("deleted"):
				return False,0
			#get an new item
			wItem = WeiboItem()

			wItem["mid"] = status['mid']
			
			result =  status["text"]

			if status.has_key("retweeted_status"):
				retweet_status = status["retweeted_status"]
				if not retweet_status.has_key("deleted"):
					result += "//@" + retweet_status["user"]["screen_name"] + ": " + retweet_status["text"]

			wItem["content"] = result
			wItem["uid"] = status['user']['id']
			wItem["pos"] = status['user']['location']
			wItem["time"] = status['created_at']
			#original weibo
			wItem["tid"] = 1
			wItem["eid"] = 1
			return True,wItem
		except:
			return False,0

	def parse_comment(self,comment):
		try:
			cItem = WeiboItem()
			cItem["mid"] =  comment["status"]["mid"]
			cItem["content"] = comment["text"]
			cItem["uid"] = comment["user"]["id"]
			cItem["pos"] = comment["user"]["location"]
			cItem["time"] = comment["created_at"]
			#user comment
			cItem["tid"] = 2
			cItem["eid"] = 1		
			return cItem
		except:
			pass



		
	def parse_user(self,user):
		try:

			userItem = UserItem()

			userItem["uid"] = user["id"]
			userItem["sname"] = user["screen_name"] 
			userItem["location"] = user["location"] 
			userItem["created_at"] = user["created_at"]  
			userItem["verified"] = user["verified"]  
			userItem["followers_count"] = user["followers_count"]
			userItem["friends_count"] = user["friends_count"]
			#follwer information
			userItem["tid"] = 3
			userItem["eid"] = 1
			return userItem
		except:
			pass	
		
	def parse_weibo(self,response):
		json_data = json.loads(response.body)
		#weibo item
		wItem = ""
		b_continue = False

		#if it is the first request
		if json_data["previous_cursor"] == 0:
			b_continue,wItem = self.parse_status(json_data["comments"][0]["status"])
			self.log(wItem)
		if b_continue == True:
			yield wItem
			for comment in json_data["comments"]:
				yield self.parse_user(comment["user"])
				yield self.parse_comment(comment)

				if json_data["next_cursor"] != 0:
					next_req_url= self.mk_request(json_data["comments"][0]["status"]["mid"],\
						json_data["next_cursor"])
					yield Request(url=next_req_url,callback=self.parse_weibo)