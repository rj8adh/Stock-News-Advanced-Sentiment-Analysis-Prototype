# So far, results are fairly unpredictable, will have to do more testing to see if this approach is viable

from NewsSentiment import TargetSentimentClassifier
from openai import OpenAI
import os

tsc = TargetSentimentClassifier()

API_KEY = os.getenv('API_KEY')

client = OpenAI(api_key=API_KEY)

def request_API(prompt, tokens: bool = True):
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                            messages=prompt)

    if tokens:  # Attempt to make a seperate box for token printing
        print(
            f'\nYou used {response.usage.prompt_tokens} prompt tokens + {response.usage.completion_tokens} completion tokens = {response.usage.total_tokens} tokens\n'
        )

    return response.choices[0].message.content.strip()



def scrapeHeadlines():

    import bs4
    import requests

    stocks = []
    titles = []
    links = []

    url='https://finance.yahoo.com/quote/'

    stock = input("What stocks do you want to webscrape?(type end to quit) ")
    stocks.append(stock.upper())

    while stocks[-1].lower() != 'end':
        stock = input("What stocks do you want to webscrape?(type end to quit) ")
        stocks.append(stock.upper())

    for i in range(len(stocks) - 1):
        soup = bs4.BeautifulSoup(requests.get(url + stocks[i] + '/').text, 'html.parser')

        anchor = soup.find_all('a', attrs={'class':'subtle-link fin-size-small thumb yf-1e4diqp'})

        for atrb in anchor:
            titles.append(atrb['title'])
            links.append(atrb['href'])

    return titles, links

headlines, hrefs = scrapeHeadlines()

data = []

i = 0

while i < len(headlines):
    # print('\n\n', headlines[i], '\n\n', hrefs[i])
    AIResponse = request_API([{"role": "system", "content": "You are stock bot designed to give extremely short responses"}, {"role": "user", "content": f"return what MAJOR stock is the main focus of the following headline, keep in mind the focus could be at end of the sentence rather than beginning:{headlines[i]} ONLY RETURN THE COMPANY NAME, NOTHING ELSE. Return 'NONE' if headline doesnt meantion a specific stock"}], False)
    if 'NONE' in AIResponse:
        headlines.pop(i)
        continue
    
    i += 1
    data.append(("", AIResponse, headlines[i]))




sentiments = tsc.infer(targets=data)

for i, result in enumerate(sentiments):
    if (result[0]['class_label']=='neutral'):
        print("Headline:", headlines[i])
        print("Sentiment: ", i, result[1]['class_label'])
        print("Probability: ", result[1]['class_prob'])
    else:
        print("Headline:", headlines[i])
        print("Sentiment: ", i, result[0]['class_label'])
        print("Probability: ", result[0]['class_prob'])
