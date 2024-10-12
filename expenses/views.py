from django.shortcuts import redirect, get_object_or_404, render
from .models import TrackingExpenses, CurrentBalance
from django.contrib import messages  

# Create your views here.

def index(request):
    if request.method=="POST":
        amount = request.POST.get("amount")
        remarks = request.POST.get("description")
        current_balance,_ = CurrentBalance.objects.get_or_create(id=1)
        if amount == "":
            messages.error(request, "Amount field cannot be empty.")
            return redirect("/")
        
        amount = float(amount)
        expense_type ="CREDIT"
        if float(amount)<0:
            expense_type="DEBIT"
        if float(amount)==0:
            messages.success(request,"Amount cannot be zero")
            return redirect("/")

            
        new_track = TrackingExpenses(current_balance=current_balance,amount=amount, description=remarks, expense_type = expense_type)
        new_track.save()
        current_balance.current_balance = current_balance.current_balance + float(new_track.amount)
        current_balance.save()
        return redirect("/")
    
    context_data = TrackingExpenses.objects.all()
    creditedAmount = 0
    debitedAmount = 0
    for transaction in context_data:
        if transaction.expense_type=="DEBIT":
            debitedAmount+=abs(transaction.amount)
            
        else: 
            creditedAmount+=transaction.amount
    currentBalance,_ = CurrentBalance.objects.get_or_create(id=1)
    currentBalance = currentBalance.current_balance
    context = {"transactions":context_data, "creditedAmount":creditedAmount, "debitedAmount":debitedAmount,"currentBalance":currentBalance}

    return render(request, "index.html", context=context)



def removeTransaction(request, id):
    # get the object, if not existed, return 404.
    transaction = get_object_or_404(TrackingExpenses, id=id)
    # get the current balance
    currentBalance = CurrentBalance.objects.get(id=1)
    # Update current balance
    if currentBalance:
        currentBalance.current_balance -=transaction.amount
        currentBalance.save()
    transaction.delete()
    messages.success(request, "Transaction deleted successfully.")
    return redirect("/")

