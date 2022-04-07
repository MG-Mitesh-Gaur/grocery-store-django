from random import randint
from django.shortcuts import render, redirect
from product.models import Orders, Product, Users, category
from django.contrib import messages


from django.conf import settings
from django.core.mail import send_mail

from django.core.files.storage import FileSystemStorage
from passlib.hash import sha256_crypt

def index(request):
	data = Product.objects.all()
	return render(request,"main/index.html", {"mydata":data})

def productDetails(request, id):
	data = Product.objects.filter(id=id)
	return render(request,"main/productDetails.html", {"mydata":data})

# ------------- CATEGORIES MANANGMENT ---------- #
def allCategories(request):
	data = category.objects.all()
	return render(request,"main/showCategories.html", {"mydata":data})

def singleCategory(request, id):
	data = Product.objects.filter(cate_id=id)
	mdata = category.objects.get(cat_id=id)
	return render(request,"main/category.html", {"mydata":data, 'catName': mdata.catName})


# ------------- USER MANAGEMENT ---------------- #

# ---- LOGIN ----- #
def log(request):
	return render(request,"main/login.html")

def login(request):
	if request.method=='POST':
		u_email = request.POST.get("xemail")
		u_pass = request.POST.get("xpass")

		if u_email == "admin@gmail.com" and u_pass == "adminroot":
			request.session['admin'] = "admin"
			request.session['adminlogin'] = True
			return redirect("/product/")
		else:
			data = Users.objects.filter(uemail=u_email)

			if not data:
				messages.error(request, "You are not registered")
				return redirect("log")

			else:
				for row in data:
					userpassword = row.upass
					username = row.uname
					useremail = row.uemail

				if(sha256_crypt.verify(u_pass, userpassword)):
					request.session['username'] = username
					request.session['useremail'] = useremail
					request.session['userlogin'] = True
					messages.success(request, "Successfully Login")
					return redirect("/")
				else:
					messages.error(request, "Password Not Matched")
					return redirect("log")

def forgotpassword(request): # if user forgot the password
	return render(request, "main/forgotpassword.html")

def verify_otp(request):
	return render(request, "main/otpVerification.html")

def verifyEmail(request):
	if request.method=='POST':
		vemail = request.POST.get("vemail")

		request.session['vermail'] = vemail

		data = Users.objects.filter(uemail=vemail)
		if data:
			request.session['otp']=randint(1111,9999)
			subject = 'OTP for reset password'
			message = 'Your otp is ' + str(request.session['otp']) + ' Do not share it with others. Thank you.'
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [vemail, ]
			send_mail( subject, message, email_from, recipient_list )
			return redirect("verifyotp")
		else:
			messages.error(request, "You are not registered")
			return redirect("forgotpassword")

def check_otp(request):
	if request.method=='POST':
		votp = request.POST.get("votp")

		if int(votp) == request.session['otp']:
			print("Now you can change your password")
			return redirect("changePassword")
		else:
			print("Error")
		# messages.error(request, "You are not registered")

def changePassword(request):
	return render(request, "main/changepassword.html")

def newPassword(request):
	if request.method == 'POST':
		newpass = request.POST.get("npass")
		newcpass = request.POST.get("ncpass")

		if newpass == newcpass:
			encrypted_password = sha256_crypt.encrypt(newpass)
			data = Users.objects.filter(uemail=request.session['vermail']).update(upass=encrypted_password)
			return redirect("log")
		else:
			messages.error(request, "Password and Confirm Password Not Match")
			return redirect("changePassword")

# ------- LOGOUT ----------#
def adminlogout(request):
	del request.session['admin']
	del request.session['adminlogin']
	return redirect("/")

def userlogout(request):
	del request.session['username']
	del request.session['userlogin']
	del request.session['useremail']
	return redirect("/")

# ---- REGISTRATION ----- #
def registration(request):
	return render(request,"main/registration.html")

def register(request):
	if request.method=='POST':
		u_name = request.POST.get("uname")
		u_email = request.POST.get("uemail")
		u_mob = request.POST.get("umob")
		upass = request.POST.get("upass")
		ucpass = request.POST.get("ucpass")

		myfile=request.FILES['uimg']
		fs = FileSystemStorage()

		if upass == ucpass:
            # CONFIRM IF THE EMAIL IS ALREADY IN THE DATABASE OR NOT
			data = Users.objects.filter(uemail=u_email)

			if data:
				messages.error(request, "Email already exist")
				return redirect("registration")
			else:
				encrypted_password = sha256_crypt.encrypt(upass)
				filename = fs.save(myfile.name, myfile)
				uploaded_file_url = fs.url(filename)
				data = Users(uimage=filename, uname=u_name, uemail=u_email, umob=u_mob, upass=encrypted_password)
				data.save()

				messages.success(request, "Successfully Registered")
				return redirect("registration")
		else:
			messages.error(request, "Password and Confirm Password Not Match")
			return redirect("registration")

# ---------------- CART PANEL ---------------- #

def cart(request):
	return render(request,"cart/cart.html")

def addToCart(request, id):
	data = Product.objects.filter(id=id)
	return render(request,"cart/addToCart.html", {"mydata":data})

