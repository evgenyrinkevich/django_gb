from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminProductCategoryUpdateForm, \
    AdminProductUpdateForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


class ProductGetSuccessUrlMixin:
    def get_success_url(self):
        return reverse('my_admin:category_products', kwargs={
            'pk': self.object.category.pk
        })


class ShopUserList(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ShopUser
    paginate_by = 3
    page_title = 'users'


class UserCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    form_class = AdminShopUserCreateForm
    page_title = 'create user'


class UserUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    form_class = AdminShopUserUpdateForm
    page_title = 'edit user'


class UserDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ShopUser
    success_url = reverse_lazy('my_admin:index')
    page_title = 'delete user'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


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


class CategoriesListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = ProductCategory
    page_title = 'categories list'


class ProductCategoryCreateView(SuperUserOnlyMixin, PageTitleMixin, CreateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories_list')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'create category'


class ProductCategoryUpdateView(SuperUserOnlyMixin, PageTitleMixin, UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories_list')
    form_class = AdminProductCategoryUpdateForm
    page_title = 'update category'


class CategoryDeleteView(SuperUserOnlyMixin, PageTitleMixin, DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('my_admin:categories_list')
    page_title = 'delete category'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda x: x.is_superuser)
def category_restore(request, pk):
    category = get_object_or_404(ProductCategory, pk=pk)
    category.is_active = True
    category.save()

    return HttpResponseRedirect(reverse('my_admin:categories_list'))


class CategoryProductsListView(SuperUserOnlyMixin, PageTitleMixin, ListView):
    model = Product
    page_title = 'category products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Product.objects.filter(category=self.kwargs['pk'])


class ProductCreateView(SuperUserOnlyMixin, PageTitleMixin, ProductGetSuccessUrlMixin, CreateView):
    model = Product
    form_class = AdminProductUpdateForm
    page_title = 'create product'

    def get_initial(self):
        return {'category': ProductCategory.objects.get(pk=self.kwargs['category_pk'])}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_id'] = self.kwargs['category_pk']
        return context


class ProductUpdateView(SuperUserOnlyMixin, PageTitleMixin, ProductGetSuccessUrlMixin, UpdateView):
    model = Product
    form_class = AdminProductUpdateForm
    page_title = 'update product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_id'] = self.kwargs['pk']
        return context


class ProductDeleteView(SuperUserOnlyMixin, PageTitleMixin, ProductGetSuccessUrlMixin, DeleteView):
    model = Product
    page_title = 'delete product'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProductDetailView(SuperUserOnlyMixin, PageTitleMixin, DetailView):
    model = Product
    page_title = 'product details'
