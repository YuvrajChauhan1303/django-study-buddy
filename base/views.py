from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .models import Room, Topic, User
from .forms import RoomForm

from django.http import HttpResponse

# rooms = [
#     {'id' : 1 , 'name' : 'Let\'s Learn Python'},
#     {'id' : 2 , 'name' : 'Design with Sam'},
#     {'id' : 3 , 'name' : 'Frontend Development'},
# ]


# Create your views here.
def Home(request): 
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q) | Q(name__icontains=q) | Q(desc__icontains=q)) 

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count}
    return render(request, 'base/home.html', context)

def Rooms(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room' : room}

    return render(request, 'base/rooms.html', context)

@login_required(login_url = 'login')
def RoomCreate(request):
    form = RoomForm()

    if request.method == "POST" :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def RoomUpdate(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('You\'re not Allowed Here!')

    if request.method == "POST":
        form  = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url = 'login')
def RoomDelete(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    if request.user != room.host:
        return HttpResponse('You\'re not Allowed Here!')

    context = {'obj' : room}
    return render(request, 'base/delete.html', context)
    
def LoginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist.")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        else:
            messages.error(request, "Username OR Password does not exist.")

    context = {'page' : page}
    return render(request, 'base/login_register.html', context)

def LogoutUser(request):
    logout(request) 
    return redirect('login')

def RegisterUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration!')
    else:
        form = UserCreationForm()

    return render(request, 'base/login_register.html', {'form': form})