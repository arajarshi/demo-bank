from django.db import models

# Create your models here.


class Details(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    Date_of_birth = models.DateField()
    Account_number = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.username} {self.password}"
    
class Transaction(models.Model):
    account_number = models.CharField(max_length=20)
    transaction_type = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.account_number}-{self.transaction_type}-{self.amount}on{self.transaction_date}"