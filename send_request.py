import requests

ARTICLE_URL = "https://elemental.medium.com/10-signs-the-pandemic-is-about-to-get-much-worse-cf261bf3885d"
print(requests.get("http://127.0.0.1:8000/color_score", json={"url": ARTICLE_URL}).json())