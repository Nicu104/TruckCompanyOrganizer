from django.shortcuts import render, redirect, HttpResponse

# TODO render the home page
def index(request):
    return render(request, 'src/index.html')
    
# TODO render log in page
def log(request):
    return render(request, 'src/login.html')

# TODO render the register page
def register(request):
    return render(request, 'src/register.html')

# TODO add a new company and redirect to company admin page
def registerForm(request):
    return redirect('/adminPage.html')

# TODO route for login user and redirect to user page
def logIn(request):
    return redirect('/userPage.html')

# TODO render about page
def about(request):
    return redirect('/userPage.html')

# TODO render a howit works page
def howitworks(request):
    return redirect('/userPage.html')

# TODO render learn more page
def learnmore(request):
    return redirect('src/learn_more.html')

