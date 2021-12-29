import re
from django.shortcuts import render
from . import util
import markdown
from markdown2 import Markdown
import random

markdowner = Markdown ()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


# Gets the page that was called
def entry(request, title):
    page = util.get_entry(title)

    # For pages that does not exist
    if not page:
        return render(request, "encyclopedia/PageDoesNotExist.html", {
            "entry": md_to_html(title),
            "page_title": title
        })

    # When the process found the page request
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": md_to_html(title),
            "page_title": title
        })


# Coverts MD to HTML
def md_to_html(title):
    entry = util.get_entry(title)
    html = markdown.markdown(entry) if entry else None
    return html

# Search for a match page
def search(request):
    if request.method == 'GET':
        name = request.GET.get('q')
        search = []

        # Checks if what was searched for is contained in existing pages 
        for entry in util.list_entries():
            if name.upper() in entry.upper(): # Add to the search list if it's true
                search.append(entry)
        
        # Checks if what was searched is, in fact, an existing page 
        for entry in util.list_entries():
            if name.upper() == entry.upper(): # Show the page if it's true
                return render(request, "encyclopedia/entry.html", {
                    "entry": md_to_html(name),
                    "page_title": name
                })
            elif search == []: # Case there are no matches show "Non existing page"
                return render(request, "encyclopedia/PageDoesNotExist.html", {
                    "page_title": name
                })
            else: # Show matches of what you searched
                return render(request, "encyclopedia/search.html", {
                    "entry": search,
                    "existents": util.list_entries()
                })

# Open up the form to create a new page
def new_page(request):
    return render(request, "encyclopedia/newPage.html", {}
                  )

# Save the new page
def save_page(request):
    if request.method == 'POST':
        title = request.POST['title']
        reserv = str(title)
        body = request.POST['body']
        exists = False

        # Checks if the page already exists
        for page in util.list_entries():
            if reserv.upper() == page.upper():
                exists = True
                      
        if exists == True: # If the page already exists, show an error
            return render(request, "encyclopedia/exists.html", {
                "title": title
            })
            
        else: # Calls the fuction that save the new page and then show it
            util.save_entry(title, body)
            return render(request, "encyclopedia/entry.html", {
                "entry": md_to_html(title),
                "page_title": title
            })

# Edit an existent page of the app
def edit_page(request,title):
    bodyEntry = util.get_entry(title)
    return render(request, "encyclopedia/editPage.html", {
        "entry": title,
        "bodyEntry": bodyEntry
    })

# Save the edited page
def save_edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        if body != md_to_html(title):
            util.save_entry(title, body)
        return render(request, "encyclopedia/entry.html", {
            "entry": md_to_html(title),
            "page_title": title
        })
        
# Random page
def random_page(request):
    entries = []
    for page in util.list_entries():
        entries.append(page)
    chosen = random.choice(entries)
    return render(request, "encyclopedia/entry.html",{
        "entry": md_to_html(chosen),
        "page_title": chosen
    })