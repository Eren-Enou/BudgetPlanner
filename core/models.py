from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creation_date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)  # Added description field

    def __str__(self):
        return self.name

class Expense(models.Model):
    class CategoryChoices(models.TextChoices):
        GROCERIES = 'GR', 'Groceries'
        TRANSPORT = 'TR', 'Transport'
        ENTERTAINMENT = 'EN', 'Entertainment'
        UTILITIES = 'UT', 'Utilities'
        RENT = 'RE', 'Rent'
        HEALTH = 'HE', 'Health'
        OTHER = 'OT', 'Other'
        TRAVEL = 'TV', 'Travel'
        EDUCATION = 'ED', 'Education'
        SAVINGS = 'SV', 'Savings'
        SUBSCRIPTIONS = 'SB', 'Subscriptions'
        # Add more categories as needed

    class FrequencyChoices(models.TextChoices):
        WEEKLY = 'WK', 'Weekly'
        BIWEEKLY = 'BW', 'Bi-weekly'
        MONTHLY = 'MN', 'Monthly'
        QUARTERLY = 'QR', 'Quarterly'
        YEARLY = 'YR', 'Yearly'
    
    budget = models.ForeignKey(Budget, related_name='expenses', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=2, choices=CategoryChoices.choices, default=CategoryChoices.OTHER)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_recurring = models.BooleanField(default=False)
    frequency = models.CharField(max_length=2, choices=FrequencyChoices.choices, blank=True, null=True)
    next_due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='images/default_profile_pic.jpg', null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    join_date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    last_accessed_budget = models.ForeignKey(Budget, null=True, blank=True, on_delete=models.SET_NULL)

    THEME_CHOICES = [
    ('light', 'Light Mode'),
    ('dark', 'Dark Mode'),
    ]
    theme_preference = models.CharField(max_length=5, choices=THEME_CHOICES, default='light')

    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
    ('N', 'Prefer Not to Say'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    category = models.CharField(max_length=255, blank=True, null=True)  # Optional field for bill categorization
    notes = models.TextField(blank=True, null=True)  # Optional field for any additional information or notes

    def __str__(self):
        return f"{self.name} - ${self.amount_due}"
    
class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'{self.source} - {self.amount}'