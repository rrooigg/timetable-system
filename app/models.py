from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
DAY_CHOICES = [
  ('Monday', 'Monday'), #first goes to DB, second is what the user sees
  ('Tuesday', 'Tuesday'),
  ('Wednesday', 'Wednesday'),
  ('Thursday', 'Thursday'),
  ('Friday', 'Friday'),
  ('Saturday', 'Saturday'),
]

#Department Model
class Department(models.Model):
  DepartmentName = models.CharField(max_length=255, primary_key=True)
  HeadOfDepartment = models.CharField(max_length=255)
  RegisteredDate = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = "Department"
    verbose_name_plural = "Departments"

  def __str__(self):
    return self.DepartmentName
  
#Instructor Model
class Instructor(AbstractUser): #AbstractUser gives ability to log in to django admin while models doesn't
  FirstName = models.CharField(max_length=255, null=True)
  MiddleName = models.CharField(max_length=255, null=True)
  LastName = models.CharField(max_length=255, null=True)
  Department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True) #deleting department deletes all instructors
  RegisteredDate = models.DateTimeField(auto_now_add=True)

  class Meta:
    verbose_name = "Instructor"
    verbose_name_plural = "Instructors"

  def __str__(self):
    return self.username #"borrowed" from built-in User Model, it's the login name for instructor

#TimeTable Main Model(what the student will input in form to get their timetable)
class TimeTableMain(models.Model):
  Programme = models.CharField(max_length=255, primary_key=True, editable=True)
  YearOfStudy = models.CharField(max_length=9)
  Semester = models.IntegerField()
  Department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
  RegisteredDate = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.Programme
  
#Course Name Model
class CourseName(models.Model):
  Course = models.CharField(max_length=255)
  CourseCode = models.CharField(max_length=100, primary_key=True)
  RegisteredDate = models.DateTimeField(auto_now_add=True)
  CourseDescription= models.CharField(max_length=200)

  class Meta:
    unique_together = (('Course', 'CourseCode')) #prevents duplicates i.e can't have the exact combination of these two fields. CS 101 can't be repeated twice

  def __str__(self):
    return self.Course
  
#Venue Model
class Venue(models.Model):
  Venue = models.CharField(max_length=50, primary_key=True)
  RegisteredDate = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.Venue
  
#TimeTable Model(generated)
class Timetable(models.Model):
  courseName = models.ForeignKey(CourseName, on_delete=models.CASCADE) #stores primary key from CourseName Model/table
  instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
  venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
  TimeStart = models.TimeField()
  TimeEnd = models.TimeField()
  Day = models.CharField(max_length=100, choices=DAY_CHOICES)
  programme = models.ForeignKey(TimeTableMain, on_delete=models.CASCADE)
  RegisteredDate = models.DateField(auto_now_add=True)
