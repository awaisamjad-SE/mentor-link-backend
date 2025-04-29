from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

class SendMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver_id')
        message_text = request.data.get('message')

        if not receiver_id or not message_text:
            return Response({"error": "receiver_id and message are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            receiver = User.objects.get(id=receiver_id)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)

        message = Message.objects.create(
            sender=request.user,
            receiver=receiver,
            message=message_text,
            is_teacher_reply=False
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            receiver=self.request.user
        ).order_by('timestamp')
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

class StudentListView(APIView):
    def get(self, request):
        students = User.objects.filter(role__iexact='student').values('id', 'username', 'email')
        return Response(students)

class TeacherListView(APIView):
    def get(self, request):
        teachers = User.objects.filter(role__iexact='teacher').values('id', 'username', 'email')
        return Response(teachers)
# views.py
# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Message

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_messages_as_read(request):
    sender_id = request.data.get("sender_id")
    if not sender_id:
        return Response({"error": "sender_id is required"}, status=400)

    Message.objects.filter(
        sender_id=sender_id,
        receiver=request.user,
        read=False
    ).update(read=True, read_at=now())

    return Response({"status": "messages marked as read"})


from datetime import timedelta

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_unread_alerts(request):
    from django.utils.timezone import now
    threshold = now() - timedelta(minutes=1)

    unread_old_msgs = Message.objects.filter(
        receiver=request.user,
        read=False,
        timestamp__lt=threshold
    )
    return Response({
        "unread_count": unread_old_msgs.count(),
        "messages": [
            {
                "id": msg.id,
                "sender": msg.sender.username,
                "message": msg.message,
                "timestamp": msg.timestamp
            } for msg in unread_old_msgs
        ]
    })
