# 10 less well-known Python packages

Here's a round-up of 10 Python packages for data science (and more) that you might not have heard of. While most are on this list because they could be useful, it's not all serious, as our first entry attests.  

## 1. Jazzit

Sound on for this one. Jazzit's docs say:
> "Ever wanted your scripts to play music while running/ on erroring out?  Of course you didn't. But here it is anyway".

Yes, this package laughs at you when you get a runtime error -- but can also celebrate your success when the code runs. Apart from being good fun, this package demonstrates how the decorator function `@` is used.

See also: [beepy](https://pypi.org/project/beepy/)

#### Example of Jazzit


```python
%%capture
!pip install jazzit
```


```python
from jazzit import error_track, success_track

@error_track("curb_your_enthusiasm.mp3", wait=9)
def run():
    for num in reversed(range(10)):
        print(10/num)

run()
```

    1.1111111111111112
    1.25
    1.4285714285714286
    1.6666666666666667
    2.0
    2.5
    3.3333333333333335
    5.0
    10.0


    Traceback (most recent call last):
       line 47, in wrapped_function
        original_func(*args)
      File "<ipython-input-1-a24a66965e4c>", line 6, in run
        print(10/num)
    ZeroDivisionError: division by zero











```python
@success_track("anime-wow.mp3")
def add(a,b):
    print(a+b)

add(10, 5)
```

    15










## 2. Handcalcs

In research, you often find yourself coding up maths and then transcribing the same maths into text (usually via typesetting language Latex). This is bad practice; do not repeat yourself suggests you should write the maths once, and once alone. Handcalcs helps with this: it can render maths in the console and export to latex equations.

![](https://pythonawesome.com/content/images/2020/08/wrong_brackets.gif)


See also: if you want to solve, render, and export latex equations, you should try out [sympy](https://www.sympy.org/en/index.html), a fully fledged library for symbolic mathematics (think Maple).

#### Example of handcalcs


```python
%%capture
!pip install handcalcs
```


```python
import handcalcs.render
```

To render maths, just use the `%%render` magic keyword. If you're running in an enviroment that doesn't have a Latex installation, this will just show Latex -- if you want the Latex, use the `%%tex` magic keyword instead. But in a Jupyter notebook on a machine with Latex installed, the `%%render` magic will render the maths into beautifully typeset equations:


```python
%%tex
a = 2
b = 3
c = 2*a + b/3
```

    \[
    \begin{aligned}
    a &= 2 \; 
    \\[10pt]
    b &= 3 \; 
    \\[10pt]
    c &= 2 \cdot a + \frac{ b }{ 3 }  = 2 \cdot 2 + \frac{ 3 }{ 3 } &= 5.0  
    \end{aligned}
    \]


## 3. Pandas profiling

Any tool that can make the process of understanding input data is very welcome, which is why the [pandas profiling](https://pandas-profiling.github.io/pandas-profiling/docs/master/rtd/) library is such a breath of fresh air. It automates, or at least facilitates, the first stage of exploratory data analysis.

What pandas profiling does is to render a HTML or ipywidget report (or JSON string) of the datatset - including missing variables, cardinality, distributions, and correlations. From what I've seen, it's really comprehensive and user-friendly---though I have noticed that the default configuration does not scale well to very large datasets.

Due to the large size of the reports, I won't run one in this notebook, although you can with `profile.to_notebook_iframe()`, but instead link to a gif demoing the package.

See also: [SweetViz](https://github.com/fbdesignpro/sweetviz)

#### Example of pandas profiling


```python
%%capture
!pip install pandas-profiling[notebook]==2.9.0
```


```python
import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport

data = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')
data.head()

# To run the pro use:
profile = ProfileReport(data, title="Titanic Dataset", html={'style': {'full_width': True}}, sort="None")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>838</th>
      <td>839</td>
      <td>1</td>
      <td>3</td>
      <td>Chip, Mr. Chang</td>
      <td>male</td>
      <td>32.0</td>
      <td>0</td>
      <td>0</td>
      <td>1601</td>
      <td>56.4958</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>628</th>
      <td>629</td>
      <td>0</td>
      <td>3</td>
      <td>Bostandyeff, Mr. Guentcho</td>
      <td>male</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>349224</td>
      <td>7.8958</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>386</th>
      <td>387</td>
      <td>0</td>
      <td>3</td>
      <td>Goodwin, Master. Sidney Leonard</td>
      <td>male</td>
      <td>1.0</td>
      <td>5</td>
      <td>2</td>
      <td>CA 2144</td>
      <td>46.9000</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>79</th>
      <td>80</td>
      <td>1</td>
      <td>3</td>
      <td>Dowdell, Miss. Elizabeth</td>
      <td>female</td>
      <td>30.0</td>
      <td>0</td>
      <td>0</td>
      <td>364516</td>
      <td>12.4750</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>841</th>
      <td>842</td>
      <td>0</td>
      <td>2</td>
      <td>Mudd, Mr. Thomas Charles</td>
      <td>male</td>
      <td>16.0</td>
      <td>0</td>
      <td>0</td>
      <td>S.O./P.P. 3</td>
      <td>10.5000</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
  </tbody>
</table>
</div>




![](https://camo.githubusercontent.com/87df79347c0acf4421a1040310ecf6f5b9a4026c/68747470733a2f2f70616e6461732d70726f66696c696e672e6769746875622e696f2f70616e6461732d70726f66696c696e672f646f63732f6d61737465722f6173736574732f696672616d652e676966)


## 4. Matplotlib!?

Alright, you've probably heard of matplotlib and might be surprised to see it on this list. But there's a nice new feature of matplotlib that you might not be aware of: placement using ASCII art. It's more useful than it sounds.

Sometimes (especially for science papers), you need a weird arrangement of panels within a figure. Specifying that so that it's exactly right is a big pain. This is where the new matplotlib mosiac subplot option comes in.

Note that you may need to restart the runtime after you have pip installed matplotlib below.

See also: if you like declarative plotting that's web-friendly and extremely high quality, [Altair](https://altair-viz.github.io/) is definitely worth your time.

#### Example of matplotlib mosaics


```python
%%capture
!pip install matplotlib==3.3.1
```


```python
import matplotlib.pyplot as plt
axd = plt.figure(constrained_layout=True).subplot_mosaic(
    """
    TTE
    L.E
    """)
for k, ax in axd.items():
    ax.text(0.5, 0.5, k,
            ha='center', va='center', fontsize=36,
            color='darkgrey')
```


![png]({{site.baseurl}}/images/10_less_img_16.png)


But it's not just ASCII that you can use, lists work too:


```python
axd = plt.figure(constrained_layout=True).subplot_mosaic(
    [['.', 'histx'],
     ['histy', 'scat']]
)
for k, ax in axd.items():
    ax.text(0.5, 0.5, k,
            ha='center', va='center', fontsize=36,
            color='darkgrey')
```


![png]({{site.baseurl}}/images/10_less_img_18.png)


## 5. Pandera data validation

Sometimes you want to validate data, not just explore it. A number of packages have popped up to help do this recently. [Pandera](https://pandera.readthedocs.io/en/stable/) is geared towards pandas dataframes and validation within a file or notebook. It can be used to check that a given dataframe has the data that you'd expect.

See also: [Great Expectations](https://docs.greatexpectations.io/en/latest/), which produces HTML reports a bit like our number 3. featured above. Great Expectations looks really rich and suitable for production, coming as it does with a command line interface.

#### Example of pandera

Let's start with a dataframe that passes muster.


```python
%%capture
!pip install pandera
```


```python
import pandas as pd
import pandera as pa

# data to validate
df = pd.DataFrame({
    "column1": [1, 4, 0, 10, 9],
    "column2": [-1.3, -1.4, -2.9, -10.1, -20.4],
    "column3": ["value_1", "value_2", "value_3", "value_2", "value_1"],
})

# define schema
schema = pa.DataFrameSchema({
    "column1": pa.Column(int, checks=pa.Check.less_than_or_equal_to(10)),
    "column2": pa.Column(float, checks=pa.Check.less_than(-1.2)),
    "column3": pa.Column(str, checks=[
        pa.Check.str_startswith("value_"),
        # define custom checks as functions that take a series as input and
        # outputs a boolean or boolean Series
        pa.Check(lambda s: s.str.split("_", expand=True).shape[1] == 2)
    ]),
})

validated_df = schema(df)
print(validated_df)
```

       column1  column2  column3
    0        1     -1.3  value_1
    1        4     -1.4  value_2
    2        0     -2.9  value_3
    3       10    -10.1  value_2
    4        9    -20.4  value_1


This passed, as expected. But now let's try the same schema with data that shouldn't pass by changing the first value of the second column to be greater than -1.2:


```python
df = pd.DataFrame({
    "column1": [1, 4, 0, 10, 9],
    "column2": [22, -1.4, -2.9, -10.1, -20.4],
    "column3": ["value_1", "value_2", "value_3", "value_2", "value_1"],
})

validated_df = schema(df)
print(validated_df)
```


    ---------------------------------------------------------------------------

    SchemaError                               Traceback (most recent call last)

    <ipython-input-10-d0c9f6a389e0> in <module>
          5 })
          6 
    ----> 7 validated_df = schema(df)
          8 print(validated_df)

    SchemaError: <Schema Column: 'column2' type=<class 'float'>> failed element-wise validator 0:
    <Check less_than: less_than(-1.2)>
    failure cases:
       index  failure_case
    0      0          22.0


As expected, this throws a "schema error" that is informative about what went wrong and what value caused it. Finding 'bad' data is the first step in cleaning it up, so this library and the others like it that are appearing could be really useful.


## 6. Tenacity

If at first you don't succeed, try and try again. [Tenacity](https://tenacity.readthedocs.io/en/latest/) has several options to keep trying a function, even if execution fails. The names of the available function decorators give a clear indication as to what they do -- `retry`, `stop_after_attempt`, `stop_after_delay`, `wait_random`, and there's even a `wait_exponential`.


See also: R package `purrr`'s `insistently` function.

#### Example of Tenacity


```python
%%capture
!pip install tenacity
```


```python
from tenacity import retry, stop_after_attempt

@retry(stop=stop_after_attempt(3))
def test_func():
    print("Stopping after 3 attempts")
    raise Exception

print(test_func())
```

    Stopping after 3 attempts
    Stopping after 3 attempts
    Stopping after 3 attempts



    ---------------------------------------------------------------------------

    Exception                                 Traceback (most recent call last)

    <ipython-input-13-6efc6b249703> in test_func()
          5     print("Stopping after 3 attempts")
    ----> 6     raise Exception
          7 


    Exception: 

    
    The above exception was the direct cause of the following exception:


    RetryError                                Traceback (most recent call last)

    <ipython-input-13-6efc6b249703> in <module>
          6     raise Exception
          7 
    ----> 8 print(test_func())

    RetryError: RetryError[<Future at 0x7feda96db7f0 state=finished raised Exception>]


## 7. Streamlit


This one almost didn't make the list, so fast has its rise in popularity been. I really like [streamlit](https://www.streamlit.io/), which sells itself as the fastest way to build data apps that are displayed in a browser window. And my experience is that it's true; you can do a lot with a very simple set of commands. But there's also depth there too - a couple of the examples on their site show how streamlit can serve up explainable AI models. Very cool.

If you build a streamlit app and want to host it on the web, Heroku offer free hosting for a limited number of app users.

Because streamlit serves up content in a browser, it's not (currently) possible to demonstrate it in a Jupyter Notebook. However, this gif gives you an idea of how easy it is to get going:

<img src="https://miro.medium.com/max/1400/1*6GG7uRmUw74CRKCXD-lr1w.gif" width="800" />

See also: [Dash](https://plotly.com/dash/)

## 8. Black

[Black](https://black.readthedocs.io/en/stable/index.html) is an uncompromising code formatter ("you can have it any colour you want, as long as it's black"). Lots of people will find it overbearing, and think the way it splits code across lines is distracting. However, if you want to easily and automatically implement a code style -- without compromise -- then it's great and you can even set it up as a github action to run on your code every time you commit. Less time formatting sounds good to me.

Black is run from the command line or via IDE integration, so the example here is just a before and after of what happens to a function definition:

```python
# in:

def very_important_function(template: str, *variables, file: os.PathLike, engine: str, header: bool = True, debug: bool = False):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, 'w') as f:
        ...

# out:

def very_important_function(
    template: str,
    *variables,
    file: os.PathLike,
    engine: str,
    header: bool = True,
    debug: bool = False,
):
    """Applies `variables` to the `template` and writes to `file`."""
    with open(file, "w") as f:
        ...
```

See also: [yapf](https://github.com/google/yapf), yet another code formatter, from Google.

## 9. Pyinstrument for profiling code

Profiling is about finding where the bottlenecks are in your code; potentially in your data too.

[pyinstrument](https://github.com/joerick/pyinstrument) is a simple-to-use tool that extends the built-in Python profiler with HTMLs output that can be rendered in a Jupyter notebook cell.

Using this profiler is very simple -- just wrap 'start' and 'stop' function calls around the code you're interested in and show the results in text or HTML. The HTML report is interactive. To use the HTML report in a Jupyter notebook, you'll need to use

```
from IPython.core.display import display, HTML
```

and then

```
display(HTML(profiler.output_html()))
```

In the example below, I'll use the display as text option.

See also: [scalene](https://github.com/emeryberger/scalene), which I almost featured instead because it profiles both code and memory use (important for data science). However, it isn't supported on Windows (yet?) and it doesn't seem to display a report inline in Jupyter notebooks.

#### Example of Pyinstrument


```python
%%capture
!pip install pyinstrument
```


```python
from pyinstrument import Profiler


profiler = Profiler()
profiler.start()

def fibonacci(n):
    if n < 0:
        raise Exception("BE POSITIVE!!!")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(20)

profiler.stop()

print(profiler.output_text(unicode=True, color=True))
```

    
      _     ._   __/__   _ _  _  _ _/_   Recorded: 19:36:56  Samples:  3
     /_//_/// /_\ / //_// / //_'/ //     Duration: 0.004     CPU time: 0.004
    /   _/                      v3.2.0
    
    
    [31m0.003[0m run_code[0m  [2mIPython/core/interactiveshell.py:3376[0m
    └─ [31m0.003[0m [48;5;24m[38;5;15m<module>[0m  [2m<ipython-input-13-ac009be8054f>:17[0m
       └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
          └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
             └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                   └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                      └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                         └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                            └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                               └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                                  └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                                     └─ [31m0.003[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                                        ├─ [31m0.002[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                                        │  ├─ [33m0.001[0m [48;5;24m[38;5;15mfibonacci[0m  [2m<ipython-input-13-ac009be8054f>:7[0m
                                        │  └─ [33m0.001[0m [self][0m  [2m[0m
                                        └─ [33m0.001[0m [self][0m  [2m[0m
    
    


# 10. tdqm

An oldie but a goodie, tdqm produces progress bars. Used sensibly, they can give a good indication of when your code will finish executing. 

See also: [alive-progress](https://github.com/rsalmei/alive-progress) is a bit less straitlaced than tdqm but is unfortunately not yet available in notebooks. Here's a gif that shows how it looks when run from a console launched on the command line.

<img src="https://raw.githubusercontent.com/rsalmei/alive-progress/master/img/alive-demo.gif" width="600" />

#### Example of tdqm


<img src="https://raw.githubusercontent.com/tqdm/tqdm/master/images/tqdm-jupyter-2.gif" width="700"/>


## Bonus: R-style analysis in Python!?

Some data scientists swear by two of R's most loved declarative packages, one for data analysis (dplyr) and one for plotting (ggplot2), and miss them when they do a project in Python. Although certainly not as well developed as the original packages, there are Python-inspired equivalents of both, called [siuba](https://github.com/machow/siuba) and [plotnine](https://plotnine.readthedocs.io/en/stable/) respectively.

It's worth noting that there are *imperative* and *declarative* plotting libraries. In imperative libraries, you often specify all of the steps to get the desired outcome, while in declarative libraries you often specify the desired outcome without the steps. Imperative plotting gives more control and some people may find each step clearer to read, but it can also be fiddly and cumbersome, especially with simple plots. Declarative plotting trades away control and flexibility in favour of tried and tested processes that can quickly produce good-looking standardised charts, but the specialised syntax can be a barrier for newcomers.

ggplot/plotnine are both declarative, while matplotlib is imperative.

As for data analysis, Python's pandas library is very similar to dplyr, it just has slightly different names for functions (eg `summarize` versus `aggregate` but both use `groupby`) and pandas uses `.` while dplyr tends to use `%>%` to apply the output of one function to the input of another.

#### Plotnine



```python
%%capture
!pip install plotnine
```


```python
from plotnine import *
from plotnine.data import mtcars


(ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
 + geom_point()
 + stat_smooth(method='lm')
 + facet_wrap('~gear'))
```


![png]({{site.baseurl}}/images/10_less_img_36.png)





    <ggplot: (8791170958969)>



#### Siuba

Siuba is more or less similar to dplyr in R. It even has a pipe operator - although in Python's **pandas** data analysis package, `.` usually plays the same role as the pipe in dplyr.


```python
%%capture
!pip install siuba
```


```python
from siuba import group_by, summarize, mutate, _
from siuba.data import mtcars

print(mtcars.head())
```

        mpg  cyl   disp   hp  drat     wt   qsec  vs  am  gear  carb
    0  21.0    6  160.0  110  3.90  2.620  16.46   0   1     4     4
    1  21.0    6  160.0  110  3.90  2.875  17.02   0   1     4     4
    2  22.8    4  108.0   93  3.85  2.320  18.61   1   1     4     1
    3  21.4    6  258.0  110  3.08  3.215  19.44   1   0     3     1
    4  18.7    8  360.0  175  3.15  3.440  17.02   0   0     3     2



```python
(mtcars
  >> mutate(normalised = (_.hp - _.hp.mean())/_.hp.std()) 
  >> group_by(_.cyl)
  >> summarize(norm_hp_mean = _.normalised.mean())
  )
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>cyl</th>
      <th>norm_hp_mean</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4</td>
      <td>-0.934196</td>
    </tr>
    <tr>
      <th>1</th>
      <td>6</td>
      <td>-0.355904</td>
    </tr>
    <tr>
      <th>2</th>
      <td>8</td>
      <td>0.911963</td>
    </tr>
  </tbody>
</table>
</div>


