# Making my own Wiki
Using Django

Steps I went through:
1) Get Base file ("django-admin startproject PROJECT_NAME" when from scratch) from CS50
2) pip3 install Django
3) python manage.py runserver
4) Look at http://127.0.0.1:8000/'s Wiki (only Home URL works but it indicates we should make a new page and 5 topics)
5) python manage.py startapp APP_NAME (encylopedia? and/or just wiki)
6) Create Page: Form (see Notes/3)
7) {% extends "tasks/layout.html" %} (change tasks)
8) Follow along with Lecture and make notes/copy the examplary code

9) Check in index.html to Create New Page
10) End up(9) in layout.html and copy Home code
11) https://cs50.harvard.edu/web/2020/projects/1/wiki/

12) If you want to allow for an HTML string to be outputted, you can do so with the safe filter (as by adding |safe after the variable name you’re substituting).
13) Follow Youtube for inspiration. Get pages overview lighting up

14) Request Method: GET (404)
15) put (assignment) Pages in (html) pages .

Entry Page: Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
The view should get the content of the encyclopedia entry by calling the appropriate util function.

If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.

Index Page: Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.
Search: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.

If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.

If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
Clicking on any of the entry names on the search results page should take the user to that entry’s page.

New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.

Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
Users should be able to click a button to save their new page.
When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.

Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
The user should be able to click a button to save the changes made to the entry.
Once the entry is saved, the user should be redirected back to that entry’s page.

Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.
Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the Markdown to HTML conversion without using any external libraries, supporting headings, boldface text, unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.

16) get entries working instead from YT instead of figuring it out myself
17) Hope to do the tutorial django assignment first and figure out how to display new pages later

18) Don't forget about:    {{ entry|safe }} in newentry.html
19) https://www.w3schools.com/tags/tag_textarea.asp

20) Start watching the Lecture for the third time: https://docs.djangoproject.com/en/3.2/ref/request-response/
21) NoReverseMatch: is not a registered namespace
22) Got confused on:
            # with open(entry, "r") as f:
            #     content = f.read()
            #     #if value.upper() in entry.upper():
            #     if value.upper() in content.upper():
            #         substStringEntries.append(entry)
             
23) non exist.page doesn't work yet.
24)                 <form action="/search">

25) Write the 404 page: It doesn't exist yet.
26) Fix Titles (# and ## in .md files: Contrast default to new entries)

27) newEntry versus NewEntry (<a href="{% url 'newEntry' %}"> to be precise; otherwise the page wouldn't load)
28) Begin to want to break assignment down into pieces:

# Entry Page: 
Visiting /wiki/TITLE, where TITLE is the title of an encyclopedia entry, should render a page that displays the contents of that encyclopedia entry.
in urls.py

```python
urlpatterns = [
    path("wiki/<str:entry>", views.entry, name="entry"),
```

# The view should get the content of the encyclopedia entry by calling the appropriate util function.
in views.py
```python
def entry(request, entry):
    entryPage = util.get_entry(entry)
```
# If an entry is requested that does not exist, the user should be presented with an error page indicating that their requested page was not found.
(continued) in views.py
    if entryPage is None:
        #we don't need to read the content, so we just display another html page
            return render(request, "encyclopedia/404.html", {
                #we can still mention the title of what we were looking for
                    "entryTitle": entry
            })
and 404.html
{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{ entryTitle }}?
{% endblock %}

{% block body %}
<h2> Looks new to me...</h2>
<p>
It looks like your entry doesn't exist... yet!</p>
<p>
Click <a href="{% url 'newEntry' %}">here</a> to create your entry, making our wiki bigger and better :D</p>
{% endblock %}

# If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.
finish entry in views.py
    else:
        #if we do have an entry, show the page
        return render(request, "encyclopedia/entry.html", {
            #Make sure it's marked down
            "entry":  markdowner.convert(entryPage),
            #the entry of the title is keyword entry
            "entryTitle": entry
        })

29) Figure out ```python urlpatterns = [] ``` notation
# Index Page: Update index.html such that, instead of merely listing the names of all pages in the encyclopedia, user can click on any entry name to be taken directly to that entry page.

{% block body %}
    <h1>All Pages</h1>

    <ul>
        {% for entry in entries %}
            <a href = "/wiki/{{ entry}}" ><li>{{ entry }}</li></a>
        {% endfor %}
    </ul>

{% endblock %}
# Search: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry.
add to layout.html
                <form action="/search">
to views.py
```python
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
```
urls.py
    path("search", views.search, name="search")
create results.html
{% extends "encyclopedia/layout.html" %}

{% block title %}
    Encyclopedia: Search Results
{% endblock %}

{% block body %}
    <h1>Search Results: {{ keyword }} </h1>

    <ul>
        {% for entry in entries %}
            <a href="/wiki/{{ entry }}" ><li>{{ entry }}</li></a>
        {% endfor %}
    </ul>

{% endblock %}
# If the query matches the name of an encyclopedia entry, the user should be redirected to that entry’s page.
create entry.html
{% extends "encyclopedia/layout.html" %}

