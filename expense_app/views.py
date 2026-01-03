
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from . models import User, Expense
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import date



# Create your views here.
def home(request):
    user_idd = request.session.get('user_id')
    if not user_idd:
        return redirect('login_page')
    user = get_object_or_404(User, id=user_idd)

    if request.method == 'POST':
        amount = request.POST.get('amount')
        category = request.POST.get('category')
        ddate = request.POST.get('date')
        Expense.objects.create(user=user,amount=amount,category=category,date=ddate)
        return redirect('home')
    expense = Expense.objects.filter(user = user)
    monthly_expense = expense.annotate(month = TruncMonth('date')).values('month').annotate(total=Sum('amount'))
    category_wise = expense.values('category').annotate(total=Sum('amount'))
    total_expense = expense.aggregate(total=Sum('amount'))['total'] or 0
    this_month = expense.filter(date__month = date.today().month,
                                date__year =date.today().year).aggregate(total=Sum('amount'))['total'] or 0
    today_expense = expense.filter(date = date.today()).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'expense' : expense,
        'monthly_expense' : monthly_expense,
        'category_wise': category_wise,
        'total_expense': total_expense,
        'this_month': this_month,
        'today_expense': today_expense,
        
    }
    return render(request, 'home.html', context)

def register_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phn_no = request.POST.get('phn_no')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {
                'error' : 'email alreay exist',
            }
            return render(request, 'registration.html',context)
        User.objects.create(name = name, email = email, phn_no = phn_no, password = password)
        return redirect('login_page')
    return render(request, 'registration.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            return render(request,'login.html',{'error' : 'incorrect email or password'})

        if user.password == password:
            request.session['user_id'] = user.id
            return redirect('home')
        else:
            return render(request,'login.html', {'error' : 'incorrect email or passsword'})
    return render(request, 'login.html')

def edit_expense(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request,'login.html')
    userr = get_object_or_404(User,id = user_id)
    expense = get_object_or_404(Expense, user = userr, pk = pk)
    if request.method == 'POST':    
        expense.amount = request.POST.get('amount')
        expense.category = request.POST.get('category')
        expense.date = request.POST.get('date')
        expense.save()
        return redirect('home')
    context = {
        'expense' : expense,
    }
    return render(request,'edit_expense.html',context) 

def delete_expense(request, pk):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request,'login.html')
    
    user = get_object_or_404(User, id = user_id)
    exp = get_object_or_404(Expense, user = user, pk = pk)
    
    if request.method == 'POST':
        exp.delete()
        return redirect('home')

