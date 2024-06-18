from django.shortcuts import render
from .models import Room
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
