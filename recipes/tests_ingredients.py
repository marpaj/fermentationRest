from django.test import TestCase
from recipes.models import Ingredient
from rest_framework.test import APIClient

class IngredientTestCase(TestCase):

    def setup(self):
        # Delete all tables
        Ingredient.objects.all().delete()

        # Ingredients
        i1 = Ingredient.objects.create(id=1, name='Tea')
        i2 = Ingredient.objects.create(id=2, name='Sugar')
        i3 = Ingredient.objects.create(id=3, name='Salt')	
    
    def test_get_ingredient_list(self):
        self.setup()
        client = APIClient()
        
        response = client.get('/ingredients/', format='json')

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
		
    def test_get_ingredient_filter(self):
        self.setup()
        client = APIClient()

        response = client.get('/ingredients/?name=s', format='json')

        # Check response is 200 (Ok)
        self.assertEqual(response.status_code, 200)

        # Check response has two elements
        data = [ {'id':2, 'name':'Sugar'}, {'id':3, 'name':'Salt'} ]
        self.assertEqual(response.data, data)

    def test_create_ingredient(self):
        self.setup()
        client = APIClient()

        data = { 'name':'Milk' }
        response = client.post('/ingredients/', data, format='json')
        
        # Check that the response is 201 Created
        self.assertEqual(response.status_code, 201)

    def test_delete_ingredient(self):
        self.setup()
        client = APIClient()

        response = client.delete('/ingredients/1/', format='json')
        
        # Check that the response is 204 
        self.assertEqual(response.status_code, 204)

        # Check that current number of ingredients is 2
        self.assertEqual(Ingredient.objects.count(), 2)
