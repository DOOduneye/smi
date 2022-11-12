import os
import time
import requests as req

import pandas as pd
import spacy
from spacy.lookups import Lookups

class GenreClassification():
    def __init__(self, lang: str='en_core_web_lg', csv: str='genres') -> None:
        self.nlp = spacy.load(lang)
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
        self.genres = ""
        self.__get_list(csv)

    def __get_list(self, csv: str) -> list:
        """If the csv file exists, load the list of genres from the csv file.
        Otherwise, download the list of genres from Wikipedia and save it to a csv file.
        
        Args:
            csv (str): Path to csv file.
            
        Returns:
            None
        """

        if not os.path.exists(f'{self.path}/data/genres_with_definitons.csv'):
            self.genres = self.load_genres(csv)
            self.__save_definitions()
        else:
            self.genres = pd.read_csv(f'{self.path}/data/genres_with_definitons.csv')
    
    def __save_definitions(self):
        """Save the definitions of the genres to a csv file.

        Returns:
            None
        """
        self.genres.to_csv(f'{self.path}/data/genres_with_definitons.csv', index=False)

    def __add_definitions(self, dataframe) -> pd.DataFrame:
        """Add definitions to a dataframe of genres.

        Args:
            pd.DataFrame: Dataframe of genres.

        Returns:
            pd.DataFrame: Dataframe of genres with definitions.
        """

        definitions = []
        for genre in dataframe.genre:
            definitions.append(self.__remove_stops_and_punctions(self.__get_definition(genre)))
        
        dataframe['definition'] = definitions

        return dataframe

    def __remove_stops_and_punctions(self, string: str) -> str:
        """Remove stopwords and punctuation from a string.

        Args:
            string (str): String to remove stopwords and punctuation from.

        Returns:
            str: String without stopwords and punctuation.
        """
        return ' '.join([token.text for token in self.nlp(string) if not token.is_stop and not token.is_punct])

    def __get_definition(self, genre: str, ending: str='music') -> str:
        """Get the definition of a genre from Wikipedia.

        Args:
            genre (str): Genre to get the definition of.

        Returns:
            str: Definition of the genre.
        """
        
        url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=" + genre + ' ' + ending
        response = req.get(url)
        data = response.json()
        if 'error' in data:
            return ''
        elif 'missing' in data['query']['pages'][list(data['query']['pages'].keys())[0]] and ending == '':
            return ''
        elif 'missing' in data['query']['pages'][list(data['query']['pages'].keys())[0]]:
            return self.__get_definition(genre, ending='')
        else:
            return data['query']['pages'][list(data['query']['pages'].keys())[0]]['extract']

    def load_nlp(self, nlp):
        """Load a different spacy model.
        
        Args:
            nlp (str): Name of the spacy model to load.
            
        Returns:
            None
        """
        self.nlp = nlp
    
    def load_genres(self, csv: str='genre') -> list:
        """Load a list of genres from a csv file.

        Args:
            csv (str): Path to csv file.

        Returns:
            list: List of genres.
        """
        return self.__add_definitions(pd.read_csv(f'{self.path}/data/{csv}.csv'))

    
    def genre_similarity(self, string: str, limit :int = 10) -> list:
        similar_genres = []
        
        for genre in self.genres.genre:
            definition = str(self.genres.loc[self.genres.genre == genre].definition.values[0])
            current_similarity = self.nlp(string).similarity(self.nlp(genre + definition))
            similar_genres.append((genre, current_similarity))
        
        similar_genres = pd.DataFrame(similar_genres, columns=['genre', 'similarity'])
        similar_genres.sort_values(by='similarity', ascending=False, inplace=True)
        similar_genres.reset_index(drop=True, inplace=True)
        
        return similar_genres[:limit if limit < len(similar_genres) else len(similar_genres)]



start_time = time.time()    
print('Loading model...')
print(GenreClassification('en_core_web_lg', 'mainstream').genre_similarity('Dinosaurs'))
print("--- %s seconds ---" % round((time.time() - start_time)))


# TODO: See how long it takes to handle all genres -> 
    # If too long, we can instead do hiearichal, where we first classify into genre groups, then into genres.
    # genre_group -> major genres, subgenres, sub-subgenres until we find the best match.

    # Sample lyrics, titles, etc


