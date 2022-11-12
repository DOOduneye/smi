import os
import time
import requests as req
from numba import jit
import numpy as np

import pandas as pd
import spacy
from definition import Definition as defi

class GenreClassification():
    def __init__(self, csv: str='genres') -> None:
        self.nlp = spacy.load('en_core_web_lg')
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') # Path to the root directory
        self.genres = None
        self.__load_genres(csv) # Load the list of genres

    def __load_genres(self, csv: str) -> list:
        """If the csv file exists, load the list of genres from the csv file.
        Otherwise, download the list of genres from Wikipedia and save it to a csv file.
        
        Args:
            csv (str): Path to csv file.
            
        Returns:
            None
        """

        if not os.path.exists(f'{self.path}/data/genres_with_definitons.csv'):
            self.genres = self.__add_definitions(pd.read_csv(f'{self.path}/data/{csv}.csv'))
            self.genres.to_csv(f'{self.path}/data/genres_with_definitons.csv', index=False)
        else:
            self.genres = pd.read_csv(f'{self.path}/data/genres_with_definitons.csv')

    def __add_definitions(self, dataframe) -> pd.DataFrame:
        """Add definitions to a dataframe of genres.

        Args:
            pd.DataFrame: Dataframe of genres.

        Returns:
            pd.DataFrame: Dataframe of genres with definitions.
        """

        definitions = []
        for genre in dataframe.genre:
            defined_word = defi().get_definition(genre)
            n_grammed = self.__generate_n_grams(defined_word)
            definitions.append(n_grammed)
        dataframe['definition'] = definitions

        return dataframe

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

        # Use n -grams to parse genres with multiple words
        similar_genres = []
        
        for genre in self.genres.genre:
            definition = str(self.genres.loc[self.genres.genre == genre].definition.values[0])
            if definition != '':
                similarity = self.nlp(string).similarity(self.nlp(genre + definition))
            else:
                similarity = self.nlp(string).similarity(self.nlp(genre))

            similar_genres.append((genre, similarity))
        similar_genres = pd.DataFrame(similar_genres, columns=['genre', 'similarity'])
        similar_genres.sort_values(by='similarity', ascending=False, inplace=True)
        similar_genres.reset_index(drop=True, inplace=True)
        
        return similar_genres[:limit if limit < len(similar_genres) else len(similar_genres)]


    # def most_similar(self, word, topn=5):
    #     """Get the most similar words to a word.

    #     Args:
    #         word (str): Word to get the most similar words to.
    #         topn (int): Number of similar words to return.

    #     Returns:
    #         list: List of tuples containing the most similar words and their similarity.
    #     """
    #     word = self.nlp(word)
    #     return sorted(word, key=lambda w: self.cosine_similarity_numba(w.vector, word.vector), reverse=True)


    # @jit(nopython=True)
    # def cosine_similarity_numba(u:np.ndarray, v:np.ndarray):
    #     assert(u.shape[0] == v.shape[0])
    #     uv = 0
    #     uu = 0
    #     vv = 0
    #     for i in range(u.shape[0]):
    #         uv += u[i]*v[i]
    #         uu += u[i]*u[i]
    #         vv += v[i]*v[i]
    #     cos_theta = 1
    #     if uu != 0 and vv != 0:
    #         cos_theta = uv/np.sqrt(uu*vv)
    #     return cos_theta



start_time = time.time()    
print('Loading model...')
# print(GenreClassification('en_core_web_lg', 'mainstream').genre_similarity('Dinosaurs'))
print("--- %s seconds ---" % round((time.time() - start_time)))
print(GenreClassification('mainstream').genre_similarity('Dinosaurs'))

# IDEAS: Take n-grams from the definition and compare them to the n-grams of the string. 
    #  Use this to increase the similarity score.

# TODO: Genre Tree
    # Major genres
    # Subgenres
    # Subsubgenres
    # etc.
    # https://en.wikipedia.org/wiki/List_of_music_genres