---
date: "2023-07-09"
layout: post
title: "TIL: Obsidian, and integrating it with Zotero"
categories: [writing, research, TIL]
image: obsidian-research-note-page.png
---

I've long been interested in how best to store knowledge; so much that I wrote about it in [this post]("../managing-public-sector-knowledge/managing-public-sector-knowledge.qmd") (in the context of the public sector). Today I learned how to combine Obsidian and Zotero to make taking notes about research literature easier and more effective!

> Note: this is being posted under a tag called TIL or "today I learned". These are shorter format posts that lower the barrier to blogging and capture a mini piece of learning. The idea for TILs has been inspired by Simon Willison's own [TIL posts](https://til.simonwillison.net/). You can find the first TIL [here](../til-how-to-break-xml/index.md).

## Storing knowledge flexibly

One of the frustrations of the generally-excellent Microsoft OneNote, which I normally use for notes, is that it uses *mutually exclusive* pages for content. This means that you can't have the same atomic piece of information (eg a note on a particular paper) filed under two different titles or concepts.

There are a couple of potential solutions to this. You could use a notes system that is label-based rather than file-based. Then an atomic piece of information can be labelled two ways. Another way to solve it is to create links between concepts, and this is the way that popular open-source note-organising software [Obsidian](https://obsidian.md/) uses, so I thought I'd give it a try.

I'm new to Obsidian but have had my eye on it for a while because it uses Markdown. Apart from its simplicity, the markdown format is FAIR: findable, accessible, interoperable, and re-usable. Obsidian also happens to free and open source software, which can have benefits such as large numbers of users and creators focused on making the software as useful as possible (there are downsides too, naturally).

Obsidian describes itself as "the private and flexible note‑taking app that adapts to the way you think", and indeed you have to specify where to store the notes you create. It acts as a fantastic front-end to a folder full of markdown files (called 'vaults'), essentially. But it does additionally introduce the double-square bracket link, ``[[concept]]``, which allows you to connect ideas *across* different atomic notes. Obsidian will display this in a graph too—helping you to visualise the space of ideas you're working in. Early days, but so far I've been impressed.

## Integrating Zotero

You might not be familiar with [Zotero](https://www.zotero.org/), but it's an excellent, open-source programme for collecting and organising research literature in the form of citations (for example, .bib files) *and* the PDFs of the actual papers. It's basically a database of your research literature, but it (very helpfully) also tracks any notes you might make on a paper *and* automatically extracts any text you highlight in a PDF into plain-text notes.[^1]

[^1]: It does some of what Mendeley did in its hey day, but is a lot better.

Now, imagine you want to use a hot key to *automatically* create an Obsidian note page that contains, for a specific paper, i) metadata on that paper, ii) notes you've made in Zotero on that paper, and iii) any annotations you made in Zotero on that paper. And imagine that, as well as all that, every time you need to link to a paper from your Zotero library that you already turned into an Obsidian note, you could just start typing `@` and get a drop down list of all your papers. **Well, amazingly, you *can* do all of this**. Honestly, it's a revelation.

If you want to achieve this research-note-taking zen, you'll need to follow a few steps. First, you'll need to install Zotero and Obsidian, and a couple of add-ons:

- the better bibtex add-on for Zotero
- the Zotero Integration plug-in for Obsidian

I then configured a bunch of settings:

- In Zotero &rarr; Tools &rarr; Better Bibtex &rarr; Open Better Bibtex Settings, I changed the citation key formula to `auth.lower + '_' + shorttitle(1,1).lower + '_' + year` to get a paper like *Hörmann, Wolfgang, and Josef Leydold. "Continuous random variate generation by fast numerical inversion." ACM Transactions on Modeling and Computer Simulation (TOMACS) 13, no. 4 (2003): 347-362.* to have a citekey of the form "hormann_continuous_2003".
- In Obsidian &rarr; Settings &rarr; Zotero Integration, I changed the 'Note Import Location' to a folder called `auto-notes-on-research`. This is for the built-in notes importer, which is very bare bones and I don't expect to use, so this is mainly to ensure there's no conflict between notes created this way and the way we're about to create with custom settings.
- I hit `Add Import Format` under Obsidian &rarr; Settings &rarr; Zotero Integration. I changed the name to "import-research-notes", set the output path to `notes-on-research/{{citekey}}.md`, the bibliography style to *Nature* (which will usually be pre-installed with Zotero), and set the template to a markdown template that I'll include at the end of the post. The markdown template is important: it controls what you'll see when you import research as a note.
- I went to Obsidian &rarr; Settings &rarr; Appearance &rarr; CSS snippets, opened the folder, and created a file I called `style.css`. I filled it with the contents at the end of this blog post, and then hit refresh.
- I then went to Obsidian &rarr; Settings &rarr; Hotkeys, and typed "Zotero Integration: import-research-notes" into the search bar. I added a <kbd>⇧ Shift</kbd> + <kbd>⌃ Control</kbd> + <kbd>c</kbd> hotkey for import-research-notes.

