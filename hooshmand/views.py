from django.shortcuts import render
from .models import Student
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.timezone import now

@receiver(pre_save, sender=Student)
def generate_greeting(sender, instance, **kwargs):
    if not instance.email:
        print("hello")
        formatted_date = instance.joined_at.strftime('%Y%m%d%H%M%S') if instance.joined_at else now().strftime('%Y%m%d%H%M%S')
        instance.email = f"King_{formatted_date}@gmail.com"

def courses_view(request):
    return render(request, "courses/index.html")

a = Student(name="noori")
a.save()