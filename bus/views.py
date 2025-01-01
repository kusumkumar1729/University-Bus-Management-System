from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from .models import BusInfo,Note,BusApplication,BusVacancy,Student, StudentLogin
from .forms import BusApplicationForm,StudentLoginForm,FeedbackForm
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout
import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
import pandas as pd
import os
from django.contrib import messages





# Create your views here.

def index(request):
    return render(request,'index.html')



def routes(request):
    buses = BusInfo.objects.all()  # Fetch all buses from the database
    image = Note.objects.all()
    return render(request, 'routes.html', {'buses': buses , 'images' : image })



def login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            student_id = form.cleaned_data['student_id']
            password = form.cleaned_data['password']
            
            try:
                # Fetch the student login record
                student_login = StudentLogin.objects.get(student__student_id=student_id, password=password)
                
                # Store the login status in the session
                request.session['student_id'] = student_login.student.student_id
                
                # Redirect to the student's page
                return redirect('studentPage', student_id=student_login.student.student_id)
            except StudentLogin.DoesNotExist:
                # If login details are invalid, return an error message
                form.add_error(None, 'Invalid Student ID or Password.')
    else:
        form = StudentLoginForm()
    
    return render(request, 'login.html', {'form': form})




def apply(request):
    submitted = False
    if request.method == 'POST':
        form = BusApplicationForm(request.POST)
        if form.is_valid():
            application = form.save()  # Save the form data to the database

            # Update bus vacancy after application is submitted
            try:
                # Find the bus based on the selected route
                bus_vacancy = get_object_or_404(BusVacancy, bus_name=application.route)

                # Check if there are remaining seats
                if bus_vacancy.occupied_seats < bus_vacancy.total_seats:
                    bus_vacancy.occupied_seats += 1
                    bus_vacancy.save() #save to the database
                    print(f"Bus vacancy updated: {bus_vacancy.bus_name} now has {bus_vacancy.occupied_seats} occupied seats.")  # Debugging line
                else:
                    print(f"Bus {bus_vacancy.bus_name} is fully booked.")  # Debugging line
                    # You can also add a user notification or error handling if needed
            except Exception as e:
                print(f"Error updating bus vacancy: {e}")  # Debugging line

            # Sending confirmation email to the user
            user_email_subject = "Bus Application Submitted"
            user_email_message = f"""Dear {application.full_name},

                We are pleased to inform you that your application for the MVGR College bus service has been successfully received and processed. We appreciate your decision to utilize our college's transportation services and are delighted to confirm the following details regarding your submission:

                Bus Name: {application.route}
                Designated Bus Stop: {application.bus_stop}

                To ensure a smooth and comfortable experience, we encourage you to visit the MVGR College Transport In-Charge at your earliest convenience. They will provide you with detailed information about bus schedules, routes, and any additional guidance you may need regarding the transportation services.

                Our team is committed to offering a reliable and secure commuting experience for all our students. Should you have any questions or require further assistance, please do not hesitate to reach out to us or contact the transport in-charge directly. We are here to support you throughout your time at MVGR College.

                Thank you for choosing our transportation services. We look forward to providing you with a convenient and pleasant commute.

                Warm regards,
                The MVGR College Transport Management Team
                """
            user_email = application.email
            send_mail(
                user_email_subject,
                user_email_message,
                settings.DEFAULT_FROM_EMAIL,
                [user_email],  # Recipient email
                fail_silently=False,
            )

            # Sending notification email to the admin
            admin_email_subject = "New Bus Application Received"
            admin_email_message = f"A new bus application has been submitted by {application.full_name} (Student ID: {application.student_id}).\n\nContact details:\nPhone: {application.contact_number}\nEmail: {application.email}\nRoute: {application.route}\nBus stop: {application.bus_stop}\nSection: {application.section}\n\nPlease review the application in the admin panel."
            admin_email = 'kusumakumar233@gmail.com'  # Admin email address
            
            send_mail(
                admin_email_subject,
                admin_email_message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],  # Admin email
                fail_silently=False,
            )

            print("Emails sent successfully.")  # Debugging line

            return HttpResponseRedirect('/apply?submitted=True')  # Redirect after successful submission
        else:
            print(form.errors)  # Print form errors for debugging
    else:
        form = BusApplicationForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'apply.html', {'form': form, 'submitted': submitted})




def vacancy(request):
    vacancies = BusVacancy.objects.all()  # You can filter this as needed
    # Pass the vacancies to the template
    return render(request, 'vacancy.html', {'vacancies': vacancies})





def studentPage(request, student_id):
    # Check if the student is logged in
    if 'student_id' not in request.session or request.session['student_id'] != student_id:
        # If not logged in, redirect to the login page
        return redirect('login')

    # Fetch the student record
    student = get_object_or_404(Student, student_id=student_id)
    
    # Get fee details using the student's method
    fees_details = student.get_fees_details()  # Ensure this method returns the correct fee data

    # Render the student page with the student info and fee details
    return render(request, 'studentPage.html', {'student': student, 'fees_details': fees_details})


def contact(request):
    return render(request, 'contact.html')





def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout




def withdrawl(request):
   return render(request, 'withdrawl.html')





stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request, student_id):
    student = Student.objects.get(student_id=student_id)
    total_balance = student.balance_amount().get('total_balance')

    if total_balance <= 0:
        return HttpResponse("No outstanding balance to pay.", status=400)

    amount_in_cents = int(total_balance * 100)  # Convert amount to cents for Stripe

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': f"Transport Fee Balance - {student.full_name}"},
                    'unit_amount': amount_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success', args=[student.student_id])) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('payment_failure')),
        )
    except Exception as e:
        return HttpResponse(f"Error creating checkout session: {str(e)}", status=500)

    return redirect(checkout_session.url, code=303)

def payment_success(request, student_id):
    session_id = request.GET.get('session_id')  # Get the session ID from the URL

    if session_id:
        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            payment_intent_id = checkout_session.payment_intent
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            student = Student.objects.get(student_id=student_id)

            Payment.objects.create(
                student=student,
                amount=payment_intent.amount_received / 100,  # Convert from cents
                transaction_id=payment_intent.id,
                status='success',
                payment_method=payment_intent.payment_method_types[0]
            )
            return render(request, 'payment_success.html', {'amount': payment_intent.amount_received / 100})

        except Exception as e:
            return HttpResponse(f"Error verifying payment: {str(e)}", status=400)

    return HttpResponse("Payment verification failed", status=400)

def payment_failure(request):
    return render(request, 'payment_failure.html')



def busInfo(request):
    return render(request, 'BusInfo.html')

    





def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            user_email = feedback.email
            # Send confirmation email to the user
            send_mail(
                'Feedback Submitted Successfully',
                'Thank you for your feedback!',
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )


            admin_email = 'kusumakumar233@gmail.com'  # Admin email address
            admin_email_subject = "New Bus FeedBack Received"
            admin_email_message = f"A new bus feedback has been submitted on {feedback.bus} (Student ID: {feedback.student_id}).\n\nEmail: {feedback.email}\nSection: {feedback.section}\n\nPlease review the Feedback in the admin panel."
            send_mail(
                admin_email_subject,
                admin_email_message,
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],  # Admin email
                fail_silently=False,
            )

            messages.success(request, 'Your feedback has been submitted successfully!')
            return redirect('Remarks')
    else:
        form = FeedbackForm()
    return render(request, 'remarks.html', {'form': form})


