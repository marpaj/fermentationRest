from rest_framework import serializers
from recipes.models import Product, Recipe, Ingredient, Test, IngredientTested

class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = ('id', 'name')
		extra_kwargs = {
            'id': {'read_only': False},
			'name': {'required': False},
            'ingredient': {'validators': []},
        }

class IngredientTestedSerializer(serializers.ModelSerializer):
	ingredient = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = IngredientTested
		fields = ('id', 'ingredient', 'amount')
		
class TestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True)
	# ingredientsTested = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='ingredients_Tested')
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'ingredientsTested')
		
class RecipeSerializer(serializers.ModelSerializer):
	ingredients = IngredientSerializer(many=True, read_only=True)
	class Meta:
		model = Recipe
		fields = ('id', 'name', 'description', 'directions', 'product','ingredients')
		extra_kwargs = {
            'id': {'read_only': False},
            'recipe': {'validators': []},
        }
		
class RecipeIngredientSerializer(serializers.Serializer):
	id = serializers.IntegerField()
	ingredients = IngredientSerializer(many=True)
		
	def create(self, validated_data):
		ingredients_data = validated_data.pop('ingredients')
		recipe = Recipe.objects.get(id=validated_data['id'])
		
		for ingredient in ingredients_data:
			ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			recipe.ingredients.add(ingredient)
		return recipe
		
# class RecipeIngredientSerializer(serializers.Serializer):
	# id = serializers.IntegerField()
	# ingredients = IngredientSerializer(many=True)
	
	# def create(self, validated_data):
		# ingredients_data = validated_data['ingredients']
		# recipe = Recipe.objects.get(id=validated_data['id'])
		# for ingredient in ingredients_data:
			# ingredient = Ingredient.objects.get(id=ingredient.get('id'))
			# recipe.ingredients.add(ingredient)
		# return recipe
		
	# def update(self, recipe, validated_data):
		# ingredient_data = validated_data['ingredients']
		# newIngredient = Ingredient.objects.get(id=ingredient_data.get('id'))
		# recipe.ingredients.add(newIngredient)
		# return recipe
		
class ProductSerializer(serializers.ModelSerializer):
	recipes = RecipeSerializer(many=True, allow_null =True)
	class Meta:
		model = Product
		fields = ('id', 'name', 'recipes')

		