from rest_framework import serializers
from recipes.models import Recipe, Category, Direction, Ingredient, Test, IngredientTested, DirectionTested, CategoryTested

class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = ('id', 'name')
		extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }
		
class CategorySerializer(serializers.ModelSerializer):
	id = serializers.IntegerField()
	class Meta:
		model = Category
		fields = ('id', 'name')
		
class DirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direction
		fields = ('id', 'title', 'description', 'order')
		extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

class RecipeIngredientSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	name = serializers.CharField(required=False, read_only=True, max_length=30)
	
	def create(self, validated_data):
		recipe = self.context["recipe"]
		id = validated_data['id']
		ingredient = Ingredient.objects.get(id=id)
		recipe.ingredients.add(ingredient)
		return ingredient
		
class IngredientTestedSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	ingredient = IngredientSerializer()
	class Meta:
		model = IngredientTested
		fields = ('id', 'ingredient', 'amount', 'units', 'brand', 'type')
		
class DirectionTestedSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	direction = DirectionSerializer()
	class Meta:
		model = DirectionTested
		fields = ('id', 'direction', 'time', 'place')
		
class RecipeTestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True, allow_null=True)
	directionsTested = DirectionTestedSerializer(many=True, allow_null=True)
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'closed', 'ingredientsTested', 'directionsTested')
	
	def create(self, validated_data):
		recipe = self.context["recipe"]
		ingredients_tested = validated_data.pop('ingredientsTested')
		directions_tested = validated_data.pop('directionsTested')
		test = Test.objects.create(recipe=recipe)
		
		for ingredient_tested in ingredients_tested:
			ingredient = Ingredient.objects.get(id=ingredient_tested.pop('ingredient').get('id'))
			IngredientTested.objects.create(test=test, ingredient=ingredient, **ingredient_tested)
		
		for direction_tested in directions_tested:
			direction = Direction.objects.get(id=direction_tested.pop('direction').get('id'))
			DirectionTested.objects.create(test=test, direction=direction, **direction_tested)
		
		return test

class TestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True, allow_null=True)
	directionsTested = DirectionTestedSerializer(many=True, allow_null=True)
	
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'closed', 'ingredientsTested', 'directionsTested')
		
	def update(self, instance, validated_data):
		# ''' Update does not delete and create ingredients or directions. 
			# Only really update them '''
		ingredients_tested = validated_data.pop('ingredientsTested')
		directions_tested = validated_data.pop('directionsTested')
		instance.vote = validated_data.get('vote', instance.vote)
		instance.description = validated_data.get('description', instance.description)
		instance.closed = validated_data.get('closed', instance.closed)
		instance.save()
		
		IngredientTested.objects.filter(test=instance).delete()
		for ingredient_tested in ingredients_tested:
			ingredient = Ingredient.objects.get(id=ingredient_tested.pop('ingredient').get('id'))
			IngredientTested.objects.create(test=instance, ingredient=ingredient, **ingredient_tested)
		
		DirectionTested.objects.filter(test=instance).delete()
		for direction_tested in directions_tested:
			direction = Direction.objects.get(id=direction_tested.pop('direction').get('id'))
			DirectionTested.objects.create(test=instance, direction=direction, **direction_tested)
		
		return instance

class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(many=True)
	directions = DirectionSerializer(many=True)
	tests = TestSerializer(many=True, read_only=True)
	
	class Meta:
		model = Recipe
		fields = ('id', 'name', 'description', 'directions', 'ingredients', 'tests')
		
	def create(self, validated_data):
		ingredients = validated_data.pop('ingredients')
		directions = validated_data.pop('directions')
		recipe = Recipe.objects.create(**validated_data)
		
		# Save the ingredients
		for ingredient in ingredients:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			recipe.ingredients.add(ingredient)
			
		# Save the directions
		for direction in directions:
			Direction.objects.create(recipe=recipe, **direction)
			
		return recipe
		
	def update(self, instance, validated_data):
		ingredients = validated_data.pop('ingredients')
		directions = validated_data.pop('directions')
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		
		# Clear and add all current ingredients
		instance.ingredients.clear()
		for ingredient in ingredients:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			instance.ingredients.add(ingredient)
			
		# Clear and add all current direcitons
		Direction.objects.filter(recipe=instance).delete()
		for direction in directions:
			Direction.objects.create(recipe=instance, **direction)
			
		return instance

# class ProductSerializer(serializers.ModelSerializer):
	# recipes = RecipeSerializer(many=True, allow_null =True)
	# class Meta:
		# model = Product
		# fields = ('id', 'name', 'recipes')