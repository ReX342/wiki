import markdown2
# for random
import secrets

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
#RTM: https://docs.djangoproject.com/en/2.2/_modules/django/contrib/auth/decorators/
from django.contrib.auth.decorators import login_required

from . import util
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
        
# trying to write classes
# https://docs.djangoproject.com/en/3.2/topics/forms/ for forms
class NewEntryForm2(forms.Form):
    title = forms.CharField(max_length = 1000, label="Entry title", widget=forms.TextInput(attrs={'class': 'special'}))
    # https://docs.djangoproject.com/en/3.2/ref/forms/widgets/
    content = forms.CharField(widget=forms.Textarea)
    # Figure out how 'edit' fits
    # https://docs.djangoproject.com/en/3.2/ref/forms/fields/#django.forms.BooleanField
    # https://docs.djangoproject.com/en/3.2/ref/forms/fields/
    
    
#This is default code
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
# Our entry function passes a request argument and an entry argument
def entry(request, entry):
    markdowner = Markdown()
    # use get_entry function already provided (to get the content)
    entryPage = util.get_entry(entry)
    # in case the page doesn't exist yet.
    if entryPage is None:
        #we don't need to read the content, so we just display another html page
            return render(request, "encyclopedia/404.html", {
                #we can still mention the title of what we were looking for
                    "entryTitle": entry
            })
    else:
        #Assuming we're in edit mode
        if request.method == "POST":
            # Take code from newEntry            
            form = NewEntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                    util.save_entry(title,content)
                    return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            
        #if we do have an entry, show the page
        return render(request, "encyclopedia/entry.html", {
            #Make sure it's marked down
            "entry":  markdowner.convert(entryPage),
            #the entry of the title is keyword entry
            "entryTitle": entry
        })

def newEntry(request):
    #we want to upload data so we'll be using post
    if request.method == "POST":
        #everything we requested is in post and can be formatted onto a form
        form = NewEntryForm(request.POST)
        if form.is_valid():
            #have this format read out title
            title = form.cleaned_data["title"]
            #and its (also cleaned out) content
            content = form.cleaned_data["content"]
            #getting an entry has a function, but if there's no title or we're editing, then
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                #we save our title and content
                util.save_entry(title,content)
                #we look at our entry
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            else:
                #if there's a (not None) title, then it exists (under that title as an entry)
                
                # Here's where we want to be taken to the already existing entry after the error
                #return render(request, "encyclopedia/newEntry.html", {
                #"form": form,
                #"existing": True,
                #"entry": title
                # I'll be using markdowner in my render{} later
                markdowner = Markdown()
                return render(request,"encyclopedia/entry.html", {
                #I don't want to go to 404.html, I want to go to path  wiki/<str:entry>, so I go to entry.html
                 
                #Make sure it's marked down
                # "entry":  markdowner.convert(entryPage),                
                # entryPage = util.get_entry(entry) 
                "entry":  markdowner.convert(util.get_entry(title)),
                #the entry of the title is keyword entry
                "entryTitle": title,
                # if condition for alerting user the entry already exists
                "existing": True
                })
                
                
                
        else:
            #if it doesn't exist and can't be created based on the form
            return render(request, "encyclopedia/newEntry.html", {
                #it being the form
                "form": form,
                #it doesn't exist
                "existing": False
            })
    else:
        return render(request,"encyclopedia/newEntry.html", {
            #otherwise, we're just trying to create a entry form
            "form": NewEntryForm(),
            #because it doesn't exist yet
            "existing": False
        })             

def edit(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render (request, "encyclopedia/404.html", {
            "entryTitle": entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/entry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })
            
def random(request):
    entries = util.list_entries()
    # This is why we imported Secrets
    randomEntry = secrets.choice(entries)
    # Arbitrary keyword arguments can be passed in a dictionary to the target view.
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))
                               
def search(request):
    value = request.GET.get('q','')                               
    if(util.get_entry(value) is not None):
        # worth figuring out the kwargs
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': value}))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            # util.get_entry(entry)
            if value.upper() in util.get_entry(entry).upper():
                subStringEntries.append(entry)
                               
        return render(request, "encyclopedia/results.html", {
            "entries" : subStringEntries,
            "search": True,
            "value": value,
            "keyword": value
})    
