from django.contrib import admin
from .models import *

   
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = ['id','type','receiver_user','sender_user_id', 'message', 'created_date','is_read']
    list_filter = ['type','receiver_user', 'message', 'created_date','is_read']
    search_fields = ['type','receiver_user__username', 'message', 'created_date','is_read']
 
    # def get_username(self, obj):
    #     return obj.user.username

    # get_username.short_description = 'User'  