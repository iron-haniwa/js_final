import amiami
from requests_html import HTMLSession
import json

headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
    }

def scrapeAmiAmi(query):
    items = []
    results = amiami.search(query)
    resultListsort = sorted(results.items, key=lambda x: x.price, reverse=True)
    for item in resultListsort:
        items.append({'Name': item.productName, 'Price': item.price, 'Image': item.imageURL, 'Link':item.productURL})
    return items

def scrapeMandarake(query):
    session = HTMLSession()
    
    response = session.get("https://www.mandarake.co.jp/", headers=headers)
    response = session.get(f"https://order.mandarake.co.jp/order/listPage/list?soldOut=1&categoryCode=02&keyword={query}&lang=en", headers=headers)



    items = []
    for product in response.html.find('.block')[52:]:
        name = product.find(".title", first=True).text
        price = product.find(".price", first=True).text
        link = list(product.find(".thum", first=True).absolute_links)[0]
        
        image = product.find("img", first=True).attrs["src"]
        items.append({'Name': name, 'Price': price, 'Image': image, 'Link':link})

    return items

def scrapeYahoo(query):
    session = HTMLSession()
    
    response = session.get(f"https://www.fromjapan.co.jp/japan/sites/yahooauction/search?keyword={query}&category=25888&sort=score&hits=100&page=1", headers=headers)
    responseJson =  json.loads(response.text)
    products = responseJson['items']
    totalHits = responseJson['hits']
    totalCount = responseJson['count']
    pageMod = 1
    while totalCount > totalHits:
        response = session.get(f"https://www.fromjapan.co.jp/japan/sites/yahooauction/search?keyword={query}&category=25888&sort=score&hits=100&page={1+pageMod}", headers=headers)
        responseJson =  json.loads(response.text)
        products += responseJson['items']
        totalHits += responseJson['hits']

    
    items = []
    for product in products:
        name = product['title']
        price = product['price']
        link = product['url']
        image = product['imageUrl']
        items.append({'Name': name, 'Price': price, 'Image': image, 'Link':link})

    return items






