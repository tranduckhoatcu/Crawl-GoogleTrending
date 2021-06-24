## Introduction

It will use Selenium to automatically crawl all data in 2020 from Google Trends of 26 categories which defined in Keywords.py 

**Be Aware of Anti-Crawler which make this script fail to connect to Google Trends please** 

**Run this script again**

## Installation

    pip3 install -r requirements.txt

## Setting
Please assign path of "chromedriver" file to webdriver_path variable in crawl_trending.py

## For Crawling

    python3 crawl_trending.py

This will generate:
- "vn_trend_2020.xls" file
- 2 figures of 10 Rising Search keywords and topics related to Finance in 2020
- 2 charts of Top 10 Search keywords and topics related to Finance in 2020