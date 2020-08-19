# content_recommendation_engine
work on the content recommendation engine for W3LL



## Scraping
uses [Scrapy](https://scrapy.org/)

files:
- `medium_scraper_tag_archive.py` : bulk scraper code
- `scrapy_wrapper.py`: wrapper to run `medium_scraper_tag_archive.py` and set parameters
- `notebooks/`: various notebooks to analyze scraped data
- `optimizing/`: tests to speed up scraping process
- `visualization/`: network visualizations using d3.js
output:
- `logs/`: log files from scrapy end up here. Filenames: `startdateTAGenddate.log`
- `scraped_data/`: JSON files of scrapped data end up here. Filenames: `startdateTAGenddate.json`

to run scraper:
- run `python scrapy_wrapper.py -tag TAG -start_date YYYMMDD -end_date YYYMMDD`
- arguments are optional, default parameters in `scrapy_wrapper.py`
