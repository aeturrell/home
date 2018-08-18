---
layout: post
title: Who is not participating in Higher Education?
---

Given my work in both the social sciences and STEM, I've become interested in what factors determine participation in higher education more broadly, what groups are left out, and what we might do about it.


### Poverty means low participation
According to a [Social Mobility Commission](https://cdn.lkmco.org/wp-content/uploads/2016/12/Ethnicity-gender-and-social-mobility-Shaw-et-al.-2016.pdf) report from 2016, the most important determinant of whether someone goes to university at all or not is poverty, or, more precisely, whether someone receives free school meals. This applies across gender and ethnicity, though as the report notes "Disadvantaged young people from White British backgrounds are the least likely to access Higher Education". 

A lack of diversity in socio-economic background is perhaps less visible than other troubling aspects of participation (such as gender in STEM and economics). However, if diversity matters at all, then all dimensions of diversity matter. 

Unfortunately, people from lower income/wealth backgrounds are probably some of the most difficult to reach with any sort of outreach campaign as they tend to live in "remote rural or coastal areas and in former industrial areas, especially in the Midlands" according to the 2017 Social Mobility Commission's 'State of the nation' [report](https://www.gov.uk/government/publications/state-of-the-nation-2017). I'm from one of the parts of the UK identified in this report, the High Peak, and it's unfortunately not all that surprising. Other poorly ranked areas are interesting: they include West Somerset (324 of 324), Thanet (274 of 324), and a cluster around West Norfolk.

A more precise measure of participation amongst young people comes from the [Office for Students](https://www.officeforstudents.org.uk/) and is shown below. The story is much the same as the report on social mobility. If you're not interested in where the data come from, skip the box below the figure.  


![]({{site.baseurl}}/images/map.png)
*Youth higher education participation rate by local authority district. Shown: Manchester and the Peak District.*

---
**Data on youth HE participation**
The Office for Students provide [data](https://www.officeforstudents.org.uk/data-and-analysis/polar-participation-of-local-areas/polar4-data/) on the number of young people who particapte in HE by middle super output areas. These are quite small areas so I've aggregated to local authority districts using a mapping which comes from data on [households in poverty](https://www.ons.gov.uk/file?uri=/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/householdsinpovertyestimatesformiddlelayersuperoutputareasinenglandandwales201112/current/householdsinpoverty201112.xls). I plotted these data with ```folium``` using [maps from the ONS Open Geography portal](http://geoportal.statistics.gov.uk/datasets/local-authority-districts-december-2016-ultra-generalised-clipped-boundaries-in-the-uk-wgs84). Minor gripe: no geojson format was available, so I had to make my own from the shapefiles.

---

### Science in the supermarket
Recently, I discussed how to reach those with the least HE participation with outreach superstar and former colleague Stuart Higgins (whose award-winning podcast [Scientists Not The Science](http://www.scinotsci.com/) you should check out). As I understand it, the best advice - based on research - is that you need to show young students a path into higher education which could work for them; that it's feasible, that it's for people 'like them', and that they're good enough to make it. Easier said than done.

I was talking to Stuart because of an amazing recent initiative he's been involved with called [Science in the Supermarket](http://www.superscience.org.uk/) which puts what he's learned into practice. Stuart and some other volunteers supported by Imperial College London went to a supermarket in Somerset to engage young and old alike with science demos, and to tell them about careers in STEM. I think this  initiative is brilliant because it avoids the self-selection problem with some other outreach programmes suffer from. There is room for many kinds of outreach targeting many different audiences, but hats off to Stuart for coming up with an innovative take which reach those previously left out. In the future, perhaps we might even see Economists in the Supermarket, or Applied Mathematicians in the Supermarket? I hope so.

