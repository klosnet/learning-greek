from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import jsonfield


class ActivityState(models.Model):
    
    user = models.ForeignKey(User)
    activity_slug = models.CharField(max_length=50)
    
    started = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True)  # NULL means in progress
    
    state = jsonfield.JSONField()
    
    class Meta:
        # @@@ initially assume an activity is only done once per user
        unique_together = [("user", "activity_slug")]


def get_activity_state(user, activity_slug):
    try:
        activity_state = ActivityState.objects.get(user=user, activity_slug=activity_slug)
    except ActivityState.DoesNotExist:
        activity_state = None
    
    return activity_state


def get_activities(user):
    # construct a list of available activities
    
    activities = []
    for slug, activity in settings.ACTIVITIES.items():
        activities.append({
            "slug": slug,
            "title": activity.title,
            "description": activity.description,
        })
    
    # annotate list with state for this user
    
    for activity in activities:
        activity.update({
            "state": get_activity_state(user, activity["slug"])
        })
    
    return activities