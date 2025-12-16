@echo off
chcp 65001 >nul
echo ============================================================
echo Scrapy 爬虫快速启动工具
echo ============================================================
echo.

:menu
echo 请选择要运行的爬虫：
echo   1. 懂车帝爬虫 (dongchedi) - 抓取销量数据
echo   2. 车质网爬虫 (chezhi) - 抓取质量投诉
echo   3. 运行所有爬虫 (all)
echo   4. 测试爬虫和数据库
echo   5. 查看日志文件
echo   0. 退出
echo.

set /p choice="请输入选项 (0-5): "

if "%choice%"=="1" goto dongchedi
if "%choice%"=="2" goto chezhi
if "%choice%"=="3" goto all
if "%choice%"=="4" goto test
if "%choice%"=="5" goto log
if "%choice%"=="0" goto end
echo 无效选项，请重新选择
goto menu

:dongchedi
echo.
echo ============================================================
echo 启动懂车帝爬虫...
echo ============================================================
python run_spider.py dongchedi
goto menu_return

:chezhi
echo.
set /p pages="请输入要爬取的页数 (默认5页): "
if "%pages%"=="" set pages=5
echo.
echo ============================================================
echo 启动车质网爬虫 (爬取 %pages% 页)...
echo ============================================================
python run_spider.py chezhi -p %pages%
goto menu_return

:all
echo.
echo ============================================================
echo 启动所有爬虫...
echo ============================================================
python run_spider.py all
goto menu_return

:test
echo.
echo ============================================================
echo 测试爬虫和数据库...
echo ============================================================
python test_spider.py
goto menu_return

:log
echo.
echo ============================================================
echo 查看日志文件...
echo ============================================================
if exist logs\scrapy_spider.log (
    type logs\scrapy_spider.log | more
) else (
    echo 日志文件不存在
)
echo.
pause
goto menu

:menu_return
echo.
echo ============================================================
pause
echo.
goto menu

:end
echo.
echo 再见！
echo.
exit
