from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UpdateUserSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch']

    def get_serializer_class(self):
        if self.action == 'me' and self.request.method == 'PATCH':
            return UpdateUserSerializer  # Use the update serializer for PATCH on /me
        elif self.action in ['partial_update', 'update']:
            return UpdateUserSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Return or update the current authenticated user's data.
        """
        user = request.user
        if request.method == 'PATCH':
            # Handling PATCH request to update user data
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            # Handling GET request to return user data
            serializer = self.get_serializer(user)
            return Response(serializer.data)