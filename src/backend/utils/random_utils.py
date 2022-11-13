
import pandas as pd

def main():
    # Open genres_with_definitions and the rows that are in the mainstream genre file

    genres_with_definitions = pd.read_csv('/Users/davidoduneye/projects/javascript/smi/src/backend/data/genres_with_definitions.csv')
    mainstream_genres = pd.read_csv('/Users/davidoduneye/projects/javascript/smi/src/backend/data/mainstream.csv')

    # Create a new dataframe with the genres that are in the mainstream genre file
    mainstream_with_definitions = pd.DataFrame(columns=['genre', 'definition'])

    for genre in mainstream_genres.genre:
        mainstream_with_definitions = mainstream_with_definitions.append(genres_with_definitions.loc[genres_with_definitions.genre == genre])
    
    print(mainstream_with_definitions)

    mainstream_with_definitions.to_csv('/Users/davidoduneye/projects/javascript/smi/src/backend/data/mainstream_with_definitions.csv', index=False)

main() 