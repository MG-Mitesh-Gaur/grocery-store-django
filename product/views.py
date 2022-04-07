from django.shortcuts import render, redirect

from np.views import order
from .models import Product, Users, category, Orders

from django.db.models import Count, F

from django.core.files.storage import FileSystemStorage

import os

# Create your views here.


def index(request):
	if not "admin" in request.session:
		return redirect("/")
	else:
		product_count = Product.objects.count()
		category_count = category.objects.count()
		oc = Orders.objects.values("order_id").annotate(num_orders=Count("order_id"))
		user_count = Users.objects.count()
		return render(
			request,
			"product/index.html",
			{
				"productCount": product_count,
				"categoryCount": category_count,
				"orderCount": len(oc),
				"userCount": user_count,
			},
		)


# ---------------- PRODUCTS ------------------ #
def allproducts(request):
	data = Product.objects.all()
	catData = category.objects.all()
	return render(
		request,
		"product/dashboard/allproducts.html",
		{"mydata": data, "catData": catData},
	)


def editProduct(request, id):
	data = Product.objects.filter(id=id)
	return render(request, "product/dashboard/editProduct.html", {"editData": data})


def editProductData(request):
	if request.method == "POST":

		# get id from hidden id field
		product_id = request.POST.get("epid")
		# get data from form
		product_name = request.POST.get("epname")
		product_price = request.POST.get("epprice")
		product_stock = request.POST.get("epquant")
		product_cat = request.POST.get("epcat")

		# update data
		Product.objects.filter(id=product_id).update(
			name=product_name,
			price=product_price,
			stock=product_stock,
			cate=category.objects.get(catName=product_cat),
		)

		return redirect("allproducts")


def addProduct(request):
	if request.method == "POST":
		myfile = request.FILES["pimg"]
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		product_name = request.POST.get("pname")
		product_price = request.POST.get("pprice")
		product_stock = request.POST.get("pquant")
		product_cat = request.POST.get("pcat")

		data = Product(
			image=filename,
			name=product_name,
			price=product_price,
			stock=product_stock,
			cate=category.objects.get(catName=product_cat),
		)
		data.save()

		return redirect("allproducts")
	# return redirect()


def deleteProduct(request, id):
	prod = Product.objects.get(id=id)
	if len(prod.image) > 0:
		os.remove(prod.image.path)
	Product.objects.filter(id=id).delete()
	return redirect("allproducts")


# ---------------- CATEGORIES ---------------- #
def categories(request):
	data = category.objects.all()
	return render(request, "product/dashboard/categories.html", {"mydata": data})


def editCategory(request, id):
	data = category.objects.filter(cat_id=id)
	return render(request, "product/dashboard/editCategory.html", {"editData": data})


def editCat(request):
	if request.method == "POST":
		cat_id = request.POST.get("ecatid")
		cat_name = request.POST.get("ecatname")
		category.objects.filter(cat_id=cat_id).update(catName=cat_name)

		return redirect("categories")


def addCategory(request):
	if request.method == "POST":
		myfile = request.FILES["catImg"]
		fs = FileSystemStorage()
		filename = fs.save(myfile.name, myfile)
		uploaded_file_url = fs.url(filename)
		cat_name = request.POST.get("catName")

		data = category(catImage=filename, catName=cat_name)
		data.save()

		return redirect("categories")


def deleteCategory(request, id):
	cat = category.objects.get(cat_id=id)
	if len(cat.catImage) > 0:
		os.remove(cat.catImage.path)
	category.objects.filter(cat_id=id).delete()
	return redirect("categories")


# ---------------- ORDERS -------------------  #


def orders(request):
	# oc = Orders.objects.all().values("order_email")
	# if oc['count'] > 1:
	# 	print("This set has ", oc['count'], " items")
	# else:
	# 	print("error")
	# SELECT * from product_orders GROUP BY order_id
	oc = Orders.objects.raw('SELECT * FROM product_orders GROUP BY order_email ORDER BY order_id')
	for x in oc:
		orderid = x.order_id
	data = Orders.objects.filter(order_id=orderid)
	return render(request, "product/dashboard/orders.html", {"mydata": data, "oc":oc})

def viewItem(request, id):
	data = Orders.objects.filter(order_id=id)
	return render(request, "product/dashboard/viewItem.html", {"mydata":data})

def cancelItem(request, id):
	data = Orders.objects.filter(order_id=id).delete()
	return redirect("orders")


def users(request):
	all_users = Users.objects.all()
	return render(request, "product/dashboard/users.html", {"mydata": all_users})
