from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django import forms
from django.utils.html import format_html

# Register your models here.

#Register Department
class DepartmentAdmin(admin.ModelAdmin):
  list_display = ("DepartmentName", "HeadOfDepartment","registered_date_badge")
  list_filter = ("HeadOfDepartment", "RegisteredDate")
  search_fields = ("DepartmentName", "HeadOfDepartment")
  date_hierarchy = "RegisteredDate"
  list_editable = ("HeadOfDepartment",) #, -> shows it's a tuple and not a string
  list_per_page=10
  list_max_show_all=10

  def registered_date_badge(self, obj):
    return format_html('<i class="text-info"></i>' '<span class="badge badge-dark p-1">{}</span>', obj.RegisteredDate.strftime('%d %b %Y'))
  registered_date_badge.short_description = "Registered Date"
admin.site.register(Department, DepartmentAdmin)

#Register Instructor
class InstructorAdmin(admin.ModelAdmin):
  list_display =("username", "FirstName", "LastName", "MiddleName", "email", "Department", "registered_date_badge")
  list_filter = ("Department", "RegisteredDate")
  search_fields = ("username", "email")
  list_per_page=10
  list_max_show_all=10
  list_editable = ("FirstName", "LastName", "MiddleName", "email", "Department",)
  fieldsets = (
    (None, {
      "fields": ("username", "password")
    }),
    ("Personal Info", {
      "fields": ("email", "FirstName", "LastName", "MiddleName")
    }),
    ("DepartmentInfo", {
      "fields": ("Department",)
    }),
    ("Permissions", {
      "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
    }),
    ("Important dates", {
      "fields": ("last_login", "date_joined")
    }),
  )
  
  def registered_date_badge(self, obj):
    return format_html('<i class="text-info"></i>' '<span class="badge badge-dark p-1">{}</span>', obj.RegisteredDate.strftime('%d %b %Y'))
  registered_date_badge.short_description = "Registered Date"
admin.site.register(Instructor, InstructorAdmin)

#Register TimetableMain
class TimeTableMainAdmin(admin.ModelAdmin):
  list_display =("YearOfStudy", "Programme", "Semester", "Department", "registered_date_badge")
  list_filter = ("YearOfStudy", "Semester", "Department", "RegisteredDate")
  search_fields = ("YearOfStudy", "Programme", "Semester")
  date_hierarchy= "RegisteredDate"
  list_per_page=10
  list_max_show_all=10
  list_editable=("Semester", "Department",)
  
  def registered_date_badge(self, obj):
    return format_html('<i class="text-info"></i>' '<span class="badge badge-dark p-1">{}</span>', obj.RegisteredDate.strftime('%d %b %Y'))
  registered_date_badge.short_description = "Registered Date"
admin.site.register(TimeTableMain, TimeTableMainAdmin)

#Time Picker
class TimePickerWidget(forms.TimeInput):
  template_name = "widgets/time_picker.html"

class TimeTableForm(forms.ModelForm):
  class Meta:
    model = Timetable
    fields = "__all__"
    widgets = {
      "TimeStart": TimePickerWidget(),
      "TimeEnd": TimePickerWidget(),
    }

#Register Timetable Admin
class TimeTableAdmin(admin.ModelAdmin):
  form = TimeTableForm
  list_display =("id", "Day", "courseName", "venue", "TimeStart", "TimeEnd", "programme", "registered_date_badge")
  list_filter = ("Day", "programme", "RegisteredDate")
  search_fields = ("courseName", "venue")
  date_hierarchy= "RegisteredDate"
  list_per_page=5
  list_max_show_all=5
  list_editable=("courseName", "Day", "venue", "programme",)
  
  def registered_date_badge(self, obj):
    return format_html('<i class="text-info"></i>' '<span class="badge badge-dark p-1">{}</span>', obj.RegisteredDate.strftime('%d %b %Y'))
  registered_date_badge.short_description = "Registered Date"
admin.site.register(Timetable, TimeTableAdmin)

#Register Course
@admin.register(CourseName)
class CourseNameAdmin(admin.ModelAdmin):
  list_display =("CourseCode", "CourseDescription", "Course")
  search_fields = ("Course", "CourseCode", "CourseDescription")
  list_per_page=10
  list_max_show_all=10
  list_editable=("Course", "CourseDescription",)

#Register Venue
admin.site.register(Venue)