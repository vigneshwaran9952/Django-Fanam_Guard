from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class UserTypeResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    user_type = serializers.CharField(allow_null=True)
    #type_user = serializers.CharField(allow_null=True)

    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    settings = serializers.DictField(required=False)

# ======================================================
# 🔐 AUTH SERIALIZERS
# ======================================================

class RegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=150)
     # ✅ New Inputs
    country_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    
    password = serializers.CharField(
    write_only=True,
    min_length=8,
    error_messages={
        "min_length": "Ensure this field has at least 08 characters."
    }
)

    user_country = serializers.CharField(required=True)
    sub_category = serializers.CharField(required=True)

    # Accept BOTH (aligned with API)
    user_type = serializers.ChoiceField(
        choices=["business"],
        required=False
    )

    user_type = serializers.ChoiceField(
    choices=["business", "regulator"]
)



    

    def validate_password(self, value):
        if (
            not any(c.islower() for c in value)
            or not any(c.isupper() for c in value)
            or not any(c.isdigit() for c in value)
        ):
            raise serializers.ValidationError(
                "Password must include uppercase, lowercase, and a number"
            )
        return value


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ChangePasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_new_password(self, value):
        if (
            len(value) < 8
            or not any(c.islower() for c in value)
            or not any(c.isupper() for c in value)
            or not any(c.isdigit() for c in value)
        ):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and include uppercase, lowercase, and a number"
            )
        return value


# ======================================================
# ⚙️ USER SETTINGS
# ======================================================

class UserSettingsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    country = serializers.CharField()
    sector = serializers.CharField()
    language = serializers.CharField()


class BusinessSaveSettingsRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    country = serializers.CharField()
    sector = serializers.CharField()
    language = serializers.CharField()


class BusinessSaveSettingsResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    settings = UserSettingsSerializer(read_only=True)


class GetSettingsResponseSerializer(serializers.Serializer):
    
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    settings = UserSettingsSerializer(read_only=True)


class SaveSettingsRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    country = serializers.CharField()
    sector = serializers.CharField()
    language = serializers.CharField()


# ======================================================
# 💬 CHAT & SESSION
# ======================================================

class NewChatResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    session_id = serializers.CharField(read_only=True)


class LoadSessionRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    session_id = serializers.UUIDField(required=True)


class LoadSessionResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    session_id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    chat_history = serializers.ListField(child=serializers.DictField(), read_only=True)
    stm_context = serializers.ListField(child=serializers.DictField(), read_only=True)


class ChatRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    session_id = serializers.CharField(required=True)
    question = serializers.CharField(required=True)
    enhance_mode = serializers.BooleanField(default=False)
    deep_research_mode = serializers.BooleanField(default=False)


class MessageSerializer(serializers.Serializer):
    role = serializers.CharField()
    content = serializers.CharField()
    sources = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    suggestions = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    intent = serializers.CharField(required=False)
    mode = serializers.CharField(required=False)
    deep_research_fallback = serializers.BooleanField(required=False)


class ChatResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    answer = serializers.CharField(read_only=True)
    sources = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )
    suggestions = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )
    chat_history = MessageSerializer(many=True, read_only=True)
    intent = serializers.CharField(read_only=True)
    intent_confidence = serializers.FloatField(read_only=True)
    deep_research_fallback = serializers.BooleanField(read_only=True)


class ChatHistoryResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    session_id = serializers.CharField(read_only=True)
    chat_history = MessageSerializer(many=True, read_only=True)
    stm_context = serializers.ListField(child=serializers.DictField(), read_only=True)
    title = serializers.CharField(read_only=True)


class AllSessionsResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    sessions = serializers.ListField(
        child=serializers.DictField(), read_only=True
    )


'''class VoiceToTextRequestSerializer(serializers.Serializer):
    audio = serializers.FileField(required=True)'''

class VoiceToTextRequestSerializer(serializers.Serializer):

    @extend_schema_field(OpenApiTypes.BINARY)
    def audio(self):
        pass

    audio = serializers.FileField(
        help_text="Upload an audio file (wav/mp3)",
        required=True
    )
'''class VoiceToTextRequestSerializer(serializers.Serializer):
    audio = serializers.FileField(
        help_text="Upload an audio file (wav/mp3)"
    )'''

# ======================================================
# 🔄 REWRITE & SUGGESTIONS
# ======================================================

class RewriteAnswerRequestSerializer(serializers.Serializer):
    message_index = serializers.IntegerField(min_value=0)

    # 🔥 NEW: allow stateless rewrite (optional)
    email = serializers.EmailField(required=False)
    session_id = serializers.CharField(required=False)



class RewriteAnswerResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)
    message = serializers.CharField(read_only=True)
    answer = serializers.CharField(read_only=True)
    sources = serializers.ListField(child=serializers.CharField(), read_only=True)
    suggestions = serializers.ListField(child=serializers.CharField(), read_only=True)
    chat_history = MessageSerializer(many=True, read_only=True)
    deep_research_fallback = serializers.BooleanField(read_only=True)


class ClickSuggestionRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    suggestion = serializers.CharField(min_length=1)


class ClickSuggestionResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    suggestion = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)


# ======================================================
# 👍 FEEDBACK
# ======================================================

class FeedbackSubmitRequestSerializer(serializers.Serializer):
    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)
    feedback_type = serializers.ChoiceField(
        choices=["Up", "Down"],
        required=True,
        error_messages={
            "invalid_choice": 'Feedback type must be either "Up" or "Down"'
        }
    )
    feedback_text = serializers.CharField(
        required=False, allow_blank=True, default=""
    )


class FeedbackSubmitResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    message = serializers.CharField(read_only=True)


# ======================================================
# 🎙️ VOICE / SPEECH
# ======================================================

class VoiceToTextResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    text = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)


class TextToSpeechRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    text = serializers.CharField(required=True, allow_blank=False)


class TextToSpeechResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    email = serializers.EmailField(read_only=True)  # ✅ ADDED
    audio = serializers.CharField(required=False, read_only=True)
    message = serializers.CharField(required=False, read_only=True)


# ======================================================
# 🚪 LOGOUT & HEALTH
# ======================================================

class LogoutResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    message = serializers.CharField(read_only=True)

class LogoutRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)


class HealthCheckResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(read_only=True)
    status = serializers.CharField(read_only=True)
    rag_initialized = serializers.BooleanField(read_only=True)


class UserInfoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    user_type = serializers.ChoiceField(choices=['business', 'guest', 'none'])
    email = serializers.EmailField(allow_null=True)
    name = serializers.CharField(allow_null=True, required=False)
    country = serializers.CharField(allow_null=True, required=False)
    sector = serializers.CharField(allow_null=True, required=False)
    language = serializers.CharField(allow_null=True, required=False)
    message = serializers.CharField(required=False)  # For error messages

class UploadPDFRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    sub_category = serializers.CharField(max_length=255)
    country = serializers.CharField()   # ✅ Add this
    pdf_file = serializers.FileField()
 
    def validate_pdf_file(self, value):
        if not value.name.endswith(".pdf"):
            raise serializers.ValidationError("Only PDF files are allowed")
        return value

class DisplayRulesRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)
    sub_category = serializers.CharField(max_length=255)
    user_country = serializers.CharField()


class NewChatRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(allow_null=True)



class RewriteRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    session_id = serializers.CharField()
    question = serializers.CharField()

class FeedbackSubmitRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)   # ✅ NEW
    session_id = serializers.CharField(required=True)  # ✅ NEW

    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)

    feedback_type = serializers.ChoiceField(
        choices=["Up", "Down"],
        required=True
    )

    feedback_text = serializers.CharField(
        required=False,
        allow_blank=True,
        default=""
    )



from rest_framework import serializers
from .models import Resource

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "resource_name", "rulebook_url", "created_on"]



class ComplianceStoreSerializer(serializers.Serializer):
    email = serializers.EmailField()
    sub_category = serializers.CharField(max_length=255)
    user_country = serializers.CharField(max_length=100)
    compliance_completed = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=True
    )

class MonthlyCountSerializer(serializers.Serializer):
    month = serializers.CharField()
    count = serializers.FloatField()
    


class StatisticsResponseSerializer(serializers.Serializer):
    subcategory = serializers.CharField()
    selected_users = serializers.IntegerField()
    other_users = serializers.IntegerField()
    other_percentage = serializers.FloatField()

    monthly_counts = MonthlyCountSerializer(many=True)


class CountryListResponseSerializer(serializers.Serializer):
    countries = serializers.ListField(
        child=serializers.CharField(),
        help_text="Available countries for compliance comparison dropdown"
    )

#class ComplianceCompareRequestSerializer(serializers.Serializer):
#    country1 = serializers.CharField(required=True)
#    country2 = serializers.CharField(required=True, allow_blank=True)
#    country3 = serializers.CharField(required=False, allow_blank=True)
#
#    def validate(self, data):
#        selected = [c for c in [data.get("country1"), data.get("country2"), data.get("country3")] if c]
#
#        # ✅ Prevent duplicates
#        if len(selected) != len(set(selected)):
#            raise serializers.ValidationError("Duplicate countries not allowed")
#
#        return data


class ComplianceCompareResponseSerializer(serializers.Serializer):
    selected_countries = serializers.ListField(
        child=serializers.CharField()
    )

    comparison_result = serializers.DictField(
        child=serializers.CharField(),
        help_text="Extracted compliance comparison sections from markdown file"
    )

from rest_framework import serializers

