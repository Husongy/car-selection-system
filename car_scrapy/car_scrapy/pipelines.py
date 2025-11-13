import csv
from pathlib import Path

class CarScrapyPipeline:
    def open_spider(self, spider):
        """爬虫启动时创建CSV文件"""
        Path("output").mkdir(exist_ok=True)  # 创建output目录
        self.csv_file = open("output/dongchedi_榜单数据.csv", "w", encoding="utf-8-sig", newline="")
        self.fieldnames = ["榜单类型", "标题", "详情链接", "额外信息"]
        self.writer = csv.DictWriter(self.csv_file, fieldnames=self.fieldnames)
        self.writer.writeheader()

    def process_item(self, item, spider):
        """处理每一条Item，写入CSV"""
        self.writer.writerow({
            "榜单类型": item["board_type"],
            "标题": item["title"],
            "详情链接": item["detail_url"],
            "额外信息": str(item["extra"])  # 字典转字符串存储（或按需拆分字段）
        })
        return item

    def close_spider(self, spider):
        """爬虫结束时关闭CSV文件"""
        self.csv_file.close()
        spider.logger.info("数据已保存到 output/dongchedi_榜单数据.csv")