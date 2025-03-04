from bs4 import BeautifulSoup
from seleniumbase import SB
from tqdm import tqdm
import pandas as pd
import requests
import json


def main():
	items = []

#	for i in range(17):
#		url = f"https://www.minipreco.pt/produtos/laticinios-e-ovos/c/WEB.005.000.00000?q=%3Arelevance&page={i}&disp="
#		items += scrape_minipreço(url)

	url = "https://mercadao.pt/store/pingo-doce/category/leite-ovos-e-natas-19"
	items += scrape_pingodoce(url)

	df = pd.DataFrame(items)
	df.to_csv("../csv/pingodoce_laticinios_e_ovos.csv")
	print(df.head())


def scrape_pingodoce(url):
	items = []

	with SB(uc=True, incognito=True, ad_block=True) as sb:
		sb.activate_cdp_mode(url)
		while (True):
			sb.sleep(2)
			product_html = sb.cdp.find_element("div[class='_35DP2XbY0vnDR6ntQlSXMJ pdo-col-block -col-collapse ng-star-inserted']").get_html()
			soup =  BeautifulSoup(product_html, "lxml")
			products = soup.find_all("article", {"class": "pdo-product-item"})
			pbar = tqdm(total=len(products), desc="Scraping...")
			for product in products:
				name = product.find("h3", {"class": "pdo-heading-s detail-title"}).text.strip()
				price = product.find("span", {"class": "pdo-inline-block pdo-middle ng-star-inserted"}).text.strip().split()[0]
				img_name = name.replace("/", "_").replace("'", "").replace(" ", "_") + ".jpg"
				try:
					img_url = product.find("img", {"class": "pdo-block media ng-star-inserted"})["src"]
					with open ("../img/" + img_name, "wb") as f:
						image = requests.get(img_url).content
						f.write(image)
				except ValueError:
					img_name = None
					pass	
			
				item = {"name": name, "price": price, "img": img_name}
				items.append(item)
				pbar.update(1)
			pbar.close()
			try:
				sb.click("button:contains('VER SEGUINTES')")
			except:
				print("Final Page")
				break
	return (items)


def scrape_minipreço(url):
	items = []

	with SB(uc=True, incognito=True, ad_block=True) as sb:
		sb.activate_cdp_mode(url)
		product_html = sb.cdp.find_element("div[class='product-list--row']").get_html()
		soup = BeautifulSoup(product_html, "lxml")
		products = soup.find_all("div", {"class": "product-list__item"})
		pbar = tqdm(total=len(products), desc="Scraping...")
		for product in products:
			name = product.find("span", {"class": "details"}).text.strip()
			price = product.find("p", {"class": "price"}).text.strip().split(" ")[0]
			img_name = name.replace(" ", "_").replace("'", "").replace("/", "_") + ".jpg"

			try:
				img_url = product.find("img", {"class": "lazy"})["data-original"]
				with open("../img/" + img_name, "wb") as f:
					image = requests.get(img_url).content
					f.write(image)
			except:
				img_name = None
				pass	
	
			item = {"name": name, "price": price, "img": img_name}
			items.append(item)
			pbar.update(1)
		pbar.close()
	return (items)


def scrape_continente(url):
	items = []
	
	with SB(uc=True, incognito=True, ad_block=True) as sb:
		sb.activate_cdp_mode(url)
		pbar = tqdm(total=100, desc="Page Loading ...")
		i = 0
		try:
			while (sb.cdp.find_element("button:contains('Ver mais produtos')")):
				sb.sleep(2)
				sb.click("button:contains('Ver mais produtos')")
				pbar.update(1)
				i += 1
		except:
			pass
		for j in range(100 - i):
			pbar.update(1)
		pbar.close()
		
		products_html = sb.cdp.find_element("div[itemid='#product']").get_html()
		soup = BeautifulSoup(products_html, "lxml")
		products = soup.find_all("div", {"class": "product"})
	
		pbar = tqdm(total=len(products), desc="Scraping...")
		for product in products:
			data = product.find("div").attrs["data-product-tile-impression"]
			try:
				data = json.loads(data)
				name = data["name"]
				price = data["price"]
		
				img = product.find("div", {"class": "ct-image-container"}).attrs
				img_url = json.loads(img["data-confirmation-image"])["url"].split("?")[0]
				img_name = name.replace(" ", "_").replace("/", "_").replace("'", "") + ".jpg"
			
				with open("../img/" + img_name, "wb") as f:
					img_content = requests.get(img_url).content
					f.write(img_content)
		
				item = {"name": name, "price": price, "img": img_name}
				items.append(item)
			except json.decoder.JSONDecodeError:
				pass
			pbar.update(1)
	
		pbar.close()
	
	return (items)
	

if __name__ == "__main__":
	main()
