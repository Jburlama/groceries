from django.shortcuts import render
from django.core.paginator import Paginator

from .models import *

# Create your views here.
def index(request):

	request.session["store"] = []
	request.session["category"] = []
	request.session["search"] = ""
	request.session["items_number"] = 10

	data = Item.objects.all().order_by("price")
	p = Paginator(data, request.session["items_number"])

	items = p.get_page(1)

	try:
		carts = request.session["carts"]
	except KeyError:
		carts = []

	request.session["carts"] = carts

	return render(request, "shop/index.html", {
		"items": items,
		"sections": [section.name.replace("_", " ") for section in Section.objects.all()],
		"carts": request.session["carts"],
	})



def load_items(request):
	page_number = request.GET.get("page")
	store = request.GET.get("store")
	category = request.GET.get("category")
	search = request.GET.get("search")
	new_cart = request.GET.get("create_cart")
	delete = request.GET.get("delete")
	add_to = request.GET.get("add_to")
	item = request.GET.get("item")


	data = Item.objects.all().order_by("price")

	if search:
		request.session["search"] = search
	if page_number:
		request.session["items_number"] = request.session["items_number"] * int(page_number)

	filter_store = request.session["store"]
	filter_category = request.session["category"]

	if store:
		if store in filter_store:
			filter_store.remove(store)
		else:
			filter_store += [store]
	if category:
		category = category.replace(" ", "_")
		if category in filter_category:
			filter_category.remove(category)
		else:
			filter_category += [category]

	try:
		carts = request.session["carts"]
	except KeyError:
		carts = []

	if new_cart:
		carts += [{
			"cart_name": new_cart,
			"amount": 0,
			"items": [],
		}]

	if delete:
		for cart in carts:
			if delete == cart["cart_name"]:
				carts.remove(cart)

	if add_to and item:
		for cart in carts:
			if add_to == cart["cart_name"]:
				i = Item.objects.get(name=item)
				cart["items"] += [i.name]
				cart["amount"] += float(i.price)

	request.session["carts"] = carts
	request.session["store"] = filter_store
	request.session["category"] = filter_category

	if filter_store:
		data = data.filter(store__in=filter_store).order_by("price")
	if filter_category:
		data = data.filter(section__in=filter_category).order_by("price")
		if request.session["search"]:
			request.session["search"] = []

	if request.session["search"]:
		data = data.filter(name__contains=request.session["search"])


	p = Paginator(data, request.session["items_number"])
	items = p.get_page(1)

	return render(request, "shop/items.html", {
		"items": items,
		"carts": request.session["carts"],
	})



def cart(request):
	return render(request, "shop/cart.html")
