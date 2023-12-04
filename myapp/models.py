from django.db import models

# Create your models here.

class User(models.Model):
	fname=models.CharField(max_length=100)
	lname=models.CharField(max_length=100)
	email=models.EmailField()
	mobile=models.PositiveBigIntegerField()
	address=models.TextField()
	password=models.CharField(max_length=100)
	profile_picture=models.ImageField(default="",upload_to="profile_picture/")
	usertype=models.CharField(max_length=100,default="buyer")

	def __str__(self):
		return self.fname

class Product(models.Model):

	category=(
			("Men","Men"),
			("Women","Women"),
			("kids","kids"),
		)

	brand=(
		    ("Levis","Levis"),
		    ("Pape","Pape"),
		    ("Killer","Killer"),
		)
	size=(
			("S","S"),
			("M","M"),
			("L","L"),
			("XL","XL"),
			("XXL","XXl"),
		)
	seller=models.ForeignKey(User,on_delete=models.CASCADE)
	product_name=models.CharField(max_length=100)
	profile_price=models.PositiveIntegerField() 
	product_category=models.CharField(max_length=100,choices=category)
	product_brand=models.CharField(max_length=100,choices=brand)
	product_size=models.CharField(max_length=100,choices=size)
	profile_image=models.ImageField(upload_to="profile_picture")
	product_desc=models.TextField()

	def __str__(self):
		return self.seller.fname+" - "+self.product_name



