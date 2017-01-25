from rest_framework import serializers
from recipes.models import Product, Recipe, Ingredient, Test, IngredientTested

class IngredientSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = Ingredient
		fields = ('id', 'name')
		# extra_kwargs = {
            # 'id': {'read_only': False},
			# 'name': {'required': False},
            # 'ingredient': {'validators': []},
        # }
		
class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(many=True)
	
	class Meta:
		model = Recipe
		fields = ('id', 'name', 'description', 'directions', 'ingredients')
		
	def create(self, validated_data):
		ingredients = validated_data.pop('ingredients')
		recipe = Recipe.objects.create(**validated_data)
		for ingredient in ingredients:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			recipe.ingredients.add(ingredient)
		return recipe
		
	def update(self, instance, validated_data):
		ingredients = validated_data.pop('ingredients')
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.directions = validated_data.get('directions', instance.directions)
		instance.save()
		
		# Delete all ingredients
		instance.ingredients.clear()
		
		# Add the current ingredients
		for ingredient in ingredients:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			instance.ingredients.add(ingredient)
		return instance

class RecipeIngredientSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(required=False, read_only=True, max_length=30)
	
	def create(self, validated_data):
		recipe = self.context["recipe"]
		id = validated_data['id']
		ingredient = Ingredient.objects.get(id=id)
		recipe.ingredients.add(ingredient)
		return ingredient
		
class ProductSerializer(serializers.ModelSerializer):
	recipes = RecipeSerializer(many=True, allow_null =True)
	class Meta:
		model = Product
		fields = ('id', 'name', 'recipes')
		
class IngredientTestedSerializer(serializers.ModelSerializer):
	# id = serializers.ReadOnlyField(source='ingredient.id')
	# name = serializers.ReadOnlyField(source='ingredient.name')
	ingredient = IngredientSerializer()
	class Meta:
		model = IngredientTested
		# fields = ('id', 'ingredient', 'amount', 'units', 'brand', 'type')
		fields = ('id', 'ingredient', 'amount', 'units', 'brand', 'type')
		# extra_kwargs = {
            # 'id': {'read_only': False}
		# }
		
class RecipeTestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True, allow_null=True)
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'closed', 'ingredientsTested')
	
	def create(self, validated_data):
		recipe = self.context["recipe"]
		ingredients_tested = validated_data.pop('ingredientsTested')
		test = Test.objects.create(recipe=recipe)
		for ingredient_tested in ingredients_tested:
			ingredient = Ingredient.objects.get(id=ingredient_tested.pop('ingredient').get('id'))
			it = IngredientTested.objects.create(test=test, ingredient=ingredient, **ingredient_tested)			
		return test
		
	def update(self, instance, validated_data):
		recipe = self.context["recipe"]
		ingredients_tested = validated_data.pop('ingredientsTested')
		instance.vote = validated_data.get('vote', instance.vote)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		
		for ingredient_tested in ingredients_tested:
			# ingredient_tested = IngredientTested.objects.get_or_create(instance)
			it = IngredientTested.objects.get(id=ingredient_tested.get('id'))
			it.amount = ingredient_tested.get('amount')
			it.units = ingredient_tested.get('units')
			it.brand = ingredient_tested.get('brand')
			it.type = ingredient_tested.get('type')
			it.save()
		return instance

class TestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True, allow_null=True)
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'closed', 'ingredientsTested')
		
	def update(self, instance, validated_data):
		ingredients_tested = validated_data.pop('ingredientsTested')
		instance.vote = validated_data.get('vote', instance.vote)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		for ingredient_tested in ingredients_tested:
			# ingredient_tested = IngredientTested.objects.get(id=ingredient_tested.get('id'))
			# ingredient = Ingredient.objects.get_or_create(id=ingredient_tested.pop('ingredient'))
			# IngredientTested.objects.create(test=test, **ingredient_tested)
			it = IngredientTested.objects.get(id=ingredient_tested.get('id'))
			it.amount = ingredient_tested.get('amount')
			it.units = ingredient_tested.get('units')
			it.brand = ingredient_tested.get('brand')
			it.type = ingredient_tested.get('type')
			it.save()
		return instance
		