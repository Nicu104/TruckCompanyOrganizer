from django.shortcuts import render, redirect, HttpResponse, reverse
from .models import *


# TODO render the home page
def index(request):
    return render(request, 'src/index.html')
    

# TODO renders the login page 
def log(request):
    return render(request, 'src/login.html')



# TODO render the register page
def register(request):
    return render(request, 'src/register.html')

# TODO add a new company and redirect to company admin page
def registerForm(request):
    if DataManager.objects.companyValidator(request):
        return redirect(reverse('main:adminpage'))
    else:
        return redirect(reverse('main:registerpage'))

# TODO route for login user and redirect to user page to check if its a compay or a user that wnts to login
def logIn(request):

    return redirect('/userPage.html')

# TODO add a new user to the data base for specific company by admin
def newUser(request):
    return render(request, 'src/adminPage.html')

def registerUser(request):
    if Users.objects.userValidation(request):
        return redirect(reverse('main:adminpage'))
    else:
        return redirect(reverse('main:adminpage'))

# TODO render about page
def about(request):
    return render(request, 'src/learn_more.html')

# TODO render a howit works page
def howitworks(request):
    return redirect(reverse('main:userpage'))

# TODO render a howit works page
def loads(request):
    return render(request, 'src/allLoads.html')

def images(request):
    return render(request, 'src/images.html')

def logout(request):
    request.session.flush()
    return redirect('/')

# TODO render learn more page
def learnmore(request):
    return redirect('src/learn_more.html')

# TODO render  adminpage
def adminpage(request):
    return render(request, 'src/adminPage.html')


# TODO render  userpage
def userpage(request):
    return render('src/userPage.html')
