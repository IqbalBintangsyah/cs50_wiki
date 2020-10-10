from random import choice
from django.shortcuts import render
from django import forms
from django.core.files.storage import default_storage
from . import util

class NewPage(forms.Form):
    title =  forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea)

def search(q):
    found = []
    entries = util.list_entries()
    for entry in entries:
        if q.lower() in entry.lower():
            found.append(entry)
    return found

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def showEntry(request, entry):
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
    pageExist = True
    page = util.get_entry(entry)
    if page is None:
        pageExist = False
    return render(request, "encyclopedia/entryPage.html", {
        "pageExist": pageExist,
        "entry": entry,
        "page": util.renderHTML(entry)
    })

def searchResults(request):  
    q = request.GET.get('q')
    found = search(q)
    return render(request, "encyclopedia/searchResult.html", {
        "search": q,
        "entries": found
    })

def new(request):
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entries = util.list_entries()
            if title not in entries:
                util.save_entry(title, content)
                pageExist = True
                return render(request, "encyclopedia/entryPage.html", {
                    "pageExist": pageExist,
                    "entry": title,
                    "page": util.renderHTML(title)
                })
            else:
                return render(request, "encyclopedia/newPage.html",{
                "form":form,
                "warning":"Page already exist!"
            })
    else:
        return render(request, "encyclopedia/newPage.html",{
            "form":NewPage(),
            "warning":"Make a new page"
        })

def edit(request, entry):
    mdEntry = entry + '.md'
    with default_storage.open(f"entries/{mdEntry}", 'r') as f:
        fileContent = f.read()
    form = NewPage({'title': entry, 'content': fileContent})
    return render(request, "encyclopedia/editPage.html",{
        "form":form,
        "entry":entry,
    })
    
def RandomPage(request):
    entries = util.list_entries()
    entry = choice(entries)
    pageExist = True
    page = util.get_entry(entry)
    return render(request, "encyclopedia/entryPage.html", {
        "pageExist": pageExist,
        "entry": entry,
        "page": util.renderHTML(entry)
    })
