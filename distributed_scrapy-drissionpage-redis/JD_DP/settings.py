# Scrapy settings for JD_DP project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "JD_DP"

SPIDER_MODULES = ["JD_DP.spiders"]
NEWSPIDER_MODULE = "JD_DP.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "JD_DP (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 1

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "JD_DP.middlewares.JdDpSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# 启用中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy_drissionpage.middleware.DrissionPageMiddleware': 543,
}

# DrissionPage配置
DRISSIONPAGE_HEADLESS = False  # 是否无头模式
DRISSIONPAGE_LOAD_MODE = 'normal'  # 页面加载模式：normal, eager, none
DRISSIONPAGE_DOWNLOAD_PATH = 'downloads'  # 下载路径
DRISSIONPAGE_TIMEOUT = 30  # 请求超时时间
DRISSIONPAGE_RETRY_TIMES = 3  # 重试次数
DRISSIONPAGE_RETRY_INTERVAL = 2  # 重试间隔（秒）

# 浏览器设置
DRISSIONPAGE_BROWSER_PATH = 'C:\Program Files\Google\Chrome\Application\chrome.exe'  # 浏览器路径，None使用默认浏览器
DRISSIONPAGE_INCOGNITO = True  # 是否使用无痕模式
DRISSIONPAGE_CHROME_OPTIONS = ['--disable-gpu']  # Chrome启动选项

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "JD_DP.pipelines.JdDpPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"


# ~~~~~~~~~~~~~~~~~~~~~~~~


# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ["JD_DP.spiders"]
NEWSPIDER_MODULE = "JD_DP.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# 设置重复过滤器的模块
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 设置调度器,scrapy_redis中的调度器具备和数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
#设置当爬虫结束的时候是否保持redis数据库中的去重集合与任务队列
SCHEDULER_PERSIST = True
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    # "example.pipelines.ExamplePipeline": 300,
    #当开启该管道,该管道将会把数据存到Redis数据库中
    "scrapy_redis.pipelines.RedisPipeline": 400,

}

#设置Redis数据库
REDIS_URL="redis://192.168.126.128:6379"

LOG_LEVEL = "DEBUG"

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.
DOWNLOAD_DELAY = 1

CONCURRENT_REQUESTS = 2