Right, if you've done all that you can enjoy your new setup. I realise it's a bit confusing so I'll spell out the workflow a bit more now:

1. In Obsidian, hit your hotkey, perhaps <kbd>⇧ Shift</kbd>+<kbd>⌃ Control</kbd>+<kbd>c</kbd> if you used the same setup as me.
2. You should see a search bar pop up in Zotero. Type in anything from the paper you'd like to include, select it with the arrow keys, then hit return.
3. In the `notes-on-research` subfolder of your Obsidian vault, you should now have a page for your paper (named with the citekey)!
4. If you want to link to this page once created, you can either use the standard double brackets or `@`, search for the paper, and then hit <kbd>⌥ Option</kbd> + <kbd>↵ Return</kbd>.

If for any reason you don't wish to use the hotkey, then you can click on the command palette and then type in Zotero, then select "Zotero Integration: import-research-notes". Then proceed with steps 2 and 3.

## Result 🔥

I've done an example run on a single paper, and this is the result:

![Example research page from an Obsidian note](obsidian-research-note-page.png)

You can see a note that has been made on the paper overall, and an annotation (which inherits the colour you used in Zotero originally) that also has a comment.

The way the template is put together, future updates to the paper will be added when you re-import it.

Later on, if you need to link to the Obsidian note on this then just use the double-bracket format. This paper has citekey `devocht_conceptualising_2021` so we would use `[[devocht_conceptualising_2021]]` to link to it.

That's it for the main post—pretty amazing tech, I think you'll agree, though a bit fiddly to set up. If you have any tips or strategies for using Zotero and Obsidian together, let me know!

## Templates

