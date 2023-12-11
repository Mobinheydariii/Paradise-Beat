from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)



class SimpleUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.SimpleUser
        fields = "__all__"


class SimpleUserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SimpleUserProfile
        fields = "__all__"


class SimpleUserRegisterSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(write_only=True, required=True)

    username = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(write_only=True, required=True,
                                        validators=[validate_password])
    
    password2 = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = models.SimpleUser
        fields = ('phone', 'email', 'username', 'password', 'password2')


class OtpSerializer(serializers.ModelSerializer):

    phone = serializers.CharField(write_only=True, required=True)

    email = serializers.EmailField(write_only=True, required=True)

    username = serializers.CharField(write_only=True, required=True)

    password = serializers.CharField(write_only=True, required=True,
                                        validators=[validate_password])
    
    password2 = serializers.CharField(write_only=True, required=True)

    type = serializers.CharField(write_only=True, required=True)

    token = serializers.CharField(write_only=True, required=True)

    code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = models.Otp
        fields = ('phone', 'email', 'username', 'password', 'password2', 'type', 'token', 'code')


class OtpCodeSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)