def delCartItem(request, id):
	cart = list(request.session['cart'])
	newcart = cart
	if id < len(newcart):
		cart[id]['cart_id'] = id
	elif id > len(newcart):
		id = len(newcart) - 1
		cart[id]['cart_id'] = id
		id = len(newcart) - 1
	elif id == len(newcart):
		cart[id-1]['cart_id'] = id 

	item_price = newcart[id-1]['p_price']
	total_old_price = request.session['totalPrice']
	newprice = total_old_price - item_price
	request.session['totalPrice'] = newprice
	cartID = request.session['cartID']
	cartID = cartID - 1
	request.session['cartID'] = cartID
	newcart.pop(id-1)
	request.session['cart'] = newcart
	print(len(newcart))
	return redirect("cart")

def clearCart(request):
	cart = list(request.session['cart'])
	cart.clear()

	request.session['cart'] = cart
	request.session['totalPrice'] = 0.0
	request.session['cartID'] = 0
	return redirect("cart")

def undoLastEntry(request):
	cart = list(request.session['cart'])
	newcart = cart
	last_index = len(newcart) - 1

	if len(newcart) < 0:
		cartID = request.session['cartID']
		request.session['cartID'] = 0

	print(newcart[last_index])

	item_price = newcart[last_index]['p_price']
	total_old_price = request.session['totalPrice']
	newprice = total_old_price - item_price
	request.session['totalPrice'] = newprice
	cart.pop(last_index)
	request.session['cart'] = newcart
	return redirect("cart")

def addToCartAction(request):
	if request.method=='POST':
		p_img = request.POST.get("cartProductImg")
		p_name = request.POST.get("cartProductName")
		p_price = request.POST.get("cartProductPrice")
		p_quant = request.POST.get("cartProductQuantity")

		price_per_quant = float(p_price) * float(p_quant)
		total = 0.0
		cartID = 1

		
		row = {'cart_id': cartID,'p_image': p_img, 'p_name':p_name, 'p_price':price_per_quant, 'p_quantity':p_quant}
		
		if('cart' in request.session):
			cart= list(request.session['cart'])

			if 'cartID' in request.session:

				if len(cart) == 0:
					cartID = 0
				else:
					cartID = request.session['cartID']
				cartID = cartID + 1
				row["cart_id"] = cartID
				request.session['cartID'] = row["cart_id"]
			else:
				row["cart_id"] = cartID
				request.session['cartID'] = row["cart_id"]
			cart.append(row)
			request.session['cart']=cart

			total = request.session['totalPrice']

			total = total + price_per_quant
			request.session['totalPrice']=total
			print(cartID)
		else:
			if len(row) == 0:
				pass
			else:
				request.session['cart'] = [row]
				total = total + price_per_quant
				request.session['totalPrice']=total
				row["cart_id"] = cartID
				request.session['cartID'] = row["cart_id"]
		
		return redirect("cart")

def buyNow(request):
	return render(request, "cart/buynow.html")

def order(request):
	if 'shippingAddress' in request.session:
		return redirect("endsession")
	else:
		return render(request,"cart/order.html")

def submitFinal(request):
	if request.method=='POST':
		cart = list(request.session['cart'])
		shipAddress = request.POST.get("shipAddress")

		if 'username' in request.session and 'useremail' in request.session:

			# check if any orders are there in the database
			order = Orders.objects.all()

			if order:
				checkData = Orders.objects.all().values('order_id').last()['order_id']

				if not checkData:
					order_id = 1
					data = Orders.objects.filter(order_id=order_id)

					if data:
						for row in range(len(cart)):
							name = cart[row]['p_name']
							quantity = cart[row]['p_quantity']
							price = cart[row]['p_price']
							order = Orders(name=name, quantity=quantity, price=price, shipping=shipAddress, order_id=order_id, order_email=request.session['useremail'])
							order.save()
							print(name, quantity, price, order_id, request.session['useremail'])

						print(shipAddress)
						request.session['shippingAddress'] = shipAddress

				else:
					order_id = checkData
					data = Orders.objects.filter(order_id=order_id)
					oid = Orders.objects.filter(order_id=order_id).values('order_id').last()['order_id']

					if data:
						if oid:
							oid = order_id + 1
							for row in range(len(cart)):
								name = cart[row]['p_name']
								quantity = cart[row]['p_quantity']
								price = cart[row]['p_price']
								order = Orders(name=name, quantity=quantity, price=price, shipping=shipAddress, order_id=oid, order_email=request.session['useremail'])
								order.save()
								print(name, quantity, price, oid)

						print(shipAddress)
						request.session['shippingAddress'] = shipAddress
			
			else:
				order_id = 1
				for row in range(len(cart)):
					name = cart[row]['p_name']
					quantity = cart[row]['p_quantity']
					price = cart[row]['p_price']
					order = Orders(name=name, quantity=quantity, price=price, shipping=shipAddress, order_id=order_id, order_email=request.session['useremail'])
					order.save()
					print(name, quantity, price, order_id)

					print(shipAddress)
					request.session['shippingAddress'] = shipAddress
			return redirect("order")
		else:
			messages.error(request, "Please login to place your order")
			return redirect("buyNow")

def endsession(request):
	del request.session['cart']
	del request.session['totalPrice']
	del request.session['cartID']
	del request.session['shippingAddress']
	return redirect("/")