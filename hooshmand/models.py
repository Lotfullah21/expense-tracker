from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()  # Course duration (e.g., hours, minutes)
    language = models.CharField(max_length=50, choices=[('EN', 'English'), ('FR', 'French')])
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50, choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')])
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)  # Free or paid courses
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Instructor(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='instructors/')
    expertise = models.CharField(max_length=100)
    social_link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Student(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    profile_picture = models.ImageField(upload_to='students/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()  # Could store video URLs, text, etc.
    video_url = models.URLField(blank=True, null=True)  # URL for lesson video
    duration = models.DurationField()  # Duration of the lesson
    order = models.PositiveIntegerField()  # To order lessons in the course

    def __str__(self):
        return self.title
