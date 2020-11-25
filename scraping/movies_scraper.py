from bs4 import BeautifulSoup as BS
import requests,datetime,json
import argparse
import pandas as pd

# defaults
genre = 'comedy'
output_file = 'scraped_data/' + genre + '.csv'
output_file_json = 'scraped_data/' + genre + '.json'
# + datetime.now().strftime(%d%m%Y)
format = 'csv'

parser = argparse.ArgumentParser()
parser.add_argument('-genre', default=genre,
                    help='Movie genre to scrape top 50 list.')
parser.add_argument('-output', default=output_file,
                    help='Output file name.')
parser.add_argument('-format', default=format,
                    help='Output file format.')
args = parser.parse_args()
genre = args.genre
output_file = 'scraped_data/' + genre + '.csv'
output_file_json = 'scraped_data/' + genre + '.json'
format = args.format

# Can delete this method
def scrape_top_list():
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    page = requests.get(url)
    soup = BS(page.text, 'html.parser')
    TopMoviesList = []
    tbody = soup.find('tbody', class_='lister-list')
    trs = tbody.find_all('tr')

    # print(tbody)

    for tr in trs:
        # Here we scrape rank,name,released year of movies.
        movie_data = tr.find('td', class_="titleColumn").get_text().strip().split()
        # print(movie_data)
        # Here we create dictionary for movie details
        movies_detail = {'rank': '', 'name': '', 'year': '', 'rating': '', 'url': '', 'reviews': []}
        movies_detail['rank'] = int(movie_data[0].strip('.'))
        movies_detail['year'] = int(movie_data[-1].strip("()"))
        movie_data.pop(0)
        movie_data.pop(-1)
        movies_detail['name'] = " ".join(movie_data)
        movies_detail['rating'] = float(tr.find('strong').get_text())
        movie_url = "https://www.imdb.com" + tr.find('a').get('href')[0:17]
        movies_detail['url'] = movie_url
        reviews_url = movie_url+'reviews'
        movies_detail['reviews'] = get_movie_reviews(reviews_url)
        # Here we appending the movie details dictonary in TopMoviesList
        # print(movies_detail)
        TopMoviesList.append(movies_detail)

    return (TopMoviesList)


def get_movie_reviews(url):
    page = requests.get(url)
    soup = BS(page.text, 'html.parser')
    body = soup.find('div', class_='lister-list')
    body_divs = body.find_all('div', class_='lister-item')
    reviews_output = []

    for movie_div in body_divs:
        review_data = movie_div.find('div',class_="lister-item-content")

        review_json = {'review_title' : '','review_description' : ''}
        review_json['review_title'] = review_data.find('a').get_text().strip('\n')
        review_description = review_data.find('div',class_="content").find('div',class_="text").get_text().strip('\n')
        review_json['review_description'] = review_description
        reviews_output.append(review_json)

    return reviews_output


def get_movie_scrape_by_genre():
    url = "https://www.imdb.com/search/title/?genres="+genre
    page = requests.get(url)
    soup = BS(page.text, 'html.parser')
    body = soup.find('div',class_="lister-list")
    movie_divs = body.find_all('div',class_="lister-item")
    Movies_By_Genre =[]

    for movie_div in movie_divs:
        # time.sleep(1)
        movie_content = movie_div.find('div',class_="lister-item-content")
        movie_details = {'rank':'', 'name':'', 'year':'', 'rating':'', 'url':'', 'certificate':'', 'runtime':'', 'reviews':[]}

        movie_header = movie_content.find('h3',class_="lister-item-header")

        try:
            rank = int(movie_header.find('span',class_="lister-item-index").get_text().strip('.'))
        except AttributeError:
            rank = -1
        movie_details['rank'] = rank

        movie_details['year'] = movie_header.find('span',class_="lister-item-year").get_text().strip("()").replace("\u2013",'-')
        movie_details['name'] = movie_header.find('a').get_text()
        movie_url = "https://www.imdb.com" + movie_header.find('a').get('href')[0:17]
        if movie_url[-1] != '/':
            movie_url += '/'
        movie_details['url'] = movie_url

        movie_subheader = movie_content.find('p',class_="text-muted")
        try:
            certificate = movie_subheader.find('span',class_="certificate").get_text()
        except AttributeError:
            certificate = "N/A"
        movie_details['certificate'] = certificate
        try:
            runtime = movie_subheader.find('span',class_="runtime",default_="").get_text()
        except AttributeError:
            runtime = 'N/A'
        movie_details['runtime'] = runtime

        try:
            rating = float(movie_content.find('strong').get_text())
        except AttributeError:
            rating = -1
        movie_details['rating'] = rating

        review_url = movie_url+'reviews'
        movie_details['reviews'] = get_movie_reviews(review_url)

        # print(movie_details)
        print("Found movie: ",movie_details['name'])

        Movies_By_Genre.append(movie_details)

    if format == 'csv' :
        df = pd.DataFrame(Movies_By_Genre)
        df.to_csv(output_file, index=False)
    else:
        with open(output_file_json, "w") as file:
            json.dump(Movies_By_Genre,file)

    print("Process complete!")

    # return (Movies_By_Genre)


# top_movies = scrape_top_list()
# pprint.pprint(top_movies)
# get_movie_reviews("https://www.imdb.com/title/tt1087461/reviews")

get_movie_scrape_by_genre()