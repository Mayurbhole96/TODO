from django.shortcuts import render , redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        if request.method == 'GET':
            if request.GET.get('query'):
                query = request.GET.get('query', '')
                todos = TODO.objects.filter(title__icontains=query,user = user, is_active = True, is_deleted = False)
                return render(request , 'index.html' , context={'form' : form , 'todos' : todos, 'query': query})
            else:
                start_date = request.GET.get('start_date')
                end_date = request.GET.get('end_date')
                
                if start_date and end_date:
                    todos = TODO.objects.filter(date__date__range=[start_date, end_date],user = user, is_active = True, is_deleted = False)               
                    return render(request , 'index.html' , context={'form' : form , 'todos' : todos, 'start_date': start_date, 'end_date': end_date})

        todos = TODO.objects.filter(user = user, is_active = True, is_deleted = False).order_by('-id')
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos})

def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        context = {
            "form" : form1
        }
        return render(request , 'login.html' , context=context )
    else:
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            context = {
                "form" : form
            }
            return render(request , 'login.html' , context=context )


def signup(request):

    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form" : form
        }
        return render(request , 'signup.html' , context=context)
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)  
        context = {
            "form" : form
        }
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request , 'signup.html' , context=context)



@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else: 
            return render(request , 'index.html' , context={'form' : form})

@login_required(login_url='login')
def edit_todo(request, pk):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        task = get_object_or_404(TODO, pk=pk)

        if request.method == 'POST':
            task.title = request.POST['title']
            task.status = 'P'
            task.save()
            return redirect('home')

        return render(request, 'edit.html', {'task': task})

def delete_todo(request , id ):
    print(id)
    todo = TODO.objects.get(pk = id)
    TODO.objects.filter(id = todo.id).update(is_active = False, is_deleted = True)
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')