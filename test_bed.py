from scrapy.spiders import XMLFeedSpider


class MySpider(XMLFeedSpider):
    name = 'polisen.se'
    allowed_domains = ['polisen.se']
    start_urls = ['https://polisen.se/aktuellt/rss/hela-landet/handelser-i-hela-landet/']
    iterator = 'iternodes'  # This is actually unnecessary, since it's the default value
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.getall()))

        item['title'] = node.xpath('title').get()
        item['date'] = node.xpath('date').get()
        item['description'] = node.xpath('description').get()
        item['link'] = node.xpath('link').get()
        print(item)
