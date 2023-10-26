from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)  # in kg
    height = models.FloatField(null=True, blank=True)  # in cm
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class PhysicalGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    GOAL_TYPES = [
        ('Weight Loss', 'Weight Loss'),
        ('Muscle Gain', 'Muscle Gain'),
        ('Stamina Increase', 'Stamina Increase'),
        # ... add more goal types as needed
    ]
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)

    def __str__(self):
        return self.description

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in minutes
    DIFFICULTIES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    difficulty = models.CharField(max_length=10, choices=DIFFICULTIES)

    def __str__(self):
        return self.name

class UserWorkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.workout.name}"

class ActivityTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    steps = models.PositiveIntegerField()
    distance = models.FloatField()  # Distance in kilometers
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class DietPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    calories = models.PositiveIntegerField()
    carbohydrates = models.PositiveIntegerField()
    proteins = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class UserDiet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    diet_plan = models.ForeignKey(DietPlan, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.diet_plan.name}"

class NutritionCalculator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food_item = models.CharField(max_length=100)
    calories = models.PositiveIntegerField()
    carbohydrates = models.PositiveIntegerField()
    proteins = models.PositiveIntegerField()
    fats = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.food_item}"

class MeditationGuide(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in minutes
    audio_link = models.URLField()

    def __str__(self):
        return self.name

class UserMeditation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meditation = models.ForeignKey(MeditationGuide, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.meditation.name}"

class DailyCheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Neutral', 'Neutral'),
        ('Sad', 'Sad'),
        # ... add more moods as needed
    ]
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    notes = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"