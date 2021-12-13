from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminProductCategoryUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory


@user_passes_test(lambda x: x.is_superuser)
def index(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
    context = {
        'title': 'admin/users',
        'object_list': users_list
    }

    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_create(request):
    if request.method == 'POST':
        user_form = AdminShopUserCreateForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserCreateForm()

    context = {
        'title': 'create user',
        'form': user_form}

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        user_form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('my_admin:index'))
    else:
        user_form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'update user',
        'form': user_form}

    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('my_admin:index'))

    context = {
        'title': 'delete user',
        'user_to_delete': user
    }

    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def user_restore(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    user.is_active = True
    user.save()
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'user restore',
        'object_list': users_list
    }

    return render(request, 'adminapp/index.html', context)


@user_passes_test(lambda x: x.is_superuser)
def categories_list(request):
    categories = ProductCategory.objects.all()
    context = {
        'title': 'admin/categories',
        'object_list': categories
    }

    return render(request, 'adminapp/categories_list.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_create(request):
    if request.method == 'POST':
        form = AdminProductCategoryUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:categories_list'))
    else:
        form = AdminProductCategoryUpdateForm()

    context = {
        'title': 'create category',
        'form': form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_update(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        form = AdminProductCategoryUpdateForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('my_admin:categories_list'))
    else:
        form = AdminProductCategoryUpdateForm(instance=category)

    context = {
        'title': 'update category',
        'form': form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('my_admin:categories_list'))

    context = {
        'title': 'delete category',
        'category_to_delete': category
    }

    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda x: x.is_superuser)
def category_restore(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.is_active = True
    category.save()

    return HttpResponseRedirect(reverse('my_admin:categories_list'))
