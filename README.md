# Web_Crawler

Web_Crawler is a Scrapy-based web crawler designed to extract PDF links, check their status, and search for specific text within web pages. This tool can be used to monitor large websites for PDF availability and validate their functionality.

## Features

- Crawl web pages to find PDF links.
- Check the status of each PDF link to identify non-working links.
- Search for specific text within the web pages and record the pages containing the text.
- Output results to CSV files for easy analysis.

## Requirements

- Python 3.6+
- Scrapy
- Requests

## Installation

1. Clone the repository

2. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Web_Crawler, use the following command format:

```bash
python run_spider.py
