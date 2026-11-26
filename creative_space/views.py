from django.urls import reverse_lazy

from .forms import ClientCreationForm, DesignCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from creative_space.models import Submission, Design, Category
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import generic, View

def index (request):
    num_submissions = Submission.objects.filter(status__exact='w').count()
    submission_ready_list = Submission.objects.filter(status__exact='r').order_by('-created_at')[:4]
    return render(request, 'creative_space/index.html', {'num_submissions': num_submissions, 'submission_ready_list': submission_ready_list,} )

class SubmissionListViewMyProfile(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'creative_space/profile.html'

    def get_queryset(self):
        return (Submission.objects.filter(client__user=self.request.user)).order_by('-created_at')[:4]

class SubmissionListViewAll(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'creative_space/submission_list_all.html'
    paginate_by = 8

    def get_queryset(self):
        queryset = Submission.objects.all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status__exact=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        return context

class SubmissionListViewMy(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'creative_space/submission_list_my.html'
    paginate_by = 6

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

class SubmissionDetailView(generic.DetailView):
    model = Submission
    template_name = 'creative_space/submission_detail.html'

class SubmissionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Submission
    fields = ['category', 'description', 'floor_plan']
    permission_required = 'creative_space.add_submission'
    success_url = reverse_lazy('my_submissions')

    def form_valid(self, form):
        form.instance.client = self.request.user.client
        return super().form_valid(form)

class SubmissionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Submission
    fields = ['category', 'description', 'floor_plan']
    permission_required = 'creative_space.change_submission'

class SubmissionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Submission
    success_url = reverse_lazy('my_submissions')
    permission_required = 'creative_space.delete_submission'

class DesignCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Design
    form_class = DesignCreationForm
    permission_required = 'creative_space.add_design'
    success_url = reverse_lazy('all_submissions')

    def form_valid(self, form):
        form.instance.submission = get_object_or_404(Submission, pk=self.kwargs['pk'])
        form.instance.designer = self.request.user.client
        return super().form_valid(form)

class CategoryListView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
    model = Category
    template_name = 'creative_space/category_list.html'
    paginate_by = 12
    permission_required = 'creative_space.view_category'
    ordering =  ['name']

    def get_queryset(self):
        queryset = Category.objects.all()
        return queryset

class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    model = Category
    fields = ['name']
    permission_required = 'creative_space.add_category'
    success_url = reverse_lazy('categories')

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
    permission_required = 'creative_space.delete_category'

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
