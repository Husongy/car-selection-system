# 启用Pipeline（优先级300，数值越小越先执行）
ITEM_PIPELINES = {
    "car_scrapy.pipelines.CarScrapyPipeline": 300,
}

# 设置请求间隔（避免爬取过快被封IP）
DOWNLOAD_DELAY = 2  # 2秒间隔

# 禁用Cookie（如需启用，改为True并在请求头添加Cookie）
COOKIES_ENABLED = False

# 配置日志级别（方便调试）
LOG_LEVEL = "INFO"

# 自定义请求头（全局生效，也可在Spider中单独配置）
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.dongchedi.com/",
}