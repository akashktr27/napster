from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import pdb


def store(request):
	print('search',request.GET.get('search'))
	search_element = request.GET.get('search')

	if search_element:
		products = Product.objects.filter(name__icontains=search_element)
	else:
		products = Product.objects.all()

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']


	context = {}
	paginator = Paginator(products, 6)  # Show 25 contacts per page.
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
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

def login_user(request):
	form = SignUpForm()

	context = {'form': form}
	return render(request, 'store/login.html', context)

def logout_user(request):
	logout(request)
	messages.success(request, 'You been logged out')
	return render(request, 'store/login.html')

def signup_user(request):
	# pdb.set_trace()
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			print('user saved here')

			login(request, user)
			return redirect('store:store')
		else:
			form = SignUpForm()
			context = {'form': form}
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





