from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .auth_serializers import RegisterSerializer, UserSerializer
from .jwt_serializers import CustomTokenObtainPairSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    return Response(
        {
            'message': 'Account created successfully.',
            'user': UserSerializer(user).data,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RefreshTokenView(TokenRefreshView):
    pass
