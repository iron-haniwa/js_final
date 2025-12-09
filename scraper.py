import amiami
from requests_html import HTMLSession
import json
import re

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
        items.append({'Name': item.productName, 'Price': f"{item.price} yen", 'Image': item.imageURL, 'Link':item.productURL, 'Logo': "https://www.amiami.com/images/common/site_logo.png"})
    return items

def scrapeMandarake(query):
    session = HTMLSession()
    
    response = session.get("https://www.mandarake.co.jp/", headers=headers)
    response = session.get(f"https://order.mandarake.co.jp/order/listPage/list?soldOut=1&categoryCode=02&keyword={query}&lang=en", headers=headers)



    items = []
    for product in response.html.find('.block')[52:]:
        logo = "logo_en.png"
        name = product.find(".title", first=True).text
        price = product.find(".price", first=True).text
        link = list(product.find(".thum", first=True).absolute_links)[0]
        
        image = product.find("img", first=True).attrs["src"]
        items.append({'Name': name, 'Price': price, 'Image': image, 'Link':link, 'Logo':logo})

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
        price = str(product['price'] ) + " yen"
        link = product['url']
        image = product['imageUrl']
        items.append({'Name': name, 'Price': price, 'Image': image, 'Link':link, 'Logo':"https://s.yimg.jp/c/logo/f/2.1/a/auctions_r_34_2x.png"})

    return items



def scrapeAmiAmiJP(query):
    session = HTMLSession()
    
    response = session.get(f"https://slist.amiami.jp/top/search/list?s_cate_tag=1&s_keywords={query}&submit_btn=&s_st_list_preorder_available=1&s_st_list_backorder_available=1&s_st_list_newitem_available=1&s_st_condition_flg=1&pagemax=60", headers=headers)

    if response.html.find('.no_result'):
        return []

    products = response.html.find(".product_box")
    totalCount = int(response.html.find(".result_nested", first=True).find('.count',first=True).text)
    totalHits = len(products)
    pageMod = 1
    while totalCount > totalHits:
        response = session.get(f"https://slist.amiami.jp/top/search/list?s_cate_tag=1&s_keywords={query}&s_st_condition_flg=1&s_st_list_backorder_available=1&s_st_list_newitem_available=1&s_st_list_preorder_available=1&pagemax=60&getcnt=0&pagecnt={1+pageMod}", headers=headers)
        products += response.html.find(".product_box")
        totalHits += len(products)


    items = []
    for product in products:
        name = product.find(".product_name_inner", first=True).text
        price = product.find(".product_price", first=True)
        if price == None:
            price = product.find(".product_price_fromto", first=True)
        price = price.text + " yen"
        linkcode = re.search("(?<=gcode=).*", list(product.find("a", first=True).absolute_links)[0]).group()
        link = "https://www.amiami.com/eng/detail/?gcode=" + linkcode
        image = product.find(".lazyload",first=True).attrs['data-src']
        items.append({'Name': name, 'Price': price, 'Image': image, 'Link':link, 'Logo':"https://www.amiami.com/images/common/site_logo.png"})
    return items





