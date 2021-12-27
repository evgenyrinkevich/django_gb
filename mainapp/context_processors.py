from mainapp.models import ProductCategory


def get_menu(request):
    return {'categories': ProductCategory.objects.filter(is_active=True)}


def get_basket(request):
    return {'basket': request.user.is_authenticated and request.user.basket.all() or []}
