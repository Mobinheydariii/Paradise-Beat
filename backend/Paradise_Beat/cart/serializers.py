from rest_framework import serializers
from beats.serializers import BeatSerializer
from .cart import Cart




class CartSerializer(serializers.Serializer):
    beat = BeatSerializer(many=True)
    
    licence = serializers.CharField()
    price = serializers.IntegerField()
    total_price = serializers.IntegerField()
    lenth = serializers.IntegerField()
    