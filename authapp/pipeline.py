from urllib.request import urlopen

import requests
from collections import OrderedDict
from datetime import datetime

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils import timezone
from urllib.parse import urlencode, urlunparse
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_100')),
                                                access_token=response['access_token'], v=5.131)), None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]

    if data['sex'] == 1:
        user.shopuserprofile.gender = ShopUserProfile.FEMALE
    elif data['sex'] == 2:
        user.shopuserprofile.gender = ShopUserProfile.MALE

    if data['first_name'] and data['last_name']:
        user.username = data['first_name'] + data['last_name']

    if data['about']:
        user.shopuserprofile.about_me = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year

    user.age = age

    if age < 18:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    if data['photo_100']:
        image_url = data['photo_100']
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(image_url).read())
        img_temp.flush()

        user.avatar.save("image_%s.jpg" % user.pk, File(img_temp))
    user.save()
