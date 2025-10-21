# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
from psycopg2 import sql


class TheNewsPipeline:
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("PG_HOST", "localhost"),
            port=crawler.settings.getint("PG_PORT", 5432),
            user=crawler.settings.get("PG_USER", "tnadmin"),
            password=crawler.settings.get("PG_PASSWORD", "12345678"),
            database=crawler.settings.get("PG_DATABASE", "the_news")
        )

    def __init__(self, host, port, user, password, database):
        self.pg_host = host
        self.pg_port = port
        self.pg_user = user
        self.pg_password = password
        self.pg_database = database
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host=self.pg_host,
            port=self.pg_port,
            user=self.pg_user,
            password=self.pg_password,
            dbname=self.pg_database
        )
        self.cur = self.conn.cursor()
        # Создаём таблицу news если её нет
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id SERIAL PRIMARY KEY,
            source TEXT,
            title TEXT,
            description TEXT,
            maintext TEXT,
            image_url TEXT,
            authors TEXT,
            category TEXT,
            date_publish TEXT,
            time_publish TEXT,
            language TEXT,
            url TEXT
        )
        """)
        self.conn.commit()

    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        # Поддерживает dict или scrapy.Item
        data = dict(item)
        values = (
            data.get("source"),
            data.get("title"),
            data.get("description"),
            data.get("maintext"),
            data.get("image_url"),
            data.get("authors"),
            data.get("category"),
            data.get("date_publish"),
            data.get("time_publish"),
            data.get("language"),
            data.get("url"),
        )
        insert_sql = """
        INSERT INTO news (
            source, title, description, maintext, image_url,
            authors, category, date_publish, time_publish, language, url
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """
        self.cur.execute(insert_sql, values)
        self.conn.commit()
        return item