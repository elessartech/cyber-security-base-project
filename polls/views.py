from django.shortcuts import render
from django.views import View

from polls.models import Selection, Poll, Vote

# Create your views here.
class IndexView(View):
    def get(self, request):
        polls = Poll.objects.all()
        return render(
            request,
            template_name="polls/index.html",
            context={
                "polls": polls,
            },
        )


class PollView(View):
    def get(self, request, poll_id):
        poll = Poll.objects.get(id=poll_id)
        votes = Vote.objects.filter(poll=poll)
        selections = Selection.objects.filter(polls=poll)
        stats = {}
        for selection in selections:
            selection_name = selection.name
            if not selection_name in stats:
                stats[selection_name] = 0
        for vote in votes:
            stats[vote.selection.name] += 1
        return render(
            request,
            template_name="polls/poll.html",
            context={
                "poll": poll,
                "stats": None if sum(stats.values()) == 0 else stats,
            },
        )

    def post(self, request, poll_id):
        selection_id = request.POST.get("selection_id")
        poll = Poll.objects.get(id=poll_id)
        selection = Selection.objects.get(id=selection_id)
        Vote.objects.create(
            poll=poll,
            selection=selection,
        )
        return render(
            request,
            template_name="polls/poll.html",
            context={
                "poll": poll,
                "message": "Your vote has been accepted",
            },
        )
