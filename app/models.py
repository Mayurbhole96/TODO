from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class TODO(models.Model):
    status_choices = [
    ('C', 'COMPLETED'),
    ('P', 'PENDING'),
    ]
    title = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2 , choices=status_choices)
    user  = models.ForeignKey(User, on_delete= models.CASCADE)

    is_active = models.BooleanField(default=True,verbose_name='Is Active')
    is_deleted = models.BooleanField(default=False,verbose_name="Is Deleted")

    class Meta:
        db_table = "table_todo"
        verbose_name_plural = "Todo List"

    def delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

    def __str__(self):
        return self.title