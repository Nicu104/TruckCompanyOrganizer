from django.db import models
from passlib.hash import pbkdf2_sha256
import re
from storages.backends.s3boto3 import S3Boto3Storage

<<<<<<< HEAD
=======

>>>>>>> 87edc9ccc26d7134b68c51a55bb4eedb268ce917


# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-copyZ0-9._-]+\.[a-zA-Z]+$')

PHONE_REGEX = re.compile(r'^[0-9+-]$')

class DataManager(models.Manager):
    def userValidation(self, request):
        firstName = request.POST['first-name']
        lastName = request.POST['last-name']
        email = request.POST['email']
        phoneNumber = request.POST['phone-number']        
        password = request.POST['password']
        password_conf = request.POST['password_conf']
        
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
    company         = models.OneToOneField(Companies, on_delete=models.CASCADE)
    address1        = models.CharField(max_length = 255)
    address2        = models.CharField(max_length = 255)
    city            = models.CharField(max_length = 255)
    state           = models.CharField(max_length = 255)
    zipcode         = models.CharField(max_length = 255)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class Photos(models.Model):
    load            = models.ForeignKey(Loads, on_delete=models.CASCADE, related_name='photo')
    user            = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='photo')
<<<<<<< HEAD
    image_field     = models.ImageField()
=======
    image_field     = models.ImageField()
    meta            = models
>>>>>>> 87edc9ccc26d7134b68c51a55bb4eedb268ce917
