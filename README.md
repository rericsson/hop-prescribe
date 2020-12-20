![Python application test with Github Actions](https://github.com/noahgift/devops-project/workflows/Python%20application%20test%20with%20Github%20Actions/badge.svg)

# hop-prescribe
This project has code to create a simple, ratings nearest-neighbors based beer recommender. It's a primitive way to create recommendations (it would probably be better to do something more review based for beer since because it can be fairly nuanced) but it makes a good example of how to build such a thing.

This was heavily influenced by a session I watched on [O'Reilly](https://learning.oreilly.com/) by [Max Humber](https://github.com/maxhumber). I'm using his [Gazpacho](https://gazpacho.xyz/) to scrape the data. It's good stuff and you should check out his projects. 

The first step in this is to get some data. That's often one of the hardest parts of the entire process. I pulled the data out of [BeerAdvocate](https://www.beeradvocate.com/). To run the code as I have it, you will need to sign up for an account there (and you might think about writing some reviews as well ;-). 

After you have created an acccount on BeerAdvocate, you will need to install a Selenium driver on your system. I've used Firefox, so I installed the [geckodriver](https://github.com/mozilla/geckodriver/releases). This [gist](https://gist.github.com/cgoldberg/4097efbfeb40adf698a7d05e75e0ff51) has a script to do that if you don't know how. 

I strongly encourage you to use [virtualenv](https://virtualenv.pypa.io/en/latest/) to create a virtual environment. It'll just make things easier in the long run. 

Once you are ready to go, create a .env file in the directory where you have cloned the code and put your BeerAdvocate username and password into the file. It should look like this:

```
BA_USERNAME="your_username"
BA_PASSWORD="your_password"
```

Now, run `make all` to install the requirements and do a quick sanity check. Then, you are ready to run `python popular_beer_scrape.py` to get the data. It will be downloaded to a csv file in the current directory. 

Next, you need to build the model. To do that, run `jupyter notebook`. A browser should launch on your computer. Open the model-beer.ipynb file and run through the code. At the end, it will create a pickle file that has the model stored and ready to go for serving up on the web. 

The last part of this is creating a simple [Flask](https://flask.palletsprojects.com/en/1.1.x/) app to serve up the model. This is the simplest thing you can possibly do here. You can run it by using the command `python app.py`. This will serve a page at `http:\\localhost:8000` where you can interact with the model.

I learned quite a bit doing this. I'm not that impressed with the prescriptions right now as they don't vary much on the input. That's probably, again, because the ratings are more nuanced and it seems that people don't just highly like one style and not like the others. Instead, ratings seem to be on some other aspect. In any event, the purpose of this wasn't to discover a new beer that I might like (although I might have done that as well), it was to go through the steps of creating a
recommender engine. Cheers!
