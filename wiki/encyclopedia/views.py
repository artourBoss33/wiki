from django.shortcuts import render
from django.http import HttpResponse
from . import util
import random

def index(request):

    if request.method == "POST":

        entry = request.POST["q"]
        
        if entry.casefold() in (list_entry.casefold() for list_entry in util.list_entries()):
            return get_page(entry)

        elif any(entry.casefold() in list_entry.casefold() for list_entry in util.list_entries()):
            related_strings = [string for string in util.list_entries() if entry.casefold() in string.casefold()]
            return render(request, "encyclopedia/related_strings.html", {
                "entries": related_strings
            })

        else:
            return render(request, "encyclopedia/not_found.html")


    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def route_entry(request, name):
    try:
        return get_page(name)
    except:
        return render(request, "encyclopedia/not_found.html")

def new(request):
    
    if request.method == "POST":

        title = request.POST["title"]
        markdown_text = request.POST["markdown_text"]

        if title.casefold() in (list_entry.casefold() for list_entry in util.list_entries()):
            return render(request, "encyclopedia/entry_already_exists.html")

        elif title != "":
            util.save_entry(title, markdown_text)
            return get_page(title)

    return render(request, "encyclopedia/new.html")

def edit(request, name):

    if request.method == "POST":
        util.save_entry(name, request.POST["md_content"])
        return get_page(name)

    if name.casefold() in (list_entry.casefold() for list_entry in util.list_entries()):

        return render(request, "encyclopedia/edit.html", {
            "entry_title": name.capitalize(),
            "textarea_value": util.get_entry(name)
        })

    else:
        return render(request, "encyclopedia/not_found.html")


def random_entry(request):

    return get_page(random.choice(util.list_entries()))

def get_page(name):
    return HttpResponse(f"<title>{name.capitalize()}</title><div style='float: right; font-size: 25px; font-family: sans-serif;'><a href='/edit/{name}'>Edit page</a><br><br><a href='/'>Home</a></div>" +
        util.md_to_html((util.get_entry(name))))