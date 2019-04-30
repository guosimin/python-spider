import scrapy

def getUrl():
    return 'https://search.51job.com/list/030200,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='



class itemSpider(scrapy.Spider):
    name = 'argsSpider'
    def start_requests(self):
        url = getUrl()
        # request_cookies =
        tag = getattr(self, 'tag', None)  # 获取tag值，也就是爬取时传过来的参数
        if tag is not None:  # 判断是否存在tag，若存在，重新构造url
            url = url + 'tag/' + tag  # 构造url若tag=爱情，url= "http://lab.scrapyd.cn/tag/爱情"
        yield scrapy.Request(url, self.parse)  # 发送请求爬取参数内容

    def parse(self, response):
        mingyan = response.css('div#resultList>.el')  # 提取首页所有名言，保存至变量mingyan
        for v in mingyan:  # 循环获取每一条名言里面的：名言内容、作者、标签
            t1 = v.css('.t1 a::text').extract_first()
            t2 = v.css('.t2 a::attr(title)').extract_first()  # 提取名言
            t3 = v.css('.t3::text').extract_first()
            t4 = v.css('.t4::text').extract_first()

            t1 = str(t1).replace(' ', '')
            t1 = str(t1).replace('\r|\n|\\s', '')
            t2 = str(t2).replace(' ', '')
            t3 = str(t3).replace(' ', '')
            t4 = str(t4).replace(' ', '')

            item = {
                't1': t1,
                't2': t2,
                't3': t3,
                't4': t4,
            }
            yield item



        #
        # next_page = response.css('div.p_in li').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     print("next_page+++++++++++"+next_page)
            # yield scrapy.Request(next_page, callback=self.parse)
