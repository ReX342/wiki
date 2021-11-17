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
urlpatterns = [
    path("wiki/<str:entry>", views.entry, name="entry"),
# The view should get the content of the encyclopedia entry by calling the appropriate util function.
in views.py
def entry(request, entry):
    entryPage = util.get_entry(entry)
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