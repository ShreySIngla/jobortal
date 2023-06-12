from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,generics,permissions,viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.viewsets import ModelViewSet
from knox.models import AuthToken
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.http import HttpResponse
import datetime
from rest_framework.decorators import api_view , permission_classes,action
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.contrib import messages

from django.shortcuts import render, redirect

from jobs.models import jobseeker,userdetails,AppliedJob,job,Contact,Subscription,blog

from django.http import HttpResponse
from django.contrib import messages


from jobs.serializers import jobseekerserializers
from django.contrib.auth import authenticate, login,logout
from django.core.paginator import Paginator
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render

from django.core.paginator import Paginator

def latest_blogs(request):
    # Retrieve all jobs from the database
    all_blogs = blog.objects.all()

    # Set the number of jobs to display per page
    blogs_per_page = 1

    # Create a paginator object
    paginator = Paginator(all_blogs, blogs_per_page)

    # Get the requested page number
    page_number = request.GET.get('page')

    # Get the jobs for the requested page
    latest_blogs = paginator.get_page(page_number)
    
    
    # Pass the latest jobs to the template for rendering
    return render(request, 'blog_list.html', {'latest_blogs': latest_blogs})



class PostDetail(generic.DetailView):
    model = blog
    template_name = 'blog.html'



def job_list(request):
  
    all_jobs = job.objects.all()

    jobs_per_page = 2

    paginator = Paginator(all_jobs, jobs_per_page)

    page_number = request.GET.get('page')

    job_list = paginator.get_page(page_number)

    return render(request, 'job-list.html', {'job_list': job_list})


