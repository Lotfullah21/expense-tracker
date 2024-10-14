from django.shortcuts import redirect, get_object_or_404, render
from .models import TrackingExpenses, CurrentBalance, Contact
from django.contrib import messages  
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

# Create your views here.
def contact(request):
    if request.method=="POST":
        name= request.POST.get("name")
        age= request.POST.get("age")
        Contact.objects.create(name=name, age=age)
        return redirect("/contact/")
    return render(request, "contact_test.html")


def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name")
        password = request.POST.get("password")
        user = User.objects.filter(username=user_name)
        if not user:
            messages.error(request,"User does not exist, please register first")
            return redirect("register_view")
        user = authenticate(username=user_name, password=password)
        if not user:
            messages.error(request,"Incorrect password, try again")
            return redirect("login_view")
        # Now user is authenticated, login it.
        login(request,user)
        return redirect("index")
    return render(request, "login.html")

# logout
def logout_view(request):
    logout(request)
    return redirect("login_view")
    

def register_view(request):
    if request.method =="POST":
        user_name = request.POST.get("user_name")
        first_name= request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        user = User.objects.filter(username=user_name)
        if user.exists():
            messages.error(request,"User already existed")
            return redirect("register_view")
            
        user = User.objects.create(
            username = user_name, 
            first_name=first_name, last_name=last_name
        )
        user.set_password(password)
        user.save()
        messages.success(request,"User created successfully")
        return redirect("login_view")
    
    return render(request, "register.html")

@login_required(login_url="login_view")
# cache for 15 minutes
@cache_page(60 * 15)
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

