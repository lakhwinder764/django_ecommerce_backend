from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'password', 'password_confirm']

    def validate_email(self, value):
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('An account with this email already exists.')
        return email

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {'password_confirm': 'Passwords do not match.'}
            )
        validate_password(attrs['password'])
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        email = validated_data.pop('email').lower().strip()
        password = validated_data.pop('password')
        return User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=validated_data.get('first_name', ''),
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'username']
