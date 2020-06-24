BOT_NAME = 'hltv_data'

SPIDER_MODULES = ['matches_data.spiders']
NEWSPIDER_MODULE = 'matches_data.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 2

RETRY_TIMES = 15
RETRY_HTTP_CODES = [500, 503, 504, 400, 403, 404, 408]
PROXY_MODE = 0

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy_proxies.RandomProxy': 100,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}
PROXY_LIST = 'proxy.txt'
ITEM_PIPELINES = {
   'matches_data.pipelines.MatchesDataPipeline': 300,
}

MONGO_URI = 'mongo_db_uri_link'
MONGO_DB = 'matches_data'