#!/bin/env python3
from bs4 import BeautifulSoup
from requests import get
from sys import argv

# World's dumbest command line arguments parser
if len(argv) > 1:
    if len(argv) == 2:
        startarticlerange = 1
        endarticlerange = int(argv[1])
    else:
        if len(argv) == 3:
            startarticlerange = int(argv[1])
            endarticlerange = int(argv[2])
else:
    print("Usage:", argv[0], "[rangestart] rangeend")
    exit()

# Main Program
for i in range(startarticlerange, endarticlerange + 1):
    print("Fetching article:", str(i))
    r = get("https://what-if.xkcd.com/" + str(i))

    if r.status_code != 200:
        print(r.status_code, "Error fetching article")
        continue

    print("Reading...")
    maintext = BeautifulSoup(r.text, "html.parser").find(id="entry-wrapper")

    print("Parsing...")
    title = maintext.find(id="title").get_text()
    towrite = title + "\n"

    # Get rid of references, otherwise there's gonna be links everywhere
    # The way references are made have changed thoughout the blog's lifetime, this gets rid of the annoying ones in the early articles
    for j in maintext.find(id="entry").find_all(class_="ref"):
        j.decompose()

    for k in maintext.find(id="entry").children:
        if k != "\n":
            if k.name == "img":
                towrite += "[" + k.get("title") + "]\n\n"
            else:
                towrite += k.get_text().replace("\n", " ") + "\n\n"
                # .replace("\n", " "): in some early articles, new lines were added to fit the text onto the page.
                # Since i wanted plain text for all screens, i get rid of the new lines

    print("Fixing unicode...")
    # Code based off of https://dan.hersam.com/tools/smart-quotes.php
    toreplace = {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00A0": " "
    }
    for l in toreplace:
        towrite = towrite.replace(l, toreplace.get(l))

    print("Writing...")
    f = open(str(i).zfill(3) + "-" + title.replace(" ", "-") + ".txt", "w")
    f.write(towrite[:-1])
    f.close()

