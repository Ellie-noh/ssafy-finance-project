from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


def _clean_username(value):
    if value is None:
        raise serializers.ValidationError("Username is required.")
    value = value.strip()
    if not value:
        raise serializers.ValidationError("Username is required.")
    if any(ch.isspace() for ch in value):
        raise serializers.ValidationError("Username cannot contain whitespace.")
    if len(value) < 3:
        raise serializers.ValidationError("Username must be at least 3 characters.")
    return value


def _clean_email(value):
    if value is None:
        return value
    return value.strip()


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def validate_username(self, value):
        return _clean_username(value)

    def validate_email(self, value):
        return _clean_email(value)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=3, max_length=150)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password2', 'joined_products']
        read_only_fields = ['joined_products']

    def validate_username(self, value):
        return _clean_username(value)

    def validate_email(self, value):
        return _clean_email(value)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if attrs.get('username') and attrs.get('password'):
            if attrs['password'] == attrs['username']:
                raise serializers.ValidationError({"password": "Password cannot be the same as username."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate_username(self, value):
        return _clean_username(value)
