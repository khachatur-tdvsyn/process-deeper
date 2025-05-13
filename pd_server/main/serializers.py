from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Computer, ComputerStat, ProcessStat, Process


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class ComputerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'

class ProcessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

class StatSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ComputerStat
        fields = '__all__'
        read_only_fields = ['record_time', 'record_time_timestamp']


class ProcessStatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProcessStat
        fields = '__all__'
        read_only_fields = ['record_time', 'record_time_timestamp']