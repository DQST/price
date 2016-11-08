from django.db import models


class Categories(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return '%s' % self.name

	class Meta:
		db_table = 't_categories'


class Dealer(models.Model):
	name = models.CharField(max_length=255, null=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = 't_dealer'


class Documents(models.Model):
	docfile = models.FileField(upload_to='uploads/')
	dealer = models.ForeignKey(Dealer, db_column='dealer_id', null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.docfile.name

	class Meta:
		db_table = 't_documents'


class Products(models.Model):
	category = models.ForeignKey(Categories, db_column='category_id', null=True, on_delete=models.SET_NULL)
	document = models.ForeignKey(Documents, db_column='document_id', null=True, on_delete=models.SET_NULL)
	dealer = models.CharField(max_length=255, null=True)			# поставщик
	articul = models.CharField(max_length=255, null=True)			# артикул, maybe string!
	name = models.CharField(max_length=255, null=True)				# название
	model = models.CharField(max_length=255, null=True)				# модель
	brand_name = models.CharField(max_length=255, null=True)		# брэнд
	producer = models.CharField(max_length=255, null=True)			# производитель
	rozn_price = models.CharField(max_length=255, null=True)		# розничная цена
	recomend_price = models.CharField(max_length=255, null=True)	# рекомендованная цена
	dealer_price = models.CharField(max_length=255, null=True)		# диллерская цена
	balance = models.CharField(db_column='ostatok', null=True, max_length=255)

	def __str__(self):
		return 'Articul: %s; Name: %s; Producer: %s; Price: %s' % (self.articul, self.name, 
			self.producer, self.recomend_price)

	class Meta:
		db_table = 't_products'
