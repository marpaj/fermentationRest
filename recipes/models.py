from django.db import models

class Type(models.Model):
	name = models.CharField(max_length=30)

# Product table
class Product(models.Model):
	name = models.CharField(max_length=30)#, unique=True)
	
	def __str__(self):
		return self.name

# Ingredient tabla
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
	# recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
	# ingredient = models.ForeignKey(Ingredient, related_name='recipes', on_delete=models.CASCADE)

########################################################################
# TO-DO
########################################################################

class Test(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	recipe = models.ForeignKey(Recipe, related_name='tests', on_delete=models.CASCADE)
	vote = models.PositiveSmallIntegerField()
	description = models.CharField(max_length=200)
	
class IngredientTested(models.Model):
	test = models.ForeignKey(Test, related_name='ingredientsTested', on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	amount = models.FloatField(null=True)
	brand = models.CharField(max_length=30)
	type = models.CharField(max_length=30)
	
	class Meta:
		unique_together = ('test', 'ingredient')
	
	def __str__(self):
		return '%d: %s' % (self.id, self.ingredient, self.amount)
	
