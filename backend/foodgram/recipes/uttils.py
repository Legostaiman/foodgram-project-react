from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.db.models import Sum
from django.http import HttpResponse

from .permissions import IsAuthor
from .models import (Amount, Recipe)


@api_view(['GET'])
@permission_classes([IsAuthor | IsAdminUser])
def download_shopping_cart(request):
    user = request.user
    recipes_in_shopping_cart = Recipe.objects.filter(
        in_shopping_cart__user=user)
    ingredients_in_shopping_cart = Amount.objects.filter(
        recipe__in=recipes_in_shopping_cart).select_related('ingredient')
    ingredients_sum = ingredients_in_shopping_cart.values(
        'ingredient').annotate(sum=Sum('amount'))

    response = HttpResponse()
    response.write('Список покупок Foodgram \n')
    response.write('\n')

    for item in ingredients_sum:
        ingredient = ingredients_in_shopping_cart.filter(
            ingredient=item['ingredient'])[0].ingredient
        ingredient_name = ingredient.name
        ingredient_unit = ingredient.measurement_unit
        sum = item['sum']
        response.write(f'{ingredient_name} ({ingredient_unit}): {sum} \n')

    response['Content-Type'] = 'text/plain'
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.txt"')
    return response
