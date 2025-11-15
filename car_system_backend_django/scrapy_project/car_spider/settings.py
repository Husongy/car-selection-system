"""
Scrapy 爬虫设置
集成 Django 环境，使用 Django ORM 存储数据
"""
import os
import sys
import django

# 添加Django项目路径到Python路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_system.settings')
django.setup()

# Scrapy 基础配置
BOT_NAME = 'car_spider'
SPIDER_MODULES = ['car_spider.spiders']
NEWSPIDER_MODULE = 'car_spider.spiders'

# 遵守 robots.txt
ROBOTSTXT_OBEY = False

# 并发请求配置
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

# 请求头配置 - 模拟真实浏览器
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# 启用 Pipeline
ITEM_PIPELINES = {
    'car_spider.pipelines.DjangoPipeline': 300,
}

# 日志配置
LOG_LEVEL = 'INFO'
LOG_FILE = 'scrapy_spider.log'

# AutoThrottle 自动限速
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0

# 缓存配置
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
