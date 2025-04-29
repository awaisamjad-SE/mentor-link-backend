from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    SignupSerializer, 
    VerifyOtpSerializer, 
    LoginSerializer, 
    PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer
)

class SignupView(APIView):
    def post(self, request):
        """
        Handle user sign up by validating data and sending OTP to email.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate OTP and send email to user
            send_mail(
                'Verify your email',
                f'Your OTP is {user.otp}',
                'no-reply@yourdomain.com',  # Change to a proper 'from' email
                [user.email],
                fail_silently=False,
            )
            return Response({'message': 'Signup successful. OTP sent to email.'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOtpView(APIView):
    def post(self, request):
        """
        Verify the OTP sent to the user's email.
        """
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            user = get_object_or_404(User, email=email)

            if user.otp == otp:
                user.is_verified = True
                user.otp = ''  # Clear OTP after verification
                user.save()
                return Response({'message': 'Email verified successfully.'})

            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.core.mail import send_mail
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        # Extract email or username and password from the request
        email_or_username = request.data.get('email_or_username')
        password = request.data.get('password')

        if not email_or_username:
            return Response({"error": "Email or Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Try to retrieve the user based on email or username
        try:
            if '@' in email_or_username:  # If it contains '@', treat it as an email
                user = User.objects.get(email=email_or_username)
            else:  # Otherwise, treat it as a username
                user = User.objects.get(username=email_or_username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is verified
        if not user.is_verified:
            return Response({"error": "Please verify your email first."}, status=status.HTTP_400_BAD_REQUEST)

        # Manually check password using the user's `check_password` method
        if not user.check_password(password):
            return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens for authenticated user
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Send alert email after successful login
        try:
            send_mail(
                'Login Alert',
                f'Hello {user.username},\n\nYou have successfully logged into your account.',
                settings.DEFAULT_FROM_EMAIL,  # Usually set in settings.py
                [user.email],  # Send to the user's email
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Login alert email could not be sent: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "message": "Login successful.",
            "access_token": str(access_token),
            "refresh_token": str(refresh),
            "role": user.role  # Return the user's role
        }, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified,
        })

class PasswordResetRequestView(APIView):
    def post(self, request):
        """
        Send a password reset link to the user's email.
        """
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)
            token = get_random_string(length=32)  # Generate a random token for the reset link
            user.otp = token
            user.save()

            reset_link = f"http://localhost:8000/api/accounts/reset-password/{user.id}/{token}/"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                'no-reply@yourdomain.com',  # Change to a proper 'from' email
                [user.email],
                fail_silently=False,
            )

            return Response({'message': 'Password reset link sent to email.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    def post(self, request, user_id, token):
        """
        Confirm password reset using the token and new password.
        """
        user = get_object_or_404(User, id=user_id)

        if user.otp != token:
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['password']
            user.set_password(new_password)
            user.otp = ''  # Clear OTP after password reset
            user.save()
            return Response({'message': 'Password reset successful.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