def index(request):
    jobs = job.objects.all()
    blogs = blog.objects.all()
    context = {
        'jobs': jobs,
        'blogs':blogs,
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        if jobseeker.objects.filter(username=username).exists():
            User = authenticate(username=username, password=password)
            if User is not None:
                if User.role_id == 2:  
                    login(request, User)
                    return redirect('index')  
                else:
    
                    return render(request, 'login.html', {'error': 'You do not have permission to access this page...'})
            else:
                
                return render(request, 'login.html', {'error': 'Invalid Password...'})
        else:
             return render(request, 'login.html', {'error': 'You Are Not Registed Jobseeker...'})

    return render(request, 'login.html')


def registration_view(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        
        if password == confirm_password:
                secure_passward= make_password(request.POST['password'])
                
                if jobseeker.objects.filter(email=email):
                    error_message = "Username already exists."
                    return render(request, 'register.html', {'error': error_message})
                elif jobseeker.objects.filter(username=username):
                    error_message = "Email already exists."
                    return render(request, 'register.html', {'error': error_message})
                else:
                    User = jobseeker.objects.create(name=name,username=username, email=email, password=secure_passward ,role_id=2)
            
                    return redirect('login')  
       
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('index')  


@login_required(login_url='/login/')
def profile(request, *args, **kwargs):
    user = request.user

    if request.method == 'POST':
        age = request.POST.get('age')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        experience = request.POST.get('experience')
        address = request.POST.get('address')
        resume = request.FILES.get('resume')

        user_details = user.userdetails
        user_details.age = age
        user_details.dob = dob
        user_details.gender = gender
        user_details.experience = experience
        user_details.address = address

        if resume:
            user_details.resume = resume

        user_details.save()

        return redirect('profile')

    context = {
        'user': user,
    }

    
    return render(request, 'profile.html', context)




def search_list(request):
    keywords = request.GET.get('keywords', '')
    
    # posts = job.objects.filter(title__icontains=keywords)  
    
    posts = job.objects.filter(Q(title__icontains=keywords) |  Q(salary__icontains=keywords) |  Q(location__icontains=keywords) |  Q(company__icontains=keywords) )

    jobs_per_page = 3
    paginator = Paginator(posts, jobs_per_page)
    page_number = request.GET.get('page')
    searched_jobs = paginator.get_page(page_number)
    print(keywords)

    
    return render(request, 'search.html',{'search_list': searched_jobs,'keywords': keywords,})

class JobDetailView(LoginRequiredMixin, generic.DetailView):
    model = job
    template_name = 'job-detail.html'
    login_url = '/login/'  # Specify the login URL

    def post(self, request, *args, **kwargs):
        jobseeker = request.user
        job = self.get_object()

        if not jobseeker.is_authenticated:
            return redirect(self.login_url)

        if AppliedJob.objects.filter(job=job, jobseeker=jobseeker).exists():
            messages.success(request, 'Already applied for the job')
        else:
            AppliedJob.objects.create(job=job, jobseeker=jobseeker)
            messages.success(request, 'Applied for the job')

        context = {
            'job': job,
            'has_applied': AppliedJob.objects.filter(job=job, jobseeker=jobseeker).exists(),
        }
        return render(request, 'job-detail.html', context)



# class JobDetailView(LoginRequiredMixin, generic.DetailView):
#     model = job
#     template_name = 'job-detail.html'
#     login_url = '/login/'  # Specify the login URL

#     def post(self, request, *args, **kwargs):
#         jobseeker = request.user
#         job = self.get_object()

#         if not jobseeker.is_authenticated:
#             return redirect(self.login_url)

#         elif AppliedJob.objects.filter(job=job, jobseeker=jobseeker).exists():

#             messages.success(request, 'Already applied for the job')

#         else:
#             AppliedJob.objects.create(job=job, jobseeker=jobseeker)
#             messages.success(request, 'Applied for the job')

#         context = {
#             'job': job,
#             'has_applied': AppliedJob.objects.filter(job=job, jobseeker=jobseeker).exists(),
#         }
#         return render(request, 'job-detail.html', context)



class contact(generic.TemplateView):
    template_name = 'contact.html'

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        print(name,email,subject,message)

        Contact.objects.create(name=name  ,email=email ,  subject=subject , message=message)

        # send_mail(
        #     rev_subject,
        #     message,
        #     email,
        #     ['email'], 
        #     fail_silently=False,
        # )
                
        recipients = ['shreylearning@gmail.com']
        context ={

                'name':name,
                'subject': subject,
                'message': message,
                'sender': email,
                'recipients': recipients
            }
            
        email_html = render_to_string('email_template.html', context)
        send_mail(subject, message, email, recipients, html_message=email_html, fail_silently=False)


        messages.success(request, 'Your message has been sent successfully!')

        # Render a success message or redirect to a success page
        return render(request, 'contact.html',{'messages_contact': messages.get_messages(request)})
    


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        print(email)
        if not email:
            messages.error(request, 'Email cannot be blank.')
        else:
            existing_subscription = Subscription.objects.filter(email=email).exists()
            if Subscription.objects.filter(email=email).exists():
                messages.warning(request, 'Already subscribed to the newsletter.')
            else:
                subscription = Subscription(email=email)
                subscription.save()
                messages.success(request, 'Successfully subscribed to the newsletter.')

        # For example, you can display a success message
        

    referer = request.META.get('HTTP_REFERER',{'messages': messages.get_messages(request)})

    
    return redirect(referer)






def emp_registration(request):
    if request.method == 'POST':

        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Perform form validation (e.g., check for empty fields, password match, etc.)
        if password == confirm_password:
                secure_passward= make_password(request.POST['password'])
                # Check if username and email are unique
                if jobseeker.objects.filter(email=email):
                    error_message = "Username already exists."
                    return render(request, 'register.html', {'error': error_message})
                elif jobseeker.objects.filter(username=username):
                    error_message = "Email already exists."
                    return render(request, 'register.html', {'error': error_message})
                else:
                    User = jobseeker.objects.create(name=name,username=username, email=email, password=secure_passward ,role_id=3)
                # Perform additional registration logic (e.g., saving additional user information)
                    return redirect('login')  # Redirect to the login page after successful registration
       
        else:
            # Handle password mismatch
            return render(request, 'register.html', {'error': 'Passwords do not match'})

    return render(request, 'register.html')


def emp_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if jobseeker.objects.filter(username=username).exists():
            User = authenticate(username=username, password=password)
            if User is not None:
                if User.role_id == 3:  
                    login(request, User)
                    return redirect('emp_index')  
                else:

                    return render(request, 'emp_login.html', {'error': 'You do not have permission to access this page.'})
            else:
    
                return render(request, 'emp_login.html', {'error': 'Invalid Password'})
        else:
    
                return render(request, 'emp_login.html', {'error': 'You Are Not Registed Employer...'})
        

    return render(request, 'emp_login.html')

def emp_index(request):
    jobs = job.objects.all()
    context = {
        'jobs': jobs,
    }
    return render(request, 'emp_index.html', context)

@login_required
def post_job(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        img = request.FILES.get('img')  # Assuming the file input name is 'img'

        # Create the Job object
        Job = job(company=company, title=title, slug=slug, description=description,
                  salary=salary, location=location, img=img)

        # Save the job to the database
        Job.save()

        # return redirect('job_list')  # Redirect to the job list page after posting the job
        messages.success(request, 'Job Posted Successfully!')

    
    return render(request, 'post_job.html',{'messages_contact': messages.get_messages(request)})



def applied_candidates(request, *args, **kwargs):
    Job = job.objects.get(pk=kwargs['pk'])
    print(Job.id)
    # applied_jobs = AppliedJob.objects.filter(job=Job)
    # print(applied_jobs)

    if not jobseeker.is_authenticated:
        return redirect('/emp_login/')
    
    else:
        applied_jobs = AppliedJob.objects.filter(job=Job)
        for applied_job in applied_jobs:
            print(applied_job.jobseeker.name)

    return render(request, 'applied_candidates.html', {'job': Job, 'applied_jobs': applied_jobs})


# class JobDeleteView(LoginRequiredMixin, generic.DetailView):
#     model = job
#     template_name = 'job-detail.html'
#     login_url = '/emp_login/'  # Specify the login URL
    
def JobDeleteView(request, *args, **kwargs):
    jobseeker = request.user
    Job = job.objects.get(pk=kwargs['pk'])

    if not jobseeker.is_authenticated:
        return redirect('/emp_login/')
    else:
        Job.delete()
        messages.error(request, 'Job Deleted Successfully!')
    
    # Get the remaining jobs to display in the 'emp_index.html'
    remaining_jobs = job.objects.all()
    # return redirect('/emp_index/', {'messages_deleted': messages.get_messages(request), 'remaining_jobs': remaining_jobs})
    referer = request.META.get('HTTP_REFERER',{'messages_deleted':  'Job Deleted Successfully!','remaining_jobs': remaining_jobs})

    
    return redirect(referer)
        
def emp_job_list(request):
  
    all_jobs = job.objects.all()

    jobs_per_page = 2

    paginator = Paginator(all_jobs, jobs_per_page)

    page_number = request.GET.get('page')

    job_list = paginator.get_page(page_number)

    return render(request, 'emp_job_list.html', {'job_list': job_list})







def candidate_profile(request, *args, **kwargs):
    Jobseeker = jobseeker.objects.get(pk=kwargs['pk'])
    print(Jobseeker.id)
    
    if not Jobseeker.is_authenticated:
        return redirect('/emp_login/')
    
    else:
        details = userdetails.objects.filter(jobseeker=Jobseeker)
        context = {
        'Candidate': Jobseeker,
    }


    return render(request, 'candidates_profile.html', context)