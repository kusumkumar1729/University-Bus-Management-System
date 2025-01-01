from django.contrib import admin
from .models import BusInfo,Note,BusApplication,BusVacancy
from .models import Student, StudentLogin,Payment
from .forms import BusVacancyForm
from .models import BusNames, Feedback


# Register your models here.

admin.site.register(BusInfo)
admin.site.register(Note)
# Register the model
admin.site.register(BusApplication)

class BusApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'student_id', 'contact_number', 'email', 'route', 'bus_stop', 'Section']



admin.site.register(Student)
admin.site.register(StudentLogin)


@admin.register(BusVacancy)
class BusVacancyAdmin(admin.ModelAdmin):
    form = BusVacancyForm  # Use your custom form, if applicable
    list_display = ['bus_name', 'total_seats', 'occupied_seats']  # Add other fields as needed





admin.site.register(BusNames)
admin.site.register(Feedback)