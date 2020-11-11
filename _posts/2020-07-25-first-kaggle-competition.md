---
layout: post
title: "first kaggle competition"
date: 2020-07-25
tags: [machine learning, projects, python, iowa housing]

---

Since my last post, after finishing Andrew Ng's Machine Learning course (which was incredibly fun, and a great introduction to the topic), I took a break from studying machine learning to look at another topic that has interested me: MIT's online <a href="https://ocw.mit.edu/resources/res-6-007-signals-and-systems-spring-2011/">Signals and Systems</a> course. After seeing convolution come up when discussing Laplace transforms in differential equations but not really understanding the operation behind it, I can visualize it with a lot more ease and accuracy. As for the electrical engineeering applications... I'll have to get back to you on that. 

Now that I'm back to putzing around with python, I'm finding Kaggle's microcourses are helping me find my footing, especially around scikit-learn. After completing their <a href="https://www.kaggle.com/learn/intro-to-machine-learning">introduction to ML</a> course (focused on decision trees and random forests), I joined the final course competition focused on predicting the sale price of houses in Ames, Iowa based on 81 features.

This dataset is important to me because I've only dealt with data which are either purely numerical, or purely categorical - this dataset comes in both, and the final predicted sale price needs to incorporate not just numerical features like lot size and year sold, but features like condition of the basement, garage, and type of sale, encoded in categories. 

So far, my latest lessons with python include:

* learning-naming-conventions-the-hard-way/dashes_for_directories_and_underscores_for_files.txt
* referencing absolute vs. local file paths
* using a preloaded script to save time on typing
~~~ python
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
~~~

Now that I've got my environment set up, expect another post dedicated to my exploration of this dataset - including plots!