---
layout: post
title: Get organised
---

# Best practice for research project organisation

This post is going to discuss one way to organise your small (as opposed to 'big') data science project or research project: data, code and outputs. I'll cover how to structure the project, version control, data and data storage, analytical tools, coding standards, and what to do when your project is over.

##### Caveats
Of course, these are just my opinions, they're far from exhaustive, and there may well be good reasons to set up your project differently depending on what it is that you're doing. I'm interested in hearing different perspectives so get in touch if you have them.

Inevitably the post is going to be geared toward Python because it's my primary language but much of the advice applies equally well to R. Similarly, although most of what I'm saying applies across platforms, in some in places it may be more relevant to Mac OS.

I'm not going to discuss topics like unit tests, automatic creation of documentation, or making the project into an installable package in this post and, for most small research projects, these features would probably be overkill.

For a more detailed perspective on best practice research project organisation, see [Good enough practices in scientific computing. PLoS computational biology, 13(6), e1005510](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510). A similar post from a more pure data science perspective may be [found here](https://www.kaggle.com/rtatman/reproducible-research-best-practices-jupytercon), and there's a [machine learning oriented cookiecutter project here](https://drivendata.github.io/cookiecutter-data-science/).

#### The example project

There's a [small research project github repository](https://github.com/aeturrell/cookie-cutter-research-project) that accompanies this post. To use it as the basis of your small research project, open up a command line and type ```git clone https://github.com/aeturrell/cookie-cutter-research-project.git``` in the directory in which you want to clone it, or download it directly from github.

It is in Python 3 and uses the ONS API to download some macroeconomic time series, process them into tidy data, and then use them within a dynamic factor model&dagger; inspired by [Chad Fulton](http://www.chadfulton.com/)'s tutorials/notebooks which you can find [here](http://www.chadfulton.com/fulton_statsmodels_2017/sections/6-out-of-the-box_models.html#dynamic-factors) and [here](https://www.statsmodels.org/dev/examples/notebooks/generated/statespace_dfm_coincident.html).

It is very much a toy example and not intended to be accurate or say anything at all about the real world! It is designed to showcase how the various components of what I'll say below fit together in practice.

Within the example project, there are Latex templates for both slides and a working paper. These are based on [Paul Goldsmith-Pinkham](https://twitter.com/paulgp?lang=en)'s excellent templates, the originals of which you can find [here for slides](https://github.com/paulgp/beamer-tips) and [here for the working paper](https://github.com/paulgp/draft-tex).

Okay, on to the main event...


## Project structure

The structure of your project should be a directed acyclic graph with raw data making up the first nodes and research outputs (e.g. paper or slides) the final nodes. Here's an example for the cookiecutter research project:

![png]({{site.baseurl}}/images/cookiecutterorg.png)

Why this directed acyclic graph structure? For reproducibility, you can't have steps earlier on in the project that depend on steps later on in the process. This may seem completely obvious but, believe or not, I have seen projects where later stage outputs are looped back to be inputs into earlier stages.

Another important principle here is to separate out different phases of the analysis. Sometimes this is about avoiding repeated effort - going from raw data to cleaned data might be very expensive in terms of time. 

Before you start your project, it's really worth taking the time to sketch out on paper how everything will fit together and which parts might depend on each other. Putting a lot of effort into this step will save you a lot of time in the long run. Armed with a clear structure, you will write better, more modular code that does not involve repetition. Of course, research work is inherently uncertain and you shouldn't be afraid to change up the structure if the focus or goals of the project change.

If you haven't tried putting figures and tables in a separate directory to your Latex code before then the example project implements an efficient way to do so. You set a single path and can then refer to outputs only by their name (not their full path). If you want to be even more fancy you can [move files around](http://www.jespertoftkristensen.com/JTK/Blog/Entries/2014/1/13_Organize_your_LaTeX_Project.html) during Latex compilation.

Perhaps you need to output your (Latex) writing to Microsoft's Word format or to markdown as part of your workflow? In that case, I'd suggest using [pandoc](https://pandoc.org/) but be warned that ensuring references, citations, equations, and inputs are included correctly can be fiddly.

One other important principle: friends do not let friends use whitespace in filenames or paths.

##### Configuration files
You'll notice that there is a config file, config.yaml, that sits above everything else. The purpose of this is to make adding global settings to your project easier, especially if they are directories. The advantage of this config file is that you can see what settings are being run from one place and, if you do need to change the structure of the project, you only have to do it in one place. Similarly, others on the project can clearly see when and how important settings were changed without trawling through lots of code.

In the example project, I've put settings for plots into the config.yaml where they can be conveniently loaded. These start with the ```- viz:``` heading in the file.

.yaml is not the only configuration file available and I don't have a very strong view as to which is best as they all have their pros and cons. I've used both .ini and .yaml, and both can work for a simple project. You can find more about the ins and outs of different config file formats [here](https://martin-thoma.com/configuration-files-in-python/) (with handy examples) and [here](https://hackersandslackers.com/simplify-your-python-projects-configuration/).


## Version control

There are many articles on why you should use version control if you're doing any sort of coding and I'm not going to go over the arguments here. I will link to [this primer](https://www.atlassian.com/git/tutorials/what-is-version-control) instead. Most people use [git](https://www.atlassian.com/git/tutorials/what-is-git) for version control (it's completely free). Git has a painful learning curve but there are just a handful of commands that you'll use most of the time, especially on smaller projects. And, if you do run into trouble, there's always [www.ohshitgit.com](https://www.ohshitgit.com). Note that git is the tool to manage version control while github, gitlab, and bitbucket are hosting services for git repositories.

Beyond the software development-type reasons for version control, there are benefits that are particular to research. Journals increasingly require code to be submitted alongside papers; version control encourages good code management that will make submitting your code much easier when the time comes. If you host your code on platforms such as [github](https://github.com/) and [gitlab](https://about.gitlab.com/), privately at first, and then publicly when you publish, you can significantly extend the impact of your work. Those same platforms enable collaboration on code, including Latex, with co-authors. Even better, you can use tools like [git-blame](https://www.atlassian.com/git/tutorials/inspecting-a-repository/git-blame) to understand who changed what and when - useful in all kinds of situations, not just blaming co-authors for that misplaced semi-colon.

<blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">who called it `git blame` and not `git whose-line-is-it-anyway`?</p>&mdash; Jessica🏳️‍🌈 (@ticky) <a href="https://twitter.com/ticky/status/1032028502961209344?ref_src=twsrc%5Etfw">August 21, 2018</a></blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The other great use of the various git platforms is to track bugs, to do lists, and even to host wikis.

A few extra tips on the interaction between version control and project structure.

Version control is not meant to track data, only code. However, for outputs, such as figures and tables, it's less clear where to draw the line. But (as shown above) I'd advise having a scratch-outputs folder that is not under version control that you can spam with hundreds of figures and tables and a (final) outputs folder that holds the tables and figures that are going to make it into the paper and/or slides.

Latex is code! Put it under version control. This also makes it easy to collaborate with co-authors, and work out who changed what when. Some prefer to use tools like [Overleaf](https://www.overleaf.com/), an online Latex editor with some WYSIWYG features, instead.

There are some folders, e.g. raw/, that you'd like to keep even though none of the *contents* of the folder should be under version control. There is a special file for that, called .gitkeep, which tells git you'd like to keep the folder. The file can be completely empty and, on Unix systems, you can create it with ```touch raw/.gitkeep``` in the command line.

Likewise, there is a lot of gunk generated by Latex compilation that you probably don't want to keep under version control. This is what the magic .gitignore file is for in the project structure. It specifies what types of file to ignore. The .gitignore file in the example project will automatically ignore Latex compilation files, everything in the raw/ and output-scratch/ folders, and anything generated indirectly by running Python code or Latex compilation.



## Data

I find it useful to think about the main possible classes of data in a research project as being raw, intermediate, cleaned, and output. 

As the example project is simple, we are going to skip intermediate data and go straight for clean data.

##### Raw data 
Raw data is just that. No matter how horrible a format it comes to you in (a 50 sheet Excel file with different formats on each sheet anyone?), you should preserve that. Don't mess with it, keep it to one side and derive other, better data from it. You'll need it later when you try and replicate your own work.

##### Intermediate data 
Intermediate data is the data you get once you've made some progress on getting whatever mess you started with into shape. Maybe you had 5 different spreadsheets and you've managed to clean each one and dump them into CSVs. Yes, they are still not tidy, or in the format you need for analysis, or merged. But you've made some progress, progress worth making into a distinct phase of your analysis.

Intermediate data can be very large, in which case you may want to consider the speed and efficiency of storing it. For the python library pandas, there's a [nice post here](https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d) looking at file sizes and loading/saving speeds. As noted, intermediate data should not be under version control. Data versioning does exist but I've not (yet) seen it used for research projects - see [pachyderm](https://github.com/pachyderm/pachyderm) for an example.

##### Cleaned data 
Cleaned data is what's used to do the analysis. It's data that's ready to go into a machine learning model or regression. If a colleague were working on a similar project, this is (hopefully) what you'd send them instead of the 50-sheet Excel monstrosity.

Cleaned data should be stored in tidy format, that is data in which each observation is a row, each variable is a column, and each type of observation unit forms a table. This figure shows a visual example of tidy data.

![png]({{site.baseurl}}/images/tidy_data_example.png)
From [R for Data Science](https://r4ds.had.co.nz/tidy-data.html).

If you want to find out more about why it's good practice to store your data in tidy format then it's worth reading [Hadley Wickham's paper on it](https://www.jstatsoft.org/article/view/v059i10).

In the vast majority of cases, the best data file format for your project's cleaned data is CSV. Everyone can open it, no matter what analytical tool or operating system they are using. As a storage format, it's unlikely to change. Without going into the [mire of different encodings](http://kunststube.net/encoding/), save it as UTF-8 (note that this is not the default encoding in Windows). This is especially true of text heavy data. 

Of course, CSV is great for tabular data but won't work for many other kinds. For other cases, Stanford's library has put together a [useful list](https://library.stanford.edu/research/data-management-services/data-best-practices/best-practices-file-formats) of preferred file formats for archiving everything from geospatial data to films. 

Do not store your data in Excel file formats. Ever. Firstly, it's not an open format, it's proprietary, even if you can open it with many open source tools. But, more importantly, Excel can do bad things like [changing the underlying values in your dataset](http://www.win-vector.com/blog/2014/11/excel-spreadsheets-are-hard-to-get-right/) (dates and booleans), and it tempts other users to start slotting Excel code around the data. This is bad - best practice is to **separate** code and data. Code hidden in Excel cells is not very transparent or auditable.

![jpg]({{site.baseurl}}/images/excel_data_tweet.jpg)

Should you put your tidy, cleaned data under version control? Probably not. But if it's small and unlikely to change much, it can be quite convenient to do so.

##### Output data

These are the final figures and tables that tell the story in your analysis. As noted, it's convenient to put the ones that are going to make it into your paper and any presentations you give under version control, and have a scratch folder for the rest. This a folder that's for the many extra figures and tables that you'll create, and perhaps want to glance at, but won't hold on to.

For figures, most journals require that you use lossless formats such as PDF and EPS. .eps and .pdf are vector image formats, they work by representing the shapes and lines of the image and so can be reproduced any resolution. They are distinct from rasterised formats (.png, .jpg) that work by having pixels that reproduce the image but only at a specific resolution. For images made up of smooth shapes and colours, like most charts, vector formats are superior because they encode the information to show an image at any resolution. For complex images, such as photographs, jpg is usually better because there is a natural limit to the resolution you would ever need in such an image. As journals tend to prefer it, my general recommendation is to use .eps wherever possible and, if you do have real images, find out what format the journal prefers. Not only do .eps files look better, but for figures they tend to take up less space on disk versus the equivalent png or jpg file. Modern programming languages like R and Python can export to all of these formats.

For reasons that are not at all obvious, Powerpoint does not play nicely with vector images but Keynote (Mac OS) and Beamer/Latex (all operating systems) do.&Dagger;

What about tables? My current strategy is to export these directly to Latex as .tex files. It's not so easy to look at these without compiling them using Latex but it saves a lot of time when (automatically) incorporating them into your paper and presentations. Tables as tex files also take up little space on disk and can happily go under version control.*


## Analytical tools

By analytical tools, I really mean the combination of programming language and integrated development environment (IDE) that you use. The best practice here is to use the right tool for the job.

In addition to that, it's worth thinking about how accessible your code will be to others when you release it. Code written in a proprietary language that requires users to shell out some cash just to run it is inevitably less accessible than code written in open source languages.

Unless you're running very computationally intensive code that needs C++ or Fortran, you're likely to be using one of Python, R, Julia, or Matlab. If you're coming from the social sciences then perhaps you'll be using Stata or EViews. Some of these languages come bundled with, and are almost inseparable from, their IDEs.

As for which IDE to use, many heavy R users swear by RStudio and I know of many Python users who either prefer Spyder (which comes bundled with the Anaconda distribution of Python) or PyCharm (anecdotally this seems to be preferred by software dev types).

Recently, I've mostly been using Visual Studio Code. VS Code is an extendible text editor and IDE that is free and very impressive: I've used it to run code in Python, R, markdown, and Latex. I believe it also supports Octave (aka free Matlab) and Julia, but I haven't tested these. There's syntax highlighting for both Stata and Matlab and - if you already have Stata installed - you can run apparently run Stata code from VSCode! Support for Python is very good; you can switch between environments within the IDE, launch interactive consoles, and [remotely connect](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) to an instance of Python running elsewhere. Switching between Python/conda environments with the click of a button is revelatory. See [here for a full list of supported languages](https://code.visualstudio.com/docs/languages/overview).

Most additional features require the installation of packages that can be found via the [package search](https://marketplace.visualstudio.com/VSCode). Two essential  extensions are [git-lens](https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens) and [Markdown preview enhanced](https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced).

## Coding standards

The validity of your research depends, to a frightening degree, on the quality of your code. There are ways to code better and minimise the risk of mistakes even for small research projects that don't look anything like a software development project. Most languages have some sort of style guide to help you. Following them will make your code easier to read, more consistent, and more manageable. 

For R, there doesn't seem to be a single agreed upon style, but I'm sure you could do much worse than follow Hadley Wickham's [R style guide](http://adv-r.had.co.nz/Style.html), itself based upon the Google R style guide, at least if you're using the ```tidyverse``` ecosystem.

For Python, there is [PEP8](https://www.python.org/dev/peps/pep-0008/). Yes, it's a bit of a monster. Rather than read through it, just install a linter extension in your favourite IDE (see [this guide](https://code.visualstudio.com/docs/python/linting) for VS Code) and your code will be automatically checked for most style breaches as you type. It's a bit daunting to turn this on at first but it encourages you to produce much cleaner code.

For research, it's worth having the extensions and robustness checks that reviewers might request in mind early on. You don't want to be faced with a request that's going to force you to do a huge re-write of your code. Better to try and anticipate reasonable variations on what you've done from the start, difficult though that may be.

Make your code as modular as possible, and never re-write the same code twice. If the same code is being re-run, stick it in a function. You will save time in the long run and having functions defined once and only once makes it easy to change in the future too. 

Code comments can be helpful. The best code actually has very *few* comments because what's happening is clear without them. When that high bar can't be reached, add comments to make it easier for a reader to understand what your code is doing. Most likely, that reader will be future you.

Perform code reviews. Give what you've done to a colleague and ask them to go through it line-by-line checking it works as intended. If they do this properly and don't find any mistakes or issues then I'd be very surprised. Return the favour to magically become a better coder yourself.

Choose clarity over optimisation, at least as a starting point. Computation is cheap, brain time is not. If you really need to optimise, do it later when you've figured out where it will count.

## After the project

##### Reproducibility

Unless you've been hiding under a rock, you'll know about the replicability crisis in research. Much of what I've outlined above should help make replication as easy as possible: you can ```git clone``` your repository into a new folder, add the raw data to the raw/ directory, and then hit go on the code. If the final outputs match up to what you did before, that's a good sign.

This is certainly not sufficient for replication in the broadest sense, but it is necessary. If even you can't reproduce your own results from scratch then you can't expect anyone else to be able to.

Technically, to make the project as reproducible as possible, you should be including information on how to set up the exact same environment (including package versions and operating system) that was used to generate the results. I do think this is going to be [essential in the future](https://www.natureindex.com/news-blog/a-petting-zoo-for-code-makes-studies-easier-to-reproduce) but, right now, it's just not practical for all but the most tech-savvy researchers. If you're using the same OS then conda's [environment files](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) are a step in the right direction when using Python, albeit an [imperfect one](https://stackoverflow.com/questions/39280638/how-to-share-conda-environments-across-platforms).

To create and use the conda environment included in the example project, use
```
conda env create -f ccenv.yml
```
on the command line, then activate the environment. To create your own environment file from an existing conda environment, use
```conda env export --no-builds | grep -v "prefix" > yourenv.yml```


##### Data

Once you have finished your analysis, what do you do with the dataset you have painstakingly put together? Hopefully you'll make it ‘findable, accessible, interoperable and reusable’ (FAIR) so that others can use it, as recommended by the journals [*Nature*](https://www.natureindex.com/news-blog/what-scientists-need-to-know-about-fair-data) and *Scientific Data*.

Briefly, Findable equates to having meta-data (including a unique and persistent identifier) and being in a searchable index; Accessible means that data (and meta-data) are retrievable via open and free tools (proprietary formats like Stata .dta or Excel .xls files do not count, but open formats like .csv do) ; Interoperable means that data are in a widely used and machine readable structure such as [tidy](https://r4ds.had.co.nz/tidy-data.html); and Re-usable means including a data usage license and meta-data on provenance. There's a more detailed list of criteria [here](https://www.force11.org/group/fairgroup/fairprinciples).


Importantly, data should not just be appended to articles as a supplement but lodged in a searchable repository with an identifier that is citable. Use the Stanford library list earlier in the post for information on what file formats to use, and [this list](https://www.nature.com/sdata/policies/repositories) from *Scientific Data* of approved FAIR data repositories.

Incentives to publish data are perhaps not all that they could be currently, but [change is afoot](https://www.nature.com/articles/d41586-019-01715-4) and I would say that best practice is to share your data on one of these repositories whenever possible.

##### Code

When your project is ready to be released, opening it up to the outside world is as easy as clicking a button on github or gitlab. It will be easily searchable. To make life even easier for those finding it, make sure to have an informative readme file (with the citation information) in the main directory, to tag the project appropriately, and to add a user license. If you're unsure which license is appropriate, there is a [useful guide here](https://choosealicense.com/).

## Conclusion

I hope you've found this post informative. Disagree with anything or think I've missed an important point? Get in touch!




------
 
*You may find that because the .eps files used for figures are not in a sub-directory of the main .tex folder, you must add a flag to the Latex compiler. In TexShop, the steps are:
- Go to Preferences
- Go to Tab "Engine"
- Go to the field "pdfTeX"
- In the Latex Input Field add ``` --shell-escape``` at the end so that it changes from
```pdflatex --file-line-error --synctex=1```
to ```pdflatex --file-line-error --synctex=1 --shell-escape```
 

&Dagger; You can use .svg in the latest versions of Microsoft Powerpoint. Microsoft dropped support for .eps in Powerpoint due to concerns about security.

&dagger; If you're interested in the model, it has the following specification:

$$
\begin{aligned} \vec{y}_t & = \Gamma \vec{f}_t + \vec{u}_t \\\\ 
        \vec{f}_t & = A_1 \vec{f}_{t-1} + A_2\vec{f}_{t-2} + \Xi_t \quad \quad \Xi_t \thicksim \mathcal{N}(0,I)\\\\ 
	 \vec{u}_t  & = B_1 \vec{u}_{t-1} + B_2\vec{u}_{t-2} + \Phi_t \quad \quad \Phi_t \thicksim \mathcal{N}(0,\Sigma)
\end{aligned}
$$

where capital Greek and Latin characters represent matrices, arrows over characters denote vectors, and it is assumed that the different components of the `innovations' in the error updating equation are uncorrelated so that $ \Sigma $ is a diagonal matrix. The model has one unobserved factor that follows an AR(2), and the errors similarly follow an AR(2).








