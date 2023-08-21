from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

#lets us create database tables from django classes


class Customer(models.Model):
	user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE) #a one to one field means each customer=user
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default = "profile1.jpeg" ,null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)


	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)
	

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Indoor','Indoor'),
			('Outdoor', 'Outdoor'),
		)

	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200, null=True, choices=CATEGORY)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name


class Order(models.Model):  #this is a one to Many relationship as it has relationships with Customer and Product

	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),

		)



	customer= models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices= STATUS)
	note = models.CharField(max_length=200, null=True)
	

	def __str__(self):
		return self.product.name




''' this is from video 18 he says he adds it in later but we'll see, 
look into django signals - https://docs.djangoproject.com/en/3.0/topics/signals/
useful for analytics on a site, i.e knowing number of page visits

class Profile(models.Model):
	user= models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
 	first_name = models.CharField(max_length=200, null=True, blank=True)
 	last_name = models.CharField(max_length=200, null=True, blank=True)
 	phone = models.CharField(max_length=200, null=True, blank=True)

 	def __str__(self):
		return str(self.user)



def create_profile(sender, instance, created, **kwargs):

	if created:
		Profile.objects.create(user=instance)
		print('Profile Created')

post_save.connect(create_profile, sender=User)


def update_profile(sender, instance, created, **kwargs):
	if created == False:
		instance.profile.save()
		print('Profile Updated')

'''


