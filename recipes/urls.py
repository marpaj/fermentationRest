from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from recipes import views

urlpatterns = [
    url(r'^recipes/$', views.RecipeList.as_view()),
    url(r'^recipes/(?P<pk>[0-9]+)/$', views.RecipeDetail.as_view()),
	url(r'^recipes/(?P<idRecipe>[0-9]+)/ingredients/$', views.RecipeIngredientList.as_view()),
	url(r'^recipes/(?P<idRecipe>[0-9]+)/ingredients/(?P<idIngredient>[0-9]+)/$', views.RecipeIngredientView.as_view()),
	
	url(r'^ingredients/$', views.IngredientList.as_view()),
    url(r'^ingredients/(?P<pk>[0-9]+)/$', views.IngredientDetail.as_view()),
	
	url(r'^tests/$', views.TestList.as_view()),
    url(r'^tests/(?P<pk>[0-9]+)/$', views.TestDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)