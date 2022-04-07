from django.db import models

class category(models.Model):
	cat_id=models.AutoField(primary_key=True)
	catName=models.CharField(max_length=255)
	catImage = models.ImageField(upload_to='category', default="")

	def __str__(self):
		return self.catName

# Create your models here.
class Product(models.Model):
	image = models.ImageField(default="")
	id=models.AutoField(primary_key=True)
	cate = models.ForeignKey(category, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=255)
	price = models.FloatField()
	stock = models.IntegerField()

	def __str__(self):
		return self.name


class Users(models.Model):
	id=models.AutoField(primary_key=True)
	uimage = models.ImageField(upload_to='users', default="")
	uname = models.CharField(max_length=255)
	uemail = models.EmailField(max_length=255)
	umob = models.CharField(max_length=255)
	upass = models.CharField(max_length=255, default="")

	def __str__(self):
		return self.uname

class Orders(models.Model):
	id=models.AutoField(primary_key=True)
	order_id = models.IntegerField(default=0)
	name = models.CharField(max_length=255, default="")
	quantity = models.IntegerField()
	price = models.CharField(max_length=255)
	shipping = models.CharField(max_length=255)
	order_email = models.EmailField(max_length=255,  default="")

	def __str__(self):
		return self.name