from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework import status
from beats.models import Beat, BeatLicence, LicenceType
from . models import Cart, CartItem
from beats.serializers import BeatSerializer, licenceSerializer
from .serializers import CartItemSerializer, CartSerializer



class AddToItemCart(APIView):
    def post(self, request, beat_id, licence_id):
        if request.user.is_authenticated == True:
            cart, created = Cart.objects.get_or_create(user=request.user)
            beat = get_object_or_404(Beat, id=beat_id)
            licence = get_object_or_404(BeatLicence, id=licence_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                beat=beat,
                user=request.user,
                licence=licence,
                price=licence.price,
            )
            cart.total_price += cart_item.price
            cart.save()
            return Response({'message': 'Added to cart', 'data': CartItemSerializer(instance=cart_item).data}, status=status.HTTP_200_OK)
        else:
            return Response({'mesage':'You need to authenticate.'}, status=status.HTTP_401_UNAUTHORIZED)


class RemoveItemCart(APIView):
    def post(self, request, beat_id, licence_id):
        if request.user.is_authenticated == True:
            cart, created = Cart.objects.get_or_create(user=request.user)
            beat = get_object_or_404(Beat, id=beat_id)
            licence = get_object_or_404(BeatLicence, id=licence_id)
            cart_item = CartItem.objects.get(cart=cart, beat=beat, user=request.user, licence=licence)
            cart.total_price -= cart_item.price
            cart.save()
            cart_item.delete()
            return Response({'message': 'Removed from cart'}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"You must login to do that."}, status=status.HTTP_401_UNAUTHORIZED)
    
class CartDetial(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            return Response({'data': CartItemSerializer(cart_items, many=True).data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Please log in first"}, status=status.HTTP_401_UNAUTHORIZED)