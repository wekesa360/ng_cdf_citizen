from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from accounts.utils import get_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout
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
from .serializers import (
    NGCDFAdminSerializer,
    NGCDFProjectsSerializer,
    NGCDFSerializer,
    BursaryApplicationSerializer,
    BursarySerializer,
    PasswordChangesSerializer,
    UserProfileSerializer,
    LocationSerializer,
    CountySerializer,
    ApplicationDocumentSerializer,
    CitizenReportSerializer,
    ReportImageSerializer,
    UserRegisterSerializer,
    EmptySerializer,
    AuthUserLoginSerializer,
    AuthUserSerializer,
    ProjectImageSerializer,
 )

User = get_user_model()


class AuthViewset(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
    'login': AuthUserLoginSerializer,
    'register': UserRegisterSerializer,
    'change_password': PasswordChangesSerializer,
    'profile': UserProfileSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST',], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST',], detail=False)
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status.HTTP_204_NO_CONTENT)
    
    @action(methods=['GET', ], detail=False)
    def profile(self, request):
        query_Set = User.objects.get(email=request.user.email)
        serializer = self.get_serializer(data=query_Set, many=False)
        data = serializer.data
        print(request.data)
        return Response(data=data, status=status.HTTP_200_OK)
    
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured('serializer_classes should be a dict mapping')
        
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    

class NGCDFViewset(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,]
    serializer_class = EmptySerializer
    serializer_classes = {
        'ng_cdf': NGCDFSerializer,
        'ng_cdf_admin': NGCDFAdminSerializer,
        'ng_cdf_projects': NGCDFProjectsSerializer,
    }

    @action(methods=['POST', 'PUT'], detail=False, permission_classes=permission_classes)
    def ng_cdf(self, request):
        user = User.objects.get(email=request.user.email)
        try:
            ng_cdf_admin = NGCDFAdmin.objects.get(administrator=user.id)
            if request.method == 'POST':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            elif request.method == 'PUT':
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            ng_cdf_admin = None
            data = {'401_unauthorized':'user not allowed'}
            return Response(data=data, status=status.HTTP_401_UNAUTHORIZED)
        
    @action(methods=['GET'], detail=False, permission_classes=[AllowAny, ])
    def ng_cdf(self, request):
        ng_cdf = NGCDF.objects.all()
        serializer = self.get_serializer(ng_cdf)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    

    


    
