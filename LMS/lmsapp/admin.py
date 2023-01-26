from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from lmsapp.models import Course, Student, Issue_book, Book

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Book)
admin.site.register(Issue_book)