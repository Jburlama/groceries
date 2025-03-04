from shop.models import *
import os
import pandas
from tqdm import tqdm

files = os.listdir("csv");

pbar = tqdm(total=len(files), desc="Loading...")

for file in files:
	store = file.split("_")[0]
	df = pandas.read_csv("csv/" + file)

	section = file.replace(store + "_", "").replace(".csv", "")

	s = Section(name=section)
	try:
		s.save()
	except Exception:
		pass	


	for index, row in df.iterrows():
		name = df["name"][index]
		try:
			price = df["price"][index].replace(",", ".").strip('"')
		except AttributeError:
			price = df["price"][index]
		img = df["img"][index]

		i = Item(store=store, name=name, price=price, img=img, section=section)
		try:
			i.save()
		except Exception:
			pass	
	pbar.update(1)

pbar.close()
