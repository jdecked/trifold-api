from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.models import User
from api.serializers import UserSerializer
from .auth import verify_token


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @staticmethod
    def get_auth_token(request):
        return request.META.get('HTTP_AUTHORIZATION').replace('Token ', '')

    @action(detail=False, url_path='me')
    def get_me(self, request):
        token = self.get_auth_token(request)
        me = User.objects.get(auth_token=token)

        if me:
            serialized_me = self.serializer_class(
                me,
                context={'request': request}
            )

            return Response(serialized_me.data)
        return Response(status=400)

    def create(self, request):
        id_token = request.data['id_token']
        user_info = verify_token(id_token)

        if user_info:
            user_id = user_info['sub']
            user = self.queryset.filter(id=user_id).first()

            if not user:
                email = user_info['email']

                user = User.objects.create_user(
                    id=user_id,
                    email=email,
                )

            serialized_user = self.serializer_class(
                user,
                context={'request': request}
            )

            data = serialized_user.data
            data['token'] = serialized_user.get_token(user)

            return Response(data)
        return Response(status=400)
