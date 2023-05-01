# -*- coding: cp1251 -*-

from datetime import datetime
import requests
from bs4  import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
import json
product_list=[]
product_list2=[]
headers= {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    }
def original_code_html(url):
    
    link = Service("chromedriver") #путь к хромдрайверу 
    driver= webdriver.Chrome(service=link)
    #driver.maximize_window() # открываю окно гугла
    try:
        driver.get(url=url)
        time.sleep(3)
        with open("datacode.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source) # создаю html с кодом страницы

            
    except Exception as _ex:
        print(_ex)

        driver.close()
        driver.quit()

def items_urls(file_path, links):
    with open(file_path, encoding='utf-8') as file:
        src=file.read()
    beautsoup=BeautifulSoup(src, "lxml")
    items_divs=beautsoup.find_all("div", class_="item-type-card__item")

    
    for item in items_divs:
        item_url=item.find("div", class_= "item-type-card__inner" ).find("a").get("href")
        links.append(item_url) #список с ссылками на каждый товар
    return links

def data_product(cnt):

    links=[]
    links=items_urls("datacode.html", links)

    
    dt_now = datetime.today().strftime("%d/%m/%Y")
    cntnum=0
    numprod=kprod()
    for link in links: # идем по списку с ссылками
            link= "https://oz.by"+link
            response=requests.get(url=link, headers=headers, verify=False, timeout=7) #запрос на страницу
            beautsoup= BeautifulSoup(response.text, "lxml")
            

            try:
                name_product=beautsoup.find("h1", {"itemprop": "name"}).text.strip()
            except Exception as _ex:
                name_product=None

            try:
                name_cost=beautsoup.find("span", {"b-product-control__text b-product-control__text_main"}).text.strip()
                name_cost=name_cost.split('.')[0]                
                
                cntnum=cntnum+1
            except Exception as _ex:
                name_cost=None

            product_list.append(
                {
                   "Product name" : name_product,
                   "Product price" : name_cost,
                   "Num product": cntnum
                }
            )
            product_list2.append(
                {
                    "Num selection": cntnum,
                    "Data selection": dt_now,
                    "Quantity": numprod
                    }
                
                )


            cnt=cnt+1
            time.sleep(3)
            print(f'{cnt} из {numprod}')


    return cnt

   
def kprod():
    response=requests.get(url="https://oz.by/appliances/", headers=headers, verify=False, timeout=7) #запрос на страницу
    beautsoup= BeautifulSoup(response.text, "lxml")
    kolvoprod=int(beautsoup.find("small", {"class":"filters__chkslist__count"}).text.strip())
    return kolvoprod

def main():
    url="https://oz.by/appliances/bestsellers"
    response=requests.get(url=url, headers=headers) #запрос на страницу
    beautsoup= BeautifulSoup(response.text, "lxml")
    pages_count=int(beautsoup.find("li", class_="g-pagination__list__li pg-link pg-last").get("data-value"))
    cnt=0    

    for page in range(2, pages_count+2):
        original_code_html(url=url)
        cnt=data_product(cnt)
        url="https://oz.by/appliances/bestsellers?page="+str(page)
        
        
    
    

if __name__== "__main__":
    main()