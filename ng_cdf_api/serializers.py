from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager
from accounts.models import Location, County
from .utils import get_models_choices
from ng_cdf.models import (
    NGCDF,
    NGCDFAdmin,
    NGCDFProjects,
    Bursary,
    ProjectImage,
    BursaryApplication,
    ApplicationDocument,
    CitizenReport,
    ReportImage,
)

User = get_user_model()

class AuthUserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.Serializer):
    auth_token = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'bio', 'phone_number', 'avatar',]
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class UserProfileSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'password', 'phone_number']
    

class UserRegisterSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar', 'password', 'phone_number']
    
    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError('Email is already taken')
        return BaseUserManager.normalize_email(value)
    
    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class PasswordChangesSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password('value'):
            raise serializers.ValidationError('current password does not match')
        return value
       
    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

class CountySerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = County
        fields = ['county_name','county_code', 'logo']

class LocationSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = Location
        fields = ['county','constituency','constituency_code',]

class NGCDFSerializer():
    """
    
    """
    class Meta:
        model = NGCDF
        fields = ['ng_cdf_id', 'ng_cdf_name', 'location', 'created_at', 'updated_at']

class NGCDFProjectsSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        models = NGCDFProjects
        fields = ['ng_cdf', 'project_name', 'project_id', 'description', 'status', 'writeup_document', 'created_at', 'updated_at']

    def validate_status_type(self, value):
        status_choices = get_models_choices(NGCDFProjects.CHOICES_STATUS)
        if value not in status_choices:
            raise ValueError('Status not allowed')
        return value


class NGCDFAdminSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        models = NGCDFAdmin
        fields = ['administrator', 'ng_cdf', 'created_at', 'updated_at']

class BursarySerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    class Meta:
        model = Bursary
        fields = ['ng_cdf', 'bursary_id', 'bursary_type', 'bursary_name',
                  'deadline_of_application', 'description', 'created_at', 'updated_at']

class BursarySerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = NGCDFAdmin
        fields = ['administrator', 'ng_cdf', 'created_at', 'updated_at']


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = ApplicationDocument
        fields =['record_id', 'national_id', 'fathers_id', 'mothers_id',
                 'institution_transcript', 'calling_letter', 'fee_structure'
                 'created_at', 'updated_at']

class BursaryApplicationSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = BursaryApplication
        fields = ['applicant', 'bursary', 'date_of_birth', 'application_documents'
                  'institution_name', 'application_date', 'status', 'institution_location'
                  'application_uid', 'created_at', 'updated_at']
    
    def validate_status(self, value):
        status_choices = get_models_choices(BursaryApplication.CHOICES_STATUS)
        if value not in status_choices:
            raise ValueError('Status not allowed')
        return value

class CitizenReportSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = CitizenReport
        fields = ['citizen', 'project_name', 'report_uid', 'project_location', 'report_type'
                  'description', 'created_at', 'updated_at']
    
    def validate_type(self, value):
        type_choices = get_models_choices(CitizenReport.CHOICES_TYPE)
        if value not in type_choices:
            raise ValueError('Type not allowed')
        return value

class ReportImageSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = ReportImage
        fields = ['project', 'image', 'created_at', 'updated_at']


class ProjectImageSerializer(serializers.ModelSerializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """
    class Meta:
        model = ProjectImage
        fields = ['project', 'image', 'created_at', 'updated_at']
    
