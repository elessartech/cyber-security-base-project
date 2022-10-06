from django.contrib import admin

from polls.models import Selection, Poll

# Register your models here.

admin.site.register(Selection)
admin.site.register(Poll)
