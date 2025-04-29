from django.urls import path
from .views import SendMessageView, MessageListView, StudentListView, TeacherListView,mark_messages_as_read,get_unread_alerts

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send-message'),
    path('messages/', MessageListView.as_view(), name='list-messages'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('chat/mark-as-read/', mark_messages_as_read, name='mark-messages-as-read'),
    path('chat/unread-alerts/', get_unread_alerts, name='get-unread-alerts'),


]
