from rest_framework import serializers
from .models import(
    Beat,
    Category,
    Comment,
    Tag,
)

class BeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beat
        fields = "__all__"
        
        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class CommntSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"

