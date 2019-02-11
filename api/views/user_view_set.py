from rest_framework import viewsets
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

            return Response(serialized_user.data)
        return Response(status=400)
