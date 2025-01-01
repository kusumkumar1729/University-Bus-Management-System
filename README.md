# University-Bus-Management-System
## College Transportation Management System

## Features
### Home Page
Displays the latest updates regarding bus routes and announcements.
Provides easy navigation to other sections of the system.

### Student Login
Secure login for students to manage their transportation applications and payments.

### Vacancies & Application Form
Students can view bus seat availability (vacancies).
Submit or withdraw transportation applications through an intuitive form.

### Remarks (Feedback)
Students can provide feedback or raise concerns about the transportation services.
Feedback is stored for future review and action.

### Contact Us
Users can easily reach out for assistance or inquiries through the contact page.
Includes email notifications for submitted queries.

### Email Notifications
Automatically sends emails for important events such as:
Successful application submissions.
Payment confirmations.
Feedback received acknowledgments.

## Installation Guide
### 1. Clone the Repository
```
git clone https://github.com/your-username/college-transportation-system.git
cd college-transportation-system 
```
### 2. Create a Virtual Environment
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```
Use the requirements.txt file to install all necessary dependencies:
pip install -r requirements.txt
```

### 4. Set Up the Database
Run migrations to set up the database:
```
python manage.py makemigrations
python manage.py migrate
```

### 5. Configure Environment Variables
``` Create a .env file in the root directory and include the following:  
SECRET_KEY=your_secret_key  
DEBUG=True  
STRIPE_TEST_PUBLIC_KEY=your_stripe_test_public_key  
STRIPE_TEST_SECRET_KEY=your_stripe_test_secret_key  
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  
EMAIL_HOST=smtp.gmail.com  
EMAIL_PORT=587  
EMAIL_USE_TLS=True  
EMAIL_HOST_USER=your_email@gmail.com  
EMAIL_HOST_PASSWORD=your_email_password  
```
### 6. Run the Development Server
```python manage.py runserver```

#### Access the application at http://127.0.0.1:8000.

``` ## Folder Structure
college-transportation-system/  
│  
├── bus/                    # Main app handling bus routes and student features  
│   ├── migrations/         # Database migrations  
│   ├── templates/          # HTML templates for the application  
│   ├── static/             # Static files (CSS, JavaScript, images)  
│   ├── views.py            # Views for handling requests   
│   ├── models.py           # Database models  
│   ├── urls.py             # URL routing for the app  
│   └── admin.py            # Admin panel configuration  
│
├── project1/               # Project settings  
│   ├── settings.py         # Django project settings  
│   ├── urls.py             # Root URL configuration  
│   ├── wsgi.py             # WSGI configuration for deployment  
│   └── asgi.py             # ASGI configuration  
│
├── requirements.txt        # Python dependencies  
├── manage.py               # Django project management script  
├── .env                    # Environment variables  
└── README.md               # Project documentation 

```

### Usage
#### Administrator
Log in to the admin panel at /admin to manage bus routes, fees, and feedback.
Approve or decline applications and monitor payment records.
#### Students
Log in to view and manage bus applications.
Submit transportation requests and make payments securely.

## Output Screenshots











