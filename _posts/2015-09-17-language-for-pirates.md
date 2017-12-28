---
layout: post
title: A language for pirates
---
I've been dabbling with R recently. I wanted to make a choropleth,  a way of showing data superimposed onto a map. I thought I would have a go at doing it in Python initially but, disappointingly, this is one area in which Python hasn't quite caught up with the competition. I'm sure it'll happen eventually.  

R was entirely new to me when I started this mini project, so it's interesting to play around with it. It requires just a few lines of code to get something that looks good, but I couldn't in all honesty say that it was intuitive.  

Living in London, it's been hard not to notice the increases in house prices over the last few years. For a bit of fun, I thought I'd plot the % change in median house price year-on-year. House price data for all the London boroughs are from [http://data.london.gov.uk/](http://data.london.gov.uk/) and my spatial data is from [http://data.london.gov.uk/dataset/statistical-gis-boundary-files-london](http://data.london.gov.uk/dataset/statistical-gis-boundary-files-london). There seems to be a good number of free spatial mapping files around on the internet, and the move toward releasing data across all fields of endeavour mean that there's never been a better time to try plotting some of this stuff.  

My choropleth is shown below.  

<div class="separator" style="clear: both; text-align: center;">[![](https://4.bp.blogspot.com/-iundFGvIMRE/VfpSKgSAZnI/AAAAAAAAAeE/Pa0rfUEDs30/s640/medpricechg.jpg)](http://4.bp.blogspot.com/-iundFGvIMRE/VfpSKgSAZnI/AAAAAAAAAeE/Pa0rfUEDs30/s1600/medpricechg.jpg)</div>

<div class="separator" style="clear: both; text-align: left;">Clearly, my code has some issues - so I haven't put it on here. It would be good to get rid of that font size display in the legend. [Check out this](http://rstudio-pubs-static.s3.amazonaws.com/63040_5ad6d00e5dde4a8588ee07e8edc7b870.html) much more impressive use of the Metropolitan Police's [data](http://maps.met.police.uk/tables.htm), including an example very similar to mine but focusing on robbery rather than house prices.</div>
