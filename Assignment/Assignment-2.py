import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
pages_to_scrape = 20

data_list = []

for page_number in range(1, pages_to_scrape + 1):
    present_url = url + str(page_number)
    response = requests.get(present_url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.find_all("div", class_="s-result-item")

    for p in products:
        p_name = p.find("h2").text.strip()
        p_url = "https://www.amazon.in" + p.find("a", class_="a-link-normal").get("href")
        p_price = p.find("span", class_="a-offscreen").text
        rating = p.find("span", class_="a-icon-alt").text.split()[0]
        num_reviews = p.find("span", {"class": "a-size-base", "dir": "auto"}).text.split()[0]

        p_response = requests.get(p_url)
        p_soup = BeautifulSoup(p_response.text, "html.parser")

        description = p_soup.find("meta", attrs={"name": "description"}).get("content", "")
        asin = p_soup.find("th", text="ASIN").find_next("td").text.strip()
        p_description = p_soup.find("div", id="product Description").get_text(strip=True, separator='\n')
        manufacturer = p_soup.find("th", text="Manufacturer").find_next("td").text.strip()

        data_list.append({
            "Product Name": p_name,
            "Product URL": p_url,
            "Product Price": p_price,
            "Rating": rating,
            "Number of Reviews": num_reviews,
            "Description": description,
            "ASIN": asin,
            "Product Description": p_description,
            "Manufacturer": manufacturer
        })

# Export the data to a CSV file
csv_filename = "amazon_products.csv"
with open(csv_filename, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["Product Name", "Product URL", "Product Price", "Rating", "Number of Reviews", 
                  "Description", "ASIN", "Product Description", "Manufacturer"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for item in data_list:
        writer.writerow(item)

print("Data has been scraped and exported to", csv_filename)
