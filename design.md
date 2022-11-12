# Music Classifcation API (MCAPI) Design Document

## Motivation

The motivation for this project is to better understand relationships. I have a large passion for music and have always wanted to work on a project that takes that hobby into account. I also don't like Spotify's recommendaiton system and although I don't think it's possible or realistic to try and improve on it, I think it would be interesting to try and create a system that is more flavorfull and more personal. 

## Problem Statement
- Simply taking in a genre and using word2vec to find similar genres is not enough. 
    1. A song is not just one genre, it is a combination of genres.
    2. A song can be a combination of genres that are not similar to each other.
    3. I think most importantly, you cannot classify a song by the name of the genre. 

## Goals    

We need to find a way to classify a phrase into a specific genre class. For example, we would like to classify "biker" into punk music. Though since this term can be multifaceted, as well as anything else given, classifications occurs over multiple genres.


![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)
![SpaCy](https://img.shields.io/badge/spacy-2.0.11-blue.svg)
