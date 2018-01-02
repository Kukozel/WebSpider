# coding:utf-8
from qzrc.URLManager import UrlManager
from qzrc.HtmlDownloader import HtmlDownloader
from qzrc.HtmlParser import HtmlParser
from qzrc.DataOutput import DataOutput
import requests
import re


class Spider_qzrc(object):
    def __init__(self):
        self.downloader = HtmlDownloader()
        self.parser = HtmlParser()
        self.output = DataOutput()

    def crawl(self):
        while (self.manager.has_new_url()):
            try:
                # 从URL管理器获取新的URL
                self.manager = UrlManager()
                new_url = self.manager.get_new_url()
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                data = self.parser.parser(new_url, html)
                # 数据存储器存储文件
                self.output.store_data(data)
                # 输出进度并保存进度
                print('抓取链接', new_url)
                print('已抓取%s个链接' % self.manager.old_url_size())
                # TODO：序列化保存进度
                self.manager.save_progress('new_urls.txt',self.manager.new_urls)
                self.manager.save_progress('old_urls.txt',self.manager.old_urls)
            except:
                print('crawl failed!')

    def initURLs(self, num):
        urls = set()
        for i in range(1, num + 1):
            page = i
            postdata = {
                'p': page,
                'pn': '150',
                'urlfrom': 'http://www.qzrc.com/gjrclist.shtml',
                'ps': '25',
            }
            # action=gjr 表示高级人才模块
            url3 = 'http://www.qzrc.com/Search.ashx?action=gjr&rnd='
            # post方法获取Json数据
            request = requests.post(url3, data=postdata)
            content = re.findall('{"UserID":"(.*?)","Birthday', request.text)
            for con in content:
                newUrl = 'http://resume.qzrc.com/' + con + '.html'
                urls.add(newUrl)
                print(newUrl)
        self.manager.save_progress('new_urls.txt', urls)
        emptyset = set()
        self.manager.save_progress('old_urls.txt', emptyset)

    def flushURLs(self, num):
        oldLen = self.manager.new_url_size()
        for i in range(1, num + 1):
            page = i
            postdata = {
                'p': page,
                'pn': '150',
                'urlfrom': 'http://www.qzrc.com/gjrclist.shtml',
                'ps': '25',
            }
            # action=gjr 表示高级人才模块
            url3 = 'http://www.qzrc.com/Search.ashx?action=gjr&rnd='
            # post方法获取Json数据
            request = requests.post(url3, data=postdata)
            content = re.findall('{"UserID":"(.*?)","Birthday', request.text)
            for con in content:
                newUrl = 'http://resume.qzrc.com/' + con + '.html'
                print(newUrl)
                self.manager.add_new_url(newUrl)
        newLen = self.manager.new_url_size()
        if newLen > oldLen:
            self.manager.save_progress('new_urls.txt', self.manager.new_urls)
            print('存在新的URL,已更新!')
        else:
            print('不存在新的URL!')


if __name__ == '__main__':
    spider = Spider_qzrc()

    # 初始化url集合,150页，高级人才专栏所有(仅第一次使用)
    # spider.initURLs(150)

    # 刷新url,是否有新的链接,150页(后期刷新使用)
    # spider.flushURLs(150)

    spider.crawl()
