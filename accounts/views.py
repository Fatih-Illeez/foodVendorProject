from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            #we do save(commit=false) because we want to assign the role to the
            #user but role is not an attribute of form. so we do user = form
            #with commit = false and then we assign the role and then we save
            #this way we first convert it to a user, then we assign the role
            #then we save.
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password) #this will hash the password
            # user.role = User.CUSTOMER
            # user.save()

            #above code and below code do the same thing

            #Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been created! You are now able to log in')
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form' : form,
    }
    return render(request, 'accounts/registerUser.html', context)