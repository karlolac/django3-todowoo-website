from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from .forms import TodoForm
from .models import Todo

def home(request):
    return render(request,'todo/home.html')


def signupuser(request):
    if request.method=='GET':
        return render(request,'todo/signupuser.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'That username has allreaday been taken.'})
        else:
            return render(request,'todo/signupuser.html',{'form':UserCreationForm(),'error':'Passwords did not match'})


def currenttodos(request):
    todos=Todo.objects.filter(user=request.user,date_completed__isnull=True)
    return render(request,'todo/currenttodos.html',{'todos':todos})


def logoutuser(request):
    if request.method =='POST':
        logout(request)
        return redirect('home')
    

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('currenttodos')
        else:
            return render(request, 'todo/loginuser.html', {'form': form,'error': 'Username or password is incorrect.'})
        

def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm ()})

    else:
        try:
            form= TodoForm(request.POST)
            newTodo=form.save(commit=False)
            newTodo.user=request.user
            newTodo.save()
            return redirect ('currenttodos')
        except ValueError:
            return render(request,'todo/createtodo.html',{'form':TodoForm(),'error':"Bad data passed in"})