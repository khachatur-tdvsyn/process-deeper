from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RecordableModel(models.Model):
    record_time = models.DateTimeField(auto_now_add=True, unique=True)
    record_time_timestamp = models.BigIntegerField(unique=True, primary_key=True)

    class Meta:
        abstract = True

# Create your models here.
class Computer(models.Model):
    os = models.CharField(max_length=255)
    os_version = models.CharField(max_length=255)
    platform = models.CharField(max_length=512)
    architecture = models.CharField(max_length=512)
    hostname = models.CharField(max_length=512, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    cpu_brand = models.CharField(max_length=255)
    cpu_cores_physical = models.PositiveIntegerField(default=0)
    cpu_cores_logical = models.PositiveIntegerField(default=0)
    cpu_frequency_mhz = models.FloatField(default=0)

    ram= models.CharField(max_length=512)
    storage= models.CharField(max_length=512)

    network_interfaces= models.TextField()
    gpu_name = models.CharField(max_length=512, null=True, blank=True)
    gpu_memory = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.hostname} | {self.ip_address}'

class OS(models.IntegerChoices):
    UNIX = 0, "UNIX"
    LINUX = 1, "Linux"
    WINDOWS = 2, "Windows"
    MAC_OS = 3, "Mac OS"


class Process(models.Model):
    name = models.CharField(max_length=255)
    os = models.IntegerField(choices=OS, default=OS.UNIX)
    description = models.TextField(null=True, blank=True)
    safety = models.FloatField(
        default=1, 
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1)
        ]
    )
    exe = models.CharField(max_length=255)

class Stat(RecordableModel):
    cpu_load = models.FloatField(default=0, help_text="Load in percents")
    ram_load = models.FloatField(default=0, help_text="Load in bytes")
    network_load = models.FloatField(default=0, help_text="Load in bytes")
    gpu_load = models.FloatField(default=0, help_text="Load in bytes", null=True, blank=True)

    class Meta:
        abstract = True

class ComputerStat(Stat):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, null=True, blank=True)

class ProcessStat(Stat):
    pid = models.IntegerField()
    exe = models.CharField(max_length=512, null=True, blank=True)
    name = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=512, null=True, blank=True)
    cmdline = models.TextField(max_length=512, null=True, blank=True)