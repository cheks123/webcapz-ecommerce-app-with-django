from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    form = ProfileForm(instance=request.user.profile)
    return render(request, "registration\profile.html", {"profile": form})

# Create your views here.
