from django.db import models

class Categories(models.Model):
	category_name = models.CharField(max_length=200)

	def __str__(self):
		return '%s' % self.category_name


class Products(models.Model):
	parent_category = models.ManyToManyField(Categories)
	url = models.CharField(max_length=255)
	# brand_id = models.IntegerField()
	# shop_id = models.IntegerField()
	name = models.CharField(max_length=255)
	body = models.TextField()
	visible = models.BooleanField()

	def __str__(self):
		return '%s' % self.name


class Document(models.Model):
	docfile = models.FileField(upload_to='uploads/')

	def __str__(self):
		return 'File: %s' % self.docfile.name
