from datetime import datetime

class CleanText:
    def process_item(self, item, spider):
        text=item.get('text','')
        if text:
            item['text']=text.strip()
        return item

class AddTime:
    def process_item(self, item, spider):
        item['crawled_time']=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return item
