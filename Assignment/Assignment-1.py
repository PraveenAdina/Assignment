import requests
from bs4 import BeautifulSoup

url="https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
page_count=20
for page in range(1,page_count+1):
    present_url=url+str(page)
    response=requests.get(present_url)
    s=BeautifulSoup(response.text,"html.parser")
    products=s.find_all("div",class_="s-result-item")
    for p in products:
        p_name=p.find("h2").text.strip()
        p_url="https://www.amazon.in" + p.find("a", class_="a-link-normal").get("href")
        p_price=p.find("span",class_="a-icon-alt").text
        p_rating=p.find("span",class_="a-icon-alt").text.split()[0]
        num_reviews=product.find("span", {"class": "a-size-base", "dir": "auto"}).text.split()[0]
        
        print("Product Name:", p_name)
        print("Product URL:", p_url)
        print("Product Price:", p_price)
        print("Rating:", p_rating)
        print("Number of Reviews:", num_reviews)
        print("_"*50)
