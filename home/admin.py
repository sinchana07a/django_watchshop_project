from django.contrib import admin
from .models import Watches ,RatingComment
# Register your models here.


@admin.register(Watches)
class WatchesAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'desc', 'price')
    search_fields=('name',)
    ordering=('upload_date',)
    

@admin.register(RatingComment)
class RatingCommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'comment', 'created_on')

