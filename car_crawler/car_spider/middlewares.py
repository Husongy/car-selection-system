import random
from scrapy import signals


class CarSpiderSpiderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        return None

    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        pass

    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class CarSpiderDownloaderMiddleware:
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class RandomUserAgentMiddleware:
    """随机 User-Agent 中间件"""
    
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent_list=crawler.settings.get('USER_AGENT_LIST')
        )
    
    def process_request(self, request, spider):
        if self.user_agent_list:
            user_agent = random.choice(self.user_agent_list)
            request.headers['User-Agent'] = user_agent
            spider.logger.debug(f'使用 User-Agent: {user_agent}')
