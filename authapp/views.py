from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserChangePasswordForm


class PageTitleMixin:
    page_title = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.page_title
        return context


def login(request):
    form = ShopUserLoginForm(data=request.POST or None)
    next_info = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserLoginForm()

    context = {
        'title': 'login',
        'form': form,
        'next': next_info
    }
    return render(request, 'authapp/login.html', context)


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect(reverse('main:index'))


def register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            if user.send_verify_mail() == 0:
                return HttpResponseRedirect(reverse('auth:register'))
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserRegisterForm()
    context = {
        'title': 'registration',
        'form': form
    }
    return render(request, 'authapp/register.html', context)


def edit(request):
    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        form = ShopUserEditForm(instance=request.user)
    context = {
        'title': 'edit profile',
        'form': form
    }
    return render(request, 'authapp/edit.html', context)


def change_password(request):
    if request.method == 'POST':
        form = ShopUserChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserChangePasswordForm(user=request.user)
    context = {
        'title': 'change password',
        'form': form
    }
    return render(request, 'authapp/change_password.html', context)
