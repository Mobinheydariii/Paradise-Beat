from django.urls import path
from . import views


app_name = "beats"


urlpatterns = [
    # Categories and beats for the public side of web
    path('categories/', views.Categories.as_view(), name="categories"),
    path('beat/detail/<slug:slug>/<int:pk>/', views.BeatDetail.as_view(), name="beat_detail"),


    # Producers beat list for producer panel
    path('producer/accepted/beats/', views.ProducerAcceptedBeats.as_view(), name="producer_accepted_beats"),
    path('producer/rejected/beats/', views.ProducerRejectedBeats.as_view(), name="producer_rejected_beats"),
    path('producer/in-checking/beats/', views.ProducerCheckingBeats.as_view(), name="producer_in_checking_beats"),
    path('producer/published/beats/', views.ProducerPublishedBeats.as_view(), name="producer_published_beats"),
    path('producer/draft/beats/', views.ProducerDraftBeats.as_view(), name="producer_draft_beats"),


    # Producer beat detail for producer panel
    path('producer/accepted/beat/<slug:slug>/', views.ProducerAcceptedBeatDetail.as_view(), name="producer_accepted_beat_detail"),
    path('producer/rejected/beat/<slug:slug>/', views.ProducerRejectedBeatDetail.as_view(), name="producer_rejected_beat_detail"),
    path('producer/in-checking/beat/<slug:slug>/', views.ProducerCheckingBeatDetail.as_view(), name="producer_in_checking_beat_detail"),
    path('producer/published/beat/<slug:slug>/', views.ProducerPublishedBeatDetail.as_view(), name="producer_published_beat_detail"),
    path('producer/draft/beat/<slug:slug>/', views.ProducerDraftBeatDetail.as_view(), name="producer_draft_beat_detail"),

    # Comments
    path('add/beat/comment/', views.AddCommentView.as_view(), name="add_comment"),


    # Beats list for panel
    path('accepted/beats/', views.AcceptedBeats.as_view(), name="accepted_beats"),
    path('rejected/beats/', views.RejectedBeats.as_view(), name="rejected_beats"),
    path('checking/beats/', views.CheckingBeats.as_view(), name="checking_beats"),
    path('published/beats/', views.PublishedBeats.as_view(), name="published_beats"),
    path('draft/beats/', views.DraftBeats.as_view(), name="draft_beats"),

    # Create or update Beat Views
]