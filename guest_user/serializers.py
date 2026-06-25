from rest_framework import serializers
from django.conf import settings


class UserTypeResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    user_type = serializers.ChoiceField(choices=['guest', 'authenticated', 'none'])
    email = serializers.EmailField(required=False)
    name = serializers.CharField(required=False)
    settings = serializers.DictField(required=False)

class ValidateEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UsageLimitQuerySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class SaveSettingsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    country = serializers.CharField(required=True)
    sector = serializers.CharField(required=True)

    def validate_country(self, value):
        if value not in settings.COUNTRIES:
            raise serializers.ValidationError("Invalid country")
        return value

    def validate_sector(self, value):
        if value not in settings.SECTORS:
            raise serializers.ValidationError("Invalid sector")
        return value


class SendMessageSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    question = serializers.CharField(required=True)
    

    def validate_country(self, value):
        if value not in settings.COUNTRIES:
            raise serializers.ValidationError("Invalid country")
        return value

    def validate_sector(self, value):
        if value not in settings.SECTORS:
            raise serializers.ValidationError("Invalid sector")
        return value


class LoginRedirectSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
class ConfigResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    countries = serializers.ListField(child=serializers.CharField())
    sectors = serializers.ListField(child=serializers.CharField())
    max_questions = serializers.IntegerField()
    cooldown_hours = serializers.FloatField()


class FeatureSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class FeaturesResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    features = FeatureSerializer(many=True)

from rest_framework import serializers

class UserInfoResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    user_type = serializers.ChoiceField(choices=['authenticated', 'guest', 'none'])
    email = serializers.EmailField(allow_null=True)
    name = serializers.CharField(allow_null=True, required=False)
    country = serializers.CharField(allow_null=True, required=False)
    sector = serializers.CharField(allow_null=True, required=False)
    language = serializers.CharField(allow_null=True, required=False)
    message = serializers.CharField(required=False)  # For error messages  