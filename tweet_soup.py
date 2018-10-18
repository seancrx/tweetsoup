import requests
import json
import sys
from bs4 import BeautifulSoup
from csv import writer

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
username = sys.argv[1]
url = 'https://twitter.com/' + username
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, 'html.parser')

tweets = soup.find_all(class_='tweet')

with open(username+'_tweets.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    csv_writer = writer(csv_file)
    header = ['Tweet', 'Date']
    csv_writer.writerow(header)

    for tweet in tweets:
        text = tweet.find(class_='TweetTextSize').get_text()
        time = tweet.find(class_='_timestamp').get_text()
        csv_writer.writerow([text, time])

    next_pointer = soup.find('div', {'class': 'stream-container'})['data-min-position']

    while next_pointer != None:
        next_url = 'https://twitter.com/i/profiles/show/' + username + '/timeline/tweets?include_available_features=1&include_entities=1&max_position=' + next_pointer + '&reset_error_state=false'

        next_response = None
        try:
            next_response = requests.get(next_url)
        except Exception as e:
            print(e)

        tweets_data = next_response.text
        tweets_obj = json.loads(tweets_data)
        
        next_pointer = tweets_obj['min_position']
        html = tweets_obj['items_html']
        soup = BeautifulSoup(html, 'lxml')
        
        tweets = soup.find_all(class_='tweet')

        for tweet in tweets:
            text = tweet.find(class_='TweetTextSize').get_text()
            time = tweet.find(class_='_timestamp').get_text()
            csv_writer.writerow([text, time])
