from django.db import models

# Product table
class Product(models.Model):
	name = models.CharField(max_length=30)
	
	def __str__(self):
		return self.name

# Ingredient table
class Ingredient(models.Model):
	name = models.CharField(max_length=50)

# Category of quality for the recipe
class Category(models.Model):
	name = models.CharField(max_length=50)	
	
# Recipe table
class Recipe(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True, null=True, help_text="This is a quick description of your recipe")
	# directions = models.TextField(blank=True, null=True, help_text="How to make the recipe")
	ingredients = models.ManyToManyField(Ingredient)
	categories = models.ManyToManyField(Category)
	
# Recipe's Instructions
class Direction(models.Model):
	recipe = models.ForeignKey(Recipe, related_name='directions', on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=True,)
	description = models.CharField(max_length=400, blank=True, null=True)
	# time = models.CharField(max_length=50, null=True)
	order = models.PositiveSmallIntegerField()
	
# Test table
class Test(models.Model):
	date = models.DateTimeField(auto_now_add=True)
	recipe = models.ForeignKey(Recipe, related_name='tests', null=False, on_delete=models.CASCADE)
	# ingredientsTested = models.ManyToManyField(IngredientTested, related_name='ingredientsTested')
	# ingredients = models.ManyToManyField(Ingredient, through='IngredientTested')
	vote = models.PositiveSmallIntegerField(null=False, default=0)
	description = models.CharField(max_length=200, null=True)
	closed = models.BooleanField(default=False)
	
# Ingredient tested table
class IngredientTested(models.Model):
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, related_name='ingredientsTested', on_delete=models.CASCADE)
	# name = models.CharField(max_length=20,  null=True)
	amount = models.FloatField(null=True)
	units = models.CharField(max_length=30, null=True)
	brand = models.CharField(max_length=60, null=True)
	type = models.CharField(max_length=60, null=True)
	
# Instruction tested table
class DirectionTested(models.Model):
	direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, related_name='directionsTested', on_delete=models.CASCADE)
	time = models.CharField(max_length=60, null=True)
	place = models.CharField(max_length=80, null=True)

# Category feedback of the test
class CategoryTested(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	test = models.ForeignKey(Test, related_name='categoriesTested', on_delete=models.CASCADE)
	vote = models.PositiveSmallIntegerField(null=False, default=0)
	description = models.CharField(max_length=200, null=True)
	
