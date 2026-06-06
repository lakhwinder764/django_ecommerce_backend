from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .auth_serializers import RegisterSerializer, UserSerializer
from .cart_utils import get_session_cart, get_user_cart, merge_session_cart_into_user_cart
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        session_cart = get_session_cart(request)
        user_cart = get_user_cart(user)
        merge_session_cart_into_user_cart(session_cart, user_cart)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RefreshTokenView(TokenRefreshView):
    pass
