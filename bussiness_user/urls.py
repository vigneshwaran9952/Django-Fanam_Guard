from django.urls import path
from . import views
from .views import *

urlpatterns = [

    # ==========================================
    # Health Check
    # ==========================================
    path('api/health/', health_check, name='health_check'),

    # ==========================================
    # Authentication
    # ==========================================
    path('api/register/', register, name='register'),
    path('api/login/', login, name='login'),
    path('api/logout/', logout, name='logout'),
    path('api/forgot-password/', forgot_password, name='forgot_password'),
    path('api/change-password/', change_password, name='change_password'),

    # ==========================================
    # User Profile & Settings
    # ==========================================
    path('api/user-info/', views.get_user_info, name='get_user_info'),
    path('api/settings/', save_settings, name='save_settings'),
    path('api/settings/get/', get_settings, name='get_settings'),

    # ==========================================
    # Chat
    # ==========================================
    path('api/chat/new/', new_chat, name='new_chat'),
    path('api/chat/', chat, name='chat'),
    path('api/chat/history/', get_chat_history, name='get_chat_history'),
    path('api/chat/sessions/', get_all_sessions, name='get_all_sessions'),
    # path('api/chat/load/', load_session, name='load_session'),

    # ==========================================
    # AI Features
    # ==========================================
    path('api/rewrite/', rewrite_response, name='rewrite_response'),
    path('api/suggestion/', click_suggestion, name='click_suggestion'),
    path('api/voice-to-text/', voice_to_text, name='voice_to_text'),
    path('api/text-to-speech/', text_to_speech, name='text_to_speech'),

    # ==========================================
    # Feedback & Metadata
    # ==========================================
    path('api/feedback/', feedback_submit, name='feedback_submit'),
    path('api/get-metadata/', get_metadata, name='get_metadata'),

    # ==========================================
    # Document Management
    # ==========================================
    path('api/upload-pdf/', upload_pdf, name='upload_pdf'),
    path('api/display-rules/', display_rules, name='display_rules'),
    path('api/resources/', resource_list, name='resource-list'),
    path('api/compliance/', store_compliance_json, name='compliance-check'),

    # ==========================================
    # Compliance Compare
    # ==========================================
    path('api/countries/', get_countries, name='get_countries'),
    path('api/compliance-compare/', compliance_compare, name='compliance_compare'),

    # ==========================================
    # Compliance Bot
    # ==========================================
    path('compliance_bot/', compliance_bot, name='compliance_bot'),
    path('api/regulator-chat/', regulator_chat, name='regulator_chat'),

    # ==========================================
    # Master Data APIs
    # ==========================================
    path('api/get-countries/', get_countries_list, name='get_countries_list'),
    path('api/get-sectors-by-country/', get_sectors_by_country, name='get_sectors_by_country'),
    path('api/get-languages/', get_languages, name='get_languages'),
    path('country-codes/', get_country_codes),

    # ==========================================
    # FAQs
    # ==========================================
    path('faqs/', views.get_faqs, name='get_faqs'),

    # ==========================================
    # Statistics
    # ==========================================
    path('statistics/', statistics_view),

    # ==========================================
    # Future APIs
    # ==========================================
    # path("api/ai-doc-reader/", ai_doc_reader, name="ai_doc_reader"),
    # path("api/regulatory-register/", RegulatoryRegister),
]