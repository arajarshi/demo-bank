from decimal import Decimal
from django.db import IntegrityError
from django.http import HttpResponse
from myapp.models import Details, Transaction
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'home.html')



def register(request):
    if request.method == "POST":
      uname = request.POST.get('uname')
      umail = request.POST.get('umail')
      upsw  = request.POST.get('upsw')
      udob  = request.POST.get('udob')
      uano  = request.POST.get('uano')
      
      if not uname or not upsw or not udob or not uano:
          return HttpResponse("All fields are required")
      
      if Details.objects.filter(Account_number=uano).exists() or Details.objects.filter(password=upsw).exists():
          return HttpResponse("Account number or password already exists.Please choose a different one.")
      
      try:
          data= Details(username=uname, password=upsw, email=umail,Date_of_birth=udob, Account_number=uano)
          data.save()
          return HttpResponse("Registered successfully")
      except IntegrityError as e:
          return HttpResponse(f"An error occured: {str(e)}")
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == "POST":
        uname= request.POST.get('uname')
        upsw=request.POST.get('upsw')
        
        if Details.objects.filter(username=uname).exists() and Details.objects.filter(password=upsw).exists():
            #return HttpResponse("valid details")
            return render(request,'home.html')
        else:
            return HttpResponse("Invalid details")
    else:
        return render(request, "login.html")
    
    
def deposit(request):
    if request.method == 'POST':
        account_no = request.POST.get('account_no')
        amount = request.POST.get('amount')
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")
        
        if not account_no or amount <=0:
            return HttpResponse("Please provide a valid account number and a positive amount")
        
        try:
            details = Details.objects.get(Account_number=account_no)
            details.balance = details.balance + amount
            details.save()
            
            Transaction.objects.create(
                account_number=account_no,
                transaction_type='DEPOSIT',
                amount=amount
            )
            return HttpResponse(f"Deposited {amount} successfully. new balance: {details.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'deposit.html')
    
def withdraw(request):
    if request.method == 'POST':
        account_no = request.POST.get('account_no')
        password = request.POST.get('password')
        amount = request.POST.get('amount')
        try:
            amount = Decimal(amount)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")
        if amount <=-0:
            return HttpResponse("Amount should be positive.")
        try:
            account= Details.objects.get(Account_number=account_no)
            
            if account.password != password:
                return HttpResponse("Invalid password for the account.")
            if account.balance < amount:
                return HttpResponse("Insufficient balance in the account.")
            
            account.balance = account.balance - amount
            account.save()
            
            Transaction.objects.create(
                account_number=account_no,
                transaction_type='WITHDRAW',
                amount=amount
            )
            
            return HttpResponse(f"Withdraw {amount} successfully. new balance:{account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'withdraw.html')
    
def balance(request):
    if request.method == 'POST':
        account_no = request.POST.get('account_no')
        password = request.POST.get('password')
        
        if not account_no or not password:
            return HttpResponse("Both account number and password are required.")
        
        try:
            account = Details.objects.get(Account_number=account_no)
            
            if account.password != password:
                return HttpResponse("Invalid password for the account.")
            
            return HttpResponse(f"Current balance: {account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("Account number does not exist.")
    else:
        return render(request, 'balance.html')
    

def transfer(request):
    if request.method == 'POST':
        source_account_no = request.POST.get('source_account_no')
        target_account_no = request.POST.get('target_account_no')
        amount = request.POST.get('amount')
        password = request.POST.get('password')
        
        try:
            amount = Decimal(amount)
        except ValueError:
            return HttpResponse("Invalid amount. Please enter a valid number.")
        
        if not source_account_no or not target_account_no or not amount or not password:
            return HttpResponse("All fields are required.")
        
        if amount <= 0:
            return HttpResponse("Amount should be positive.")

        try:
            source_account = Details.objects.get(Account_number=source_account_no)
            target_account = Details.objects.get(Account_number=target_account_no)

            if source_account.password != password:
                return HttpResponse("Invalid password for the source account.")
            
            if source_account.balance < amount:
                return HttpResponse("Insufficient balance in the source account.")
            
            source_account.balance = source_account.balance -  amount
            target_account.balance = target_account.balance + amount

            source_account.save()
            target_account.save()
            
            
            Transaction.objects.create(
                account_number=source_account_no,
                transaction_type='DEBIT',
                amount=amount
            )
            
            Transaction.objects.create(
                account_number=target_account_no,
                transaction_type='CREDIT',
                amount=amount
            )
            

            return HttpResponse(f"Transferred {amount} successfully from account {source_account_no} to account {target_account_no}. New balance: {source_account.balance}")
        except Details.DoesNotExist:
            return HttpResponse("One or both account numbers do not exist.")
    else:
        return render(request, 'transfer.html')
        