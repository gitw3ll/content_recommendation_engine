# Content Recommendation Engine (CRE) for W3LL
Goal: to recommend media content (articles, videos, music, etc.) to users which will most suit their wellness needs.

---

## Scraping (Medium Articles)
uses [Scrapy](https://scrapy.org/)

files:
- `medium_archive_article_scraper.py` : bulk scraper code. Given tag and other parameters, scrapes information from articles in Medium archive.
- `scrapy_wrapper.py`: wrapper to run `medium_archive_article_scraper.py` and set parameters.
- `medium_tag_crawler.py` : different scraper code for scraping tags only and not articles. Mainly used for network visualization.
- `notebooks/`: various notebooks to analyze scraped data
- `optimizing/`: tests to speed up scraping process

output:
- `logs/`: log files from scrapy end up here. Filenames: `startdate_TAG_enddate.log`
- `scraped_data/`: JSON files of scrapped data end up here. Filenames: `startdate_TAG_enddate.json`

to run scraper:
- run `python scrapy_wrapper.py -tag TAG -start_date YYYMMDD -end_date YYYMMDD -clap_limit N --include_body`
- arguments are optional, default parameters in `scrapy_wrapper.py`

## Text Analysis
files:
- `medium_article_scoring.ipynb` : returns top x articles from tag
- `medium_tag_scoring.ipynb` : color scores overall tag
- `text_scorer.py ` : color scoring for text file
- ` top_health_articles.json ` : health scrape
- `top_wellness_articles.json ` : wellness scrape

to run text_scorer:
- run `python text_scorer.py filepath`
- argument is required

## Streamlit App
- enter URL of an article (Medium, NYT, WP, etc.) and see a radar chart showing a breakdown of the color score from the text analysis.
- Requires [Streamlit](https://www.streamlit.io/) to run locally. Can be added to website.
- To run locally:
`streamlit run text_scoring_app.py`

## Network Visualization of Tags on Medium
[View current state](https://raw.githack.com/gitw3ll/content_recommendation_engine/master/visualization/networks.html)

