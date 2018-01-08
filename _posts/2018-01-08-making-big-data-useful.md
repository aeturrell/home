---
layout: post
title: Putting SOCs on: making big data work for economics
---

"Big data" is changing just about every field of inquiry, and economics is no exception. It isn't just that there are more data than there were before, although there are, it is that data now come in many shapes and sizes. Data can be in the form of numbers, but it could also be audio, text, or images. The granularity of data are also increasing, getting further into the choices we make as individuals. A striking example is in how mobile phone data have become a window into our lives, [as this study](http://dx.doi.org/10.1098/rsif.2015.0185) showed when they used mobile phone usage changes as a predictor for workers becoming unemployed.

Ever more granular data has positives and negatives. Naturally occurring data may be biased, because only certain types of people are using smart phones, or visiting a particular website. This could have unintended consequences. As a parable, some high-end cars may eventually be fitted with sensors to detect and report potholes, as [reported here](http://media.economist.com/news/science-and-technology/21731813-sensors-cameras-and-smart-cars-help-cities-spot-them-they-grow-potholes). But if the algorithms only see data from these cars, it may bias road repairs away from less wealthy areas.

In this post, we focus on one way to maximise the positives. Big data offer many potential complementarities to more traditional data, like surveys. Surveys suffer from mis-reporting and tend to be costly to do at scale. Naturally occurring data can be both cheap and on scales undreamt of when surveys first began. Information recorded incidentally by mobile phones is a good example.

But there are challenges for economists trying to get the best out of big data. They are difficult to use in analysis because of their scale; they may require tools which are unfamiliar to many economists. Data are often unstructured, or in a format which doesn't directly relate to the quantity of interest. In the mobile phone study, the researchers used, amongst other data, call records to predict unemployment. In the case of text or images, it isn't always clear how to transform data into the quantitative information which most economists' models need.

In a [research project on the determinants of productivity growth in the UK](www.bankofengland.co.uk), we faced just this problem of making a big, unstructured dataset of text useful in answering an economics question. Our data are 15 million job adverts from an online [recruitment website](www.reed.co.uk). These job vacancies appear at daily frequency over a number of years, and come with rich information on each job including a job description. We wanted to use these data to look at the market for labour in different occupations in the UK but there was a problem: all of the UK statistics on workers produced by the ONS are in designated categories - standard occupational classification (SOC) codes. An example is SOC code 242 which includes economists and statisticians.

In order to say anything about how employment and vacancies were related by occupation, we needed our job vacancies to be labelled with these same SOC codes. What we had were millions of job titles, job sectors, and job descriptions which had been posted online - but not a single one of them with a SOC code. This meant that we could not use supervised machine learning techniques. Extra challenges came in the form of job text information which was not relevant to the job, or job titles that had extra requirements in them (like 'must have driving licence'). Respondents to a survey are unlikely to add these details to their self-reported job titles!

To put our SOCs on, we created an algorithm which maps the text associated with each job vacancy into the official occupational classifications. Using materials from the ONS, we created an index of words associated with every SOC code. To get these words into a quantitative form, we used a measure called term frequency - inverse document frequency. This represents terms (phrases up to three words long) as a matrix with dimensions given by the number of unique terms and the number of SOC codes. Each SOC code $d$ has a vector representation $\mathbf{v}_d$ in this space.

Because the term frequency - inverse document frequency matrix acts as a map from text into the space of all SOC codes, it is now possible to express job vacancies, $v$, in the vector space: $\mathbf{v}_v$. One of the strengths of our approach is that we use all of the text associated with a job, including the job description. Surveys do not have this data and so cannot make use of it. The process of finding the top SOC code for job vacancy $v$ is completed by solving:

$$
\argmax_{d}\left\{\mathbf{v}_v \cdot \mathbf{v}_d\right\}
$$

which finds the SOC code vector which is closest in direction to the job ad vector using the inner product of the vector space. Because there may be several similar jobs, we find the top five SOC codes using this method and then we choose between them based on which has the closest job title to the job vacancy title. To do this, we use fuzzy matching, which counts the number of changes it takes to go from one string to another, between the two job titles. For instance, to get from 'Painter' to 'Printer' takes just one move: 'a' to 'r'. Fuzzy matching helps to find the right SOC code for each job ad title even if there are spelling mistakes in that title: 'ekonomist' is just one move away from 'economist'.

This process of matching up naturally occurring text data to official categories is sure to arise frequently for economists and statisticians. Because of this we are releasing the code on [Github](https://github.com) for anyone to use and adapt to their own needs. You can download the Python package [here](https://github.com/aeturrell/occupationcoder). How does it work in practice? There are instructions on how to install the package on the readme file. Once you have installed it, it can be used with the following Python code:
```python
import pandas as pd
from occupationcoder.coder import coder
myCoder = coder.Coder()
```
To run the code on a single job, use the following syntax with the ```codejobrow(job_title,job_description,job_sector)``` method:
```python
myCoder.codejobrow('Physicist',
'Make calculations about the universe, do research, perform experiments and understand the physical environment.'
,'Professional scientific')
```
which will return
| job_title     | job_description| job_sector | SOC_code |
| ------------- |:--------------| :----------| ------|
| Physicist     | Make calculations about the universe, do research, perform experiments and understand the physical environment. | Professional, scientific & technical activities | 211 |

Once all of the job vacancies have labels for each SOC code $d$, we can begin to look at the relationship between vacancies and unemployment for each SOC code. Our paper goes into more detail, but a flavour of what we can do is given by this figure of Beveridge Curves which shows how heterogeneous the behaviour of different occupations is in vacancy-unemployment space:

![codeoutput]({{site.baseurl}}/images/BevCurves1DigitSOC.png)

Big data presents fantastic opportunities to understand the forces of demand and supply - but it will be most useful if it can be matched to existing official categories.
