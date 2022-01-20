from django.shortcuts import render, redirect

from django.db.models import Sum

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import NewUserForm
from .models import MyWallet


def homepage(request):
    return render(request=request, template_name='app_wallet/home.html')


def register_request(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('app_wallet:homepage')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    return render(request=request, template_name='app_wallet/register.html', context={'register_form': form})


def login_request(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}.")
                return redirect('app_wallet:homepage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request=request, template_name='app_wallet/login.html', context={'login_form': form})


def add_request(request):
    if request.method == 'POST':
        payment = MyWallet(admission=request.POST.get('admission'),
                           consumption=request.POST.get('consumption'),
                           description=request.POST.get('description'),
                           users_date=request.POST.get('users_date'),
                           username_id=request.user.id)
        payment.save()
        return redirect('app_wallet:homepage')
    return render(request=request, template_name='app_wallet/add.html')


def find_request(request):
    if request.method == 'POST':
        payments = MyWallet.objects.filter(users_date__range=[request.POST.get('date_from'),
                                                              request.POST.get('date_to')],
                                           username_id=request.user.id).order_by('users_date')
        admission__sum = payments.aggregate(Sum('admission'))
        consumption__sum = payments.aggregate(Sum('consumption'))
        return render(request=request, template_name='app_wallet/report.html',
                      context={
                          'payments': payments,
                          'admission__sum': admission__sum,
                          'consumption__sum': consumption__sum
                      })
    return render(request=request, template_name='app_wallet/find.html')


def show_request(request):
    payments = MyWallet.objects.all().order_by('users_date').filter(username_id=request.user.id)
    admission__sum = payments.aggregate(Sum('admission'))
    consumption__sum = payments.aggregate(Sum('consumption'))
    return render(request=request, template_name='app_wallet/show.html',
                  context={
                      'payments': payments,
                      'admission__sum': admission__sum,
                      'consumption__sum': consumption__sum
                  })


def edit_request(request):
    if request.method == 'POST':
        if request.POST.get('data') == 'admission':
            MyWallet.objects.filter(id=request.POST.get('id')).update(admission=request.POST.get('new_data'))
        elif request.POST.get('data') == 'consumption':
            MyWallet.objects.filter(id=request.POST.get('id')).update(consumption=request.POST.get('new_data'))
        elif request.POST.get('data') == 'description':
            MyWallet.objects.filter(id=request.POST.get('id')).update(description=request.POST.get('new_data'))
        elif request.POST.get('data') == 'date':
            MyWallet.objects.filter(id=request.POST.get('id')).update(users_date=request.POST.get('users_date'))
        return redirect('app_wallet:homepage')
    return render(request=request, template_name='app_wallet/edit.html')


def delete_request(request):
    if request.method == 'POST':
        MyWallet.objects.filter(id=request.POST.get('id')).delete()
        return redirect('app_wallet:homepage')
    return render(request=request, template_name='app_wallet/delete.html')


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('app_wallet:login')
