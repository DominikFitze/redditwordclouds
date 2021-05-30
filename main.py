# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import praw
# import pillow
import os
from os import path
from wordcloud import WordCloud, ImageColorGenerator, STOPWORDS
import matplotlib.pyplot as plt
import sys
import io
import numpy as np
from os import path
from PIL import Image


#Initializes praw to scrape off reddit.
#A praw.ini file with the credentials needs to be set, see https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html)
reddit = praw.Reddit("bot1", user_agent="python:philscraper:v.0.1 (by u/as-well)")

#Sets how many posts are downloaded. Reddit usually requests stuff to 1000, so that is a good number.
limit = 1000

def main():
    #User can input which subreddit to analyse.
    sub = input(str("Which Subreddit would you like to analyze? "))
    subreddit = reddit.subreddit(sub)
    # Gets a string with as many post titles as the limit defines from the function below
    text = get_string_posts(subreddit)
    posts = str(text)
    #create a word cloud with the most common words
    wordcloud = create_wordcloud(posts)
    #Quick test whether the scraping was successful (Reddit's API is sometimes down). Should return a 5- or 6 digit number
    #if your limit set above was 1000
    print("A small test that the reddit scraper has worked correctly! What's the length of the text file? " + str(
        len(posts)))
    #Users can choose which picture to use. Optimally, a picture is larger than 1000x1000 pixels,
    # RGB coded and a black-and-white 'stencil', but it works with any pic.
    pic = input(str("Which picture should the wordcloud overlay? Enter name including file extension: "))
    # Next line makes the masking work, that is it makes the pic overlay a 'stenil'
    philmask = np.array(Image.open(path.join(pic)))

    # cloud parameters
    wc = WordCloud(background_color="white", max_font_size=150, max_words=250, mask=philmask)

    # generating the cloud
    wc.generate(posts)
    wc.to_file(path.join("philo.png"))

    image_colors = ImageColorGenerator(philmask)
    plt.figure(figsize=[7, 7])
    plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.savefig('phil-final.png')
    plt.show()

# saves the scraped titles into a file for further use
    with open('data.txt', 'w', encoding='UTF-8') as f:
        f.write(posts)
    f.close()

def get_string_posts(subreddit):
    # this function scrapes from the top posts of all time from a subreddit and returns it into a string variable
    text = ""
    for submission in subreddit.top(limit=limit):
        text += str(submission.title)
    return text



def create_wordcloud(file):  #this simply generates the wordcloud object, to be shown with matplotlib
    wordcloud = WordCloud().generate(file)
    return wordcloud




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

