# API Real-Estate

## Project Guidelines

- Repository: `challenge-api-deployment`
- Type of Challenge: `Learning`
- Duration: `5 days`
- Deadline: `30/07/2021 16:00 (code)`
- Presentation: `02/08/2021 10:00`
- Team challenge : `Solo`

## Technologies / Libraries 

|   [<img src="https://raw.githubusercontent.com/github/explore/80688e429a7d4ef2fca1e82350fe8e3517d3494d/topics/python/python.png" alt="python logo" width="80">](https://www.python.org/) |  [<img src="https://www.scipy.org/_static/images/numpylogoicon.png" alt="cpp logo" width="80">](https://numpy.org/)  |  [<img src="https://github.com/scikit-learn/scikit-learn/blob/main/doc/logos/scikit-learn-logo-thumb.png?raw=true" alt="bash logo" width="80">](https://scikit-learn.org/stable/index.html)  |  [<img src="https://camo.githubusercontent.com/86d9ca3437f5034da052cf0fd398299292aab0e4479b58c20f2fc37dd8ccbe05/68747470733a2f2f666173746170692e7469616e676f6c6f2e636f6d2f696d672f6c6f676f2d6d617267696e2f6c6f676f2d7465616c2e706e67" alt="bash logo" width="80">](https://fastapi.tiangolo.com/)  | [<img src="https://pandas.pydata.org/static/img/pandas_white.svg" alt="bash logo" width="60">](https://www.json.org/json-fr.html)  |
|---|---|---|---|---|

- [X]  [Python](https://www.python.org/) : A programming language
- [X]  [Numpy](https://numpy.org/) : The fundamental package for scientific computing with Python
- [X]  [Scikit-Learn](https://scikit-learn.org/stable/index.html) : Machine Learning Library
- [X]  [Pandas](https://pandas.pydata.org/) : A fast, powerful, flexible and easy to use open source data analysis and manipulation tool
- [X]  [fastAPI](https://fastapi.tiangolo.com/) : A modern, fast (high-performance), web framework for building APIs with Python 3.6+

## Documentation

### Objectives
This API can be used to get a predicted price for a given (hypothetical) property: it can be a house, an apartment, but also a farmhouse, etc. (many types are allowed by the API).
In order to make a prediction, the API runs a model (more information on that in the last section) that needs some real-estate data.

### API Framework
I used fastAPI rather than Flask because the integration with Pydantic Models
				is simply amazing. Almost all the validation takes place within the models (i.e. classes) definition: it's
				OOP, it's easy, readable and customizable. <br> <br> In other words, there's no code needed to manually check the
				structure of the data, because the Pydantic library is doing that automatically, including returning some
				nicely formatted and explicit error messages. As an example, instead of receiving a head-scratching '500 Internal Error'
				in case you forgot to send a required field, fastAPI and Pydantic will automatically send a 422 Validation Error with a
				message saying exactly which field is missing! <br> <br> And although it did not matter here, fastAPI can be used asynchronously,
				with performance on par with Node.js - which is great for people like me who don't know anything about JavaScript!
				If you are interested, go check fastAPI <a href="https://fastapi.tiangolo.com/">official documentation</a>

### Model Building
#### Data collection
Data about real-estate in Belgium was scraped from Immoweb around June 2021 with BeautifulSoup and Selenium libraires.
The first one allows us to retrieve (static) information contained within the HTML code, while the second one provides
automated interaction with the Website in order to click, scroll, wait for some JS script to be executed, fill in fields, etc.
Collected data includes information about the size, the condition of the building, the postal code, the type of building, etc.
Eventually only the relevant features for the model were kept, and are shown in the /docs and /redoc.<br> <br>
Part of the reason why predictions are not super accurate (as discussed below) is that collecting this Immoweb data
presented some challenges. First, many properties were missing some fields that had some predictive values (or at the
very least, we were not able to retrieve them from the page's code. Second, we did not know about regression and
Machine Learning at that time; it's plausible that if we were to do it all over again, we would focus more on getting
specific fields that in hindsight could help train the model.
<br><br>

#### Exploratory Data Analysis (EDA)
The first step - called EDA for Exploratory Data Analysis - was to find out which features seemed to be
most correlated with the price, and how much variance ("variability") was affected by outliers in the
relations between variables. A business-oriented presentation was given at this stage, if you are
interested you can find the slides <a href="https://docs.google.com/presentation/d/1M11hxMh23T3_ekDTXdYrt9FqNda51EgjlWvOKnej7e4/edit?usp=sharing">here</a>.
<br> <br>
The second step was to further clean the data: properties with too many missing fields were dropped and
outliers were removed (about 0.1%).
<br> <br>
The third step - called feature engineering - was to turn categorical features into numerical ones,
to create a 'province' feature based on the postal codes (because it quickly appeared that clustering the
data at the province level would yield better predictions), and finally to rescale the target (i.e.
the price) with a logarithm to avoid too much "dispersion" at high prices.
<br> <br>
Finally, after trying a few linear regressions, a non-linear estimator called a Random Forest Classifier was selected
and trained.
<br> <br> For more information on what it means to "train a model", you can check
<a href="https://www.youtube.com/watch?v=Gv9_4yMHFhI">this video</a>. If you don't enjoy the author's singing, you can check <a href="https://www.youtube.com/watch?v=nKW8Ndu7Mjw">this other video</a> as well.
<br> <br> For more information on Random Forest in general, you can check
<a href="https://williamkoehrsen.medium.com/random-forest-simple-explanation-377895a60d2d">this article</a>.
<br> <br> 
#### How well is it working?
Unfortunately, not *that* good right now... It can be pretty spot on, but it can also be off by more than half a
million for the most expensive or peculiar properties. Usually though, the predicted price is in acceptable
range and kind of make sense. On a more technical level, the Adjusted R2 score is about 0.70.

### Usage
You can use the endpoint `/predict/` (with a POST request) to send a properly formatted JSON object with all the required fields 
and their respective values (and yes, those are <i>case sensitive</i>). To help you figure out what the
API expects from you, you can check 2 super important links. <br> <br> <a href="https://corentin-api-test.herokuapp.com/redoc#operation/price_prediction_predict__post">The first one</a> allows you to check all the
acceptable values for all the required fields. Again, the string values are case-sensitive!
<a href="https://corentin-api-test.herokuapp.com/docs"> <br> <br> The second one</a> allows you to try the API
by directly typing some values in a JSON object and see what response and potential error message you
get with the values you've entered. It's completely safe, don't hesitate to try different combinations.
