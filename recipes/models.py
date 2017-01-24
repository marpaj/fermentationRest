from django.db import models

# Product table
class Product(models.Model):
	name = models.CharField(max_length=30)#, unique=True)
	
	def __str__(self):
		return self.name

# Ingredient table
class Ingredient(models.Model):
	name = models.CharField(max_length=30)#, unique=True)
	
	def __str__(self):
		return self.name

# Recipe table
class Recipe(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True, help_text="This is a quick description of your recipe")
	directions = models.TextField(blank=True, null=True, help_text="How to make the recipe")
	product = models.ForeignKey(Product, related_name='recipes', on_delete=models.CASCADE)
	ingredients = models.ManyToManyField(Ingredient)

# class RecipeIngredient(models.Model):
	# recipe = models.ForeignKey(Recipe)
	# ingredient = models.ForeignKey(Ingredient)
	
# Test table
class Test(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	recipe = models.ForeignKey(Recipe, related_name='tests', null=False, on_delete=models.CASCADE)
	# ingredientsTested = models.ManyToManyField(IngredientTested, related_name='ingredientsTested')
	# ingredients = models.ManyToManyField(Ingredient, through='IngredientTested')
	vote = models.PositiveSmallIntegerField(null=True)
	description = models.CharField(max_length=200,  null=True)
	closed = models.BooleanField(default=False)
	
# Ingredient tested table
class IngredientTested(models.Model):
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, related_name='ingredientsTested', on_delete=models.CASCADE)
	# name = models.CharField(max_length=20,  null=True)
	amount = models.FloatField(null=True)
	units = models.CharField(max_length=20,  null=True)
	brand = models.CharField(max_length=30,  null=True)
	type = models.CharField(max_length=30,  null=True)
	
	# class Meta:
		# unique_together = ('test', 'ingredient')
	
	# def __str__(self):
		# return '%d: %s' % (self.id, self.ingredient, self.amount)
	
