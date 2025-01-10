from django.contrib import admin
from .models import ScamReport, Comment, Reaction

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Number of empty rows for adding new comments

class ReactionInline(admin.TabularInline):
    model = Reaction
    extra = 1  # Number of empty rows for adding new reactions

@admin.register(ScamReport)
class ScamReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'reported_by', 'created_at', 'updated_at']
    inlines = [CommentInline, ReactionInline]

admin.site.register(Comment)
admin.site.register(Reaction)
