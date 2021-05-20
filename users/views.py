from django.forms.fields import EmailField
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# django generated forms for user regesteration, class is 
# automatically converted to hitml
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) #passing in the post data from the user
        if form.is_valid():
            form.save()         #saving the form to the databse
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created! You can log in now')
            return redirect('login')            
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user) #pass in the current values for the fields
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile') #redirect to the same page to prevent the creation of new post request
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)  


    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)




