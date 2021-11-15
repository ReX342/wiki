from django.shortcuts import render
# Tim
from django.http import HttpResponse
#from .models import ToDoList, Item
from .forms import CreateNewList
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# Tim
#def index(response, id):
#    ls = ToDoList.objects.get(id=id)
#   return render(response, "main/list.html", {"ls":ls})
def home(reponse):
    return render(response, "main/home.html", {})
# Tim
# https://youtu.be/sm1mokevMWk
def create(respone):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})