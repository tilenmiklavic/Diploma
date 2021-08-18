# function for web scraping
def scrape(coins):
    date = datetime.today().strftime('%Y-%m-%d')
    tweets_current = { 'tweets': [], 'date': date}
    results = []
    browser = webdriver.Chrome()

    for coin in coins:
        name = coin['name']
        symbol = coin['symbol']

        url = 'https://bitinfocharts.com/' + name + '/'
        browser.get(url)

        element = browser.find_element_by_xpath('//tr[td[a[contains(text(), "Tweets per day")]]]/td[2]/a')
        tweets = element.text
        print(tweets)

        results.append({ "name": name, "tweet": tweets })

    browser.close()
    tweets_current['tweets'] = results
    return tweets_current