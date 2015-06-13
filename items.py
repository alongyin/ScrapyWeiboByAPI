# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class WeiboItem(Item):
	mid = Field()
	content = Field()
	uid = Field()
	pos = Field()
	time = Field()
	tid = Field()
	eid = Field()

#
class UserItem(Item):
	uid = Field()
	sname = Field() 
	location = Field() 
	created_at = Field()  
	verified = Field()  
	followers_count = Field()
	friends_count = Field()
	tid = Field()
	eid = Field()