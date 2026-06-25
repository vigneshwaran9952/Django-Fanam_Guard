from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user


'''class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    # ✅ Add these 2 fields
    country = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']'''

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    # ✅ Add user_type Field
    user_type = models.CharField(
    max_length=20,
    default="business"
)

    
    # ✅ New Fields
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # 🔄 Renamed fields
    user_country = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']



from django.utils.timezone import now

class UserSettings(models.Model):
    user_email = models.EmailField(unique=True)
    country = models.CharField(max_length=100)
    sector = models.CharField(max_length=100)
    language = models.CharField(max_length=100)

    created_at = models.DateTimeField(default=now)  # ✅ Fix
    updated_at = models.DateTimeField(default=now)  # ✅ Fix

    class Meta:
        db_table = "bussiness_user_usersettings"




class ChatSession(models.Model):
    user_email = models.CharField(max_length=255)
    session_id = models.CharField(max_length=255, unique=True)
    chat_history = models.TextField()
    stm_context = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255, default="New Chat")


class Feedback(models.Model):
    user_email = models.EmailField()
    
    session_id = models.CharField(max_length=255, null=True, blank=True)  # ✅ ADD THIS

    question = models.TextField()
    answer = models.TextField()

    feedback_type = models.CharField(max_length=10)
    feedback_text = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)



class Resource(models.Model):
    resource_name = models.CharField(max_length=255)
    rulebook_url = models.URLField()
    created_on = models.DateTimeField()

    def __str__(self):
        return self.resource_name


class RegulatoryUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)

    user_type = models.CharField(
    max_length=20,
    default="regulator"
)


    # ✅ Same Fields as Normal User
    country_code = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    user_country = models.CharField(max_length=100, null=True, blank=True)
    sub_category = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "regulatory_user"


class ComplianceRuleStatus(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    user_email = models.EmailField()
    sub_category = models.CharField(max_length=255)
    user_country = models.CharField(max_length=100)

    rule_id = models.CharField(max_length=50)
    rule_text = models.TextField()

    completed = models.BooleanField(default=False)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user_email", "sub_category", "user_country", "rule_id")
        db_table = "compliance_rule_status"
