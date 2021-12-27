from django.contrib import auth
from django.contrib.auth import update_session_auth_hash, get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserChangePasswordForm, \
    ShopUserProfileUpdateForm
from authapp.models import ShopUser, ShopUserProfile


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
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
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
        form_2 = ShopUserProfileUpdateForm(request.POST, request.FILES,
                                           instance=request.user.shopuserprofile)
        if form.is_valid() and form_2.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = ShopUserEditForm(instance=request.user)
        form_2 = ShopUserProfileUpdateForm(instance=request.user.shopuserprofile)
    context = {
        'title': 'edit profile',
        'form': form,
        'form_2': form_2,
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


def verify(request, email, activation_key):
    try:
        user = get_user_model().objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return HttpResponseRedirect(reverse('auth:register'))
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('main:index'))


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)
    else:
        instance.shopuserprofile.save()