# FAQ Serializers
class FAQRequestSerializer(serializers.Serializer):
    country = serializers.ChoiceField(
        choices=["India", "US", "UAE", "China"],
        required=True,
        help_text="Country for which to retrieve FAQs"
    )
    sector = serializers.ChoiceField(
        choices=["Banking", "Finance", "Healthcare", "Environment","Shariat", "Ancillary Service Providers","Banking and Fintech", "Cryptocurrency and Blockchain related Services", "Financial Advisory Services", "Fund Management & Custodian", "Insurtech", "Investment and wealth management platforms", "Lending platforms", "Payment service providers", "Regtech"],
        required=True,
        help_text="Sector for which to retrieve FAQs"
    )

class FAQResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    country = serializers.CharField()
    sector = serializers.CharField()
    faqs = serializers.ListField(
        child=serializers.CharField(),
        help_text="List of frequently asked questions"
    )
    message = serializers.CharField(required=False)



#class ComplianceCompareRequestSerializer(serializers.Serializer):
#    category = serializers.CharField()
#    country1 = serializers.CharField()
#    country2 = serializers.CharField(required=False)
#    country3 = serializers.CharField(required=False)

class ComplianceCompareRequestSerializer(serializers.Serializer):
    category = serializers.CharField()
    country1 = serializers.CharField(required=True)
    country2 = serializers.CharField(required=False, allow_blank=True)
    country3 = serializers.CharField(required=False, allow_blank=True)

    def validate(self, data):
        selected = [c for c in [data.get("country1"), data.get("country2"), data.get("country3")] if c]

        # ✅ Prevent duplicates
        if len(selected) != len(set(selected)):
            raise serializers.ValidationError("Duplicate countries not allowed")

        return data

class RegulatoryRegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)

    country_code = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    user_country = serializers.CharField(required=True)
    sub_category = serializers.CharField(required=True)

class CountryCodesResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    codes = serializers.ListField(
        child=serializers.CharField()
    )



# Add to serializers.py

from rest_framework import serializers

class RulesChatRequestSerializer(serializers.Serializer):
    """
    Request serializer for rules_chat endpoint
    """
    language = serializers.CharField(
        required=True,
        help_text="Language for response (e.g., 'English', 'Hindi', 'Arabic')"
    )
    question = serializers.CharField(
        required=True,
        help_text="Natural language question about compliance rules"
    )
    email = serializers.EmailField(
        required=True,
        help_text="User's email address"
    )
    sub_category = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Business sub-category (e.g., 'Banking and Fintech')"
    )
    user_country = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="User's country (e.g., 'India', 'UAE', 'USA')"
    )


class RuleDataSerializer(serializers.Serializer):
    """
    Serializer for individual rule data
    """
    id = serializers.IntegerField(required=False)
    user_email = serializers.EmailField(required=False)
    sub_category = serializers.CharField(required=False)
    user_country = serializers.CharField(required=False)
    rule_id = serializers.CharField(required=False)
    rule_text = serializers.CharField(required=False)
    completed = serializers.BooleanField(required=False)
    last_updated = serializers.CharField(required=False)


class RulesChatResponseSerializer(serializers.Serializer):
    """
    Response serializer for rules_chat endpoint
    """
    success = serializers.BooleanField()
    email = serializers.EmailField(required=False)
    question = serializers.CharField(required=False)
    language = serializers.CharField(required=False)
    response = serializers.CharField(
        required=False,
        help_text="AI-generated human-readable response"
    )
    raw_data = serializers.ListField(
        child=RuleDataSerializer(),
        required=False,
        help_text="Structured database results"
    )
    total_records = serializers.IntegerField(
        required=False,
        help_text="Number of records returned"
    )
    query_executed = serializers.CharField(
        required=False,
        help_text="SQL query that was executed"
    )
    message = serializers.CharField(
        required=False,
        help_text="Error or info message"
    )
    error = serializers.CharField(
        required=False,
        help_text="Error details if request failed"
    )    

class ComplianceBotRequestSerializer(serializers.Serializer):
    #language = serializers.CharField()
    question = serializers.CharField()


class ComplianceBotResponseSerializer(serializers.Serializer):
    response = serializers.CharField()

class ChatRegulatorRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    session_id = serializers.CharField(required=True)
    question = serializers.CharField(required=True)

    enhance_mode = serializers.BooleanField(default=False)
    deep_research_mode = serializers.BooleanField(default=False)
    rag_mode = serializers.BooleanField(default=False)

class ChatRegulatorResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    email = serializers.EmailField()
    session_id = serializers.CharField()

    answer = serializers.CharField()
    mode = serializers.CharField()

    is_cached = serializers.BooleanField(required=False)

    sources = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=[]
    )

    deep_research_used = serializers.BooleanField(
        required=False,
        default=False
    )

    suggestions = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=[]
    )


class RegulatorChatRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    session_id = serializers.CharField(required=True)
    question = serializers.CharField(required=True)
    enhance_mode = serializers.BooleanField(default=False)
    deep_research_mode = serializers.BooleanField(default=False)
    query_mode = serializers.BooleanField(default=False)

