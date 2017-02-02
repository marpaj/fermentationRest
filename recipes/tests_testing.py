from django.test import TestCase
from recipes.models import Product, Recipe, Ingredient, Test, IngredientTested
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
		r1 = Recipe.objects.create(id=1, name='Recipe 1', ingredients=[])
		r1.ingredients.add(i1)
		r1.ingredients.add(i2)
		
		# Recipe id=2 with one ingredient stored
		r2 = Recipe.objects.create(id=2, name='Recipe 2', ingredients=[])
		
		# Tests for recipe with id=1
		t1r1 = Test.objects.create(id=1, recipe=r1, vote=5)
		IngredientTested.objects.create(id=1, test=t1r1, ingredient=i1, amount=100, units='grms')
		IngredientTested.objects.create(id=2, test=t1r1, ingredient=i2, amount=200, units='grms')
		
		t2r1 = Test.objects.create(id=2, recipe=r1, vote=7)
		IngredientTested.objects.create(id=3, test=t2r1, ingredient=i1, amount=150, units='grms')
		IngredientTested.objects.create(id=4, test=t2r1, ingredient=i2, amount=150, units='grms')
	
	def test_get_recipe_tests(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/1/tests/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# To-Do: Deserialize for verify
		
	def test_get_test(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/tests/1/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
	
	def test_new_test_without_ingredients(self):
		self.setup()
		client = APIClient()
		
		data = {'ingredientsTested':[]}
		
		response = client.post('/recipes/1/tests/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
	
	def test_new_test_with_ingredients(self):
		self.setup()
		client = APIClient()
		
		data = {'ingredientsTested':[{'ingredient':{'id':1, 'name':'Ingr1'}, 'amounts':111, 'units':'grms'}]}
		
		response = client.post('/recipes/1/tests/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
	def test_update_ingredients_test(self):
		self.setup()
		client = APIClient()
		
		# data = {'ingredientsTested':[{'ingredient':1, 'amount':150, 'units':'grms'},
			# {'ingredient':2, 'amount':1, 'units':'lt'}]}
			
		data = {'ingredientsTested':[{'id':2, 'ingredient':{'id':2, 'name':'Ingr2'}, 'amount':444, 'units':'grms'}]}
		
		response = client.put('/tests/1/', data, format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Check that amount is 444
		ingredientTested2 = IngredientTested.objects.get(id=2)
		self.assertEqual(ingredientTested2.amount, 444)
		
		# Check that number of ingredients tested is still 2
		test1 = Test.objects.get(id=1)
		ingredients = IngredientTested.objects.filter(test=test1)
		self.assertEqual(ingredients.count(), 2)
		
	def test_update_test(self):
		self.setup()
		client = APIClient()
		
		# data = {'ingredientsTested':[{'ingredient':1, 'amount':150, 'units':'grms'},
			# {'ingredient':2, 'amount':1, 'units':'lt'}]}
			
		data = {'vote':5, 'ingredientsTested':[]}
		
		response = client.put('/tests/1/', data, format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Check that vote field is 5
		test1 = Test.objects.get(id=1)
		self.assertEqual(test1.vote, 5)
		
		# Check that number of ingredients tested is still 2
		ingredients = IngredientTested.objects.filter(test=test1)
		self.assertEqual(ingredients.count(), 2)
	