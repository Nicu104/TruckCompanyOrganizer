from django.shortcuts import render, redirect, HttpResponse, reverse
from .models import *
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

# TODO render the home page
def index(request):
    if 'company_id' in request.session:
        return redirect(reverse('main:adminpage'))
    
    # return render(request, 'src/index.html')
    
    if 'user_id' in request.session:
        return redirect(reverse('main:userPage'))
    
    return render(request, 'src/index.html')



# TODO renders the login page 
def log(request):
    if 'company_id' in request.session:
        return redirect(reverse('main:adminpage'))
    
    # return render(request, 'src/index.html')
    if 'user_id' in request.session:
        return redirect(reverse('main:userPage'))
    
    return render(request, 'src/login.html')



# TODO render the register page
def register(request):
    if 'company_id' in request.session:
        return redirect(reverse('main:adminpage'))
    
    # return render(request, 'src/index.html')
    if 'user_id' in request.session:
        return redirect(reverse('main:userPage'))
    
    return render(request, 'src/register.html')


# TODO add a new company and redirect to company admin page
def registerForm(request):
    if Companies.objects.companyValidator(request):
        return redirect(reverse('main:adminpage'))
    else:
        return redirect(reverse('main:registerpage'))



# TODO route for login user and redirect to user page to check if its a compay or a user that wnts to login
def logIn(request):
    if EMAIL_REGEX.match(request.POST['email']):
        if Users.objects.autenticate(request):
            return redirect(reverse('main:userPage'))
        else:
            return redirect(reverse('main:loginform'))
    else:
        if Companies.objects.cAutenticate(request):
            return redirect(reverse('main:adminpage'))
        else:
            return redirect(reverse('main:loginform'))

    print('*' * 50, 'nothing worked')
    return redirect(reverse('main:loginform'))



# TODO add a new user to the data base for specific company by admin
def newUser(request):
    if Users.objects.userValidation(request):
        return redirect(reverse('main:adminpage'))
    else:
        return redirect(reverse('main:adminpage'))
    # return render(request, 'src/adminPage.html')

def registerUser(request):
    return render(request, 'src/adminPage.html')


# # TODO render about page
# def about(request):
#     return render(request, 'src/learn_more.html')

# TODO render a howit works page
def howitworks(request):
    return redirect(reverse('main:userpage'))

# TODO render a table with all loads
def loads(request):
    if not 'user_id' in request.session:
        return redirect(reverse('main:login'))

    user = Users.objects.get(id = request.session['user_id'])
    # company = user.company
    loads = Loads.objects.filter(company = user.company)

    context = {
        'loads' : loads
    }
    return render(request, 'src/allLoads.html', context)



def images(request):
    return render(request, 'src/images.html')

def logout(request):
    # del(request.session['company_id'])
    # del(request.session['user_id'])
    # del(request.session['company_name'])
    request.session.flush()
    return redirect(reverse('main:home'))

# TODO render  adminpage
def adminpage(request):
    return render(request, 'src/adminPage.html')


# TODO render  userpage
def userpage(request):
    if not 'user_id' in request.session:
        return redirect(reverse('main:login'))

    return render(request, 'src/userPage.html')


# TODO get the post data and upload it to the server
def upload_pic(request):
    if Loads.objects.loadValidator(request):
        return redirect(reverse('main:userPage'))
    else:
        return redirect(reverse('main:userPage'))
            
    # return render(request, 'src/userPage.html')




# TODO render page with all pictures for a specific load
def picturesLoad(request, id):
    if not 'user_id' in request.session:
        return redirect(reverse('main:login'))

    load = Loads.objects.get(id = id)
    pictures = FileItem.objects.filter(loadFile = load)

    context = {
        'pictures' : pictures
    }

    return render(request, 'src/images.html', context)

