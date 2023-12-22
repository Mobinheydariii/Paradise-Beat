from rest_framework.views import APIView, Response
from rest_framework.viewsets import ViewSet
from rest_framework import status
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from django.db.models.functions import Random
from .models import(
    Category, 
    Comment,
    Beat,
    Tag,
    BeatLike,
    BeatDisLike
)
from . import serializers
from .paginations import BeatPagination


class BeatViewSet(ViewSet, BeatPagination):
    """
    A viewset for working with beat instances.
    """
    def list(self, request, category_slug=None, status=None):
        queryset = Beat.published.filter(status='AC')
        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        if status is not None:
            queryset = queryset.filter(status=status)
        
        # Add the random function to the queryset
        queryset = queryset.annotate(random=Random()).order_by('random')
        result = self.paginate_queryset(queryset, request)
        serializer = serializers.BeatSerializer(result, many=True)
        return self.get_paginated_response(serializer.data)
    

    def retrieve(self, request, slug, pk):
        queryset = get_object_or_404(Beat,slug=slug, id=pk)
        serializer = serializers.BeatDetailSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimularBeatView(APIView):
    """
    This view is for simular beats that user wants to order or listen.
    """

    def get(self, request, pk):
        # We can get the main beat that selected by user by using primery key (pk).
        beat = get_object_or_404(Beat, id=pk)

        # Here we nead to get multiple accepted beaats for user in queryset variable.
        queryset = Beat.accepted.all()

        # Filter the queryset to get random similar beats
        random_similar_beats = queryset.filter(category=beat.category)

        # Annotate the queryset with a random ordering
        random_similar_beats = random_similar_beats.annotate(random=Random()).order_by('random')[:6]

        # We shoud serialize the qurysets in to itrable objects.
        serializer = serializers.BeatSerializer(random_similar_beats, many=True)
        # Now we have to return the serializer datas with 200 status code.
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProducerRelatedBeatView(APIView):
    """
    This view created for returning more beats for user from the exact producer and category
    """
    def get(self, request, pk):
        # We can get the main beat that selected by user by using primery key (pk).
        beat = get_object_or_404(Beat, id=pk)

        # Filter the queryset to get random related beats
        queryset = Beat.accepted.filter(
            producer = beat.producer,
            category = beat.category,
            main_status = 'PU'
        )

        # Annotate the queryset with a related ordering
        result = queryset.annotate(random=Random()).order_by('random')[:6]

        # We shoud seialize our query data to json data
        serializer = serializers.BeatSerializer(result, many=True)

        # We have to return the serializer data and the corect ststus code (200).
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProducerBeatView(ViewSet):
    """
    This view created for Producer beats managemants
    """
    # Create method is for creating new beat 
    def create(self, request):
        # At first we need to have a auhenticated user to create a beat
        if request.user.is_authenticated == True:
            user = request.user
            # Then we will check that this user is the Producer user or Musician user or not?
            if user.type == 'PRD' or 'MUC':
                # If yes then we will go forward
                serializer = serializers.BeatSerializer(data=request.data, partial=True)
                # If the data is valid then save the data into database else give errors
                if serializer.is_valid(raise_exception=True):
                    slug = get_random_string(50)
                    beat = Beat.drafts.create(
                        producer = user,
                        title = serializer.validated_data['title'],
                        slug = str(slug),
                        main_status = "DF",
                        status = "CH"
                    )
                    # Save the data into database
                    beat.save()
                    # We have to save the data and return the 201 status code that means created to the client.
                    return Response({"Response":"Created."}, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"invalid user type."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Unauthorized user."},status=status.HTTP_401_UNAUTHORIZED)

    # Update method
    def update(self, request, slug, pk):
        queryset = get_object_or_404(Beat, slug=slug, id=pk)
        if request.user.is_authenticated == True:
            if request.user == queryset.producer:
                serializer = serializers.BeatSerializer(queryset, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"you are not the main producer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"you are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Delete method
    def delete(self, request, slug, pk):
        queryset = get_object_or_404(Beat, slug=slug, id=pk)
        if request.user.is_authenticated == True:
            if request.user == queryset.producer:
                queryset.delete()
                return Response({"Response":"Deleted."}, status=status.HTTP_200_OK)
            else:
                return Response({"error":"you are not the main producer."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"you are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        

class CommentViewSet(BeatViewSet):
    """
    API endpoint that allows comments to be viewed or edited.
    """
    def list(self, request, beat_id):
        beat = get_object_or_404(Beat, id=beat_id)
        queryset = Comment.objects.filter(beat=beat).order_by('-created')
        serializer = serializers.CommentListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request, beat_id):
        if request.user.is_authenticated == True:
            queryset = Beat.objects.get(id=beat_id)
            serializer = serializers.CommentSerializer(data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                comment = Comment.objects.create(
                    comment = serializer.validated_data['comment'],
                    user = request.user,
                    beat = queryset
                )
                comment.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Detail":"you are not authenticated."}, status=status.HTTP_403_FORBIDDEN)
        
    def update(self, request, pk):
        if request.user.is_authenticated == True:
            queryset = Comment.objects.get(id=pk)
            if request.user == queryset.user:
                serializer = serializers.CommentSerializer(data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response({"Detail":"Comment updated."}, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
    def delete(self, request, pk):
        if request.user.is_authenticated == True:
            queryset = Comment.objects.get(id=pk)
            if request.user == queryset.user:
                queryset.delete()
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        

class DraftBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.drafts.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)


class PublishedBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.published.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
class PrivateBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.private.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
class AcceptedBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.accepted.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
class RejectedBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.rejected.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        
class CheckingBeatsView(APIView):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            if user.type == 'PRD' or 'MUC':
                queryset = Beat.checking.filter(producer=user).order_by('-created')
                serializer = serializers.BeatSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"Detail":"You are not the comment auther."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"Detail":"You are not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        

class BeatLikeView(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated == True:
            beat = get_object_or_404(Beat, id=pk)
            like = BeatLike.objects.create(
                user = request.user,
                beat = beat,
                is_liked = True
            )
            beat.likes += 1
            like.save()
            beat.save()
            return Response({"Detail":"Beat liked."}, status=status.HTTP_200_OK)
        else:
            return Response({"Detail":"You need to authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

class BeatUnLikeView(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated == True:
            beat = get_object_or_404(Beat, id=pk)
            like = BeatLike.objects.get(user=request.user, beat=beat)
            like.is_liked == False
            beat.likes -= 1
            like.save()
            beat.save()
            return Response({"Detail":"You unlike the beat."}, status=status.HTTP_200_OK)
        else:
            return Response({"Detail":"You need to authenticate."})

class BeatDisLikeView(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated == True:
            beat = get_object_or_404(Beat, id=pk)
            dislike = BeatDisLike.objects.create(
                user = request.user,
                beat = beat,
                is_liked = True
            )
            beat.dislikes += 1
            dislike.save()
            beat.save()
            return Response({"Detail":"Beat dis liked."}, status=status.HTTP_200_OK)
        else:
            return Response({"Detail":"You need to authenticate"}, status=status.HTTP_401_UNAUTHORIZED)

class BeatUnDisLikeView(APIView):
    def post(self, request, pk):
        if request.user.is_authenticated == True:
            beat = get_object_or_404(Beat, id=pk)
            dislike = BeatDisLike.objects.get(user=request.user, beat=beat)
            dislike.is_liked == False
            beat.dislikes -= 1
            dislike.save()
            beat.save()
            return Response({"Detail":"You un dis liked the beat."}, status=status.HTTP_200_OK)
        else:
            return Response({"Detail":"You need to authenticate."})
