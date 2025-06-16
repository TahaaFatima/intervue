from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.core.serializers.json import DjangoJSONEncoder
from .forms import RegisterForm, CustomLoginForm, InterviewEntryForm
from .models import InterviewEntry
import json
from .utils import suggest_questions

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email    = request.POST['email'].strip()
        password = request.POST['password']
        confirm  = request.POST['confirm_password']

        if password != confirm:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)  # Auto login after registration
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'members/register.html', {'form': form})

# Login view using built-in class-based view
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'members/login.html'

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    entries = InterviewEntry.objects.filter(user=request.user)

    events = []
    for entry in entries:
        events.append({
            "title": entry.job_title,
            "start": entry.date.isoformat(),  # ensure correct format
            "id"   : entry.id
        })

    return render(request, 'members/dashboard.html', {
        'events_json': json.dumps(events, cls=DjangoJSONEncoder)
    })

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = InterviewEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.questions = suggest_questions(entry.description)  # Save generated questions
            entry.save()
            # return redirect('dashboard')
            questions = suggest_questions(entry.description)
            return render(request, 'members/suggested_questions.html', {
                'questions': questions,
                'entry': entry
            })
    else:
        # Prefill selected date from calendar
        initial_date = request.GET.get('date')
        form = InterviewEntryForm(initial={'date': initial_date})
    return render(request, 'members/entry_form.html', {'form': form, 'mode' : 'add'})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(InterviewEntry, id=entry_id, user=request.user)
    if request.method == 'POST':
        form = InterviewEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = InterviewEntryForm(instance=entry)
    return render(request, 'members/entry_form.html', {'form': form, 'mode' : 'edit'})

@login_required
def view_questions(request, entry_id):
    entry = get_object_or_404(InterviewEntry, id=entry_id, user=request.user)
    return render(request, 'members/view_questions.html', {'entry': entry})


class CustomLogoutView(LogoutView):
    next_page = 'home'  # Redirect after logout

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)