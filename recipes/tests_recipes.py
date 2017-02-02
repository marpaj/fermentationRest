from django.test import TestCase
from recipes.models import Product, Recipe, Ingredient
from rest_framework.test import APIClient

class RecipeTestCase(TestCase):
	
	def setup(self):
		# Product id=1
		# p1 = Product.objects.create(id=1, name='Product1')
		
		# Ingredients
		i1 = Ingredient.objects.create(id=1, name='Ingr1')
		i2 = Ingredient.objects.create(id=2, name='Ingr2')
		i3 = Ingredient.objects.create(id=3, name='Ingr3')
		
		# Recipe id=1 with no ingredients
		r1 = Recipe.objects.create(id=1, name='Recipe 1', ingredients=[])
		
		# Recipe id=2 with one ingredient stored
		r2 = Recipe.objects.create(id=2, name='Recipe 2', ingredients=[])
		r2.ingredients.add(i1)
	
	def test_get_recipes(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
	
	# Passing test
	def test_new_recipe(self):
		self.setup()
		client = APIClient()
		
		data = {'id':3, 'name':'Recipe 3', 'ingredients':[]}
		response = client.post('/recipes/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of recipes is 2
		self.assertEqual(Recipe.objects.count(), 3)
		
		# Check that number of ingredients of recipe is 0
		recipe3 = Recipe.objects.get(id=3)
		self.assertEqual(recipe3.ingredients.count(), 0)
		
	def test_new_recipe_failed_by_data_no_ingredients(self):
		self.setup()
		client = APIClient()
		
		data = {'id':3, 'name':'Recipe 3'}
		response = client.post('/recipes/', data, format='json')
		
		# Check that the response is 400 Bad Request
		self.assertEqual(response.status_code, 400)
		
		# Check that number of recipes is 2
		self.assertEqual(Recipe.objects.count(), 2)
		
	def test_update_recipe_name(self):
		self.setup()
		client = APIClient()
		name = 'New name of recipe 1'
		
		data = {'id':1, 'name':name, 'description':'new description', 
				'directions':'new directions', 'ingredients':[]}
		response = client.put('/recipes/1/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that name is the new one
		self.assertEqual(Recipe.objects.get(id=1).name, name)
		
	def test_update_recipe_name_ingredients(self):
		self.setup()
		client = APIClient()
		name = 'New name of recipe 1'
		
		data = {'id':1, 'name':name, 'description':'new description', 
			'directions':'new directions', 'ingredients':[{'id':1, 'name':'Ingr1'}]}
		response = client.put('/recipes/1/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that name is the new one
		self.assertEqual(Recipe.objects.get(id=1).name, name)
		
		# Check that number of ingredients of recipe is 1
		recipe1 = Recipe.objects.get(id=1)
		self.assertEqual(recipe1.ingredients.count(), 1)
		
	def test_update_recipe_for_delete_ingredient(self):
		self.setup()
		client = APIClient()
		
		data = {'id':2, 'name':'Recipe 2', 'ingredients':[]}
		response = client.put('/recipes/2/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that number of ingredients of recipe is 1
		recipe2 = Recipe.objects.get(id=2)
		self.assertEqual(recipe2.ingredients.count(), 0)
		
	def test_delete_recipe(self):
		self.setup()
		client = APIClient()
		
		response = client.delete('/recipes/1/', format='json')
		
		# TO-DO: solution to have 200 (OK) code
		# Check that the response is 204 
		self.assertEqual(response.status_code, 204)
		
		# Check that number of recipes is 0
		self.assertEqual(Recipe.objects.count(), 1)
	
	
	#############################################################
	# Unit test for ingredient component within a recipe
	#############################################################
	
	def test_add_ingredient_in_empty(self):
		self.setup()
		client = APIClient()
		
		data = {'id':1}
		response = client.post('/recipes/1/ingredients/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of ingredients of recipe is 1
		recipe1 = Recipe.objects.get(id=1)
		self.assertEqual(recipe1.ingredients.count(), 1)
		
	def test_add_ingredient_in_not_empty(self):
		self.setup()
		client = APIClient()
		
		data = {'id':2}
		response = client.post('/recipes/2/ingredients/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of ingredients of recipe is 1
		recipe_with_ingredient = Recipe.objects.get(id=2)
		self.assertEqual(recipe_with_ingredient.ingredients.count(), 2)
		
	def test_delete_ingredient_recipe(self):
		self.setup()
		client = APIClient()
		
		response = client.delete('/recipes/2/ingredients/1/', format='json')
		
		# Check that the response is 204 Not Content
		self.assertEqual(response.status_code, 204)
		
		# Check that number of ingredients is 0
		recipe_with_ingredient = Recipe.objects.get(id=2)
		self.assertEqual(recipe_with_ingredient.ingredients.count(), 0)
		
	def test_delete_no_existing_ingredient(self):
		self.setup()
		client = APIClient()
		
		response = client.delete('/recipes/2/ingredients/3/', format='json')
		
		# Check that the response is 404 Not Found
		self.assertEqual(response.status_code, 404)
		
		# Check that number of ingredients is 0
		recipe_with_ingredient = Recipe.objects.get(id=2)
		self.assertEqual(recipe_with_ingredient.ingredients.count(), 1)
	
	