# content_recommendation_engine
work on the content recommendation engine for W3LL



## Scraping
uses [Scrapy](https://scrapy.org/)

files:
- `medium_scraper_tag_archive.py` : bulk scraper code
- `scrapy_wrapper.py`: wrapper to run `medium_scrapper_tag_archive.py` and set parameters
- `reading_scraped_data.ipynb`: notebook to analyze scraped data

output:
- `logs/`: log files from scrapy end up here. Filenames: `startdateTAGenddate.log` 
- `scraped_data/`: JSON files of scrapped data end up here. Filenames: `startdateTAGenddate.json`

to run scraper:
- set parameters in `scrapy_wrapper.py`
- run `python scrapy_wrapper.py`
