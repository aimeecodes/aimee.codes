---
layout: post
title: "Process Pooling and Ordered Outputs"
date: 2021-08-2
tags: [python, big book of small python projects, multiprocessing]
---

Lately, I have been searching for meaningful or interesting projects to motivate me to do the following things:
* Write more code
* Write better code
* Learn a new programming language (right now, I work almost entirely in python, and can comfortably use Java, R, and MATLAB)

___

### Problem description ###

Since I am feeling stuck with my data and machine learning projects, I want to stop looking at `pandas` DataFrames for a while. To give myself a new bone to chew on, I picked up [Al Sweigart\'s *The Big Book of Small Python Projects*](https://nostarch.com/big-book-small-python-projects). In one exercise, a Monte-Carlo simulation demonstrates the effect of the so-called [Birthday Problem](https://en.wikipedia.org/wiki/Birthday_problem): as the number of people in a room increases, the probability that some people in that room share a birthday grows quickly, faster than you might think!

While the book\'s code is very clear, I want to pare the program down:
* Birthdays are now represented by integer values between 1 and 365 instead of `datetime` objects
* The function that checks for collisions returns a boolean, rather than the first colliding birthday it finds (this part of the code accounted for a lot of the original program\'s time complexity, since it found collisions using nested `for` loops)

{% highlight python %}
def getBirthdays(n):
    """ n is an integer;
        getBirthdays generates
        n birthdays for n people,
        returns a list of birthdays
        of length n """
    birthdays = [random.randint(
	  1,365) for i in range(n)]
    return birthdays

def checkCollisions(dates):
    """ checks a list of
	integer values for duplicates
	/ collisions """
    if len(set(dates)) == len(dates):
        return False
    else:
        return True
{% endhighlight %}

Since this is a Monte Carlo simulation, the process of generating birthdays &rarr; checking for collisions &rarr; reporting a collision has to be repeated on the order of 100,000 times. After running the code on a single core a few times and impatiently waiting for a few seconds, I remembered my current setup has 8 cores. Sounds like a job for `multiprocessing.Pool`!

To use `multiprocessing.Pool`\'s `map`, I need a function and an iterable. My plan:
* Create a list of length 100,000 called `maplist`, where each item in the list is the number of birthdays we want to generate
* Create a function which, given a number n, generates n birthdays &rarr; checks these birthdays for collisions &rarr; returns `0`  or `1`

Here is the function:
{% highlight python %}
def generateAndCheckBirthdays(n):
    """ generates n dates, and checks
	the dates for collisions """
    birthdays = getBirthdays(n)
    result =
	  checkCollisions(birthdays)
    if result: return 1
    else: return 0
{% endhighlight %}

I store these results in another list called `results`, sum over the list, and see how many trials in the 100,000 produced any colliding birthdays.

{% highlight bash %}
$ python unattendedpartiesopt.py 30 8

Checking 30 random birthdays using
8 process(es) 100,000 times...

map               0.526920 seconds.

imap_unordered    0.000027 seconds.

imap_unordered    19732.625 times
                  faster than map
                  in 0.00507% of
                  the ordered time.

70550/100,000 trials had
matching birthdays.
Group of 30 has a 70.55% chance of
matching birthdays.
{% endhighlight %}

___

### `map` or `imap_unordered`? ###

`map` preserves ordering. This means that if I need a result to be accessible at the same index, `map` will do this for me, with an increased time complexity cost. However, if I am not concerned with the order I receive results from `map`, I can use `Pool.imap_unordered`.

In the case of this Birthday Problem, I do not care about the ordering - if a result generated using data at `maplist[i]` is accessible at `results[j]`, this is not a big deal since all members of `maplist` are the same value. The reason `imap_unordered` is faster is because each process does not have to wait for the previous one to finish in order to begin its execution. The question is... how much faster?

___

### Setting up the simulations ###

I wanted to see how much faster `imap_unordered` worked than `map`; keeping in mind that I am just tracking how fast this program is executed, I added some pieces to the code for consistency across different CPUs and number of birthdays generated:
* setting python\'s `random.seed(23)` to generate the same pseudo-random birthdays every time
* importing `sys` so `NUM_BDAYS` and `NUM_PROCESSES` can be passed in as command line arguments via `sys.argv[1]` and `sys.argv[2]`, respectively

I have two machines to run the program on:
* A laptop with a 4 core / 8 thread i7-8550U CPU
* A desktop with a 16 core / 32 thread Ryzen 9 5950x CPU

There is a world of differences between these two chips, so the only meaningful data we can get out of this experiment is how much faster the Ryzen chip runs this program than the i7 with the same parameters.

The results are grouped by `NUM_PROCESSES` (1, 8, 32); each row displays a trial\'s `NUM_BDAYS` generated, and how fast it ran on the:
* i7 using `map`
* Ryzen using `map`
* i7 using `imap_unordered` (`imap_un`)
* Ryzen using `imap_unordered` (`imap_un`)

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th class='text'>NUM_PROCESSES</th>
      <th class='numeric'>NUM_BDAYS</th>
      <th class='numeric'>i7 map</th>
      <th class='text'>Ryzen map</th>
      <th class='text'>i7 imap_un</th>
	  <th class='text'>Ryzen imap_un</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th data-title='NUM_PROCESSES' class='text'>1</th>
      <td data-title='NUM_BDAYS' class='numeric'>30</td>
      <td data-title='i7 map' class='numeric'>1.850070</td>
      <td data-title='Ryzen map' class='text'>1.884730</td>
      <td data-title='i7 imap_un' class='text'>0.000026</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000019</td>
    </tr>
    <tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>70</td>
      <td data-title='i7 map' class='numeric'>4.160560</td>
      <td data-title='Ryzen map' class='text'>4.421220</td>
      <td data-title='i7 imap_un' class='text'>0.000030</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000020</td>
    </tr>
    <tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>700</td>
      <td data-title='i7 map' class='numeric'>1.850070</td>
      <td data-title='Ryzen map' class='text'>1.884730</td>
      <td data-title='i7 imap_un' class='text'>0.000026</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000019</td>
    </tr>
    <tr>
      <th data-title='NUM_PROCESSES' class='text'>8</th>
      <td data-title='NUM_BDAYS' class='numeric'>30</td>
      <td data-title='i7 map' class='numeric'>0.538490</td>
      <td data-title='Ryzen map' class='text'>0.252430</td>
      <td data-title='i7 imap_un' class='text'>0.000032</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000024</td>
    </tr>
	<tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>70</td>
      <td data-title='i7 map' class='numeric'>1.233160</td>
      <td data-title='Ryzen map' class='text'>0.560390</td>
      <td data-title='i7 imap_un' class='text'>0.000034</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000023</td>
    </tr>
	<tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>700</td>
      <td data-title='i7 map' class='numeric'>13.265560</td>
      <td data-title='Ryzen map' class='text'>5.698570</td>
      <td data-title='i7 imap_un' class='text'>0.000035</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000031</td>
    </tr>
	<tr>
      <th data-title='NUM_PROCESSES' class='text'>32</th>
      <td data-title='NUM_BDAYS' class='numeric'>30</td>
      <td data-title='i7 map' class='numeric'>/</td>
      <td data-title='Ryzen map' class='text'>0.138530</td>
      <td data-title='i7 imap_un' class='text'>/</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000026</td>
    </tr>
	<tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>70</td>
      <td data-title='i7 map' class='numeric'>/</td>
      <td data-title='Ryzen map' class='text'>0.303690</td>
      <td data-title='i7 imap_un' class='text'>/</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000021</td>
    </tr>
	<tr>
      <th data-title='NUM_PROCESSES' class='text'></th>
      <td data-title='NUM_BDAYS' class='numeric'>700</td>
      <td data-title='i7 map' class='numeric'>/</td>
      <td data-title='Ryzen map' class='text'>3.081280</td>
      <td data-title='i7 imap_un' class='text'>/</td>
	  <td data-title='Ryzen imap_un' class='text'>0.000026</td>
    </tr>
	</tbody>
</table>
<p align="center"><sup>Even when I try to get away from data, there is no escape!</sup></p>

Clearly `imap_unordered`, pardon my French, whips ass, and so does that Ryzen 9 5950x.

___

Seeing the huge time delay between `map` and `imap_unordered` got me thinking about using `imap_unordered` with a results dictionary, which lead me down the stack hole to `multiprocessing.Manager` objects and the `itertools` library. While I dig myself out, feel free to check out the script from this post `unattendedpartiesopt.py` [here](https://github.com/aimosjo/aimee.codes/blob/main/assets/code/2021-08-02/unattendedpartiesopt.py) on my github. Perhaps I will have enough material to write a post on `itertools` by the time I emerge!

Until next time!