{% block title %}
    {{ entryTitle }}
{% endblock %}

{% block body %}
    <h1> {{ entryTitle }} </h1>
    <a class="btn btn-outline-secondary" href="/wiki/{{ entryTitle }}/edit" role="button">Edit</a>
    {{ entry|safe }}
{% endblock %}
# If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results page that displays a list of all encyclopedia entries that have the query as a substring. For example, if the search query were ytho, then Python should appear in the search results.
earlier in entry.html we used for in logic
        {% for entry in entries %}
            <a href="/wiki/{{ entry }}" ><li>{{ entry }}</li></a>
        {% endfor %}
# Clicking on any of the entry names on the search results page should take the user to that entry’s page.
    <a href="/wiki/{{ entry }}" ><li>{{ entry }}</li></a>   
# New Page: Clicking “Create New Page” in the sidebar should take the user to a page where they can create a new encyclopedia entry.
copy index code block syntaxis from earlier(index) in layout.html
                    <a href="{% url 'newEntry' %}">Create New Page</a>                    

# Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
get views.py working
    from markdown2 import Markdown
    
def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
            else:
                return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": True,
                "entry": title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request,"encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "existing": False
        })             
# Users should be able to click a button to save their new page.
create newEntry.html
    {% extends "encyclopedia/layout.html" %}

    {% block title %}
        Create a New Page
    {% endblock %}

    {% block body %}
        <h1>New Entry</h1>
        <form action="{% url 'newEntry' %}" method="post">
            {% csrf_token %}
            {{ form }}
            {{ entry|safe }}        
            <input type="submit">
        </form>
    {% endblock %}
# When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
30) Write If entry == condition then "Already exists!" error message. 
# Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
It already does this by default.
# Edit Page: On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
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
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })
# The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
31) Collect socks??
# The user should be able to click a button to save the changes made to the entry.
32) Profit from step 30 to 31
# Once the entry is saved, the user should be redirected back to that entry’s page.

# Random Page: Clicking “Random Page” in the sidebar should take user to a random encyclopedia entry.
layout.html
                <div>
                    <a href="{% url 'random' %}">Random Page</a>              
                </div>

add to views.py
    import secrets

    def random(request):
        entries = util.list_entries()
        # This is why we imported Secrets
        randomEntry = secrets.choice(entries)
        # Arbitrary keyword arguments can be passed in a dictionary to the target view.
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': randomEntry}))
# Markdown to HTML Conversion: On each entry’s page, any Markdown content in the entry file should be converted to HTML before being displayed to the user. You may use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.


Topic of Missing libraries:
urls.py
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random"),
    path("search", views.search, name="search")

view.py
    from django.shortcuts import render
    from django.http import HttpResponseRedirect
    from django import forms
    from django.urls import reverse

    class NewEntryForm(forms.Form):
        title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
        content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
        edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)
# Challenge for those more comfortable: If you’re feeling more comfortable, try implementing the Markdown to HTML conversion without using any external libraries, supporting headings, boldface text, unordered lists, links, and paragraphs. You may find using regular expressions in Python helpful.
33) *Sweats profusely*
forms.py
    from django import forms

    class CreateNewList(forms.Form):
        name = forms.CharField(label="name", max_lenght=200)
        check = forms.BooleanField(required=False)
34) fix py -m venv project-name         
35) See above:
# When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    30) Write If entry == condition then "Already exists!" error message.
in newEntry.html ?
    {% if get_entry(title) == None %}
        pass
    {% else %}
        Alert("Seems like we already have an entry!")
        # https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
    {% endif %}
[or
    {% if entry is not in entry %}]
or in .py
    from django.contrib import messages
        messages.error(request, 'Entry already exists in our wiki!')
    {% if messages %}
    <ul class="messages">
        {% for message in messages %}
        <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}
## When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
36)
Solution steps 25, 28:
For 404: 
return HttpResponseNotFound('<h1>Page not found</h1>')
https://docs.djangoproject.com/en/3.2/topics/http/views/#django.http.Http404

        {% if entry %}
            We already have that entry
        {% endif %}

## When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
37) if entry exists, show alert to user
add to entry.html
    {% if existing %}
    <h2> We already have an entry for this topic!</h2>
     {% endif %}

38) cliking edit button gives us "New Entry" at the top
# On each entry page, the user should be able to click a link to be taken to a page where the user can edit that entry’s Markdown content in a textarea.
# The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
The content of textarea is fine. But a nice feature would be to see the title instead of "New Entry" above.

39) Looks finished. Let's look back if we possible didn't solve any of the previous steps:
    Styling: Isn't saved when editing.
    Do I remove safe (HTML formatting) from         <p> {{ entry|safe }} </p> ?

40) Rebuild.
#Got stuck on git again
41) have Placeholder="# {{title}}" preview in the first line of content (on NewEntry.html)
== supposed solution (to): double title's ARE a good thing AND I'm doubling down!
42) How did I come up with forms.py and is it linked/needed for anything?N
class CreateNewList(forms.Form):
    name = forms.CharField(label="name", max_lenght=200)
    check = forms.BooleanField(required=False)
