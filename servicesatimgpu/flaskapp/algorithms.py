import os

import inline as inline
import matplotlib
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import re
import string
from collections import defaultdict
import nltk
from nltk.corpus import stopwords
import string
import pymorphy2
from os import path
from os import listdir
from PIL import Image
import numpy as np
#определяем количество файлов в каталоге
import pathlib

def remove_urls(vTEXT):
    vTEXT = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', vTEXT, flags=re.MULTILINE)
    return (vTEXT)


#Mapper 1
def mapper1(data):
    words = re.split(r'\W+', data)
    for word in words:
        yield(word, 1)
#Mapper 2
def mapper2(data):
    words = re.split(r'\W+', data)
    for word in words:
        yield(word, 1)

#Reducer
#Defining the reducer function

def reducer(word, counts):
    yield(word, sum(counts))


#Reducer 1
#Preparing and feeding the data into the reducer function
def reduce1(data):
    text = defaultdict(list)
    for word, count in data:
        text[word].append(count)
    return[output
          for word, counts in text.items()
          for output in reducer(word, counts)]

#Reducer2
#Preparing and feeding the data into the reducer function
def reduce2(data):
    text = defaultdict(list)
    for word, count in data:
        text[word].append(count)
    return[output
          for word, counts in text.items()
          for output in reducer(word, counts)]