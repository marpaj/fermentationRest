from recipes.models import Product, Ingredient, Recipe, Test, IngredientTested
from recipes.serializers import IngredientSerializer, RecipeSerializer, RecipeIngredientSerializer, TestSerializer, IngredientTestedSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

class RecipeList(generics.ListCreateAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer
	
	# def perform_create(self, serializer):
		# serializer.save(ingredients=self.ingredients)
	
class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer
	
class RecipeIngredientList(generics.ListCreateAPIView):
	serializer_class = RecipeIngredientSerializer
	
	def get_queryset(self):
		return Recipe.objects.get(id=self.kwargs['idRecipe']).ingredients.all()
		
	def get_serializer_context(self):
		recipe = Recipe.objects.get(id=self.kwargs['idRecipe'])
		return {"recipe": recipe}

class RecipeIngredientView(APIView):
	"""
	Class-based view for manage ingredients in a recipe obejct
	"""
	def get_recipe(self, idRecipe):
		try:
			return Recipe.objects.get(id=idRecipe)
		except Recipe.DoesNotExist:
			raise Http404
		
	def get_ingredient(self, idRecipe, idIngredient):
		try:
			recipe = self.get_recipe(idRecipe=idRecipe)
			return recipe.ingredients.get(id=idIngredient)
		except Ingredient.DoesNotExist:
			raise Http404		
	
	def get(self, request, idRecipe, idIngredient, format='json'):
		recipe = self.get_recipe(idRecipe)
		serializer = IngredientSerializer(recipe.ingredients.all(), many=True)
		return Response(serializer.data)
		
	# def post(self, request, idRecipe, format='json'):
		# serializer = RecipeIngredientSerializer(data=request.data)
		# if serializer.is_valid():
			# serializer.save()
			# return Response(status=status.HTTP_201_CREATED)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, idRecipe, idIngredient, format='json'):
		recipe = self.get_recipe(idRecipe)
		ingredient = self.get_ingredient(idRecipe, idIngredient)
		
		recipe.ingredients.remove(ingredient)
		return Response(status=status.HTTP_204_NO_CONTENT)
	
class IngredientList(generics.ListCreateAPIView):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer
	
class IngredientDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer
	
class TestList(generics.ListCreateAPIView):
	queryset = Test.objects.all()
	serializer_class = TestSerializer
	
class TestDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Test.objects.all()
	serializer_class = TestSerializer
