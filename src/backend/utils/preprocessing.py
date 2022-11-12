from spacy.lang.en.stop_words import STOP_WORDS

GENDERED_WORDS = set(
    """
    he she him her his hers himself
    girl boy man woman father daughter son grandfather
    grandmother grandson granddaughter step-sister step-father
    step-daughter step-son 
    """.split()
)
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

    def remove_gendered_language(self, string: str) -> str:
        """Remove gendered language from a string.

        Args:
            string (str): String to remove gendered language from.

        Returns:
            str: String without gendered language.
        """
        return ' '.join([word for word in string.split(' ') if word not in GENDERED_WORDS])