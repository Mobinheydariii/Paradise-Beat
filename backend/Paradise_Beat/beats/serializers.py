from rest_framework import serializers
from .models import(
    Beat,
    Category,
    Comment,
    Tag,
    BeatLicence,
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


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"


class licenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BeatLicence
        fields = "__all__"