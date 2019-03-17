from rest_framework import serializers
from rest_framework.authtoken.models import Token
from api.models import User
from .token_serializer import TokenSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
        )

    def get_token(self, user):
        return TokenSerializer(Token.objects.get(user=user)).data.get('key')
