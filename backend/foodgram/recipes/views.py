from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.permissions import IsAuthenticated

from foodgram.pagination import FoodgramPagination

from .filters import RecipeFilter
from .mixins import ReadOnlyViewSet
from .models import (Amount, Favorite, Ingredient, Recipe, ShoppingCart,
                     Subscribe, Tag)
from .permissions import SubscribePermission
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, SubscribeSerializer,
                          TagSerializer)

User = get_user_model()


class TagsViewSet(ReadOnlyViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'


class IngredientsViewSet(ReadOnlyViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]
    lookup_field = 'id'
    search_fields = ['name']
    filterset_fields = ('author', 'tag')
    pagination_class = FoodgramPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeSerializer
        return CreateRecipeSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribeSerializer
    permission_classes = [SubscribePermission, ]
    pagination_class = FoodgramPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['user']
    lookup_field = 'author_id'

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.kwargs.get('author_id'))
        serializer.save(user=self.request.user, author=author)

    def perform_destroy(self, instance):
        user = self.request.user
        author = get_object_or_404(User, pk=self.kwargs.get('author_id'))
        follow = user.follower.get(author=author)
        follow.delete()


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user']
    lookup_field = 'recipe_id'

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        favorite = user.favorite_user.get(recipe=recipe)
        favorite.delete()


class ShoppingCartViewSet(viewsets.ModelViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user']
    lookup_field = 'recipe_id'

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_destroy(self, instance):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))
        favorite = user.in_shopping_cart.get(recipe=recipe)
        favorite.delete()
