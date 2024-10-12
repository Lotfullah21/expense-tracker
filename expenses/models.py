from django.db import models

# Create your models here.


class CurrentBalance(models.Model):
    current_balance = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"the current balance is = {self.current_balance}"

class TrackingExpenses(models.Model):
    current_balance = models.ForeignKey(CurrentBalance,on_delete =models.CASCADE)
    amount = models.FloatField(default=0)
    description = models.CharField(max_length = 200)
    expense_type = models.CharField(choices=(("DEBIT", "Debit"),("CREDIT","Credit")),max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now =True)
    
    def __str__(self):
        return f"item {self.description} - with price =  {self.current_balance}"