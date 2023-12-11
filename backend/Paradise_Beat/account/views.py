from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.utils.crypto import get_random_string
from rest_framework.views import APIView, Response
from rest_framework import status
from . import models
from . import serializers
from random import randint


class LoginView(APIView):
   def post(self, request):
        if request.user.is_authenticated:
           return Response("You are already logged in", status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return Response("Successfully logged in", status=status.HTTP_200_OK)
                    else:
                        return Response("User account is disabled", status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response("Invalid username or password", status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
           

class LogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response("Successfully logged out", status=status.HTTP_200_OK)
        else:
            return Response("You are not logged in", status=status.HTTP_400_BAD_REQUEST)

class SimleUserRegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response({"detail": "You are authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.OtpSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                password = serializer.validated_data['password']
                password2 = serializer.validated_data['password2']
                if password == password2:
                    token = get_random_string(length=100)
                    code = randint(100000, 999999)
                    otp = models.Otp.objects.create(
                        phone = serializer.validated_data['phone'],
                        email = serializer.validated_data['email'],
                        username = serializer.validated_data['username'],
                        password = serializer.validated_data['password'],
                        code = str(code),
                        token = str(token),
                        type = "SIU"
                    )
                    otp.save()
                    return Response("otp created", {
                        "code" : code,
                        "token" : token
                    })
                else:
                    return Response("password is invalid")
                
            else:
                return Response({"errores" : serializer.errors})
            

class SimpleUserCheckOtp(APIView):
    def post(self, request, token):
        if request.user.is_authenticated:
            return Response("you are authenticated", status=status.HTTP_400_BAD_REQUEST)
        else:
            otp = get_object_or_404(models.Otp, token=token)
            if otp:
                if otp.type == "SIU":
                    serializer = serializers.OtpCodeSerializer(data=request.data)
                    if serializers.is_valid(raise_exception=True):
                        code = serializer.validated_data['code']
                        if otp.code == code:
                            user = models.SimpleUser.objects.create(
                                phone = otp.phone,
                                email = otp.email,
                                username = otp.username,
                                password = otp.password,
                                type = "SIU"
                            )
                            user.save()
                            profile = models.SimpleUserProfile.objects.create(user=user)
                            profile.save()
                            authenticate(user)
                            login(request, user)
                        else:
                            return Response("otp code is invalid", status=status.HTTP_400_BAD_REQUEST)    
                    else:
                        return Response({"errores" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response("you are not a Simple_User", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("otp is not exists", status=status.HTTP_404_NOT_FOUND)
        
        
            




class SimpleUserProfileView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            profile = models.SimpleUserProfile.objects.get(user=user)
            serializer = serializers.SimpleUserSerializer(instance=profile)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("you ar not authenticate", status=status.HTTP_401_UNAUTHORIZED)
        

    def put(self, request):
       if request.user.is_authenticated:
           user = request.user
           profile = models.SimpleUserProfile.objects.get(user=user)
           serializer = serializers.SimpleUserProfileSerializer(instance=profile, data=request.data, partial=True)
           if serializer.is_valid(raise_exception=True):
               serializer.save()
               return Response("updated", status=status.HTTP_200_OK)
           else:
               return Response({"error": serializer.errors})
       else:
           return Response("you are not authenticated", status=status.HTTP_401_UNAUTHORIZED)

class SimpleUserDeleteView(APIView):
    def delete(self, request, pk):
        if request.user.is_authenticated:
            user = get_object_or_404(models.SimpleUser, pk=pk)
            user.delete()
            return Response("User successfully deleted", status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
