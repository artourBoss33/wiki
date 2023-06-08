import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

h1 = re.compile("^# (\S|\S.*)$", re.M)
h2 = re.compile("^## (\S|\S.*)$", re.M)
h3 = re.compile("^### (\S|\S.*)$", re.M)
h4 = re.compile("^#### (\S|\S.*)$", re.M)
h5 = re.compile("^##### (\S|\S.*)$", re.M)
h6 = re.compile("^###### (\S|\S.*)$", re.M)

bold1 = re.compile("[*][*](\S|\S.*?\S)[*][*]", re.S)
bold2 = re.compile("__(\S|\S.*?\S)__", re.S)

li = re.compile("^([*]|-) (\S.*)$", re.M)
ul0 = re.compile("^(<li>.*</li>)")
ul1 = re.compile(r"[^(</li>)]\n(<li>\S.*</li>)")
ul2 = re.compile("(<li>\S.*</li>)\n(?!<li>)")
ul3 = re.compile("(<li>\S.*</li>)$")

g1 = re.compile("^([a-zA-Z].*?)\n\n", re.S)
g2 = re.compile("\n\n([a-zA-Z].*?)((\n\n)|$)", re.S)

link = re.compile("\[(\S.*?)\]\((\S+)\)", re.S)

def md_to_html(markdown):

    markdown = h1.sub(r"<h1>\1</h1>", markdown)
    markdown = h2.sub(r"<h2>\1</h2>", markdown)
    markdown = h3.sub(r"<h3>\1</h3>", markdown)
    markdown = h4.sub(r"<h4>\1</h4>", markdown)
    markdown = h5.sub(r"<h5>\1</h5>", markdown)
    markdown = h6.sub(r"<h6>\1</h6>", markdown)
    markdown = bold1.sub(r"<b>\1</b>", markdown)
    markdown = bold2.sub(r"<b>\1</b>", markdown)
    markdown = g1.sub(r"\n<p>\1</p>\n\n", markdown)
    markdown = g2.sub(r"\n<p>\1</p>\n\n", markdown)
    markdown = li.sub(r"<li>\2</li>", markdown)
    markdown = ul0.sub(r"<ul>\1", markdown)
    markdown = ul1.sub(r"\n<ul>\n\1", markdown)
    markdown = ul2.sub(r"\1\n</ul>", markdown)
    markdown = ul3.sub(r"\1\n</ul>", markdown)
    markdown = link.sub(r'<a href="\2">\1</a>', markdown)

    return markdown