43) Using Lecture4 video (assignment code also contains this source code)
in views.py ; you're importing login, logout
# def login_view(request):
def NewEntry(title, content):
# At least this way the content doesn't get lost: The user could save with another title
else:
#    return render(request, "users/login.html", {
    return render(request, "encyclopedia/NewEntry, {
        "message" : An entry already exists with this title!
    })

in NewEntry.html
{ % block body %}
    {% if message %}
        <div>{{ message }}</div>
    {% endif %}

44) Noticed in lecture 4 in 43)
in views.py
    from django.contrib.auth import authenticate, login, logout
Only used in login/logout. Not needed in wiki. Only in next assignment!
Correction of 32) needed before any profit can be seen: This readme is a partial loss!
# This used to be in missing libraries, it was removed. Proftis ensured!
45) Side by side apps in a project is how Django works: Why am I making the git part so hard on myself?
# Surely the next git project I open will fail (it's always the one I'm working on that keeps working)
46) venv ?

47) Watching Javascript Lecture 5
New Entry.html
<script> function already_exists() {
    if Existing == True {
    alert('We already have an entry for that topic!')
    }
}
Put following into submit button?
<button onclick="already_exists()">Click here to execute the function hello</button>
This way, the user doesn't lose everything they've typed.
48) Better yet, use onsubmit="already_exists in listening for events (so add it to submit button instead of vice versa)
<script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelector('form').onsubmit = function() {}
    })
49) Convinced no JS should be used yet, fixing the old bug of text next to submit button instead of taking the user to the next page should be unfixed error warning that doesn't make the user lose everything.
50) https://docs.djangoproject.com/en/3.2/ref/forms/fields/
name = forms.CharField(error_messages={'required': 'Please enter your name'})
name.clean('')
This could be our alert (flash from flask/instead of JavaScript or custom/rudimentary solution)
title = forms.CharField(error_messages={'Already_exists': 'We already have an entry by that title'})
title.clean('')
This only works for checking if empty? Only is_valid protects against CSRF?
51)     content = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}))
This inpunt-field is too big (low on screen). We're given that css class though in styles.css
it also feels like this is related to:
# Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
duckduckgo:
https://www.bitdegree.org/learn/bootstrap-col-md
https://www.tutorialrepublic.com/twitter-bootstrap-tutorial/bootstrap-grid-system.php
https://getbootstrap.com/docs/5.0/forms/form-control/
52) Changelog: (Branch suggested: Almost clean slating codebase: Made style ugly)
Removed forms.py and need for step 33
53) Disabled submit button for when it already exists (not needed: Submit checks if it exists and should remain being able to do so): 
<input class="form-control" type="text" placeholder="Disabled input" aria-label="Disabled input example" disabled>
<input class="form-control" type="text" value="Disabled readonly input" aria-label="Disabled input example" disabled readonly>
Unclear to me why the first one is greyed out anyway.
54) Tasks from lecture indicates CharField for passing data(txt) with .POST
from django import forms
...
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
...
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })    
             
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
55) in views.py
# Create your views here.
So we create all our pages here (Solution to earlier problem of how many pages to make and yes we should make and html named after every def in views.py: That's what it's there for: To view our [extended layout].html)
cfr. 6) 9) 13) Pages. 7) 10) how to make the .html (mirrored in .py in question) page
56) Question 29 lingering: python annotation/styling in this document.
Other than that almost ready (where to start 52) + clean slate 55)) 
57) I did not set up max_length for CharField ! (How is this possible?)
https://docs.djangoproject.com/en/3.2/intro/tutorial02/
Some Field classes have required arguments. CharField, for example, requires that you give it a max_length. That’s used not only in the database schema, but in validation, as we’ll soon see.
58) https://docs.djangoproject.com/en/3.2/ref/forms/api/
Form.errors
On Alerting/warning user: warning entry already exists!
59) https://docs.djangoproject.com/en/3.2/ref/models/querysets/
Author.objects.values_list('name', 'entry__headline')
<QuerySet [('Noam Chomsky', 'Impressions of Gaza'),
 ('George Orwell', 'Why Socialists Do Not Believe in Fun'),
 ('George Orwell', 'In Defence of English Cooking'),
 ('Don Quixote', None)]>
60) CharField has max_length as a requirement in models only.
Doesn't require max_length as an attribute in classes that are made elsewhere:
https://docs.djangoproject.com/en/3.2/ref/forms/fields/
from django import forms
class CommentForm(forms.Form):
...     name = forms.CharField(label='Your name')
...     url = forms.URLField(label='Your website', required=False)
...     comment = forms.CharField()
>>> f = CommentForm(auto_id=False)
>>> print(f)
61) Search:
https://docs.djangoproject.com/en/3.2/topics/db/search/
62) Alert user
https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.INFO: '',
    50: 'critical',
}
Change to:
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
messages.WARNING: 'Entry already exist',
}