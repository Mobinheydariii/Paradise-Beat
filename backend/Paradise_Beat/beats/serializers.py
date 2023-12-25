from rest_framework import serializers
from .models import(
    Beat,
    Category,
    Comment,
    Tag,
    BasicBeatLicence,
    PermiumBeatLicence
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



class BasicLicenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BasicBeatLicence
        fields = "__all__"

class PermiumLicenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermiumBeatLicence
        fields = "__all__"