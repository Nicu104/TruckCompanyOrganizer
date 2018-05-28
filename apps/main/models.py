from __future__ import unicode_literals
from passlib.hash import pbkdf2_sha256
import re
from django.contrib import messages
from django.contrib.messages import get_messages
from storages.backends.s3boto3 import S3Boto3Storage
from django.db import models
from django.utils.deconstruct import deconstructible
import os, time, random, string
from uuid import uuid4

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

# PHONE_REGEX = re.compile(r'^[0-9+-]$')

class DataManager(models.Manager):
    
    
    def userValidation(self, request):
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        email = request.POST['email']
        pNumber = request.POST['phone']   
        #   user level 1-driver
        #  0 - dispatcher     
        uLevel = request.POST['userLevel']
        
        password = request.POST['password']
        password_conf = request.POST['confirmPassword']
        
        if len(firstName) < 3:
            messages.add_message(request, messages.ERROR, "Your first name should be at least 3 char long")
        
        if len(lastName) < 3:
            messages.add_message(request, messages.ERROR, "Your last name should be at least 3 char long")
        
        if len(pNumber) < 10: #or not PHONE_REGEX.match(phoneNumber):
            messages.add_message(request, messages.ERROR, "Phone number should be 10 characters long and next format xxx-xxx-xxxx")

        if not EMAIL_REGEX.match(email):
            messages.add_message(request, messages.ERROR, "Wrong email format it should be test@test.com")

        if len(password) < 8 or password != password_conf:
            messages.add_message(request, messages.ERROR, 'Password does not match or is shorter than 8 characters')

        if len(Users.objects.filter(email = email)) != 0:
            messages.add_message(request, messages.ERROR, "A user with this username exists already, please contact the admin")

        if len(get_messages(request)) > 0:
            return False
        else:
            encrypted_password = pbkdf2_sha256.encrypt(password, rounds = 12000, salt_size = 32)
            cmp = Companies.objects.get(id = request.session['company_id'])

            Users.objects.create(
                firstName = firstName,
                lastName = lastName,
                email = email,
                password = encrypted_password,
                phoneNumber = pNumber,
                company = cmp,
                level = uLevel
            )
            return True



    def autenticate(self, request):
        login       = request.POST["email"]
        password    = request.POST['password']
        try:
            user = Users.objects.get(email = login)
        except:
            messages.add_message(request, messages.ERROR, "No User with this email")
            return False

        if pbkdf2_sha256.verify(password, user.password):
            request.session["user_id"] = user.id
            request.session["access_level"] = user.level
            return True
        else:
            return False
    
    def cAutenticate(self, request):
        login       = request.POST["email"]
        password    = request.POST['password']
        company = Companies.objects.get(companyMC = login)

        if pbkdf2_sha256.verify(password, company.password):
            request.session["company_id"] = company.id
            request.session["company_name"] = company.companyName
            return True
        else:
            return False    

    def companyValidator(self, request):
        cName = request.POST['companyName'] 
        cMc = request.POST['mcNumber'] 
        cFId = request.POST['federalId'] 
        cPhone = request.POST['phone'] 
        password = request.POST['password'] 
        password_conf = request.POST['confirmPassword']

        add1 = request.POST['address1']
        add2 = request.POST['address2']
        cityf = request.POST['city']
        statef = request.POST['state']
        zipc = request.POST['zip']


        if len(password) < 15 or password != password_conf:
            messages.add_message(request, messages.ERROR, 'Password does not match or is shorter than 8 characters')

        if len(Companies.objects.filter(companyMC = cMc)) != 0:
            messages.add_message(request, messages.ERROR, "A company with this MC exists already, please contact the admin")

        if len(get_messages(request)) > 0:
            return False
        else:
            encrypted_password = pbkdf2_sha256.encrypt(password, rounds = 12000, salt_size = 32)

            cm = Companies.objects.create(
                companyName = cName,
                companyMC = cMc,
                companyPhone = cPhone,
                password = encrypted_password
            )

            Address.objects.create(
                company = cm,
                address1 = add1,
                address2 = add2,
                city = cityf,
                state = statef,
                zipcode = zipc,
            )
            return True

    def loadValidator(self, request):
        loadNr = request.POST['loadNumber']
        imgs = []

        try:
            imgs.append(request.FILES['myImage1'])
        except:
            print('error, myImage1')
 
        try:
            imgs.append(request.FILES['myImage2'])
        except:
            print('error, myImage2')
 
        try:
            imgs.append(request.FILES['myImage3'])
        except:
            print('error, myImage3')
 
        try:
            imgs.append(request.FILES['myImage4'])
        except:
            print('error, myImage4')
 
        try:
            imgs.append(request.FILES['myImage5'])
        except:
            print('error, myImage5')
 
        try:
            imgs.append(request.FILES['myImage6'])
        except:
            print('error, myImage6')       

        
        user = Users.objects.get(id = request.session['user_id'])

        if len(loadNr) < 1:
            messages.add_message(request, messages.ERROR, "invalid load number")

        if len(get_messages(request)) > 0:
            return False
        try:
            load = Loads.objects.get(loadNumber = loadNr)
        except:
            load = Loads.objects.filter(loadNumber = loadNr)
            if len(load) > 1:
                messages.add_message(request, messages.ERROR, "Too many loads with same number")
                return False
            
        load = Loads.objects.filter(loadNumber = loadNr)
        if len(load) > 0:
            load = load.last()
            for img in imgs:
                file = FileItem.objects.create(
                    image = img,
                    userFile = user,
                    loadFile = load,
                )
            return True

        else:
            load = Loads.objects.create(
                loadNumber = loadNr,
                driver = user,
                company = user.company
            )
            print(load)

            for img in imgs:
                file = FileItem.objects.create(
                    image = img,
                    userFile = user,
                    loadFile = load, 
                )
            return True


