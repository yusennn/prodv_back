from django.shortcuts import render, redirect
from .forms import ProblemForm
from .models import Problem
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def create_problem(request):
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            problem = form.save(commit=False)
            problem.save()
            reception_group = Group.objects.get(name='Reception')
            reception_users = reception_group.user_set.all()
            if reception_users.exists():
                assigned_user = reception_users.first()
                problem.assigned_user = assigned_user
                problem.save()
            return redirect('index')
    else:
        form = ProblemForm()

    return render(request, 'create_problem.html', {'form': form})


@login_required
def problem_list(request):
    problems = Problem.objects.filter(assigned_user=request.user)
    return render(request, 'problem_list.html', {'problems': problems})


@login_required
def problem_detail(request, problem_id):
    problem = Problem.objects.get(pk=problem_id)
    reception_group = Group.objects.get(name='Reception')
    reception_users = reception_group.user_set.all()

    is_tester = request.user.groups.filter(name='Tester').exists()

    if request.method == 'POST':
        problem.actions = request.POST.get('actions', '')
        problem.status = request.POST.get('status', 'new')

        new_assigned_user_id = request.POST.get('assigned_user', None)
        if new_assigned_user_id:
            new_assigned_user = User.objects.get(id=new_assigned_user_id)
            problem.assigned_user = new_assigned_user

        problem.save()

        if problem.status == 'resolved':
            tester_group = Group.objects.get(name='Tester')
            tester_users = tester_group.user_set.all()
            if tester_users.exists():
                resolved_user = tester_users.first()
                problem.resolved_user = resolved_user
                problem.assigned_user = resolved_user

            problem.save()
        return HttpResponseRedirect(reverse('problem-list'))

    return render(request, 'problem_detail.html', {'problem': problem, 'reception_users': reception_users, 'is_tester': is_tester})

