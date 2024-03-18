from django.db import models
from authuser.models import AuthUser
# Create your models here.
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Notification(models.Model):
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    receiver_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    sender_user_id = models.IntegerField()
    action = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField()
    is_read = models.BooleanField()


    class Meta:
        managed = False
        db_table = 'notification'
    
    def save(self, *args, **kwargs):
        is_new = self.pk is  None 
        print("+++++++  USer +++++++ ", self.receiver_user.id)
        print("+++++++ Save notification +++++++",is_new, self.pk,self.id)
        super().save(*args, **kwargs)
      
        if is_new:
            print("+++++++ Create new notification +++++++")
            channel_layer = get_channel_layer()
            group_name = f'user_{self.receiver_user.id}'
            notification_count = Notification.objects.filter(receiver_user=self.receiver_user, is_read=0).count()
            receiver=self.receiver_user
            sender=AuthUser.objects.get(id=self.sender_user_id)
            
            # Format datetime to a string
            formatted_datetime = self.created_date.strftime("%Y-%m-%d %H:%M:%S")
            print("create count ==>",notification_count)

            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'send_notification',  
                    'content': {
                        'sender_user_id':sender.id,
                        'sender_username':sender.username,
                        'sender_fname':sender.first_name,
                        'sender_lname':sender.last_name,
                        'notification_count': notification_count,
                        'type': self.type,
                        'message': self.message,
                        'created_date': formatted_datetime,
                        'action': self.action,
                        'is_read': self.is_read,
                    }
                }
            )
        else:
            notification_count = Notification.objects.filter(receiver_user=self.receiver_user, is_read=0).count()
            
            print("update count ==>",notification_count)
            channel_layer = get_channel_layer()
            group_name = f'user_{self.receiver_user.id}'
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'update_notification',  
                    'content': {
                        'notification_count': notification_count,
                    }
                    })