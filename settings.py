# Scrapy settings for ScrapyWeiboByAPI project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ScrapyWeiboByAPI'

SPIDER_MODULES = ['ScrapyWeiboByAPI.spiders']
NEWSPIDER_MODULE = 'ScrapyWeiboByAPI.spiders'

ITEM_PIPELINES = ['ScrapyWeiboByAPI.pipelines.ScrapyweibobyapiPipeline']
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'ScrapyWeiboByAPI (+http://www.yourdomain.com)'
SCHEDULER_ORDER = 'DFO'
CONCURRENT_REQUESTS = 50

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scrapyweibobyapi'
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 15

# Specify the host and port to use when connecting to Redis (optional).
REDIS_HOST = '192.168.1.152'
REDIS_PORT = 6379
