# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time
import csv
import os

class Crawler:
    def __init__(self, crawlArea = 'dongcheng'):
        self.pageIndex = 35
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.links = []
        self.crawlArea = crawlArea

    def getPageLimit(self):
        url = 'http://bj.lianjia.com/ershoufang/' + self.crawlArea
        session = requesocks.session()
        session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
        response = session.get(url)
        pageCode = response.read()
        pattern = re.compile('totalPage":(.*?),')
        item = re.findall(pattern, pageCode)
        print "Page limit is " + str(item[0])
        return int(item[0])
        # try:
        #     url = 'http://bj.lianjia.com/ershoufang/' + self.crawlArea
        #     request = urllib2.Request(url, headers = self.headers)
        #     response = urllib2.urlopen(request)
        #     pageCode = response.read()
        #     # print pageCode
        #     # Get limit from pageCode
        #     pattern = re.compile('totalPage":(.*?),')
        #     item = re.findall(pattern, pageCode)
        #     print "Page limit is " + str(item[0])
        #     return int(item[0])

        # except urllib2.URLError, e:
        #     if hasattr(e,"reason"):
        #         print "Get page limit failed...",e.reason
        #         return 0

    def getPageCode(self, url):
        session = requesocks.session()
        session.proxies = {'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'}
        response = session.get(url)
        pageCode = response.read()
        print "Geting page code of " + url + " ..."
        return pageCode
        # try:
        #     request = urllib2.Request(url, headers = self.headers)
        #     response = urllib2.urlopen(request)
        #     pageCode = response.read()
        #     print "Geting page code of " + url + " ..."
        #     return pageCode
 
        # except urllib2.URLError, e:
        #     if hasattr(e,"reason"):
        #         print "Connection failed...",e.reason
        #         quit()
        #         return None
 	
 	# Extract links in one page and add it to memory
 	# If no more link, return false
    def addLinks(self, pageCode):
 		pattern = re.compile('<li class="clear"><a class="img " href="(.*?)" target')
		items = re.findall(pattern, pageCode)
		self.links.extend(items)

    def crawlPage(self, pageCode):
        print "Crawl page..."

        # 价格，均价，小区名称，所在区域
        pattern = re.compile('<div class="overview">.*?<div class=".*?price.*?"><span class="total">(.*?)</span>' + #0
            '<span class="unit"><span>(.*?)</span>.*?' + #1
            '<span class="unitPriceValue">(.*?)<i>(.*?)</i>.*?' + #2, 3
            '小区名称.*?</span>.*?<a.*?>(.*?)</a>.*?' + #4
            '所在区域.*?</span>.*?<a.*?>(.*?)</a>.*?' #5
            )
        items = re.findall(pattern, pageCode)
        print items
        if len(items) <= 0:
            print "CANNOT crawl this page."
            return items
        item = items[0]
        ret = []
        price = str(item[0]) + str(item[1])
        avgPrice = str(item[2]) + str(item[3])
        court = str(item[4])
        area = str(item[5])
        ret.append(price)
        ret.append(avgPrice)
        ret.append(court)
        ret.append(area)  
        # 基本属性，房屋标签，经纬度，反馈，小区介绍
        # To do

        return ret

    def start(self):
        print "Start Crawling..."
        pageLimit = self.getPageLimit()
        proxy_handler = urllib2.ProxyHandler({"http" : '127.0.0.1:9050'})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        # Load all pages
        while(self.pageIndex <= pageLimit):
        	print "Loading page " + str(self.pageIndex) + "..."
        	url = 'http://bj.lianjia.com/ershoufang/' + self.crawlArea + '/pg' + str(self.pageIndex)
        	pageCode = self.getPageCode(url)
        	self.addLinks(pageCode)
        	self.pageIndex = self.pageIndex + 1
        # Crawling pages
        with open(os.getcwd() + '/' + str(self.crawlArea) +'.csv', 'a') as f:
            writer = csv.writer(f)
            index = ['价格','均价','小区名称','所在区域']
            writer.writerow(index)
            for link in self.links:
                pageCode = self.getPageCode(link)
                row = self.crawlPage(pageCode)
                writer.writerow(row)

