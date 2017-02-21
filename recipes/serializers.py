from rest_framework import serializers
from recipes.models import Recipe, Direction, Ingredient, Test, IngredientTested, DirectionTested, Parameter, ParameterTested

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
		
# class CategorySerializer(serializers.ModelSerializer):
	# id = serializers.IntegerField()
	# class Meta:
		# model = Category
		# fields = ('id', 'name')
		
class DirectionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Direction
		fields = ('id', 'description', 'order', 'deleted')
		extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }

# class DirectionSerializer(serializers.Serializer):
# 	id = serializers.IntegerField()
# 	description = serializers.CharField(required=False, read_only=True, max_length=400)
# 	order = serializers.IntegerField()
# 	deleted = serializers.BooleanField()

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
		
class ParameterSerializer(serializers.ModelSerializer):
	class Meta:
		model = Parameter
		fields = ('id', 'name')
		extra_kwargs = {
            "id": {
                "read_only": False,
                "required": False,
            },
        }
		
class ParameterTestedSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	parameter = ParameterSerializer()
	class Meta:
		model = ParameterTested
		fields = ('id', 'parameter', 'value')
		
class DirectionTestedSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(required=False)
	direction = DirectionSerializer()
	parametersTested = ParameterTestedSerializer(many=True, allow_null=True)
	class Meta:
		model = DirectionTested
		fields = ('id', 'direction', 'done', 'parametersTested')
		
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
			parameters_tested = direction_tested.pop('parametersTested')
			newDT = DirectionTested.objects.create(test=test, direction=direction, **direction_tested)
			
			for parameter_tested in parameters_tested:
				parameter = Parameter.objects.get(id=parameter_tested.pop('parameter').get('id'))
				ParameterTested.objects.create(parameter=parameter, directionTested=newDT, **parameter_tested)
		
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
			parameters_tested = direction_tested.pop('parametersTested')
			newDT = DirectionTested.objects.create(test=instance, direction=direction, **direction_tested)
			
			for parameter_tested in parameters_tested:
				parameter = Parameter.objects.get(id=parameter_tested.pop('parameter').get('id'))
				ParameterTested.objects.create(parameter=parameter, directionTested=newDT, **parameter_tested)

		# if not directions_tested:
		# 	DirectionTested.objects.filter(test=instance).delete()
		
		return instance

class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(many=True)
	directions = DirectionSerializer(many=True)

	# directions = serializers.SerializerMethodField('get_directionsWE')

	# def get_directionsWE(self, recipe):
	# 	qs = Direction.objects.filter(deleted=False, recipe=recipe)
	# 	serializer = DirectionSerializer(instance=qs, many=True)
	# 	return serializer.data
	
	class Meta:
		model = Recipe
		fields = ('id', 'name', 'description', 'directions', 'ingredients')
		
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
		directions_data = validated_data.pop('directions')
		instance.name = validated_data.get('name', instance.name)
		instance.description = validated_data.get('description', instance.description)
		instance.save()
		
		# Clear and add all current ingredients
		instance.ingredients.clear()
		for ingredient in ingredients:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			instance.ingredients.add(ingredient)
			
		# Save all direction's id of recipe for delete  
		idArray = []
		for direction_data in directions_data:
			id = direction_data.get('id')
			if id:
				direction = Direction.objects.get(id=id)
				direction.description = direction_data.get('description')
				direction.order = direction_data.get('order')
				# direction.deleted = direction_data.get('deleted')
				direction.save()

				idArray.append(id)
			else:
				direction = Direction.objects.create(recipe=instance, **direction_data)
				idArray.append(direction.id)
		
		directions = Direction.objects.filter(recipe=instance)
		for id in idArray:
			directions = directions.exclude(id=id)

		if directions.count() > 0:
			for direction in directions:
				direction.deleted = True
				direction.save()
			# directions.delete()

		return instance

# class ProductSerializer(serializers.ModelSerializer):
	# recipes = RecipeSerializer(many=True, allow_null =True)
	# class Meta:
		# model = Product
		# fields = ('id', 'name', 'recipes')