from django.test import TestCase
from recipes.models import Recipe, Ingredient, Direction, Test, IngredientTested, DirectionTested, Parameter, ParameterTested
from rest_framework.test import APIClient

class TestingTestCase(TestCase):
	
	def setup(self):
		# Ingredients
		i1 = Ingredient.objects.create(id=1, name='Ingr1')
		i2 = Ingredient.objects.create(id=2, name='Ingr2')
		i3 = Ingredient.objects.create(id=3, name='Ingr3')
		
		# Recipe id=1 with no ingredients
		r1 = Recipe.objects.create(id=1, name='Recipe 1', ingredients=[])
		r1.ingredients.add(i1)
		r1.ingredients.add(i2)
		d11 = Direction.objects.create(id=1, recipe=r1, title='Direction 1', description='descrip 1', order=1)
		d12 = Direction.objects.create(id=2, recipe=r1, title='Direction 2', description='descrip 2', order=2)
		
		# Recipe id=2 with one ingredient stored
		r2 = Recipe.objects.create(id=2, name='Recipe 2', ingredients=[])
		d21 = Direction.objects.create(id=3, recipe=r2, title='Direction 1', description='descrip 1', order=1)
		d22 = Direction.objects.create(id=4, recipe=r2, title='Direction 2', description='descrip 2', order=2)
		
		# Parameters
		p1 = Parameter.objects.create(id=1, name='Time');
		p2 = Parameter.objects.create(id=2, name='Temperature');
		p3 = Parameter.objects.create(id=3, name='Place');
		
		# Tests for recipe with id=1
		t1r1 = Test.objects.create(id=1, recipe=r1, vote=5)
		IngredientTested.objects.create(id=1, test=t1r1, ingredient=i1, amount=100, units='grms')
		IngredientTested.objects.create(id=2, test=t1r1, ingredient=i2, amount=200, units='grms')
		t1dt1 = DirectionTested.objects.create(id=1, test=t1r1, direction=d11)
		ParameterTested.objects.create(id=1, directionTested=t1dt1, parameter=p1, value='5 days')
		ParameterTested.objects.create(id=2, directionTested=t1dt1, parameter=p3, value='owen')
		t1dt2 = DirectionTested.objects.create(id=2, test=t1r1, direction=d12)
		ParameterTested.objects.create(id=3, directionTested=t1dt2, parameter=p1, value='0.5 horus')
		
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
	
	def test_new_test_with_nothing(self):
		self.setup()
		client = APIClient()
		
		data = {'ingredientsTested':[], 'directionsTested':[]}
		
		response = client.post('/recipes/1/tests/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
	
	def test_new_test_with_ingredients_directions(self):
		self.setup()
		client = APIClient()
		
		data = { 'ingredientsTested':[ {'ingredient':{'id':1, 'name':'Ingr1'}, 'amounts':111, 'units':'grms'} ], 
				'directionsTested': [ {'direction':{'id':1, 'title':'Direction 1', 'description':'descrip 1', 'order':1}, 'parametersTested':[{'parameter':{'id':1, 'name':'Time'}, 'value':'1 days'}] }, 
						{'direction':{'id':2, 'title':'Direction 2', 'description':'descrip 2', 'order':2}, 'parametersTested':[{'parameter':{'id':1, 'name':'Time'}, 'value':'12 hours'}] } ] }
		
		response = client.post('/recipes/1/tests/', data, format='json')
		
		# Check that the response is 201 Created
		self.assertEqual(response.status_code, 201)
		
		# Check that there are one more test
		r1 = Recipe.objects.get(id=1)
		self.assertEqual(Test.objects.filter(recipe=r1).count(), 3)
		
		# Check that IngredientTested has 1 ingredient for this test
		t = Test.objects.get(id=response.data.get('id'))
		self.assertEqual(IngredientTested.objects.filter(test=t).count(), 1)
		
		# Check that DirectionTested has 2 directions for this test
		self.assertEqual(DirectionTested.objects.filter(test=t).count(), 2)
		
	def test_update_test(self):
		self.setup()
		client = APIClient()
			
		data = {'vote':6, 'ingredientsTested':[], 'directionsTested':[]}
		
		response = client.put('/tests/1/', data, format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Check that vote field is 5
		test1 = Test.objects.get(id=1)
		self.assertEqual(test1.vote, 6)
		
		# Check that number of ingredients tested is 0
		ingredients = IngredientTested.objects.filter(test=test1)
		self.assertEqual(ingredients.count(), 0)
		
		# Check that number of directions tested is 0
		directions = DirectionTested.objects.filter(test=test1)
		self.assertEqual(directions.count(), 0)
		
	def test_update_ingredients_directions(self):
		self.setup()
		client = APIClient()
			
		data = { 'ingredientsTested':[ {'id':2, 'ingredient':{'id':2, 'name':'Ingr2'}, 'amount':444, 'units':'grms'} ],
				'directionsTested':[ {'id':1, 'direction':{'id':1, 'title':'Direction 1', 'description':'descrip 1', 'order':1}, 
						'parametersTested':[{'parameter':{'id':1, 'name':'Time'}, 'value':'444 days'}
								, {'parameter':{'id':3, 'name':'Place'}, 'value':'toilet'}] } ] }
		
		response = client.put('/tests/1/', data, format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		
		# Check that amount is 444
		ingredientTested2 = IngredientTested.objects.get(id=2)
		self.assertEqual(ingredientTested2.amount, 444)
		
		# Check that number of ingredients tested is not still 2
		test1 = Test.objects.get(id=1)
		ingredients = IngredientTested.objects.filter(test=test1)
		self.assertEqual(ingredients.count(), 1)
		
		# Check that number of directions tested is not still 2
		directions = DirectionTested.objects.filter(test=test1)
		self.assertEqual(ingredients.count(), 1)
	
	def test_best_test(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/recipes/1/bestTest/', format='json')
		
		# Check that the response is 200 Ok
		self.assertEqual(response.status_code, 200)
		