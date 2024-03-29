from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib import admin
#from import_export.admin import ImportExportActionModelAdmin
from django.utils import timezone
from datetime import timedelta
from constance import config

# Create your models here. Use set_password
EASY = "EA"
MEDIUM = "ME"
HARD = "HA"

CATEGORY_CHOICE = ((EASY, "Easy"), (MEDIUM, "Medium"), (HARD, "Hard"))
QUESTION_CATEGORY = (("web", "Web"), ("reversing", "Reversing"), ("steg", "Steganography"),("foren","Forensics"),("crypt","Cryptography"),("misc","Miscellaneous"))


class Team(AbstractUser):

    points = models.IntegerField(default=0)
    timeRequired = models.FloatField(default=0,verbose_name="Time required")
    lastSubmission = models.DateTimeField(default=timezone.localtime,verbose_name="Last submission")
    
    def convert(self):
        return f"{self.lastSubmission.day}-{self.lastSubmission.month}-{self.lastSubmission.year} {self.lastSubmission.hour}:{self.lastSubmission.minute}:{self.lastSubmission.second}"

    def __str__(self):
        return self.username


class TeamAdmin(admin.ModelAdmin):

    list_display = ("username", "timeRequired", "points","email")
    readonly_fields = ("password", "points", "timeRequired")
    search_fields = ["username", "timeRequired", "points"]


class Questions(models.Model):

    questionId = models.AutoField(primary_key=True,verbose_name = "ID")
    questionDescription = models.TextField(verbose_name = "Description")
    questionTitle = models.CharField(max_length=40, default="Lakshya",verbose_name = "Title")
    questionPoints = models.IntegerField(default=0,verbose_name = "Points")
    questionData = models.FileField(blank=True,verbose_name = "Data")
    questionFlag = models.CharField(max_length=50,
                                    default="lakshya_CTF{hack_me_now}")
    questionHint = models.TextField(default="Sample hint",verbose_name = "Hint")
    questionSolvers = models.IntegerField(default=0,verbose_name = "Solvers")
    questionType = models.CharField(max_length = 15,choices = QUESTION_CATEGORY, default = "web",verbose_name = "Category")

    easyRating = models.IntegerField(default = 0,verbose_name = "Easy raters")
    mediumRating = models.IntegerField(default = 0,verbose_name = "Medium raters")
    hardRating = models.IntegerField(default = 0,verbose_name = "Hard raters")


    def __str__(self):
        return self.questionDescription

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"


class Machines(models.Model):
    
    machineId = models.AutoField(primary_key=True,verbose_name = "ID")
    machineTitle = models.CharField(max_length=20, verbose_name = "Name")
    machineIp = models.CharField(max_length=20,verbose_name = "IP Address")
    machinePoints = models.IntegerField(default=0,verbose_name = "Points")
    machineSolvers = models.IntegerField(default = 0,verbose_name = "Solvers")
    enumeration = models.IntegerField(choices = zip(range(1,6), range(1,6)), blank=True,verbose_name = "Enumeration rating")
    ctf_like = models.IntegerField(choices = zip(range(1,6), range(1,6)),blank=True,verbose_name="CTF-Like rating")
    custom_exploitation = models.IntegerField(choices = zip(range(1,6), range(1,6)), blank=True,verbose_name = "Custom exploitation Rating")
    real_life = models.IntegerField(choices = zip(range(1,6), range(1,6)), blank=True,verbose_name = "Real-life rating")
    cve = models.IntegerField(choices = zip(range(1,6), range(1,6)), blank=True, verbose_name = "CVE rating")

    easyRating = models.IntegerField(default = 0,verbose_name = "Easy raters")
    mediumRating = models.IntegerField(default = 0,verbose_name = "Medium raters")
    hardRating = models.IntegerField(default = 0,verbose_name = "Hard raters")
    
    userFlag = models.CharField(max_length=50,default="lakshya_CTF{hack_me_now}")
    rootFlag = models.CharField(max_length=50,default="lakshya_CTF{hack_me_now}")

    def __str__(self):
        return self.machineTitle

    class Meta:
        verbose_name = "Machine"
        verbose_name_plural = "Machines"


class SolvedTimestamps(models.Model):

    username = models.ForeignKey(Team, on_delete=models.CASCADE)
    timestamp_record = models.DateTimeField(default=timezone.localtime)
    points = models.IntegerField(default=0)

    def convert(self):
        return f"{self.timestamp_record.year}-{self.timestamp_record.month}-{self.timestamp_record.day} {self.timestamp_record.hour}:{self.timestamp_record.minute}:{self.timestamp_record.second}"

class SolvedQuestions(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    user = models.ForeignKey(Team,on_delete=models.CASCADE)

class SolvedMachines(models.Model):
    machine = models.ForeignKey(Machines,on_delete=models.CASCADE)
    user = models.ForeignKey(Team,on_delete=models.CASCADE)
    root = models.BooleanField(default = False)

class TakenQuestionHint(models.Model):
    question = models.ForeignKey(Questions,on_delete=models.CASCADE)
    user = models.ForeignKey(Team,on_delete=models.CASCADE)
    hint = models.BooleanField(default = False)


class Events(models.Model):

    receiptid = models.CharField(db_column="ReceiptID",
                                 primary_key=True,
                                 max_length=100)  # Field name made lowercase.
    college = models.CharField(max_length=250)
    slot = models.CharField(max_length=20, blank=True, null=True)
    noofmem = models.IntegerField()
    domain = models.CharField(max_length=250)
    city = models.CharField(db_column="City",
                            max_length=100)  # Field name made lowercase.
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    date = models.CharField(db_column="Date",
                            max_length=30)  # Field name made lowercase.
    name1 = models.CharField(max_length=100)
    gender = models.CharField(db_column="Gender",
                              max_length=20)  # Field name made lowercase.
    email1 = models.CharField(max_length=100)
    phone1 = models.BigIntegerField()
    name2 = models.CharField(max_length=100)
    gender2 = models.CharField(db_column="Gender2",
                               max_length=20)  # Field name made lowercase.
    email2 = models.CharField(max_length=100)
    phone2 = models.BigIntegerField()
    name3 = models.CharField(max_length=100)
    gender3 = models.CharField(db_column="Gender3",
                               max_length=20)  # Field name made lowercase.
    email3 = models.CharField(max_length=100)
    phone3 = models.BigIntegerField()
    name4 = models.CharField(max_length=100)
    gender4 = models.CharField(db_column="Gender4",
                               max_length=20)  # Field name made lowercase.
    email4 = models.CharField(max_length=100)
    phone4 = models.BigIntegerField()
    name5 = models.CharField(max_length=100)
    gender5 = models.CharField(db_column="Gender5",
                               max_length=20)  # Field name made lowercase.
    email5 = models.CharField(max_length=100)
    phone5 = models.BigIntegerField()
    name6 = models.CharField(max_length=100)
    gender6 = models.CharField(db_column="Gender6",
                               max_length=10)  # Field name made lowercase.
    email6 = models.CharField(max_length=100)
    phone6 = models.BigIntegerField()

    def __str__(self):
        return self.receiptid

    class Meta:
        managed = False
        db_table = "events"
        verbose_name = "Event"
        verbose_name_plural = "Events"
