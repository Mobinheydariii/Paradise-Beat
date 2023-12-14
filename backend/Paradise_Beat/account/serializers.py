from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import(
    User,
    UserProfile,
    Otp
)



class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # These are claims, you can add custom claims
        token['phone'] = user.phone
        token['username'] = user.username
        token['email'] = user.email
        token['slug'] = user.slug

        return token
    

class UserLoginSerializer(serializers.Serializer):

    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


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
        model = Otp
        fields = ('phone', 'email', 'username', 'password', 'password2', 'type', 'token', 'code')


class OtpCodeSerializer(serializers.Serializer):
    code = serializers.CharField(write_only=True, required=True)


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)