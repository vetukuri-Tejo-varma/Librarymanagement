from django.db import models

# Create your models here.
from django.db import models

class Course(models.Model):
    course_name=models.CharField(max_length=50)
    def __str__(self):
        return f"{self.course_name}"

class Student(models.Model):
    student_name = models.CharField(max_length=50)
    student_phone = models.BigIntegerField()
    student_password = models.CharField(max_length=50)
    student_semester = models.IntegerField()
    student_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.student_name}"


class Book(models.Model):
    book_name = models.CharField(max_length=50)
    author_name = models.CharField(max_length=50)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.book_name}"


class Issue_book(models.Model):
    student_name=models.ForeignKey(Student, on_delete=models.CASCADE)
    book_name=models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date=models.DateField()
    end_date=models.DateField()
