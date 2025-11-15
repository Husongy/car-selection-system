"""
Scrapy 爬虫运行脚本
可以直接运行此文件来启动爬虫，无需使用 scrapy crawl 命令
"""
import os
import sys
from scrapy.cmdline import execute

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # 切换到 scrapy 项目目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 运行爬虫
    # 可以选择运行不同的爬虫：
    
    # 运行东车帝爬虫
    # execute(['scrapy', 'crawl', 'dongchedi'])
    
    # 运行车质网爬虫
    # execute(['scrapy', 'crawl', 'chezhi'])
    
    # 同时运行所有爬虫
    print("可用的爬虫：")
    print("1. dongchedi - 东车帝销量数据")
    print("2. chezhi - 车质网质量投诉")
    print("\n运行命令示例：")
    print("  python run_spider.py dongchedi")
    print("  python run_spider.py chezhi")
    
    if len(sys.argv) > 1:
        spider_name = sys.argv[1]
        execute(['scrapy', 'crawl', spider_name])
    else:
        print("\n请指定要运行的爬虫名称")
