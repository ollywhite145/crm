from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User #the standard User model



class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']


class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__' #creates a form with all of the order fields in it
		#fields = ['customer'] or have it as a list for specific ones



class CreateUserForm(UserCreationForm): #inherits from the django UserCreationForm
	class Meta:
		model= User
		fields = ['username', 'email', 'password1', 'password2'] #gives us a form with these 4 fields




