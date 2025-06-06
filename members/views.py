from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegisterForm, CustomLoginForm

# ✅ Register view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'members/register.html', {'form': form})

# ✅ Login view using built-in class-based view
class CustomLoginView(LoginView):
    authentication_form = CustomLoginForm
    template_name = 'members/login.html'

from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'members/dashboard.html')


class CustomLogoutView(LogoutView):
    next_page = 'home'  # Redirect after logout

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)