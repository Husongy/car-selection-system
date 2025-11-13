import scrapy
import re
from datetime import datetime
from car_scrapy.items import SalesItem

class DongchediSalesSpider(scrapy.Spider):
    name = 'dongchedi_sales'
    allowed_domains = ['dongchedi.com']
    # 销量榜页面（示例链接，需替换为真实销量榜地址）
    start_urls = ['https://www.dongchedi.com/auto/sales-rank']

    def parse(self, response):
        # 提取销量项（根据实际网页结构调整xpath）
        sales_items = response.xpath('//div[@class="sales-item"]')

        for sales in sales_items:
            item = SalesItem()

            # 1. 关联汽车（先提取品牌和车系，后续需与Car模型关联）
            car_name = sales.xpath('.//h3[@class="car-name"]/text()').get().strip()
            brand_series = car_name.split(' ', 1)
            item['car'] = f"{brand_series[0]} {brand_series[1]}" if len(brand_series) > 1 else '未知车系'

            # 2. 年月（假设页面显示的是当月数据，格式：2025-10）
            item['year_month'] = datetime.now().strftime('%Y-%m')

            # 3. 销量
            sales_text = sales.xpath('.//div[@class="sales-num"]/text()').get(default='0').strip()
            item['sales_volume'] = int(re.findall(r'\d+', sales_text)[0]) if re.findall(r'\d+', sales_text) else 0

            # 4. 排名
            rank_text = sales.xpath('.//div[@class="rank"]/text()').get(default='0').strip()
            item['rank'] = int(rank_text) if rank_text.isdigit() else 0

            # 5. 时间
            item['create_time'] = datetime.now()

            yield item