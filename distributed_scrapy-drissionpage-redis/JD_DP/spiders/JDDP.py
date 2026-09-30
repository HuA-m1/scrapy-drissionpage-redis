import time
import scrapy
from JD_DP.items import JdDpItem
from scrapy_drissionpage.spider import DrissionSpider

# 修改为分布式爬虫
# ---1. 导入分布式爬虫类(添加)
from scrapy_redis.spiders import RedisSpider

# ---2. 继承分布式爬虫类
class JddpSpider(DrissionSpider,RedisSpider):
    name = "JDDP_REDIS"
    
# ---3. 注销 start
    # async def start(self):
    #     with open("./JD_DP/spiders/UrlRequests.txt","r",encoding="utf-8")as f:
    #         keywords=f.read().splitlines()
    #     for keyword in keywords:
    #         yield self.drission_request(
    #                 f'https://search.jd.com/Search?keyword={keyword}',
    #                 page_type='chromium', # 浏览器模式
    #                 callback=self.parse,
    #                 )
# ---4. 设置 redis-key    
    redis_key='JD'

    def make_request_from_data(self, data):
        url = data.decode('utf-8') if isinstance(data, bytes) else data
        return self.drission_request(
            url,
            page_type='chromium',
            callback=self.parse,
            dont_filter=True
        )
    
    def parse(self, response):
        # response.page.ele('x://*[@id="search-condition"]//span[text()="ROG"]').click(by_js=True)
        while True:
            oldHeight=response.page.run_js('return document.body.scrollHeight')
            response.page.scroll.to_bottom()
            time.sleep(0.8)
            newHeight=response.page.run_js('return document.body.scrollHeight')
            if newHeight==oldHeight:
                break
        divs=response.page.eles('x://*[@id="searchCenter"]/div/div/div[3]/div[1]/div/div[position()>1]')
        for div in divs:
            title=div.ele('x:.//div/div[2]/div/div[1]/span').text
            price=div.ele('x:.//div/div[2]/div/div[3]/span[1]/span').text
            QuantitySold=div.ele('x:.//div/div[2]/div/div[5]/span/span').text
            StoreName=div.ele('x:.//div/div[2]/div/div[6]/span/span').text
            item=JdDpItem(
                title=title,
                price=price,
                QuantitySold=QuantitySold,
                StoreName=StoreName,
            )
            print(item.title+'***'+item.price+'***'+item.QuantitySold+'***'+item.StoreName)
            yield item