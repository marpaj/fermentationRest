from django.test import TestCase
from recipes.models import Product, Recipe, Ingredient, Direction
from rest_framework.test import APIClient

class RecipeTestCase(TestCase):
	
	def setup(self):
		# Delete all tables
		Ingredient.objects.all().delete()
		Recipe.objects.all().delete()
		
		# Ingredients
		i1 = Ingredient.objects.create(id=1, name='Ingr1')
		i2 = Ingredient.objects.create(id=2, name='Ingr2')
		i3 = Ingredient.objects.create(id=3, name='Ingr3')
		
		# Recipe id=1 with no ingredients
		r1 = Recipe.objects.create(id=1, name='Recipe 1', ingredients=[])
		d11 = Direction.objects.create(id=1, recipe=r1, title='Direction 1', description='descrip 1', order=1)
		d12 = Direction.objects.create(id=2, recipe=r1, title='Direction 2', description='descrip 2', order=2)
		
		# Recipe id=2 with one ingredient stored
		r2 = Recipe.objects.create(id=2, name='Recipe 2', ingredients=[])
		r2.ingredients.add(i1)
		d21 = Direction.objects.create(id=3, recipe=r2, title='Direction 1', description='descrip 1', order=1)
		d22 = Direction.objects.create(id=4, recipe=r2, title='Direction 2', description='descrip 2', order=2)
	
	def test_get_recipes(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
	
	# Passing test
	def test_new_recipe_with_nothing(self):
		self.setup()
		client = APIClient()
		
		data = {'id':3, 'name':'Recipe 3', 'ingredients':[], 'directions':[]}
		response = client.post('/recipes/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of recipes is 2
		self.assertEqual(Recipe.objects.count(), 3)
		
		# Check that number of ingredients of recipe is 0
		recipe3 = Recipe.objects.get(id=3)
		self.assertEqual(recipe3.ingredients.count(), 0)
		
	# Passing test
	def test_new_recipe_with_ingredients_directions(self):
		self.setup()
		client = APIClient()
		
		data = {'id':3, 'name':'Recipe 3', 'ingredients':[{'id':1, 'name':'Ingr1'}, {'id':2, 'name':'Ingr2'}]
				, 'directions':[{'title':'Direction 1', 'description':'descrip 1', 'order':1} ] }
		response = client.post('/recipes/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of recipes is 3
		self.assertEqual(Recipe.objects.count(), 3)
		
		# Check that number of ingredients of recipe is 2
		recipe3 = Recipe.objects.get(id=3)
		self.assertEqual(recipe3.ingredients.count(), 2)
		
	# Passing test
	def test_new_recipe_without_descrption_in_direction(self):
		self.setup()
		client = APIClient()
		
		data = {'id':3, 'name':'Recipe 3', 'ingredients':[{'id':1, 'name':'Ingr1'}], 
			'directions':[{'title':'Direction 1', 'description':'', 'order':1}]}
		response = client.post('/recipes/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that number of recipes is 2
		self.assertEqual(Recipe.objects.count(), 3)
		
		# Check that number of ingredients of recipe is 1
		recipe3 = Recipe.objects.get(id=3)
		self.assertEqual(recipe3.ingredients.count(), 1)
		
		# Check that number of directions of recipe is 1
		self.assertEqual(recipe3.directions.count(), 1)
	
	# Not passing test
	def test_new_recipe_failed_by_no_ingredients(self):
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
		
		data = { 'id':1, 'name':name, 'description':'new description', 'ingredients':[],
				'directions':[{'id':1, 'title':'Direction 1', 'description':'descrip 1', 'order':1},
						{'id':2, 'title':'Direction 2', 'description':'descrip 2', 'order':2}] }
				
		response = client.put('/recipes/1/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that name is the new one
		self.assertEqual(Recipe.objects.get(id=1).name, name)
		
		# Check that number of directions of recipe is 1
		self.assertEqual(Recipe.objects.get(id=1).directions.count(), 2)
		
	def test_update_recipe_with_less_directions(self):
		self.setup()
		client = APIClient()
		name = 'New name of recipe 1'
		
		data = { 'id':1, 'name':name, 'description':'new description', 
				'ingredients':[ {'id':1, 'name':'Ingr1'}] , 
				'directions':[ {'id':1, 'title':'Direction 1', 'description':'descrip 1', 'order':1} ] }
						
		response = client.put('/recipes/1/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that name is the new one
		self.assertEqual(Recipe.objects.get(id=1).name, name)
		
		# Check that number of ingredients of recipe is 1
		self.assertEqual(Recipe.objects.get(id=1).ingredients.count(), 1)
		
		# Check that number of directions of recipe is 2
		self.assertEqual(Recipe.objects.get(id=1).directions.count(), 2)

		directions = Recipe.objects.get(id=1).directions
		self.assertEqual(directions.filter(deleted=False).count(), 1)

	def test_update_recipe_with_more_directions(self):
		self.setup()
		client = APIClient()
		name = 'New name of recipe 1'
		
		data = { 'id':1, 'name':name, 'description':'new description', 
			'ingredients':[ {'id':1, 'name':'Ingr1'}] , 
			'directions':[ 
					{'id':1, 'title':'Direction 1', 'description':'descrip 1', 'order':1}, 
					{'id':2, 'title':'Direction 2', 'description':'descrip 2', 'order':2},
					{'title':'Direction 3', 'description':'descrip 3', 'order':3},
					{'title':'Direction 4', 'description':'descrip 4', 'order':4}
			] 
		}
						
		response = client.put('/recipes/1/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that name is the new one
		self.assertEqual(Recipe.objects.get(id=1).name, name)
		
		# Check that number of ingredients of recipe is 1
		self.assertEqual(Recipe.objects.get(id=1).ingredients.count(), 1)
		
		# Check that number of directions of recipe is 4
		directions = Recipe.objects.get(id=1).directions
		self.assertEqual(directions.filter(deleted=False).count(), 4)
		
	def test_update_for_delete_ingredients_directions(self):
		self.setup()
		client = APIClient()
		
		data = {'id':2, 'name':'Recipe 2', 'ingredients':[], 'directions':[]}
		response = client.put('/recipes/2/', data, format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that number of ingredients of recipe is 1
		self.assertEqual(Recipe.objects.get(id=2).ingredients.count(), 0)
		
		# Check that number of directions of recipe is 2 but with deleted field to False
		directions = Recipe.objects.get(id=2).directions
		self.assertEqual(directions.count(), 2)
		self.assertEqual(directions.filter(deleted=False).count(), 0)
		
	def test_delete_recipe(self):
		self.setup()
		client = APIClient()
		
		response = client.delete('/recipes/1/', format='json')
		
		# TO-DO: solution to have 200 (OK) code
		# Check that the response is 204 
		self.assertEqual(response.status_code, 204)
		
		# Check that number of recipes is 0
		self.assertEqual(Recipe.objects.count(), 1)
		
		# Check that number of directions is 0
		self.assertEqual(Direction.objects.count(), 2)
	
	
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
	
	