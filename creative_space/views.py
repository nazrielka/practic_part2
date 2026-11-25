from .forms import ClientCreationForm
from django.shortcuts import render, redirect
from creative_space.models import Submission
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic, View

def index (request):
    num_submissions = Submission.objects.filter(status__exact='w').count()
    submission_ready_list = Submission.objects.filter(status__exact='r').order_by('-created_at')
    return render(request, 'creative_space/index.html', {'num_submissions': num_submissions, 'submission_ready_list': submission_ready_list,} )

class SubmissionListViewMyProfile(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'creative_space/profile.html'
    paginate_by = 4

    def get_queryset(self):
        return (Submission.objects.filter(client__user=self.request.user)).order_by('-created_at')

class SubmissionListViewMy(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'creative_space/submission_list_my.html'
    paginate_by = 4

    def get_queryset(self):
        queryset = (Submission.objects.filter(client__user=self.request.user)).order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status__exact=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        return context

def profile(request):
    return render(request, 'creative_space/profile.html')

def submission_create(request):
    pass

def submission_delete(request):
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