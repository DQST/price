from django.db import models


class Document(models.Model):
	docfile = models.FileField(upload_to='uploads/')

	def __str__(self):
		return 'File: %s' % self.docfile.name


class SBlog(models.Model):
	name = models.CharField(max_length=500)
	url = models.CharField(max_length=255)
	meta_title = models.CharField(max_length=500)
	meta_keywords = models.CharField(max_length=500)
	meta_description = models.CharField(max_length=500)
	annotation = models.TextField()
	text = models.TextField()
	visible = models.IntegerField()
	date = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 's_blog'


class SBrands(models.Model):
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	meta_title = models.CharField(max_length=500)
	meta_keywords = models.CharField(max_length=500)
	meta_description = models.CharField(max_length=500)
	description = models.TextField()
	image = models.CharField(max_length=255)

	class Meta:
		managed = False
		db_table = 's_brands'


class SCategories(models.Model):
	parent_id = models.IntegerField()
	name = models.CharField(max_length=255)
	meta_title = models.CharField(max_length=255)
	meta_keywords = models.CharField(max_length=255)
	meta_description = models.CharField(max_length=255)
	tagline = models.TextField()
	description = models.TextField()
	url = models.CharField(max_length=255)
	image = models.CharField(max_length=255)
	position = models.IntegerField()
	visible = models.IntegerField()
	external_id = models.CharField(max_length=36)

	class Meta:
		managed = False
		db_table = 's_categories'


class SCategoriesFeatures(models.Model):
	category_id = models.IntegerField()
	feature_id = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_categories_features'
		unique_together = (('category_id', 'feature_id'),)


class SComments(models.Model):
	id = models.BigAutoField(primary_key=True)
	date = models.DateTimeField()
	ip = models.CharField(max_length=20)
	object_id = models.IntegerField()
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	text = models.TextField()
	type = models.CharField(max_length=7)
	approved = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_comments'


class SCoupons(models.Model):
	id = models.BigAutoField(primary_key=True)
	code = models.CharField(max_length=256)
	expire = models.DateTimeField(blank=True, null=True)
	type = models.CharField(max_length=10)
	value = models.DecimalField(max_digits=10, decimal_places=2)
	min_order_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	single = models.IntegerField()
	usages = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_coupons'


class SCurrencies(models.Model):
	name = models.CharField(max_length=255)
	sign = models.CharField(max_length=20)
	code = models.CharField(max_length=3)
	rate_from = models.DecimalField(max_digits=10, decimal_places=2)
	rate_to = models.DecimalField(max_digits=10, decimal_places=2)
	cents = models.IntegerField()
	position = models.IntegerField()
	enabled = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_currencies'


class SDelivery(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	free_from = models.DecimalField(max_digits=10, decimal_places=2)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	enabled = models.IntegerField()
	position = models.IntegerField()
	separate_payment = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 's_delivery'


class SDeliveryPayment(models.Model):
	delivery_id = models.IntegerField()
	payment_method_id = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_delivery_payment'
		unique_together = (('delivery_id', 'payment_method_id'),)


class SFeatures(models.Model):
	name = models.CharField(max_length=255)
	position = models.IntegerField()
	in_filter = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 's_features'


class SFeedbacks(models.Model):
	id = models.BigAutoField(primary_key=True)
	date = models.DateTimeField()
	ip = models.CharField(max_length=20)
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	message = models.TextField()

	class Meta:
		managed = False
		db_table = 's_feedbacks'


class SGroups(models.Model):
	name = models.CharField(max_length=255)
	discount = models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		managed = False
		db_table = 's_groups'


class SImages(models.Model):
	name = models.CharField(max_length=255)
	product_id = models.IntegerField()
	filename = models.CharField(max_length=255)
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_images'


class SLabels(models.Model):
	name = models.CharField(max_length=255)
	color = models.CharField(max_length=6)
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_labels'


class SMenu(models.Model):
	name = models.CharField(max_length=255)
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_menu'


class SOptions(models.Model):
	product_id = models.IntegerField()
	feature_id = models.IntegerField()
	value = models.CharField(max_length=1024)

	class Meta:
		managed = False
		db_table = 's_options'
		unique_together = (('product_id', 'feature_id'),)


class SOrders(models.Model):
	id = models.BigAutoField(primary_key=True)
	delivery_id = models.IntegerField(blank=True, null=True)
	delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
	payment_method_id = models.IntegerField(blank=True, null=True)
	paid = models.IntegerField()
	payment_date = models.DateTimeField()
	closed = models.IntegerField()
	date = models.DateTimeField(blank=True, null=True)
	user_id = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=255)
	address = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	comment = models.CharField(max_length=1024)
	status = models.IntegerField()
	url = models.CharField(max_length=255, blank=True, null=True)
	payment_details = models.TextField()
	ip = models.CharField(max_length=15)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	note = models.CharField(max_length=1024)
	discount = models.DecimalField(max_digits=5, decimal_places=2)
	coupon_discount = models.DecimalField(max_digits=10, decimal_places=2)
	coupon_code = models.CharField(max_length=255)
	separate_delivery = models.IntegerField()
	modified = models.DateTimeField()

	class Meta:
		managed = False
		db_table = 's_orders'