As promised, here are the templates I used, which I got from [nocona71 on github](https://github.com/nocona71/obsidian-literature-note), but tweaked a little (only a little) for my needs.

The contents of `zotero-import-template.md`, which is in a subdirectory I called `templates`.

```markdown
### {{title}}
{{" "}}
year: {{date | format ("YYYY")}}
tags: research
authors: {{authors}}
{{" "}}
Abstract:  {{abstractNote}}
{{" "}}
{{pdfZoteroLink}}
{{" "}}
{#- infer latest annotation Date -#}
{% macro maxAnnotationsDate() %}
   {%- set tempDate = "" -%}
	{%- for a in annotations -%}
		{%- set testDate = a.date | format("YYYY-MM-DD#HH:mm:ss") -%}
		{%- if testDate > tempDate or tempDate == ""-%}
			{%- set tempDate = testDate -%}
		{%- endif -%}
	{%- endfor -%}
	{{tempDate}}
{%- endmacro %}
{# infer earliest annotation date #}
{%- macro minAnnotationsDate() -%}
   {%- set tempDate = "" -%}
	{%- for a in annotations -%}
		{%- set testDate = a.date | format("YYYY-MM-DD#HH:mm:ss") -%}
		{%- if testDate < tempDate or tempDate == ""-%}
			{%- set tempDate = testDate -%}
		{%- endif -%}
	{%- endfor -%}
	{{tempDate}}
{%- endmacro -%}
{# infer latest note date #}
{%- macro maxNotesDate() -%}
   {%- set tempDate = "" -%}
	{%- for n in notes -%}
		{%- set testDate = n.dateModified | format("YYYY-MM-DD#HH:mm:ss") -%}
		{%- if testDate > tempDate or tempDate == ""-%}
			{%- set tempDate = testDate -%}
		{%- endif -%}
	{%- endfor -%}
	{{tempDate}}
{%- endmacro -%}
{#- infer earliest note date -#}
{%- macro minNotesDate() -%}
   {%- set tempDate = "" -%}
	{%- for n in notes -%}
		{%- set testDate = n.dateAdded | format("YYYY-MM-DD#HH:mm:ss") -%}
		{%- if testDate < tempDate or tempDate == "" -%}
			{%- set tempDate = testDate -%}
		{%- endif -%}
	{%- endfor -%}
	{{tempDate}}
{%- endmacro -%}
{# find earliest date of two dates #}
{%- macro minDate(min1, min2) -%}
		{%- if min1 <= min2 -%}
			{{min1}}
		{%- else -%}
		    {{min2}}
		{%- endif -%}
{%- endmacro -%}
{# find latest date of two dates #}
{%- macro maxDate(min1, min2) -%}
		{%- if min1 >= min2 -%}
			{{min1}}
		{%- else -%}
		    {{min2}}
		{%- endif -%}
{%- endmacro -%}

{# colorCategory to hex:
"green": "#5fb236",
"yellow": "#ffd400",
"red": "#ff6666",
"blue": "#2ea8e5",
"purple": "#a28ae5",
"magenta": "#e56eee",
"orange": "#f19837",
"gray": "#aaaaaa"
#}

{%- set colorToColorCategory = {
"#ffd400": "yellow",
"#ff6666": "red",
"#5fb236": "green",
"#2ea8e5": "blue",
"#a28ae5": "purple",
"#e56eee": "magenta",
"#f19837": "orange",
"#aaaaaa": "gray"
}
-%}
{%- set colorCategoryToType = {
"yellow": "Relevant / Important",
"red": "Disagree",
"green": "Important to me",
"blue": "Question / Understanding / Vocabulary",
"purple": "Reference / Term to lookup later",
"magenta": "margenta",
"orange": "orange",
"gray": "gray"
}
-%}
{# lookup Zotero colors in annotations with Category #}
{%- macro colorCategoryToName(noteColor) -%}
{%- if colorCategory[noteColor]-%}
{{colorCategory[noteColor]}}
{% else %}
{{colorCategory["yellow"]}}
{%endif%}
{%- endmacro -%}

{%- macro colorToName(noteColor) -%}
{%- if colorToColorCategory[noteColor]-%}
{{colorCategoryToType[colorToColorCategory[noteColor]]}}
{% else %}
{{colorCategoryToType["orange"]}}
{%endif%}
{%- endmacro -%}


{%- set calloutHeaders = {
"highlight": "Highlight",
"strike": "Strike Through",
"underline": "Underline",
"note": "Sticky Note",
"image": "Image"
}
-%}
{# lookup callout headers by type of annotation #}
{%- macro calloutHeader(type) -%}
{%- if calloutHeaders[type]-%}
{{calloutHeaders[type]}}
{% else %}
{{Note}}
{%endif%}
{%- endmacro -%}

{#- handle space characters in zotero tags -#}
{%- set space = joiner(' ') -%} 
{%- macro printTags(rawTags) -%}
	{%- if rawTags.length > 0 -%}
		{%- for tag in rawTags -%}
			#zotero/{{ tag.tag | lower | replace(" ","_") }} {{ space() }} 
		{%- endfor -%}
	{%- endif -%}
{%- endmacro %}

{#- handle | characters in zotero strings used in MD -#}
{% macro formatCell(cellText) -%}
{{ cellText | replace("|","❕")}}
{%- endmacro %}

{%- macro formatDate(testDate, dateFormat) -%}
{%- if testDate -%}
{{date | format (dateFormat)}}
{%- endif %}	
{%- endmacro %}

{#- handle | characters in zotero strings used in MD -#}
{# {%- set comma = joiner(', ') -%} 
{%- macro generateCreators(prefix) -%}
{%- for creatorType, creators in creators | groupby("creatorType") -%}
{{prefix}}{{ creatorType }}:: {{ space() }} 
    {%- for creator in creators -%}
        {{ creator.firstName }} {{ creator.lastName }} 
		{%- if not loop.last -%}
		{{comma()}}
		{%- endif -%}
    {%- endfor %}
{% endfor -%}
{%- endmacro -%} #}

{#- generate fields based on Zotero properties -#}
{%- macro generateFields(prefix) -%}
{%- for field, property in fields -%}
{%- if property.length > 0 -%}
{{ generateField(prefix, field, property) }}
{%- endif -%}
{%- endfor %}
{%- endmacro -%}

{{printTags(tags)}}
{{ "" }}

🔥🔥🔥everything above this line might change during an update 🔥🔥🔥

## Notes and Annotations

{% persist "notes" %}
{{ "" }}
{%- set newNotes = notes | filterby("dateModified", "dateafter", lastImportDate) -%}
{% if newNotes.length > 0 %}

⬇️*Notes imported on: {{importDate | format("YYYY-MM-DD#HH:mm:ss")}}*⬇️
{% for note in newNotes %}
### 🟨 Note
Modified: {{ note.dateModified | format("YYYY-MM-DD#HH:mm:ss") }}
{{ "" }}
{#- change heading level -#}
{{ note.note | replace ("# ","### ") }}
[Link to note](zotero://select/library/items/{{note.key}})
{{printTags(note.tags)}}
{{ "" }}
---
{% endfor %}
{% endif -%} 

{% endpersist -%}
{{ " " }}

{{ " " }}
{% persist "annotations" %}
{{ " " }}
{%- set newAnnotations = annotations | filterby("date", "dateafter", lastImportDate) -%}
{% if newAnnotations.length > 0 %}
{{ " " }}
⬇️*Annotation imported on {{importDate | format("YYYY-MM-DD#HH:mm:ss")}}*⬇️

{# {% for color, colorCategory in colorToColorCategory %} #}
{#-Filter empty colorCategory-#}
{%- for annotation in newAnnotations -%}
{# {% if loop.first -%} #}
{# #### {{colorToName(color | lower)-}} #}
{# {% endif %} #}
> [!annotation-{% if annotation.color %}{% if colorToColorCategory[annotation.color].length > 0 %}{{colorToColorCategory[annotation.color]}}{% else %}yellow{% endif %}]{% endif %} {{calloutHeader(annotation.type)}}
{%- if annotation.annotatedText.length > 0 -%} 
> {{-annotation.annotatedText | nl2br -}} (p. [{{annotation.page}}](zotero://open-pdf/library/items/{{annotation.attachment.itemKey}}?page={{annotation.page}}&annotation={{annotation.id}})){% endif %}{%- if annotation.imageRelativePath -%}
> ![[{{annotation.imageRelativePath}}|300]]
{%- endif %}{%- if annotation.ocrText -%}
> {{-annotation.ocrText | nl2br-}}{%- endif -%}
{%- if annotation.comment -%} 
>
> **comment:**
> {{annotation.comment | nl2br }}{% endif %}
> {{annotation.date | format("YYYY-MM-DD#HH:mm")}}
{%- if annotation.tags.length > 0 %} 
> {{printTags(annotation.tags)}}
{% endif %}
{% endfor -%}
{# {% endfor %} #}
{%- endif -%}

{% endpersist -%}
```

And the contents of `style.css`, which I put in the hidden folder that can be found by following Obsidian &rarr; Settings &rarr; Appearance &rarr; CSS snippets.

```css
/* See https://lucide.dev for icon codes */

/* annotation */
.callout[data-callout="annotation-yellow"] {
  --callout-color: 255, 212, 0;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-red"] {
  --callout-color: 255, 102, 102;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-green"] {
  --callout-color: 95, 178, 54;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-blue"] {
  --callout-color: 46, 168, 255;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-purple"] {
  --callout-color: 162, 138, 229;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-purple"] {
  --callout-color: 162, 138, 229;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-magenta"] {
  --callout-color: 229, 110, 238;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-orange"] {
  --callout-color: 241, 152, 55;
  --callout-icon: lucide-highlighter 
}

.callout[data-callout="annotation-gray"] {
  --callout-color: 170, 170, 170;
  --callout-icon: lucide-highlighter 
}

/* note */
.callout[data-callout="note-yellow"] {
  --callout-color: 255, 212, 0;
  --callout-icon: lucide-sticky-note 
}

.callout[data-callout="note-red"] {
  --callout-color: 255, 102, 102;
  --callout-icon: lucide-sticky-note 
}

.callout[data-callout="note-green"] {
  --callout-color: 95, 178, 54;
  --callout-icon: lucide-sticky-note 
}

.callout[data-callout="note-blue"] {
  --callout-color: 46, 168, 255;
  --callout-icon: lucide-sticky-note 
}

.callout[data-callout="note-purple"] {
  --callout-color: 162, 138, 229;
  --callout-icon: lucide-sticky-note 
}
```