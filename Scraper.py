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
        # Get all the information from the webpage
        soup = bs4.BeautifulSoup(requests.get(url + stocks[i] + '/').text, 'html.parser')

        # Sort through the information for what we want(the a tag)
        anchor = soup.find_all('a', attrs={'class':'subtle-link fin-size-small thumb yf-1e4diqp'})

        # Sort through all the html that uses the a tag and get the titles and links
        for atrb in anchor:
            titles.append(atrb['title'].lower())
            links.append(atrb['href'])

    return titles, links