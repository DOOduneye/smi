import os
import pandas as pd
import time
import spacy 

class GenreClassification():
    def __init__(self, lang: str='en_core_web_lg', csv: str='genres') -> None:
        self.nlp = spacy.load(lang)
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.genres = self.load_genres(csv)
        print(self.genres)
        
    def load_genres(self, csv: str='genre') -> list:
        """Load a list of genres from a csv file.

        Args:
            csv (str): Path to csv file.

        Returns:
            list: List of genres.
        """
        return pd.read_csv(os.path.join(self.path, csv + '.csv'))
    
    def load_nlp(self, nlp):
        """Load a different spacy model.
        
        Args:
            nlp (str): Name of the spacy model to load.
            
        Returns:
            None
        """
        self.nlp = nlp
    
    def tokenize(self, string: str) -> list:
        """Tokenize a string into a list of tokens, removing punctuation and whitespace.    

        Args:
            string (str): String to tokenize.

        Returns:
            list: List of tokens.
        """
        doc = self.nlp(string)
        return [token.text for token in doc]
    
    def lemmatize(self, string: str) -> list:
        """Lemmatize a string into a list of tokens, removing punctuation and whitespace. 

        Args:
            string (str): String to lemmatize.

        Returns:
            list: List of tokens.
        """
        doc = self.nlp(string)
        return [token.lemma_ for token in doc]
    
    def genre_similarity(self, string: str) -> list:
        start_time = time.time()
        max_similarity = 0
        best_genre = ''
        
        for genre in self.genres.genre:
            current_similarity = self.nlp(string).similarity(self.nlp(genre))
            print(genre, current_similarity)
            if current_similarity > max_similarity:
                max_similarity = current_similarity
                best_genre = genre
                
        return (best_genre, max_similarity, "~" + str(round(abs(start_time - time.time()), 2)) + "ms")
    
    def genre_similarity_v2(self, string: str) -> list:
        start_time = time.time()
        similar_genres = []
        
        for genre in self.genres.genre:
            current_similarity = self.nlp(string).similarity(self.nlp(genre))
            print(genre, current_similarity)
            if current_similarity > 0.5:
                similar_genres.append((genre, current_similarity))
        
        similar_genres = pd.DataFrame(similar_genres, columns=['genre', 'similarity'])
        similar_genres.sort_values(by='similarity', ascending=False, inplace=True)
        similar_genres.reset_index(drop=True, inplace=True)
        
        return (similar_genres, "~" + str(round(abs(start_time - time.time()), 2)) + "ms")
    
print(GenreClassification('en_core_web_lg').genre_similarity_v2('I like to listen to rock music'))


# TODO: See how long it takes to handle all genres -> c
    # If too long, we can instead do hiearichal, where we first classify into genre groups, then into genres.
    # genre_group -> major genres, subgenres, sub-subgenres until we find the best match.