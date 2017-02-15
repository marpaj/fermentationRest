from django.test import TestCase
from recipes.models import Recipe, Ingredient, Parameter
from rest_framework.test import APIClient
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

class BasicsTestCase(TestCase):
	
	def setup(self):
		# Ingredients
		i1 = Ingredient.objects.create(id=1, name='Ingr1')
		i2 = Ingredient.objects.create(id=2, name='Ingr2')
		i3 = Ingredient.objects.create(id=3, name='Ingr3')
		
		# Parameters
		p1 = Parameter.objects.create(id=1, name='Time');
		p2 = Parameter.objects.create(id=2, name='Temperature');
		p3 = Parameter.objects.create(id=3, name='Place');
		
		# Recipe id=1 with no ingredients
		Recipe.objects.create(id=1, name='Recipe 1', ingredients=[])
		
		# Recipe id=2 with one ingredient stored
		Recipe.objects.create(id=2, name='Recipe 2', ingredients=[])
	
	def test_get_ingredient_list(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/ingredients/', format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		
		# Check that number of ingredients is 3
		# stream = BytesIO(response.data)
		# data = JSONParser().parse(stream)
		# serializer = IngredientSerializer(data=data)
		# serializer.is_valid()
		
	def test_get_parameter_list(self):
		self.setup()
		client = APIClient()
		
		response = client.get('/parameters/', format='json')
		
		# Check that the response is 200 OK
		self.assertEqual(response.status_code, 200)
		