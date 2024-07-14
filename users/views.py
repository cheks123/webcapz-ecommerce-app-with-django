from django.shortcuts import render, redirect
from .forms import ProfileForm

def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    
    form = ProfileForm(instance=request.user.profile)
    context = {"form": form}
    return render(request, "registration\profile.html", context)




# Create your views here.
