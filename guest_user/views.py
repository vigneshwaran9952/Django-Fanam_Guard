from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import status
from django.conf import settings
import time
from drf_spectacular.utils import OpenApiParameter
from .models import GuestEmail
from .models import UserSettings



from .serializers import (
    ValidateEmailSerializer,
    SaveSettingsSerializer,
    SendMessageSerializer,
    LoginRedirectSerializer,
    UsageLimitQuerySerializer,
    ConfigResponseSerializer,
    FeaturesResponseSerializer,
    UserInfoResponseSerializer,  # Add this new serializer
)


from .serializers import (
    ValidateEmailSerializer,
    SaveSettingsSerializer,
    SendMessageSerializer,
    LoginRedirectSerializer,
    UsageLimitQuerySerializer,
)

from .utils import (
    is_email_well_formed,
    check_limit,
    update_usage,
    get_llm_response
)





from .models import GuestEmail

@extend_schema(
    request=ValidateEmailSerializer,
    responses={200: dict, 400: dict}
)
@api_view(['POST'])
def validate_email(request):

    serializer = ValidateEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']

    if not is_email_well_formed(email):
        return Response(
            {'status': 'error', 'message': 'Invalid email'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_data = check_limit(email)

    # ✅ Store guest email in session
    request.session['guest_email'] = email
    request.session['user_type'] = 'guest'

    # ✅ Store email ONLY in DB
    GuestEmail.objects.get_or_create(email=email)

    return Response({
        'status': 'success',
        'is_valid': True,
        'user_type': 'guest',
        'email': email,
        'usage_data': user_data
    })


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="email",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="User email to fetch settings"
        )
    ],
    responses={200: dict, 404: dict},
    summary="Get user settings from DB",
    description="Fetch saved user settings directly from database"
)
@api_view(['GET'])
def get_settings(request):

    # ✅ Read email from query param
    email = request.query_params.get("email")

    # ❌ Email missing
    if not email:
        return Response(
            {
                "success": False,
                "message": "Email is required"
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Fetch settings from DB
    try:
        user_settings = UserSettings.objects.get(email=email)

        return Response(
            {
                "success": True,
                "email": email,
                "settings": {
                    "country": user_settings.country,
                    "sector": user_settings.sector
                }
            },
            status=status.HTTP_200_OK
        )

    except UserSettings.DoesNotExist:
        return Response(
            {
                "success": False,
                "message": "Settings not found for this email"
            },
            status=status.HTTP_404_NOT_FOUND
        )

@extend_schema(
    request=SaveSettingsSerializer,
    responses={200: dict, 400: dict}
)
@api_view(['POST'])
def save_settings(request):

    serializer = SaveSettingsSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    country = serializer.validated_data['country']
    sector = serializer.validated_data['sector']

    if not is_email_well_formed(email):
        return Response(
            {'status': 'error', 'message': 'Valid email required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Store only in DB (no session)
    settings_obj, created = UserSettings.objects.update_or_create(
        email=email,
        defaults={
            "country": country,
            "sector": sector
        }
    )

    return Response({
        'status': 'success',
        'email': email,
        'country': country,
        'sector': sector,
        'saved_in_db': True,
        'new_entry': created
    })




@extend_schema(
    parameters=[
        OpenApiParameter(
            name='email',
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description='User email address'
        )
    ],
    responses={200: dict, 400: dict}
)
@api_view(['GET'])
def get_usage_limit(request):

    """
    GET /api/get-usage-limit/?email=user@example.com
    """
    serializer = UsageLimitQuerySerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']

    if not is_email_well_formed(email):
        return Response(
            {'status': 'error', 'message': 'Valid email required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_data = check_limit(email)
    usage = user_data.get('usage_count', 0)

    response = {
        'status': 'success',
        'usage_count': usage,
        'max_questions': settings.MAX_QUESTIONS,
        'remaining_questions': max(0, settings.MAX_QUESTIONS - usage),
        'limit_reached': usage >= settings.MAX_QUESTIONS
    }

    if usage >= settings.MAX_QUESTIONS and user_data.get('first_use_timestamp'):
        remaining = settings.COOLDOWN_SECONDS - (
            time.time() - user_data['first_use_timestamp']
        )
        if remaining > 0:
            response['cooldown_remaining_seconds'] = int(remaining)

    return Response(response)



from .models import UserSettings

@extend_schema(
    request=SendMessageSerializer,
    responses={200: dict, 400: dict, 429: dict}
)
@api_view(['POST'])
def send_message(request):
    """
    POST /api/send-message/
    """
    serializer = SendMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    question = serializer.validated_data['question']

    # ✅ Email validation
    if not is_email_well_formed(email):
        return Response(
            {'status': 'error', 'message': 'Valid email required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # ✅ Fetch country & sector from DB instead of session
    try:
        user_settings = UserSettings.objects.get(email=email)
        country = user_settings.country
        sector = user_settings.sector

    except UserSettings.DoesNotExist:
        country = None
        sector = None

    # ✅ Usage check
    user_data = check_limit(email)
    if user_data.get('usage_count', 0) >= settings.MAX_QUESTIONS:
        return Response(
            {'status': 'error', 'message': 'Usage limit reached'},
            status=status.HTTP_429_TOO_MANY_REQUESTS
        )

    # ✅ LLM call with DB values
    ai_response = get_llm_response(question, country, sector)

    update_usage(email)

    return Response({
        'status': 'success',
        'email': email,
        'country': country,
        'sector': sector,
        'answer': ai_response
    })

@extend_schema(
    responses={200: ConfigResponseSerializer}
)
@api_view(['GET'])
def get_config(request):
    return Response({
        'status': 'success',
        'countries': settings.COUNTRIES,
        'sectors': settings.SECTORS,
        'max_questions': settings.MAX_QUESTIONS,
        'cooldown_hours': settings.COOLDOWN_SECONDS / 3600
    })


@extend_schema(
    responses={200: FeaturesResponseSerializer}
)
@api_view(['GET'])
def get_features(request):
    return Response({
        'status': 'success',
        'features': [
            {'id': 1, 'title': 'Global Access'},
            {'id': 2, 'title': 'Chat History'},
            {'id': 3, 'title': 'Expert Mode'},
        ]
    })



@extend_schema(
    request=LoginRedirectSerializer,
    responses={200: dict, 400: dict}
)
@api_view(['POST'])
def login_redirect(request):
    """
    POST /api/login-redirect/
    """
    serializer = LoginRedirectSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']

    if not is_email_well_formed(email):
        return Response(
            {'status': 'error', 'message': 'Valid email is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response({
        'status': 'success',
        'message': 'Redirecting to login portal...',
        'redirect_url': '/login',
        'email': email
    })

