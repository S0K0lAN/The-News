import scrapy
from scrapy import Request

class RbcNewsSpider(scrapy.Spider):
    name = "rbc_news"
    start_urls = [
        "https://www.rbc.ru/",  # Главная с футером для рубрик
        "https://rssexport.rbc.ru/rbcnews/news/30/full.rss",  # RSS-канал
    ]

    def parse(self, response):
        # Если это RSS-страница
        if "rss" in response.url:
            yield from self.parse_rss(response)
            return  # Не ищем рубрики в RSS

        # Извлекаем рубрики из футера (только на главной)
        rubric_elements = response.css('div.footer__title:contains("Рубрики") + ul.footer__list a')
        for elem in rubric_elements:
            rubric_name = elem.css('::text').get().strip()  # "Политика", "Экономика" и т.д.
            href = elem.css('::attr(href)').get()
            if rubric_name and href:
                full_url = response.urljoin(href)
                yield Request(full_url, callback=self.parse_rubric, meta={'rubric_name': rubric_name})

    def parse_rss(self, response):
        items = response.css("channel item")
        language = response.css("channel language::text").get()
        if items:
            for item in items:
                yield {
                    'source': 'rss',
                    'title': item.css("title::text").get(),
                    'description': item.css("description::text").get(),
                    'maintext': item.css("rbc_news\\:full-text::text").get(),
                    'image_url': item.css("rbc_news\\:url::text").get(),
                    'authors': item.css("author::text").get(),
                    'category': item.css("rbc_news\\:newsline::text").get(),
                    'date_publish': item.css("rbc_news\\:date::text").get(),
                    'time_publish': item.css("rbc_news\\:time::text").get(),
                    'language': language,
                    'url': item.css("link::text").get(),
                }

    def parse_rubric(self, response):
        rubric_name = response.meta['rubric_name']
        
        # Извлекаем новости с текущей страницы
        news_items = response.css("article.news-item")  # Адаптируй: проверь в shell, может быть "div.js-news-item" или "article"
        if news_items:
            for news in news_items:
                yield {
                    'source': rubric_name,
                    'title': news.css("h2 a::text").get(),
                    'description': news.css("p.lead::text").get(),
                    'maintext': news.css(".article__text::text").get() or "",  # Если нет — пусто
                    'image_url': news.css("img::attr(src)").get(),
                    'authors': news.css(".author::text").get(),
                    'date_publish': news.css("time::attr(datetime)").get(),
                    'url': response.urljoin(news.css("a::attr(href)").get()),
                }

        # ПАГИНАЦИЯ: Ищем ссылку на следующую страницу
        next_page = response.css('a.pagination-next::attr(href)').get()  # Вариант 1: класс next
        # Альтернативы (протестируй одну):
        # next_page = response.css('li.next a::attr(href)').get()  # Вариант 2: li.next
        # next_page = response.css('a[href*="page="]:last::attr(href)').get()  # Вариант 3: последняя ссылка с page=
        
        if next_page is not None:
            full_next_url = response.urljoin(next_page)
            # Передаём rubric_name дальше для всех страниц
            yield Request(full_next_url, callback=self.parse_rubric, meta={'rubric_name': rubric_name})