"""
Scrapy 爬虫设置
集成 Django 环境，使用 Django ORM 存储数据
优化版本：增强反爬策略、性能调优、错误处理
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

# ============== Scrapy 基础配置 ==============
BOT_NAME = 'car_spider'
SPIDER_MODULES = ['car_spider.spiders']
NEWSPIDER_MODULE = 'car_spider.spiders'

# ============== 反爬虫配置 ==============
# 不遵守 robots.txt（仅用于正当数据采集）
ROBOTSTXT_OBEY = False

# 请求头配置 - 模拟真实浏览器
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# User-Agent 随机化（避免被封）
USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]

import random
USER_AGENT = random.choice(USER_AGENT_LIST)

# Cookies 启用
COOKIES_ENABLED = True

# ============== 并发和限速配置 ==============
# 并发请求数（不要设置太高，避免被封）
CONCURRENT_REQUESTS = 8

# 对单个域名的并发请求数
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# 下载延迟（秒）
DOWNLOAD_DELAY = 2

# AutoThrottle 自动限速（智能调整请求速度）
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1  # 初始延迟
AUTOTHROTTLE_MAX_DELAY = 5    # 最大延迟
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0  # 目标并发数
AUTOTHROTTLE_DEBUG = False

# ============== 下载超时和重试 ==============
# 下载超时时间（秒）
DOWNLOAD_TIMEOUT = 30

# 重试配置
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 403]

# ============== Middleware 配置 ==============
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    # 'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# ============== Pipeline 配置 ==============
ITEM_PIPELINES = {
    'car_spider.pipelines.DjangoPipeline': 300,
}

# ============== 缓存配置 ==============
# HTTP缓存（避免重复请求）
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600  # 1小时
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 400, 403, 404, 408]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# ============== 日志配置 ==============
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/scrapy_spider.log'
LOG_ENCODING = 'utf-8'
LOG_STDOUT = False

# 日志格式
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# ============== 性能优化 ==============
# DNS缓存
DNSCACHE_ENABLED = True
DNSCACHE_SIZE = 10000

# 启用持久连接
DOWNLOAD_HANDLERS = {
    'http': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
    'https': 'scrapy.core.downloader.handlers.http.HTTPDownloadHandler',
}

# ============== 其他配置 ==============
# 禁用Telnet控制台
TELNETCONSOLE_ENABLED = False

# 禁用Cookies调试
COOKIES_DEBUG = False
