import scrapy

class RbcNewsSpider(scrapy.Spider):
    name = "rbc_news"
    allowed_domains = ["rssexport.rbc.ru"]
    start_urls = ["https://rssexport.rbc.ru/rbcnews/news/30/full.rss"]

    def parse(self, response):
        items = response.xpath("//channel/item")
        language = response.xpath("//channel/language/text()").get() or "ru"
        for item in items:
            yield {
                "source": "rss",
                "title": item.xpath("title/text()").get() or "",
                "description": item.xpath("description/text()").get() or "",
                "maintext": item.xpath("*[local-name() = 'full-text']/text()").get() or "",
                "image_url": item.xpath("*[local-name() = 'url']/text()").get() or "",
                "authors": item.xpath("author/text()").get() or "",
                "category": item.xpath("*[local-name() = 'newsline']/text()").get() or "",
                "date_publish": item.xpath("*[local-name() = 'date']/text()").get() or "",
                "time_publish": item.xpath("*[local-name() = 'time']/text()").get() or "",
                "language": language,
                "url": item.xpath("link/text()").get() or "",
            }