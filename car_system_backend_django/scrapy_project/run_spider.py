"""
Scrapy 爬虫运行脚本
优化版本：支持命令行参数、批量运行、日志管理
"""
import os
import sys
import argparse
from datetime import datetime
from scrapy.cmdline import execute

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def ensure_log_dir():
    """确保日志目录存在"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f'✓ 创建日志目录: {log_dir}')


def run_spider(spider_name, max_pages=5):
    """
    运行指定爬虫
    :param spider_name: 爬虫名称
    :param max_pages: 最大页数（仅对chezhi爬虫有效）
    """
    ensure_log_dir()
    
    print('='*60)
    print(f'开始运行爬虫: {spider_name}')
    print(f'运行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*60)
    
    # 切换到 scrapy 项目目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # 构建命令
        cmd = ['scrapy', 'crawl', spider_name]
        
        # 如果是车质网爬虫，传递最大页数参数
        if spider_name == 'chezhi':
            cmd.extend(['-a', f'max_pages={max_pages}'])
        
        execute(cmd)
        
        print('\n' + '='*60)
        print(f'爬虫 {spider_name} 运行完毕')
        print('='*60)
        
    except Exception as e:
        print(f'\n✗ 爬虫运行失败: {e}')
        sys.exit(1)


def run_all_spiders():
    """运行所有爬虫"""
    spiders = ['dongchedi', 'chezhi']
    
    print('\n' + '='*60)
    print('开始运行所有爬虫')
    print('='*60)
    
    for spider_name in spiders:
        run_spider(spider_name, max_pages=3)  # 批量运行时减少页数
        print('\n')
    
    print('='*60)
    print('所有爬虫运行完毕')
    print('='*60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='Scrapy 爬虫运行工具')
    parser.add_argument(
        'spider',
        nargs='?',
        choices=['dongchedi', 'chezhi', 'all'],
        help='要运行的爬虫名称（dongchedi/chezhi/all）'
    )
    parser.add_argument(
        '-p', '--pages',
        type=int,
        default=5,
        help='车质网爬虫的最大页数（默认: 5）'
    )
    
    args = parser.parse_args()
    
    if not args.spider:
        # 显示帮助信息
        print('\n' + '='*60)
        print('Scrapy 爬虫运行工具')
        print('='*60)
        print('\n可用的爬虫：')
        print('  1. dongchedi  - 懂车帝销量数据')
        print('  2. chezhi     - 车质网质量投诉')
        print('  3. all        - 运行所有爬虫')
        print('\n运行命令示例：')
        print('  python run_spider.py dongchedi')
        print('  python run_spider.py chezhi')
        print('  python run_spider.py chezhi -p 10   # 爬取10页')
        print('  python run_spider.py all')
        print('='*60 + '\n')
        parser.print_help()
        return
    
    # 运行爬虫
    if args.spider == 'all':
        run_all_spiders()
    else:
        run_spider(args.spider, args.pages)


if __name__ == '__main__':
    main()
