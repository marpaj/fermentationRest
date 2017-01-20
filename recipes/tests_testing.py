from django.test import TestCase
from recipes.models import Product, Recipe, Ingredient
from rest_framework.test import APIClient

class RecipeTestCase(TestCase):
	
	def setup(self):
		# Product id=1
		p1 = Product.objects.create(id=1, name='Product1')
		
		# Ingredients
		i1 = Ingredient.objects.create(id=1, name='Ingr1')
		i2 = Ingredient.objects.create(id=2, name='Ingr2')
		i3 = Ingredient.objects.create(id=3, name='Ingr3')
		
		# Recipe id=1 with no ingredients
		r1 = Recipe.objects.create(id=1, name='Recipe 1', product=p1, ingredients=[i1, i2])
		
		# Recipe id=2 with one ingredient stored
		r2 = Recipe.objects.create(id=2, name='Recipe 2', product=p1, ingredients=[])
		
		# Tests for recipe with id=1
		t1r1 = Test.objects.create(recipe=r1, vote=5)
		IngredientTested.objects.create(test=t1r1, ingredient=i1, amount=100)
		IngredientTested.objects.create(test=t1r1, ingredient=i2, amount=200)
		
		t2r1 = Test.objects.create(recipe=r1, vote=7)
		IngredientTested.objects.create(test=t2r1, ingredient=i1, amount=150)
		IngredientTested.objects.create(test=t2r1, ingredient=i2, amount=150)
	
	def test_get_all_tests():
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Deserialize for verify
		
	def test_get_the_best_test():
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/1/bestTest', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Deserialize for verify
	
	# def test_get_all_ingredients_tested():
		# self.setup()
		# client = APIClient()
	
	# def test_add_correct_test(self):
		# self.setup()
		# client = APIClient()
	
	# def test_add_bad_test(self):
		# self.setup()
		# client = APIClient()
		