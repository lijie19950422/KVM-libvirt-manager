from django.db import models

# Create your models here.
class KVMUser(models.Model):
    username = models.TextField(max_length=64)
    passwd = models.TextField(max_length=64)

    def __str__(self):
        return self.username


class CMDB(models.Model):
    IP = models.CharField(primary_key=True, max_length=20)
    hostname = models.CharField(max_length=50)
    gateway = models.CharField(max_length=20)
    mac = models.CharField(max_length=30)
    distribution = models.CharField(max_length=20)
    distribution_version = models.CharField(max_length=20)
    architecture = models.CharField(max_length=20)
    kernel = models.CharField(max_length=30)
    processor = models.CharField(max_length=100)
    processor_cores = models.CharField(max_length=20)
    processor_count = models.CharField(max_length=20)

    def __str__(self):
        return self.IP
