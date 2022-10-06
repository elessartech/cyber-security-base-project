from django.db import models

# Create your models here.
class Selection(models.Model):
    name = models.CharField(max_length=50)


class Poll(models.Model):
    name = models.CharField(max_length=50)
    selections = models.ManyToManyField(Selection, related_name="polls", blank=True)


class Vote(models.Model):
    selection = models.ForeignKey(
        Selection,
        on_delete=models.SET_NULL,
        related_name="votes",
        null=True,
        blank=True,
    )
    poll = models.ForeignKey(
        Poll, on_delete=models.SET_NULL, related_name="votes", null=True, blank=True
    )
