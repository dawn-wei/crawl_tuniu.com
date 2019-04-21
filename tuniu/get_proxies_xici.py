# -*- coding: utf-8 -*-
import scrapy
import json
 
#高匿代理
class ProxySpider(scrapy.Spider):
    name = 'proxy'
    allowed_domains = ['www.xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/%s' % i for i in range(1,6)]
 
    def parse(self, response):
        #position()>1 获取tr标签位置大于1的标签
        for sel in response.css('table#ip_list').xpath('.//tr[position()>1]'):
            # nth-child(2)获取第二个子标签 （注意这里的顺序从1开始）
            ip = sel.css('td:nth-child(2)::text').extract_first()   #ip
            port = sel.css('td:nth-child(3)::text').extract_first()  #端口
            scheme = sel.css('td:nth-child(6)::text').extract_first()  #类型HTTP，https
 
            # 拼接代理url
            proxy = '%s://%s:%s' % (scheme,ip,port)
 
            # 定义json数据 meta 文本
            meta = {
                'proxy':proxy,
                'dont_retry':True,        #只下载一次，失败不重复下载
                'download_timeout':10,    # 设置等待时间 
 
                '_proxy_ip':ip,
                '_proxy_scheme':scheme
            }
 
            #校验代理是否可用  通过访问httpbin.org/ip,进行检测
            url = '%s://httpbin.org/ip' % scheme
            yield scrapy.Request(url,callback=self.check,meta=meta,dont_filter=True)
 
    def check(self,response):
        proxy_ip = response.meta['_proxy_ip']
        proxy_scheme = response.meta['_proxy_scheme']
 
        #json.loads（）将json文本返回字典类型   origin原代理
        if json.loads(response.text)['origin'] == proxy_ip:
            yield {
                'proxy':response.meta['proxy'],
                'scheme':proxy_scheme,
            }