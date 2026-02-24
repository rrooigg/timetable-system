from django.shortcuts import render
from . models import *
from datetime import datetime, timedelta

#For downloading the timetable
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import get_template

#Get the current date
today = datetime.now()
#Calculate the date of Monday and Friday of the current week
monday = today - timedelta(days=today.weekday())
friday = monday + timedelta(days=4)
#Get the current year
current_year = today.year
#Format the dates
monday_formatted = monday.strftime('%Y-%m-%d')
friday_formatted = friday.strftime('%Y-%m-%d')
#Define the sequence 
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

# Create your views here.
def index(request):
  #Fetch distinct programmes, semesters and years of study from TimetableMain model
  programmes = TimeTableMain.objects.values_list('Programme', flat=True).distinct()
  semesters = TimeTableMain.objects.values_list('Semester', flat=True).distinct()
  years_of_study = TimeTableMain.objects.values_list('YearOfStudy', flat=True).distinct()

  #Fetch selected Programme and it's Department when a POST request is made
  if request.method == 'POST':
    programme = request.POST.get('programme')
    semester = request.POST.get('semester')
    year_of_study = request.POST.get('year_of_study')

    #Fetch the selected Programme and it's Department from TimetableMain model
    timetable_main_entry = TimeTableMain.objects.filter(Programme=programme).first()
    if timetable_main_entry:
      selected_programme = timetable_main_entry.Programme
      department = timetable_main_entry.Department
    else:
      selected_programme = None
      department = None

    #Fetch timetable entries for the selected programme, semester and year of study
    timetable_entries = Timetable.objects.filter(programme__Programme=programme,
     programme__Semester=semester,
     programme__YearOfStudy=year_of_study
    ).order_by('TimeStart')
    #Extract unique days from the fetched timetable entries
    days = set(entry.Day for entry in timetable_entries)
    timetable_data = {}
    for day in day_order:
      #Find all entries for this specific day
      day_entries = [entry for entry in timetable_entries if entry.Day == day]

      # Only add the day to the dictionary if there are classes on that day
      if day_entries:
        #We sort by TimeStart so 8:00 AM appears before 2:00 PM
        timetable_data[day] = sorted(day_entries, key=lambda x: x.TimeStart)       

    #Initial rendering of the page without POST data
    context = {
      'programmes': programmes,
      'semesters': semesters,
      'years_of_study': years_of_study,
      'timetable_data': timetable_data,
      'selected_programme': selected_programme,
      'department': department,
      'semester': semester,
      'year_of_study': year_of_study,
      'monday': monday_formatted,
      'friday': friday_formatted,
      'current_year': current_year,

    }
    return render(request, 'index.html', context)
  
  context = {
    'programmes': programmes,
    'semesters': semesters,
    'years_of_study': years_of_study,
    'selected_programme': None,
    'department': None,
    'monday': monday_formatted,
    'friday': friday_formatted,
    'current_year': current_year,

  }

  return render(request, 'index.html', context)

def suppirt(request):
  return render(request, 'support.html')

#To download the timetable to a pdf
def export_timetable_pdf(request):
    # Get the same data used for the table
    programme = request.GET.get('programme')
    semester = request.GET.get('semester')
    year = request.GET.get('year_of_study')

    # Re-run your filter logic
    timetable_entries = Timetable.objects.filter(
        programme__Programme=programme,
        programme__Semester=semester,
        programme__YearOfStudy=year
    ).select_related('courseName', 'venue').order_by('TimeStart')
    
    #Define correct order here
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    #Build the ordered dictionary
    timetable_data = {}
    for day in day_order:
      day_entries = [entry for entry in timetable_entries if entry.Day == day]
      if day_entries:
        timetable_data[day] = day_entries

    context = {
        'timetable_data': timetable_data,
        'selected_programme': programme,
        'current_year': datetime.now().year,
    }

    # Render the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Timetable_{programme}.pdf"'
    
    template = get_template('timetable_pdf_template.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response