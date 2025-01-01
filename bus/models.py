from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class BusInfo(models.Model):
    name = models.CharField(max_length=100)  # Bus name
    routes = models.TextField()  # List of stops
    morning_start_time = models.TimeField()  # Start time in the morning
    college_start_time = models.TimeField()  # Start time from the college
    description = models.TextField(blank=True, null=True)  # Optional description field for notes
    image = models.ImageField(upload_to='media',blank = True,null=True)  # Upload field for images

    def __str__(self):
        return self.name


class Note(models.Model):
    image = models.ImageField(upload_to='media',blank = True,null=True)  # Image field
    note = models.TextField(blank=True, null=True)  # Additional description or note

    def __str__(self):
        return f"Image {self.id}"



class BusApplication(models.Model):
    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    route = models.CharField(max_length=50)
    bus_stop = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.student_id



class BusVacancy(models.Model):
    bus_name = models.CharField(max_length=100)  # Name of the bus
    total_seats = models.IntegerField(default=50)  # Total seats in the bus
    occupied_seats = models.IntegerField(default=0)  # Occupied seats

    @property
    def remaining_seats(self):
        return self.total_seats - self.occupied_seats

    def __str__(self):
        return f"{self.bus_name} - Occupied: {self.occupied_seats}, Remaining: {self.remaining_seats}"




class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    year = models.IntegerField()
    image = models.ImageField(upload_to='media', blank=True, null=True)
    
    # Fee fields for each year
    first_year_fee = models.DecimalField(max_digits=10, decimal_places=2, default=35000)
    second_year_fee = models.DecimalField(max_digits=10, decimal_places=2, default=35000)
    third_year_fee = models.DecimalField(max_digits=10, decimal_places=2, default=35000)
    fourth_year_fee = models.DecimalField(max_digits=10, decimal_places=2, default=35000)  # Add fourth-year fee
     
    # Paid amount fields for each year
    paid_amount_first_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount_second_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount_third_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid_amount_fourth_year = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add paid amount for fourth year


    def get_transport_fee_for_year(self, year):

        """Return the transport fee for a specific year."""
        if year == 1:
            return self.first_year_fee
        elif year == 2:
            return self.second_year_fee
        elif year == 3:
            return self.third_year_fee
        elif year == 4:
            return self.fourth_year_fee
        return 0  # Default if year is not recognized

    def get_paid_amount_for_year(self, year):
        """Return the paid amount for a specific year."""
        if year == 1:
            return self.paid_amount_first_year
        elif year == 2:
            return self.paid_amount_second_year
        elif year == 3:
            return self.paid_amount_third_year
        elif year == 4:
            return self.paid_amount_fourth_year
        return 0  # Default if year is not recognized



    def balance_amount(self):

        """Calculate balance amounts for each year and return a dictionary with total balance."""
        total_balance = 0
        balances = {}

        for year in range(1, 5):  # Iterate through years 1 to 4
            transport_fee = self.get_transport_fee_for_year(year)
            paid_amount = self.get_paid_amount_for_year(year)
            balance = transport_fee - paid_amount

            balances[year] = {
                'year': year,
                'transport_fee': transport_fee,
                'paid_amount': paid_amount,
                'balance_amount': balance,
            }

            total_balance += balance  # Add to total balance

        # Return balances along with the total balance
        balances['total_balance'] = total_balance

        return balances 


    def balance_amount_per_year(self):
        """Calculate balance amounts for each year and return a dictionary."""
        balances = {}
        for year in range(1, 5):  # Iterate through years 1 to 4
            balances[year] = {
                'year': year,
                'transport_fee': self.get_transport_fee_for_year(year),
                'paid_amount': self.get_paid_amount_for_year(year),
                'balance_amount': self.get_transport_fee_for_year(year) - self.get_paid_amount_for_year(year),
            }

        return balances


  

    def get_fees_details(self):
        """Returns a dictionary with fees details for all years up to the student's current year."""
        fees = {}
        for year in range(1, self.year + 1):  # Only include years up to the student's current year
            fees[year] = {
                'year': year,
                'transport_fee': self.get_transport_fee_for_year(year),
                'paid_amount': self.get_paid_amount_for_year(year),
                'balance_amount': self.get_transport_fee_for_year(year) - self.get_paid_amount_for_year(year),
            }
        return fees

        

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"




class StudentLogin(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    password = models.CharField(max_length=50,default='webcap')  # This should be hashed for security

    def __str__(self):
        return self.student.student_id





class Payment(models.Model):
    student = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)  # e.g., 'success' or 'failed'
    payment_method = models.CharField(max_length=50)  # e.g., 'card', 'google_pay'
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.amount} ({self.transaction_id})"





class BusNames(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Feedback(models.Model):
    bus = models.ForeignKey(BusNames, on_delete=models.CASCADE)
    student_id = models.CharField()
    section = models.CharField()
    Buscondition = models.TextField()
    email = models.EmailField()
    driver_performance = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.bus.name} on {self.submitted_at}"
