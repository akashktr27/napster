from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pdb

class DemoException(Exception):
	pass

def store(request):

	search_element = request.GET.get('search')

	if search_element:
		products = Product.objects.filter(name__icontains=search_element)
	else:
		products = Product.objects.all().order_by('id')
	x = Product.objects.values()

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']



	paginator = Paginator(products, 6)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)
	context = {'page_obj': page_obj, 'cartItems': cartItems}

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user_check = authenticate(request, username=username, password=password)
		if user_check is not None:
			login(request, user_check)
			return render(request, 'store/store.html', context)
		else:
			messages.success(request, 'there is problem loggin in')
			return render(request, 'store/login.html')


	# raise DemoException('Demo exception')
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = request.POST

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	# total = float(data['total'])
	order.transaction_id = transaction_id

	# if total == order.get_cart_total:
	# 	order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['address'],
		city=data['city'],
		state=data['state'],
		zipcode=data['zipcode'],
		)

	return redirect('store:store')

def login_user(request):
	form = SignupForm()
	context = {'form': form}
	return render(request, 'store/login.html', context)

def logout_user(request):
	logout(request)
	messages.success(request, 'You been logged out')
	form = SignupForm()
	context = {'form': form}
	return render(request, 'store/login.html', context)

def signup_user(request):
	# pdb.set_trace()
	if request.method == 'POST':

		form = SignupForm(request.POST)


		print('eror',form.error_messages)
		if form.is_valid():
			user = form.save()
			print('user saved here')
			print()
			login(request, user)
			return redirect('store:store')
		else:
			form = SignupForm()
			context = {'form': form}
			messages.success(request, 'Error in Signup')
			return render(request, 'store/login.html', context)

def product_view(request, pk):
	data = cartData(request)
	cartItems = data['cartItems']
	obj = Product.objects.get(id=pk)
	context = {
		'obj': obj,
		'cartItems': cartItems
	}

	return render(request, 'store/product_view.html', context)



def profile(request):

	customer = request.user.customer
	order = Order.objects.filter(customer=customer).all()
	print(order)
	# print(customer.email)
	context = {
		'name': customer.name,
		'email': customer.email,
		'orders': order
	}
	return render(request, 'store/profile.html', context)





