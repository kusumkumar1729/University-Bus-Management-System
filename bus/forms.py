from django import forms
from .models import BusApplication,BusVacancy
from .models import StudentLogin
from .models import Feedback, BusNames



class BusApplicationForm(forms.ModelForm):
    class Meta:
        model = BusApplication
        fields = ['full_name', 'student_id', 'contact_number', 'email', 'route', 'bus_stop', 'section']
    
    def clean(self):
        cleaned_data = super().clean()

        

class BusVacancyForm(forms.ModelForm):
    class Meta:
        model = BusVacancy
        fields = ['bus_name', 'total_seats', 'occupied_seats']  # List the fields you want in the form



class StudentLoginForm(forms.Form):
    student_id = forms.CharField(max_length=20, label="Student ID")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")





class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['bus', 'student_id', 'section', 'Buscondition', 'email', 'driver_performance']
