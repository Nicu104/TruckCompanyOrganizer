from django.db import models
from passlib.hash import pbkdf2_sha256
import re
from storages.backends.s3boto3 import S3Boto3Storage


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

PHONE_REGEX = re.compile(r'^[0-9+-]$')

class DataManager(models.Manager):
    def userValidation(self, request):
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        email = request.POST['email']
        phoneNumber = request.POST['phone']        
        password = request.POST['password']
        password_conf = request.POST['confirmPassword']
        
        if len(firstName) < 3:
            messages.add_message(request, messages.ERROR, "Your first name should be at least 3 char long")
        
        if len(lastName) < 3:
            messages.add_message(request, messages.ERROR, "Your last name should be at least 3 char long")
        
        if len(phoneNumber) < 10 or not PHONE_REGEX.match(phoneNumber):
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

            Users.objects.create(
                firstName = firstName,
                lastName = lastName,
                email = email,
                password = encrypted_password,
                phoneNumber = phoneNumber
            )
            return True



#try to login with either of accounts Users or Company
#in case of successful login equal to email means it is a user and returns 1
# in case login is a number ir means is a company MC ad we return 0
# in case neither of those two or wrong password we return -1
    def autenticate(self, request):
        login       = request.POST["email"]
        password    = request.POST['password']

        if EMAIL_REGEX.match(login):
            user = Users.objects.get(email = login)
            if pbkdf2_sha256.verify(password, user.password):
                request.session["user_id"] = user.id
                return 1
            else:
                return -1

        elif PHONE_REGEX.match(login):
            company = Companies.objects.get(companyMC = login)
            if pbkdf2_sha256.verify(password, company.password):
                request.session["company_id"] = company.id
                return 0
            else:
                return -1
        else:
            return -1
    

    def companyValidator(self, request):
        cName = request.POST['companyName'] 
        cMC = request.POST['mcNumber'] 
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

        if len(Companies.objects.filter(companyMC = cMC)) != 0:
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



# class MediaStorage(S3Boto3Storage):
#     location = 'assets'
#     file_overwrite = False


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
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    objects         = DataManager()



class Loads(models.Model):
    loadNumber      = models.CharField(max_length = 255)
    # pickUplocation
    # dropOffLocation
    driver          = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="load")
    company         = models.ForeignKey(Companies, on_delete=models.CASCADE, related_name='loads')
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)



class FileItem(models.Model):
    # user            = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    user            = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='photo')
    name            = models.CharField(max_length=120, null=True, blank=True)
    path            = models.TextField(blank=True, null=True)
    size            = models.BigIntegerField(default=0)
    file_type       = models.CharField(max_length=120, null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    uploaded        = models.BooleanField(default=False)
    active          = models.BooleanField(default=True)

    @property
    def title(self):
        return str(self.name)

class Address(models.Model):
    company         = models.OneToOneField(Companies, on_delete=models.CASCADE, related_name='address_field')
    address1        = models.CharField(max_length = 255)
    address2        = models.CharField(max_length = 255)
    city            = models.CharField(max_length = 255)
    state           = models.CharField(max_length = 255)
    zipcode         = models.CharField(max_length = 255)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


