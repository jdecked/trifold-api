from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import User
# from oauth2_provider.settings import oauth2_settings
# from oauthlib.common import generate_token
# from oauth2_provider.models import AccessToken, Application


class BaseTestMixin(object):
    def setUp(self):
        self.client = APIClient()

    def login(self, user):
        self.client.login(username=user.email, password=None)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.client.force_authenticate(user=user)

    def logout(self):
        self.client.logout()
        self.client.credentials()  # overwrite any existing credentials


class BaseTestCase(BaseTestMixin, APITestCase):
    pass


def generate_user(is_superuser=False):
    user = User.objects.create(email='test@gmail.com')
    user.first_name = 'User'
    user.last_name = str(user.id)
    user.email = 'test-{}@gmail.com'.format(user.id)
    user.username = 'test-{}@gmail.com'.format(user.id)
    user.is_superuser = is_superuser
    user.save()
    return user
