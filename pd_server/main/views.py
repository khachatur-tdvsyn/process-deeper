from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets

from .models import Computer, ProcessStat, ComputerStat, Process
from .serializers import (
    GroupSerializer, 
    UserSerializer, 
    ComputerSerializer, 
    StatSerializer, 
    ProcessStatSerializer,
    ProcessSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer

class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all().order_by('hostname')
    serializer_class = ComputerSerializer

class ComputerStatViewSet(viewsets.ModelViewSet):
    queryset = ComputerStat.objects.all().order_by('record_time')
    serializer_class = StatSerializer

class ProcessStatViewSet(viewsets.ModelViewSet):
    queryset = ProcessStat.objects.all().order_by('record_time')
    serializer_class = ProcessStatSerializer

class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all().order_by('id')
    serializer_class = ProcessSerializer