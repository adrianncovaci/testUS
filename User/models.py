from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from .utils import read_text
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_active=True, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError("Users must have an email")

        if not password:
            raise ValueError("Users must have a password")

        if not first_name:
            raise ValueError("Users must have a first name")

        if not last_name:
            raise ValueError("Users must have a last name")
        
        now = timezone.now()

        user_obj = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.superuser = is_superuser
        user_obj.active = is_active
        user_obj.last_login = now
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, password=None):
        user_obj = self.create_user(email=email, first_name=first_name, last_name=last_name,
                                    password=None, is_staff=True)
        return user_obj

    def create_superuser(self, email, first_name, last_name, password=None):
        user_obj = self.create_user(email=email, first_name=first_name, last_name=last_name,
                                    password=password, is_staff=True, is_superuser=True)
        return user_obj


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=60, blank=False)
    last_name = models.CharField(max_length=60, blank=False)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login',
                                      auto_now=True)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_superuser(self):
        return self.superuser
    
    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Student(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    def __str__(self):
        return Account.get_full_name(self.user)

class Professor(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=60, blank=False)

    def __str__(self):
        return self.title + " " + Account.get_full_name(self.user)



class Test(models.Model):
    name = models.CharField(max_length=60, blank=False)
    added = models.DateTimeField(auto_now_add=True, verbose_name='Date Added')
    date = models.DateTimeField(null=True, blank=True)
    professor = models.OneToOneField(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + self.date.strftime("%d/%m/%y, %H:%M")

    def get_absolute_url(self):
        return reverse('submissions_list', args=[str(self.id)])


class Class(models.Model):
    name = models.CharField(max_length=60, blank=False, unique=True)
    students = models.ManyToManyField(Student, related_name='class_students')
    professors = models.ManyToManyField(Professor, related_name='class_professors')
    tests = models.ManyToManyField(Test, related_name='tests')

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('class_detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Submission(models.Model):
    text = models.TextField(blank=True)
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/')

    def __str__(self):
        return str(self.user) + " - " + str(self.test)

    def get_absolute_url(self):
        return reverse('submissions_list', args=[str(self.id)])


@receiver(post_save, sender=Submission, dispatch_uid='generate_social_number')
def gen_text(sender, instance, **kwargs):
    if kwargs.get('created', False):
        content = read_text(instance.image.url)
        instance.text = content
        instance.save()