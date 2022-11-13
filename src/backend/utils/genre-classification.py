import os
import time
import requests as req
from numba import jit
import numpy as np

import pandas as pd
import spacy
# from definition import Definition as defi
from preprocessing import Preprocessor as prep

class GenreClassification():
    def __init__(self, csv: str='genres') -> None:
        self.nlp = spacy.load('en_core_web_lg')
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') # Path to the root directory
        self.genres = None
        self.__load_genres(csv) # Load the list of genres

    def __load_genres(self, csv: str) -> list:
        """Load the list of genres, with their definitions.
        
        Args:
            csv (str): Path to csv file.
            
        Returns:
            None
        """
        try:
            self.genres = pd.read_csv(f'{self.path}/data/{csv}.csv') 
        except FileNotFoundError:
            print('File not found, please check the path to the csv file.')
            exit()

    def __generate_n_grams(self, string: str, ngram: int=2) -> list:
            """Generate n-grams from a string.

            Thanks to: https://www.analyticsvidhya.com/blog/2021/09/what-are-n-grams-and-how-to-implement-them-in-python/

            Args:
                text (str): String to generate n-grams from.
                ngram (int): Number of words in the n-grams.

            Returns:
                list: List of n-grams.
            """
            words = [word for word in string.split(" ") if word not in self.nlp.Defaults.stop_words]
            temp = zip(*[words[i:] for i in range(0,ngram)])
            ans = [' '.join(ngram) for ngram in temp]
            return ans

    def genre_similarity(self, string: str, limit :int = 10) -> list:
        similar_genres = []
        
        for genre in self.genres.genre:
            input = self.nlp(prep().remove_gendered_language(prep().remove_stops_and_punctions(string)))
            genre_information = self.nlp(genre + str(self.genres.loc[self.genres.genre == genre].definition.values[0]))

            similarity = input.similarity(genre_information)
            similar_genres.append((genre, similarity))

        similar_genres = pd.DataFrame(similar_genres, columns=['genre', 'similarity'])
        similar_genres.sort_values(by='similarity', ascending=False, inplace=True)
        similar_genres.reset_index(drop=True, inplace=True)
        
        return similar_genres[:limit if limit < len(similar_genres) else len(similar_genres)]


    def most_similar(self, word, topn=5):
        """Get the most similar words to a word.

        Args:
            word (str): Word to get the most similar words to.
            topn (int): Number of similar words to return.

        Returns:
            list: List of tuples containing the most similar words and their similarity.
        """


start_time = time.time()    
print('Loading model...')
print(GenreClassification('mainstream_with_definitions').genre_similarity('feeling like clouds'))
print("--- %s seconds ---" % round((time.time() - start_time)))

# IDEAS: Take n-grams from the definition and compare them to the n-grams of the string. 
    #  Use this to increase the similarity score.

# GOALS:
    # 1. Create a function that takes in a word and/or n-gram and can return a list of similar words.
    # 2. Create a function that takes the given input string and can reverse lookup words similar to that  
        # dinosaur -> animal, prehistoric, extinct, etc.

# TODO: Genre Tree
    # Major genres
    # Subgenres
    # Subsubgenres
    # etc.
    # https://en.wikipedia.org/wiki/List_of_music_genres