from django.urls import path
from . import views

urlpatterns = [
    # ❌ REMOVE THESE TWO LINES - handled by main app
    # path('api/user-type/', views.get_user_type, name='get_user_type'),
    # path('user-info/', views.get_user_info, name='user-info'),
    
    # ✅ KEEP THESE - Guest-specific endpoints
    path('validate-email/', views.validate_email),
    path('get_settings/', views.get_settings),
    path('save-settings/', views.save_settings),
    path('usage-limit/', views.get_usage_limit),
    path('send-message/', views.send_message),
    path('config/', views.get_config),
    path('features/', views.get_features),
    path('login-redirect/', views.login_redirect),
]