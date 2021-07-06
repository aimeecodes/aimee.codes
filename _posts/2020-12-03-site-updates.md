---
layout: post
title: "Site Updates"
date: 2020-12-03
tags: [projects, jekyll]
---

Here's a list of the most recent updates to the site!
* Completely overhauled the site's `css` based around the responsive top navigation bar, with the classic hamburger drop down mobile menu - thank you to <a href="https://www.youtube.com/watch?v=8QKOaTYvYUA">Kevin Powell</a> for the easy to follow tutorial!
* Reformatted how tables are displayed! In an upcoming post, I work with long and kind of unweildy data summaries and I want a clean way of displaying that for both desktop and mobile users. Using <a href="https://css-tricks.com/responsive-data-tables/">this</a> as my jumping off point, I made the tables easier to view on a mobile device (rows transform into "cards"). By default, only the headers, 2 rows of data, and a link to the full table are displayed to avoid content disruption.
    <br>*If you want to see the change happen live and you're on the desktop site, try resizing the window under 1000px*

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th class='text'>Feature</th>
      <th class='numeric'>NA Count</th>
      <th class='numeric'>% Missing</th>
      <th class='text'>Data Type</th>
      <th class='text'>Overview</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th data-title='Feature' class='text'>PoolQC</th>
      <td data-title='NA Count' class='numeric'>2909</td>
      <td data-title='% Missing' class='numeric'>0.99657</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, Ex, Fa, Gd]</td>
    </tr>
    <tr>
      <th data-title='Feature' class='text'>MiscFeature</th>
      <td data-title='NA Count' class='numeric'>2814</td>
      <td data-title='% Missing' class='numeric'>0.96403</td>
      <td data-title='Data Type' class='text'>object</td>
      <td data-title='Overview' class='text'>[nan, Shed, Gar2, Othr, TenC]</td>
    </tr>
    <tr>
      <th class='styling-space'>...</th>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
      <td class='styling-space' class='disappearing'>...</td>
    </tr>
  </tbody>
</table>

<a class='read-more-link' href='/assets/html-tables/2021-03-17/missing-values-responsive-asset-access.html'> See full table </a>

* Created content pages so when you do access the linked full table, or a plot , the `css` formatting makes the table easier to read, in both mobile and desktop view
* Changed graphics from `.png` format to `.svg` and create multiple `@media` inquiries in `css` to determine picture position / scaling for different screen sizes
    <br>*Note - this only applies to my most recent posts, as I have not yet revisited the graphs generated in Octave from Andrew Ng's Machine Learning course*
* Now `assets/` holds ~all~ site assets, including `css` code, images, html tables, and (now) fonts! Within `assets/` items are organized on a media type level first, then further divide into specific posts. This might change in the future when the media I use gets significantly more complicated

___

### Upcoming Changes ###
* Create site logo, to be displayed alongside navigation bar
* Update `css` to shrink top bar on horizontal mobile displays
* Add alt-text and titles to all images
* Add rounded edges to tables, to match other site formatting

___

Now that I'm satisfied with the site changes (...for now...) I'm going to replace my web dev hat with my data analyst one. My next post in the Iowa housing dataset involes both data cleaning and feature engineering. It's been a long time coming, and I'm excited to share what I've been up to!

Until next time, 祝好！
