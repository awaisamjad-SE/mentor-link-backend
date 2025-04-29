# contactapp/views.py
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os

@api_view(['POST'])
def contact_view(request):
    data = request.data
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not (name and email and subject and message):
        return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Email to Admin
        admin_subject = f"New Contact Form Submission: {subject}"
        admin_message = f"""
        You have received a new message from your website contact form.

        Details:
        -----------------------------
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        -----------------------------
        """

        send_mail(
            subject=admin_subject,
            message=admin_message,
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=['awaisamjad.official@gmail.com'],
            fail_silently=False,
        )

        # Friendly Thank You Email to User
        user_subject = "Thanks for contacting us!"
        user_message = f"""
        Hi {name},

        Thank you for reaching out to us! We have received your message and our team will get back to you shortly.

        Please wait for our reply.

        Best regards,
        Awais Amjad Team
        """

        send_mail(
            subject=user_subject,
            message=user_message,
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({'message': 'Emails sent successfully. Thank you for contacting us!'}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
