import scrapy
from car_scrapy.items import DongchediItem  # 导入Scrapy Item
from typing import List, Dict, Optional, Any

# ===== 保留你已有的解析逻辑（HotSearchItem/HotSaleItem/LiveItem/DongchediParser）=====
class HotSearchItem:
    def __init__(self, title: str, detail_url: str, icons: Optional[Dict] = None):
        self.title = title
        self.detail_url = detail_url
        self.icons = icons or {"dark_serial_icon": "无", "serial_icon": "无"}

    def to_dict(self) -> Dict[str, str]:
        return {
            "热搜标题": self.title,
            "详情链接": self.detail_url,
            "深色图标": self.icons["dark_serial_icon"],
            "默认图标": self.icons["serial_icon"]
        }

class HotSaleItem:
    def __init__(self, series_name: str, sale_count: int, price_text: str,
                 rank_change: str, detail_url: str, extra: Optional[Dict] = None):
        self.series_name = series_name
        self.sale_count = sale_count
        self.price_text = price_text
        self.rank_change = rank_change
        self.detail_url = detail_url
        self.extra = extra or {"series_id": "无", "cover_url": "无", "trend_icon": "无"}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "车型名称": self.series_name,
            "全国销量": self.sale_count,
            "价格区间": self.price_text,
            "排名变化": self.rank_change,
            "车型ID": self.extra["series_id"],
            "车型封面": self.extra["cover_url"],
            "趋势图标": self.extra["trend_icon"],
            "详情链接": self.detail_url
        }

class LiveItem:
    def __init__(self, anchor_id: str, anchor_name: str, avatar_url: Optional[str]):
        self.anchor_id = anchor_id
        self.anchor_name = anchor_name
        self.avatar_url = avatar_url or "无"

    def to_dict(self) -> Dict[str, str]:
        return {
            "主播ID": self.anchor_id,
            "主播名称": self.anchor_name,
            "头像链接": self.avatar_url
        }

class DongchediParser:
    @staticmethod
    def parse_json(json_data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        result = {
            "热搜榜": [],
            "热销榜": [],
            "直播小时榜": []
        }
        data = json_data.get("data", {})
        rank_boards = data.get("rank_board", [])

        for board in rank_boards:
            board_name = board.get("rank_name", "")
            board_code = board.get("rank_code", -1)
            tops = board.get("tops", [])

            if board_code == 0 and board_name == "热搜榜":
                for item in tops:
                    icons = {"dark_serial_icon": item.get("dark_serial_icon", "无"), "serial_icon": item.get("serial_icon", "无")}
                    hot_search = HotSearchItem(title=item.get("title", "无标题"), detail_url=item.get("detail_url", "无链接"), icons=icons)
                    result["热搜榜"].append(hot_search.to_dict())

            elif board_code == 2 and board_name == "热销榜":
                for item in tops:
                    extra_info = {"series_id": item.get("series_id", "无"), "cover_url": item.get("cover_url", "无"), "trend_icon": item.get("trend_icon", "无")}
                    hot_sale = HotSaleItem(
                        series_name=item.get("series_name", item.get("title", "无名称")),
                        sale_count=item.get("sale_count", 0),
                        price_text=item.get("price_text", "暂无价格"),
                        rank_change=item.get("description", "无变化"),
                        detail_url=item.get("detail_url", "无链接"),
                        extra=extra_info
                    )
                    result["热销榜"].append(hot_sale.to_dict())

            elif board_code == 8 and board_name == "直播小时榜":
                for item in tops:
                    if "anchor_id" in item and "anchor_name" in item:
                        live = LiveItem(anchor_id=item.get("anchor_id", "无"), anchor_name=item.get("anchor_name", "无名称"), avatar_url=item.get("avatar_url"))
                        result["直播小时榜"].append(live.to_dict())

        return result

# ===== 新增 Scrapy Spider 类（爬虫核心）=====
class DongchediCarSpider(scrapy.Spider):
    name = "dongchedi_car"  # 爬虫名称（必须唯一）
    # 替换为「懂车帝榜单真实API地址」（关键！需要你抓包获取）
    start_urls = ["https://www.dongchedi.com/motor/searchpage/launcher/main/v1/?aid=1839&app_name=auto_web_pc"]  # 示例地址，需替换为真实接口

    def start_requests(self):
        """发起请求（添加请求头，避免被反爬）"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://www.dongchedi.com/",
            "Accept": "application/json, text/plain, */*",
            # 如需Cookie，抓包后添加："Cookie": "你的Cookie值"
        }
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers=headers,
                callback=self.parse  # 响应交给parse方法处理
            )

    def parse(self, response):
        """处理响应：解析JSON → 封装到Scrapy Item → 提交给Pipeline"""
        try:
            # 1. 解析API返回的JSON数据
            json_data = response.json()
            self.logger.info(f"成功获取API响应，状态：{json_data.get('message')}")

            # 2. 调用你的解析逻辑，得到结构化数据
            parsed_result = DongchediParser.parse_json(json_data)

            # 3. 将解析结果封装到Scrapy Item（匹配items.py字段）
            # 处理热搜榜
            for hot_search in parsed_result["热搜榜"]:
                item = DongchediItem()
                item["board_type"] = "热搜榜"
                item["title"] = hot_search["热搜标题"]
                item["detail_url"] = hot_search["详情链接"]
                item["extra"] = {
                    "深色图标": hot_search["深色图标"],
                    "默认图标": hot_search["默认图标"]
                }
                yield item  # 提交Item给Pipeline存储

            # 处理热销榜
            for hot_sale in parsed_result["热销榜"]:
                item = DongchediItem()
                item["board_type"] = "热销榜"
                item["title"] = hot_sale["车型名称"]
                item["detail_url"] = hot_sale["详情链接"]
                item["extra"] = {
                    "全国销量": hot_sale["全国销量"],
                    "价格区间": hot_sale["价格区间"],
                    "排名变化": hot_sale["排名变化"],
                    "车型ID": hot_sale["车型ID"],
                    "车型封面": hot_sale["车型封面"]
                }
                yield item

            # 处理直播小时榜
            for live in parsed_result["直播小时榜"]:
                item = DongchediItem()
                item["board_type"] = "直播小时榜"
                item["title"] = live["主播名称"]
                item["detail_url"] = ""  # 直播榜无详情链接，留空
                item["extra"] = {
                    "主播ID": live["主播ID"],
                    "头像链接": live["头像链接"]
                }
                yield item

        except Exception as e:
            self.logger.error(f"解析响应失败：{str(e)}")
            raise
