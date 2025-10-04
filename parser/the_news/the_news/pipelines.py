# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TheNewsPipeline:
    def open_spider(self, spider):
        self.file = open('news.json', 'w')  # 'w' mode deletes existing contents
        self.file.write('[\n')  # Start JSON array

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + ',\n'
        self.file.write(line)
        return item