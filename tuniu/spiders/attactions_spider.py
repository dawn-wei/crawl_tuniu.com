# -*- coding: utf-8 -*-
import scrapy
from tuniu.items import AttractionsItem, RateItem
from tuniu.getIps import GetIpThread

# xpath 尚未完善

class AttactionsSpiderSpider(scrapy.Spider):
	name = 'attactions_spider'
	allowed_domains = ['tuniu.com']
	#start_urls = ['http://www.tuniu.com/place']

	custom_settings = {

    	"ITEM_PIPELINES": {
            'tuniu.pipelines.AttractionsPipeline': 300,
            'tuniu.pipelines.RatePipeline': 300,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        },
        "ROBOTSTXT_OBEY": False  # 需要忽略ROBOTS.TXT文件
    }


	total_pages = 0
	'''
	#base_url = 'http://tuniu.com'
	#handle_httpstatus_list = [301, 302]
	# 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
	order = "请把这里替换为您的IP提取码"
	# 获取IP的API接口
	apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
	# 获取IP时间间隔，建议为5秒
	fetchSecond = 5
	# 开始自动获取IP
	GetIpThread(apiUrl, fetchSecond).start()
'''

	def start_requests(self):
		url = 'http://www.tuniu.com/place/'
		#yield scrapy.Request(url, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301, 302]}, dont_filter = True, callback = self.parse)
		yield scrapy.Request(url, callback = self.parse)


	def parse(self, response):
		# crawl all city_urls
		city_urls = response.xpath('//a[@class="J-city_item"]/@href').extract()
		print(len(city_urls))
		for city_url in city_urls:
			#yield scrapy.Request(city_url,  meta = {'dont_redirect': True, 'handle_httpstatus_list': [301, 302]}, callback = self.parse_guide, dont_filter = True)   
			yield scrapy.Request(city_url, callback = self.parse_guide)   


	def parse_guide(self, response):
		
		base_url = 'http://www.tuniu.com'
		jingdian_url = response.xpath('//*[@id="container"]/div[1]/div[3]/div/ul/li[3]/a/@href').extract()
		
		if len(jingdian_url) > 0:

			jingdian_url = jingdian_url[0]
			#yield scrapy.Request(base_url + jingdian_url, meta = {'dont_redirect': True, 'handle_httpstatus_list': [301, 302]}, callback = self.parse_jingdian_firstPage, dont_filter = True)
			yield scrapy.Request(base_url + jingdian_url, callback = self.parse_jingdian_firstPage)

			#print('***************')
			# next page
			url_firstPage = base_url + jingdian_url

			for i in range(self.total_pages):
				next_url = url_firstPage + '0/0/' + str(i + 1) + '/#allSpots'
				yield scrapy.Request(next_url, callback = self.parse_jingdian)

	def parse_jingdian_firstPage(self, response):
		# get total pages num
		#print('*******************')

		items = response.xpath('//*[@id="allSpots"]/div/div[3]/div/a/@href').extract()
		
		if len(items) == 11:
			self.total_pages = int (items[-1].split('/')[-1].split('#')[0])
		else:
			self.total_pages = len(items)


	def parse_jingdian(self, response):
		# crawl all sites
		site_urls = response.xpath('//a[@class="pic"]/@href').extract()
		# for each
		base_url = 'http://tuniu.com'
		for site_url in site_urls:
			url = base_url + site_url
			yield scrapy.Request(url, callback = self.parse_site_info)


	def parse_site_info(self, response):

		site_name = response.xpath('//*[@id="container"]/div[3]/div/a[1]/div/div/h1/text()').extract()
		if len(site_name) > 0:
			site_name = site_name[0]
		else:
			return

		description = response.xpath('//*[@id="view_bar"]/div[1]/p/text()').extract()
		if len(description) > 0:
			description = description[0]
		else:
			description = ''

		rates = response.xpath('//div[@class="item"]//div[@class="content "]/text()').extract()


		print(site_name)
		print(description)
		
		for rate in rates:
			print(rate)

		#save to json file
		import json

		save_json1 = {'site':site_name , 'description': description}
		with open('save_json1.json', 'a') as file1:
			json.dump(save_json1, file1)
			file1.write('\n')

		for rate in rates:
			save_json2 = {'site': site_name, 'rate': rate}
			with open('save_json2.json', 'a') as file2:
				json.dump(save_json2, file2)
				file2.write('\n')

		'''

		# store site info
		item = AttractionsItem()
		item['site_name'] = site_name.encode('utf-8').strip()
		item['description'] = description.encode('utf-8').strip()
		yield item



		# rates exists
		if len(rates) > 0:
			# store site reviews
			item = RateItem()
			for i in range(len(rates)):
				item['site_name'] = site_name.encode('utf-8').strip()
				item['rate'] = rates[i].encode('utf-8').strip()
				yield item

				'''