class SOrdersLabels(models.Model):
	order_id = models.IntegerField()
	label_id = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_orders_labels'
		unique_together = (('order_id', 'label_id'),)


class SPages(models.Model):
	url = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	meta_title = models.CharField(max_length=500)
	meta_description = models.CharField(max_length=500)
	meta_keywords = models.CharField(max_length=500)
	body = models.TextField()
	menu_id = models.IntegerField()
	position = models.IntegerField()
	visible = models.IntegerField()
	header = models.CharField(max_length=1024)

	class Meta:
		managed = False
		db_table = 's_pages'


class SPaymentMethods(models.Model):
	module = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	description = models.TextField()
	currency_id = models.FloatField()
	settings = models.TextField()
	enabled = models.IntegerField()
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_payment_methods'


class SProducts(models.Model):
	url = models.CharField(max_length=255)
	brand_id = models.IntegerField(blank=True, null=True)
	vendor_id = models.IntegerField()
	name = models.CharField(max_length=500)
	annotation = models.TextField()
	body = models.TextField()
	visible = models.IntegerField()
	position = models.IntegerField()
	meta_title = models.CharField(max_length=500)
	meta_keywords = models.CharField(max_length=500)
	meta_description = models.CharField(max_length=500)
	created = models.DateTimeField(blank=True, null=True)
	featured = models.IntegerField(blank=True, null=True)
	external_id = models.CharField(max_length=36)

	class Meta:
		managed = False
		db_table = 's_products'


class SProductsCategories(models.Model):
	product_id = models.IntegerField()
	category_id = models.IntegerField()
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_products_categories'
		unique_together = (('product_id', 'category_id'),)


class SPurchases(models.Model):
	order_id = models.IntegerField()
	product_id = models.IntegerField(blank=True, null=True)
	variant_id = models.IntegerField(blank=True, null=True)
	product_name = models.CharField(max_length=255)
	variant_name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	amount = models.IntegerField()
	sku = models.CharField(max_length=255)

	class Meta:
		managed = False
		db_table = 's_purchases'


class SRelatedProducts(models.Model):
	product_id = models.IntegerField()
	related_id = models.IntegerField()
	position = models.IntegerField()

	class Meta:
		managed = False
		db_table = 's_related_products'
		unique_together = (('product_id', 'related_id'),)


class SSettings(models.Model):
	setting_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=255)
	value = models.TextField()

	class Meta:
		managed = False
		db_table = 's_settings'


class SUsers(models.Model):
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	company = models.CharField(max_length=255)
	number_unp = models.CharField(max_length=14)
	con_tel = models.CharField(max_length=20)
	group_id = models.IntegerField()
	enabled = models.IntegerField()
	last_ip = models.CharField(max_length=15, blank=True, null=True)
	created = models.DateTimeField(blank=True, null=True)

	class Meta:
		managed = False
		db_table = 's_users'


class SVariants(models.Model):
	id = models.BigAutoField(primary_key=True)
	product_id = models.IntegerField()
	sku = models.CharField(max_length=255)
	name = models.CharField(max_length=255)
	price = models.DecimalField(max_digits=14, decimal_places=2)
	compare_price = models.DecimalField(max_digits=14, decimal_places=2, blank=True, null=True)
	stock = models.IntegerField(blank=True, null=True)
	position = models.IntegerField()
	attachment = models.CharField(max_length=255)
	external_id = models.CharField(max_length=36)

	class Meta:
		managed = False
		db_table = 's_variants'


class SVendors(models.Model):
	user_id = models.IntegerField()
	name = models.CharField(max_length=255)
	url = models.CharField(max_length=255)
	meta_title = models.CharField(max_length=500)
	meta_keywords = models.CharField(max_length=500)
	meta_description = models.CharField(max_length=500)
	description = models.TextField()
	image = models.CharField(max_length=255)

	class Meta:
		managed = False
		db_table = 's_vendors'
