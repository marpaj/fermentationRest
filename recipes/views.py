from recipes.models import Ingredient, Direction, Recipe, Test, IngredientTested, DirectionTested, Parameter
from recipes.serializers import IngredientSerializer, DirectionSerializer, RecipeSerializer, RecipeIngredientSerializer, RecipeTestSerializer, TestSerializer, IngredientTestedSerializer, ParameterSerializer, DirectionTestedSerializer
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
	
	# To pass a parameter to the serializer
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
	
class RecipeDirectionList(generics.ListAPIView):
	serializer_class = DirectionSerializer
	
	def get_queryset(self):
		return Direction.objects.filter(recipe=self.kwargs['idRecipe'])
	
class RecipeTestList(generics.ListCreateAPIView):
	serializer_class = RecipeTestSerializer
	
	def get_queryset(self):
		return Test.objects.filter(recipe=self.kwargs['idRecipe'])
		
	# To pass a parameter to the serializer
	def get_serializer_context(self):
		recipe = Recipe.objects.get(id=self.kwargs['idRecipe'])
		return {"recipe": recipe}

class TestDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = TestSerializer
	queryset = Test.objects.all()
	
class ParameterList(generics.ListCreateAPIView):
	queryset = Parameter.objects.all()
	serializer_class = ParameterSerializer
		
class BestTest(APIView):
	"""
	Class-based view for manage the best test
	"""
	def get(self, request, idRecipe, format='json'):
		try:
			tests = Test.objects.filter(recipe=idRecipe, closed=True)
			bestTest = tests.order_by('-vote').first()
			serializer = TestSerializer(bestTest)
			return Response(data=serializer.data)
		except Recipe.DoesNotExist:
			raise Http404

class ActiveTest(APIView):
	"""
	Class-based view for return the active test 
	"""
	def get(self, request, idRecipe, format='json'):
		try:
			testList = Test.objects.filter(recipe=idRecipe, closed=False)
			if testList:
				serializer = TestSerializer(testList[0])
				return Response(data=serializer.data)
			else:
				return Response(status=status.HTTP_204_NO_CONTENT)
		except Recipe.DoesNotExist:
			raise Http404

class CurrentDirection(APIView):
	"""
	Class-based view for return the order of the current direction
	"""
	def get(self, request, idTest, format='json'):
		try:
			test = Test.objects.get(id=idTest)
			directionsTested = DirectionTested.objects.filter(test=test, done=False)
			current = directionsTested.order_by('id').first()
			serializer = DirectionTestedSerializer(current)
			return Response(data=serializer.data)
		except Recipe.DoesNotExist:
			raise Http404