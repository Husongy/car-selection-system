import scrapy

class DongchediItem(scrapy.Item):
    # 榜单类型（热搜榜/热销榜/直播小时榜）
    board_type = scrapy.Field()
    # 核心标题（热搜标题/车型名称/主播名称）
    title = scrapy.Field()
    # 详情链接
    detail_url = scrapy.Field()
    # 额外信息（不同榜单的扩展字段，用字典存储）
    extra = scrapy.Field()