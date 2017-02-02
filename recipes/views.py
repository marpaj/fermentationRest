from recipes.models import Product, Ingredient, Recipe, Test, IngredientTested
from recipes.serializers import IngredientSerializer, RecipeSerializer, RecipeIngredientSerializer, RecipeTestSerializer, TestSerializer, IngredientTestedSerializer
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
	
class RecipeTestList(generics.ListCreateAPIView):
	serializer_class = RecipeTestSerializer
	
	def get_queryset(self):
		return Test.objects.filter(recipe=self.kwargs['idRecipe'])
		
	# To pass a parameter to the serializer
	def get_serializer_context(self):
		recipe = Recipe.objects.get(id=self.kwargs['idRecipe'])
		return {"recipe": recipe}

# class TestDetail(APIView):
	# # def get_queryset(self):
		# # return Test.objects.filter(id=self.kwargs['idTest'])

	# def get_object(self, pk):
		# try:
			# return Test.objects.get(pk=pk)
		# except Test.DoesNotExist:
			# raise Http404

	# def get(self, request, pk, format=None):
		# test = self.get_object(pk)
		# serializer = TestSerializer(test)
		# return Response(serializer.data)

	# def put(self, request, pk, format=None):
		# test = self.get_object(pk)
		# serializer = TestSerializer(test, data=request.data)
		# if serializer.is_valid():
			# serializer.save()
			# return Response(serializer.data)
		# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	
		
class TestDetail(generics.RetrieveUpdateDestroyAPIView):
	serializer_class = TestSerializer
	# lookup_field='idTest'
	queryset = Test.objects.all()
	
	# def get_queryset(self):
		# return Test.objects.filter(id=self.kwargs['idTest'])
		
	# def get_object(self):
		# return Test.objects.all()#filter(id=idTest)
	
	# def get_recipe(self, idRecipe):
		# try:
			# return Recipe.objects.get(id=idRecipe)
		# except Recipe.DoesNotExist:
			# raise Http404
	
	# def get_test(self, idRecipe, idTest):
		# try:
			# return Test.objects.filter(id=idTest)
		# except Ingredient.DoesNotExist:
			# raise Http404
	
	# def get(self, request, idRecipe, idTest, format='json'):
		# tests = self.get_test(idRecipe, idTest)
		# serializer = TestSerializer(tests, many=True)
		# return Response(serializer.data)
		
class BestTest(APIView):
	"""
	Class-based view for manage the best test
	"""
	def get(self, request, idRecipe, format='json'):
		try:
			tests = Test.objects.filter(recipe=idRecipe)
			bestTest = tests.order_by('-vote').first()
			serializer = TestSerializer(bestTest)
			return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
		except Recipe.DoesNotExist:
			raise Http404
