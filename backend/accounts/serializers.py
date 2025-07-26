from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Team


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role',
                  'avatar', 'position', 'department', 'phone', 'full_name']
        read_only_fields = ['id', 'full_name']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Must include email and password')

        # Try to find user by email
        try:
            user_obj = User.objects.get(email=email)
            print(f"Found user: {user_obj.username}, Active: {user_obj.is_active}")
        except User.DoesNotExist:
            print(f"No user found with email: {email}")
            raise serializers.ValidationError('Invalid email or password')

        # Authenticate with username and password
        user = authenticate(username=user_obj.username, password=password)
        print(f"Authentication result: {user}")

        if not user:
            # Try direct password check for debugging
            password_valid = user_obj.check_password(password)
            print(f"Direct password check: {password_valid}")
            raise serializers.ValidationError('Invalid email or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        attrs['user'] = user
        return attrs


class TeamSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = '__all__'

    def get_member_count(self, obj):
        return obj.members.count()
