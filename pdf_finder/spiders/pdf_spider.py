import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import csv
import requests

class PdfSpider(CrawlSpider):
    name = 'pdf_spider'

    def __init__(self, start_url=None, search_text=None, *args, **kwargs):
        super(PdfSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = [start_url.split('/')[2]]
        self.start_urls = [start_url]
        self.search_text = search_text

        self.pdf_links_file = open('pdf_links.csv', 'w', newline='', encoding='utf-8')
        self.pdf_writer = csv.writer(self.pdf_links_file)
        self.pdf_writer.writerow(['pdf_url', 'page_url'])

        self.non_working_pdfs_file = open('non_working_pdfs.csv', 'w', newline='', encoding='utf-8')
        self.non_working_writer = csv.writer(self.non_working_pdfs_file)
        self.non_working_writer.writerow(['status_code', 'pdf_url', 'page_url'])

        self.search_results_file = open('search_results.csv', 'w', newline='', encoding='utf-8')
        self.search_writer = csv.writer(self.search_results_file)
        self.search_writer.writerow(['page_url'])

        self.page_count = 0

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.page_count += 1
        print(f'Pages processed: {self.page_count}')
        page_text = response.text

        pdf_links = response.css('a::attr(href)').re(r'.*\.pdf')
        for pdf_link in pdf_links:
            pdf_url = response.urljoin(pdf_link)
            self.pdf_writer.writerow([pdf_url, response.url])
            self.pdf_links_file.flush()

            try:
                r = requests.get(pdf_url, headers={'Range': 'bytes=0-1024'}, timeout=60)
                if r.status_code != 206 and r.status_code != 200:
                    self.non_working_writer.writerow([r.status_code, pdf_url, response.url])
                    self.non_working_pdfs_file.flush()
            except requests.exceptions.RequestException as e:
                self.non_working_writer.writerow([str(e), pdf_url, response.url])
                self.non_working_pdfs_file.flush()

        if self.search_text and self.search_text in page_text:
            self.search_writer.writerow([response.url])
            self.search_results_file.flush()

    def closed(self, reason):
        self.pdf_links_file.close()
        self.non_working_pdfs_file.close()
        self.search_results_file.close()
        print(f'Total pages processed: {self.page_count}')
        print(f'Total PDFs found: {self.pdf_links_file}')
        print(f'Total non-working PDFs: {self.non_working_pdfs_file}')
        print(f'Total search results: {self.search_results_file}')