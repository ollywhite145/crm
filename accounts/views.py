from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticted_user, allowed_users, admin_only


#REGISTRATION PAGE
@unauthenticted_user
def registerPage(request):

	form = CreateUserForm() #inherits from a really useful provided form that deals with lots of stuff like similar usernames etc, hashes password

	if request.method =='POST':
		form = CreateUserForm(request.POST) 
		if form.is_valid():

			user = form.save()
			username = form.cleaned_data.get('username') #gets us the username from the form 

			messages.success(request, 'Account was created for ' + username)  #adds a success message to the HTML from a useful lib


			return redirect('login') #redirects them to the login page


	context={'form':form}
	return render(request, 'accounts/register.html', context)



#LOGIN PAGE
@unauthenticted_user  #this is a decorator that checks if the user is authenticated, see decorators.py file for detail
def loginPage(request):
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')

		else: 
			messages.info(request, 'Username or Password is incorrect')
			

	context={}
	return render(request, 'accounts/login.html', context)



#LOGOUT
def logoutUser(request):
	logout(request)
	return redirect('login')

#SNOWDON SUNRISE TOURS PAGE
def tours(request):
	context={}
	return render(request, 'accounts/tours.html', context)



#HOME PAGE (FOR ADMINS)
@login_required(login_url = 'login') #this is a decorator and means if you arent logged in you cant see the home page
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context ={'orders':orders, 'customers':customers, 
				'total_customers':total_customers,
				'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending
				}

	return render(request, 'accounts/dashboard.html', context) #a dictioanry that is refercned in the html





#USER PAGE THAT CUSTOMERS CAN SEE
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders= request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	
	context={'orders':orders,'total_orders':total_orders,
				'delivered':delivered,
				'pending':pending}
	return render(request, 'accounts/user.html', context)



#USER STIINGS PAGE THAT CUSTOMERS CAN SEE
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer= request.user.customer
	form= CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()

	context={'form':form}
	return render(request, 'accounts/account_settings.html', context)







#PRODUCTS PAGE FOR ADMINS
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all() #queries the databse for products
	return render(request, 'accounts/products.html', {'products':products}) #adds a dictioary that is referenced in the HTML






#CUSTOMERS PAGE FOR ADMINS
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test): # adding the pk_test has made the url dynamic
	customer = Customer.objects.get(id=pk_test)



	orders= customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs #remakes the order variable with the filter



	context = {'customer':customer, 'orders':orders, 
				'order_count':order_count,
				'myFilter':myFilter
				}

	return render(request, 'accounts/customer.html', context)








#CREATE ORDERS PAGE FOR ADMINS
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product','status'), extra=10)

	customer = Customer.objects.get(id=pk)

	formset = OrderFormSet(queryset= Order.objects.none(), instance=customer)

	#form = OrderForm(initial = {'customer':customer})
	if request.method == 'POST':
		#print('Printing post', request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')


	context={'formset':formset,}
	return render(request, 'accounts/order_form.html', context)


#UPDATE ORDERS PAGE FOR ADMINS
@login_required(login_url = 'login') 
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context={'form':form}
	return render(request, 'accounts/order_form.html', context)


#DELETE ORDERS PAGE FOR ADMINS
@login_required(login_url = 'login')
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')


	context={'item':order}
	return render(request, 'accounts/delete.html', context)






