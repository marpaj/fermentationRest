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
	ingredient = serializers.PrimaryKeyRelatedField(read_only=True)
	class Meta:
		model = IngredientTested
		fields = ('id', 'ingredient', 'amount')
		
class TestSerializer(serializers.ModelSerializer):
	ingredientsTested = IngredientTestedSerializer(many=True)
	class Meta:
		model = Test
		fields = ('id', 'date', 'vote', 'description', 'ingredientsTested')
		

		