class Companies(models.Model):
    companyName     = models.CharField(max_length = 255)
    companyMC       = models.CharField(max_length = 255)
    companyFId      = models.CharField(max_length = 255)
    companyPhone    = models.CharField(max_length = 255)
    password        = models.TextField()
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    objects         = DataManager()


class Users(models.Model):
    firstName       = models.CharField(max_length = 255)
    lastName        = models.CharField(max_length = 255)
    email           = models.CharField(max_length = 255)
    phoneNumber     = models.CharField(max_length = 255)
    password        = models.TextField()
    company         = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name="user")
    level           = models.IntegerField()
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    objects         = DataManager()



class Loads(models.Model):
    loadNumber      = models.CharField(max_length = 255)
    driver          = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="load")
    company         = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name='loads')
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    objects = DataManager()



class FileItem(models.Model):
    
    @deconstructible
    class PathAndRename(object):

        def __init__(self, sub_path):
            self.path = sub_path

        def __call__(self, instance, filename):
            # eg: filename = 'my uploaded file.jpg'
            ext = filename.split('.')[-1]  #eg: 'jpg'
            uid = str(uuid4())[:10]    #eg: '567ae32f97'

            # eg: 'my-uploaded-file'
            new_name = '-'.join(filename.replace('.%s' % ext, '').split())

            # eg: 'my-uploaded-file_64c942aa64.jpg'
            renamed_filename = '%(new_name)s_%(uid)s.%(ext)s' % {'new_name': new_name, 'uid': uid, 'ext': ext}

            # eg: 'images/2017/01/29/my-uploaded-file_64c942aa64.jpg'
            return os.path.join(self.path, renamed_filename)

    image_path = time.strftime('images/%Y/%m/%d')
    image = models.ImageField(upload_to=PathAndRename(image_path))
    
    userFile        = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_photo')
    loadFile        = models.ForeignKey(Loads, on_delete=models.CASCADE, related_name='load_photo')  
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class Address(models.Model):
    company         = models.OneToOneField(Companies, on_delete=models.CASCADE, related_name='address_field')
    address1        = models.CharField(max_length = 255)
    address2        = models.CharField(max_length = 255)
    city            = models.CharField(max_length = 255)
    state           = models.CharField(max_length = 255)
    zipcode         = models.CharField(max_length = 255)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


