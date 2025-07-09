from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import Task
from .forms import TaskForm, PositionForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(user=self.request.user)

        # Filters
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            tasks = tasks.filter(title__icontains=search_input)

        category_filter = self.request.GET.get('category') or ''
        if category_filter in ['work', 'personal', 'urgent']:
            tasks = tasks.filter(category=category_filter)

        priority_filter = self.request.GET.get('priority') or ''
        if priority_filter in ['low', 'medium', 'high']:
            tasks = tasks.filter(priority=priority_filter)

        # Progress
        completed_tasks = tasks.filter(complete=True).count()
        total_tasks = tasks.count()
        percent_complete = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

        context.update({
            'tasks': tasks,
            'count': tasks.filter(complete=False).count(),
            'search_input': search_input,
            'category_filter': category_filter,
            'priority_filter': priority_filter,
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'percent_complete': percent_complete,
        })
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)
        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')
            with transaction.atomic():
                # You must implement this method in your User model
                self.request.user.set_task_order(positionList)
        return redirect('tasks')


@method_decorator(csrf_exempt, name='dispatch')
class ToggleCompleteView(View):
    def post(self, request):
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id, user=request.user)
            task.complete = not task.complete
            task.save()
            return JsonResponse({'status': 'success', 'complete': task.complete})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'not found'})
