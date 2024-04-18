from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UpdateUserSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.action in ['partial_update', 'update']:
            return UpdateUserSerializer
        return super().get_serializer_class()