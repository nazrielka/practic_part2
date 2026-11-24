from .forms import ClientCreationForm
from django.shortcuts import render, redirect
from creative_space.models import Submission
from django.contrib.auth import login

def index (request):
    num_submissions = Submission.objects.filter(status__exact='w').count()
    submission_ready_list = Submission.objects.filter(status__exact='r').order_by('-created_at')
    return render(request, 'creative_space/index.html', {'num_submissions': num_submissions, 'submission_ready_list': submission_ready_list,} )

def profile(request):
    return render(request, 'creative_space/profile.html')

def my_submissions(request):
    pass

def submission_create(request):
    pass

def book_details(request):
    pass

def submission_detail(request):
    pass

def register(request):
    if request.method == 'POST':
        form = ClientCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = ClientCreationForm()
    return render(request, 'registration/register.html', {'form': form})