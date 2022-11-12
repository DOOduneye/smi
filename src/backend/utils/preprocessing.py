from spacy.lang.en.stop_words import STOP_WORDS

class Preprocessor():
    def __init__(self):
        pass

    def remove_stops_and_punctions(self, string: str) -> str:
        """Remove stopwords and punctuation from a string.

        Args:
            string (str): String to remove stopwords and punctuation from.

        Returns:
            str: String without stopwords and punctuation.
        """
        return ' '.join([word for word in string.split(' ') if word not in STOP_WORDS and word.isalpha()])
