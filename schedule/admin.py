from django.contrib import admin
from schedule.models import Subject, SubjectRating, Profile, UserSubject
# Register your models here.

admin.site.register(Subject)
admin.site.register(SubjectRating)
admin.site.register(Profile)
admin.site.register(UserSubject)
