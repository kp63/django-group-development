from django.contrib import admin
from votes.models import Vote, Choice, VoteResult

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class VoteAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Vote, VoteAdmin)
admin.site.register(Choice)
admin.site.register(VoteResult)
