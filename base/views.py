from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# from django.http import HttpResponse

# rooms = [
#     {'id' : 1 , 'name' : 'Let\'s Learn Python'},
#     {'id' : 2 , 'name' : 'Design with Sam'},
#     {'id' : 3 , 'name' : 'Frontend Development'},
# ]


# Create your views here.
def Home(request): 
    rooms = Room.objects.all()
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def Rooms(request, pk):
    room = Room.objects.get(id=pk)

    context = {'room' : room}

    return render(request, 'base/rooms.html', context)

def RoomCreate(request):
    form = RoomForm()

    if request.method == "POST" :
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

def RoomUpdate(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form  = RoomForm(request.POST, instance=room)

        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

def RoomDelete(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect('home')

    context = {'obj' : room}
    return render(request, 'base/delete.html', context)
    