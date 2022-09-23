import TexSoup

OUTDIR = "sivut/content/kirja"
SKIP = ['Kirjoittajat', '12 teesiä työelämästä']

with open("kirja/kirja.tex", 'r') as infile:
    ts = TexSoup.TexSoup(infile)

i = 0
c = 0
this_file = open("dump.md", 'w')
footnotes = []
for t in ts.document:
    #print(i)
    if type(t) == TexSoup.data.TexNode:
        if t.name == "chapter":
            chapter_name = t.text[0]
            if chapter_name in SKIP:
                continue
            c += 1 # Chapter count
            chapter_name_slug = chapter_name.replace(" ", "-")
            chapter_name_slug = chapter_name_slug.lower()
            print(f"New chapter: {chapter_name}\n")
            # Write footnotes
            f = 1
            for footnote in footnotes:
                this_file.write(f"[^{f}]: {footnote}\n")
                f += 1
            footnotes = []
            # Deal with fp
            this_file.close()
            this_file = open(f"{OUTDIR}/{c}-{chapter_name_slug}.md", 'w')
            frontmatter = f"""+++
draft = false
weight = {i}
description = "{{description}}"
title = "{chapter_name}"
bref = ""
toc = false
+++\n\n"""
            frontmatter_written = False
            #this_file.write(frontmatter)
        elif t.name == "sidenote":
            this_text = t.text[0]
            this_text = this_text.replace("\n", " ")
            footnotes += [this_text]
            this_footnote = len(footnotes)
            this_file.write(f"[^{this_footnote}]")
    if type(t) == TexSoup.utils.Token:
        if not frontmatter_written:
            first_sentence = t.text.split(".")[0] + "..."
            first_sentence = first_sentence.replace("\n", " ")
            frontmatter = frontmatter.format(description = first_sentence)
            this_file.write(frontmatter)
            frontmatter_written = True
        this_file.write("\n" + t.text)
    i += 1
this_file.close()