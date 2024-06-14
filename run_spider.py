from scrapy.crawler import CrawlerProcess
from pdf_finder.spiders.pdf_spider import PdfSpider

if __name__ == '__main__':
    start_url = input("Enter the start URL: ")
    search_text = input("Enter the paragraph to search for: ")

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'LOG_ENABLED': False,
    })
    process.crawl(PdfSpider, start_url=start_url, search_text=search_text)
    process.start()