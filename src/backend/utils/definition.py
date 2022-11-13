# import requests as req 
# from preprocessing import Preprocessor as prep

# class Definition():
#     """Defines a given word using the wikipedia API."""

#     def __init__(self):
#         self.wikiurl = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles="

#     def get_definition(self, genre: str, ending: str='music') -> str:
#         """Get the definition of a genre from Wikipedia. Removing stop words and punctuation.

#         Args:
#             genre (str): Genre to get the definition of.

#         Returns:
#             str: Definition of the genre.
#         """
        
#         response = req.get(self.wikiurl + genre + ' ' + ending)
#         data = response.json()

#         # TODO: Ugly function, fix later
#         if 'error' in data:
#             return ''
#         elif 'missing' in data['query']['pages'][list(data['query']['pages'].keys())[0]] and ending == '':
#             return ''
#         elif 'missing' in data['query']['pages'][list(data['query']['pages'].keys())[0]]:
#             return self.get_definition(genre, ending='')
#         else:
#             return prep().remove_stops_and_punctions(data['query']['pages'][list(data['query']['pages'].keys())[0]]['extract'])

#     def __unfound_definiton(self, string: str) -> str:
#         """Returns a string of similar words, if the genre is not found
        
#         Args:
#             string (str): String to find similar words of.
        
#         Returns:
#             str: String of similar words.
#         """

#         return f'No definition found for {string}'



