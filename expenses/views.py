from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from .middlewares import auth,guest
from expenses.models import Expense
from .forms import MyForm,UserRegistrationForm
from django.db.models import Sum,F


@guest
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})
@guest
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username':'', 'password':''}
        form = AuthenticationForm(initial = initial_data)
    return render(request, 'authentication/login.html' ,{'form':form})
# Only logged-in users can access
def dashboard_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            expense_id = request.POST.get('expense_id')
            delete_expense = request.POST.get('delete_expense')
            if delete_expense:
                # Delete the expense
                expense = get_object_or_404(Expense, id=delete_expense, user=request.user)
                expense.delete()
                return redirect('dashboard')
            elif expense_id:
                # Update existing expense
                expense = get_object_or_404(Expense, id=expense_id, user=request.user)
                expense.category = form.cleaned_data['category']
                expense.cost = form.cleaned_data['cost']
                expense.description = form.cleaned_data['description']
                expense.save()
            else:
                # Create new expense
                expense = Expense(
                    user=request.user,
                    category=form.cleaned_data['category'],
                    cost=form.cleaned_data['cost'],
                    description=form.cleaned_data['description']
                )
                expense.save()
        return redirect('dashboard')
    else:
        form = MyForm()

    expenses = Expense.objects.filter(user=request.user).order_by(F('created_at').desc())
    total_expenses = expenses.aggregate(Sum('cost'))['cost__sum'] or 0
    total_expense_count = expenses.count()

    return render(request, 'dashboard.html', {'form': MyForm(), 'expenses': expenses, 'total_expenses': total_expenses, 'total_expense_count': total_expense_count})




def logout_view(request):
    logout(request)
    return redirect('login')




