from django.db import models

# Create your models here.


class BaseManager(models.Manager):
    def userValidation(self, request):
        firstName = request.POST['first-name']
        lastName = request.POST['last-name']
        email = request.POST['email']
        paswd = request.POST['password']
        paswd_conf = request.POST['password_conf']
        if len(name) < 3:
            messages.add_message(request, messages.ERROR, "Your name should be at least 3 char long")
        
        if len(username) < 3:
            messages.add_message(request, messages.ERROR, "User name should be at least 3 chars long")

        if len(paswd) < 8 or paswd != paswd_conf:
            messages.add_message(request, messages.ERROR, 'Password does not match or is shorter than 8 characters')

        if len(Users.objects.filter(user_name = username)) != 0:
            messages.add_message(request, messages.ERROR, "A user with this username exists already, please contact the admin")

        if len(get_messages(request)) > 0:
            return False
        else:
            password = paswd
            enc_pass = pbkdf2_sha256.encrypt(paswd, rounds = 12000, salt_size = 32)

            Users.objects.create(
                name = name,
                user_name = username,
                password = enc_pass
            )
            return True