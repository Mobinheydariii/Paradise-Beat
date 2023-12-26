from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework import status
from beats.models import Beat, BeatLicence, LicenceType
from .cart import Cart
from beats.serializers import BeatSerializer, licenceSerializer
from . import serializers


class CartDetail(APIView):
    def get(self, request):
        cart = Cart(request)
        
        serializer = serializers.CartSerializer(instance=cart, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CartAddView(APIView):
    def post(self, request, beat_id, licence):
        if request.user.is_authenticated == True:
            beat = get_object_or_404(Beat, id=beat_id)
            licence = get_object_or_404(BeatLicence, beat=beat, id=licence)
            beat_serializer = BeatSerializer(instance=beat)
            licence_serializer = licenceSerializer(instance=licence)
            beat_ser = beat_serializer.data
            licence_ser = licence_serializer.data
            cart = Cart(request)
            cart = cart.add(beat=beat_ser, licence=licence_ser, price=licence_ser['price'])
            return Response({'message': 'Added to your shopping cart', 'cart':cart}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "You must login first"}, status=status.HTTP_401_UNAUTHORIZED)
        

class CartRemove(APIView):
    def delete(self, request, beat_id):
        cart = Cart(request)
        beat = get_object_or_404(Beat, id=beat_id)
        cart.remove(beat)
        return Response({'massage':'Removed.'}, status=status.HTTP_200_OK)
