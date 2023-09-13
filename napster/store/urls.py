from django.urls import path

from . import views
app_name='store'

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login_user/', views.login_user, name="login_user"),
	path('logout_user/', views.logout_user, name="logout_user"),
	path('signup_user/', views.signup_user, name="signup_user"),
	path('product_view/<int:pk>', views.product_view, name="product_view"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),

]