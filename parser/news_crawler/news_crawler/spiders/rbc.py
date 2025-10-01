import scrapy

class RbcSpider(scrapy.Spider):
    name = "rbc"
    allowed_domains = ["www.rbc.ru"]
    start_urls = ["https://rssexport.rbc.ru/rbcnews/news/30/full.rss"]

    def parse(self, response):
        items = response.css("channel item")
        language = items.css("language::text").get()
        for item in items:
            yield {
                'title' : item.css("title::text").get(),
                'description' : item.css("description::text").get(),
                'maintext' : item.css("rbc_news\\:full-text::text").get(),
                'image_url' : item.css("rbc_news\\:url::text").get(),
                'authors' : item.css("author::text").get(),
                'category' : item.css("rbc_news\\:newsline::text").get(),
                'date_publish' : item.css("rbc_news\\:date::text").get(),
                'time_publish' : item.css("rbc_news\\:time::text").get(),
                'language' : language,
                'url' : item.css("link::text").get(),
            }

        

