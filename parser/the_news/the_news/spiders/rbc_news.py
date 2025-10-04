import scrapy
from scrapy import Request

class RbcNewsSpider(scrapy.Spider):
    name = "rbc_news"
    allowed_domains = ["www.rbc.ru"]
    start_urls = ["https://rssexport.rbc.ru/rbcnews/news/30/full.rss"]  # Только RSS для последовательного старта

    def parse(self, response):
        # Если это RSS-страница
        if "rss" in response.url:
            yield from self.parse_rss(response)
            # После завершения RSS переходим к главной странице
            yield Request("https://www.rbc.ru/", callback=self.parse)
            return

        # Извлекаем рубрики из футера (для главной страницы)
        rubric_elements = response.css('div.footer__title:contains("Рубрики") + ul.footer__list a')
        for elem in rubric_elements:
            rubric_name = elem.css('::text').get().strip() if elem.css('::text').get() else None
            href = elem.css('::attr(href)').get()
            if rubric_name and href:
                full_url = response.urljoin(href)
                yield Request(full_url, callback=self.parse_rubric, meta={'rubric_name': rubric_name})

    def parse_rss(self, response):
        items = response.css("channel item")
        language = response.css("channel language::text").get() or "ru"
        if items:
            for item in items:
                yield {
                    'source': 'rss',
                    'title': item.css("title::text").get() or "",
                    'description': item.css("description::text").get() or "",
                    'maintext': item.css("rbc_news\\:full-text::text").get() or "",
                    'image_url': item.css("rbc_news\\:url::text").get() or "",
                    'authors': item.css("author::text").get() or "",
                    'category': item.css("rbc_news\\:newsline::text").get() or "",
                    'date_publish': item.css("rbc_news\\:date::text").get() or "",
                    'time_publish': item.css("rbc_news\\:time::text").get() or "",
                    'language': language,
                    'url': item.css("link::text").get() or "",
                }

    def parse_rubric(self, response):
        rubric_name = response.meta['rubric_name']

        # Извлекаем ссылки на новости
        links = response.css(".item__link::attr(href)").getall()
        if links:
            for link in links:
                yield Request(link, callback=self.parse_news_page, meta={'rubric_name': rubric_name})

    def parse_news_page(self, response):
        image_src = response.css(".smart-image__img::attr(src)").get() or ""
        yield {
            'source': response.meta['rubric_name'],
            'title': response.css("h1::text").get() or "",
            'description': response.css(".article__header__yandex::text").get() or "",
            'maintext': ' '.join([text.strip() for text in response.css(".article__text p::text").getall() if text.strip()]),
            'image_url': image_src.strip(),
            'authors': response.css(".article__authors__author__name::text").get() or "",
            'date_publish': response.css(".article__header__date::text").get() or "",
            'url': response.url
        }