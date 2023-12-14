from django.db.models import Manager
from . import models


class AcceptedManager(Manager):
    def get_queryset(self):
        """Filter records based on the 'accepted' status."""
        return super().get_queryset().filter(status=models.Beat.Status.ACCEPTED)

class DraftManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=models.Beat.Status.DRAFT)