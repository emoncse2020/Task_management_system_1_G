from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import m2m_changed, post_save, pre_save, post_delete
from tasks.models import Task, TaskDetail, Employee, Project

@receiver(m2m_changed, sender=Task.assigned_to.through)
def notify_employees_on_task_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        print(instance, instance.assigned_to.all())
        assigned_emails = [emp.email  for emp in instance.assigned_to.all()]
        print("Checking...", assigned_emails)

        send_mail(
            "New Task Assigned", 
            f"You have been assigned to the task: {instance.title}",
            "mrhstu01@gmail.com",
            assigned_emails
        )

@receiver(post_delete, sender = Task)
def delete_associate_details(sender, instance, **kwargs):
    if instance.details:
        print(instance)
        instance.details.delete()
        
        print('deleted Successfully')