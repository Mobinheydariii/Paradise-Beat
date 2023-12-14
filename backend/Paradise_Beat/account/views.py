from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework.views import APIView, Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from . import serializers
from random import randint
from .models import(
    User,
    UserProfile,
    Otp
)



class TokenObtainView(TokenObtainPairView):
    serializer_class = serializers.TokenObtainSerializer


class UserLogin(APIView):
   def post(self, request):
        if request.user.is_authenticated == True:
           return Response("You are already logged in", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.UserLoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = authenticate(username=serializer.validated_data['phone'], password=serializer.validated_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        token = RefreshToken.for_user(user)
                        return Response({"refresh": str(token),
                                          "access": str(token.access_token)}, status=status.HTTP_200_OK)
                    else:
                        return Response("User account is disabled", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response("Invalid username or password", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
           

class UserLogout(APIView):
    def post(self, request):
        if request.user.is_authenticated == True:
            logout(request)
            return Response("Successfully logged out", status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response("You are not logged in", status=status.HTTP_400_BAD_REQUEST)
        

class UserRegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated == True:
            return Response({"detail": "You are authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.OtpSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data['password']
                password2 = serializer.validated_data['password2']
                if password == password2:
                    token = get_random_string(length=100)
                    code = randint(100000, 999999)
                    otp = Otp.objects.create(
                        phone = serializer.validated_data['phone'],
                        email = serializer.validated_data['email'],
                        username = serializer.validated_data['username'],
                        password = serializer.validated_data['password'],
                        type = serializer.validated_data['type'],
                        code = str(code),
                        token = str(token)
                    )
                    otp.save()
                    return Response({"otp created":[{'code':code, 'token':token}]}, status=status.HTTP_201_CREATED)
                else:
                    return Response("password is invalid", status=status.HTTP_403_FORBIDDEN)
                
            else:
                return Response({"errores" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            

class UserCheckOtp(APIView):
    def post(self, request, token):
        if request.user.is_authenticated == True:
            return Response("you are authenticated", status=status.HTTP_400_BAD_REQUEST)
        else:
            otp = get_object_or_404(Otp, token=token)
            if otp:
                serializer = serializers.OtpCodeSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    code = serializer.validated_data['code']
                    if otp.code == code:
                        otp.is_used = True
                        otp.save()
                        user = User.objects.create_user(
                            phone = otp.phone,
                            email = otp.email,
                            username = otp.username,
                            password = otp.password,
                            type = otp.type,
                            slug = token
                        )
                        user.save()
                        authenticate(user)
                        token = RefreshToken.for_user(user)
                        return Response({"refresh": str(token), "access": str(token.access_token)}, status=status.HTTP_200_OK)
                    else:
                        return Response("otp code is invalid", status=status.HTTP_400_BAD_REQUEST)    
                else:
                    return Response({"errores" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("otp is not exists", status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    def get(self, request, username, slug):
        user = get_object_or_404(User, username=username, slug=slug)
        profile = UserProfile.objects.get(user=user)
        serializer = serializers.UserProfileSerializer(instance=profile)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserDeleteAccount(APIView):
    def delete(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            user = get_object_or_404(User, slug=user.slug)
            user.delete()
            return Response("User successfully deleted", status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserChangePasswordView(APIView):
    def post(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            serializer = serializers.UserChangePasswordSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                oldpassword = serializer.validated_data['oldpassword']
                newpassword = serializer.validated_data['newpassword']
                confirm_new_password = serializer.validated_data['confirm_newpassword']
                if user.check_password(oldpassword):
                    if newpassword == confirm_new_password:
                        user.set_password(newpassword)
                        user.save()
                        return Response('Password changed', status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'New password and confirmation do not match'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error':'Old password is incorrect'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'errors':serializer.errors}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response('you are not authenticated', status=status.HTTP_401_UNAUTHORIZED)
