from django.urls import path
from .views import SignupView, VerifyOtpView, LoginView, PasswordResetRequestView, PasswordResetConfirmView,UserProfileView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify-otp/', VerifyOtpView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/<int:user_id>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('user/', UserProfileView.as_view(), name='user-profile'),
]
