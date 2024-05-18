import csv
import matplotlib.pyplot as plt

# Path to the CSV file containing Netflix titles data
csv_file_path = "netflix_titles.csv"

# Dictionary to store movie counts by country
countries_and_movies = {}

# Read the CSV file using csv.DictReader
with open(csv_file_path, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # Process each row in the CSV file
    for row in csv_reader:
        # Filter for movies
        if row['type'] == 'Movie':
            # Get the country
            country = row['country']
            
            # Increment movie count for the country
            if country:
                if country in countries_and_movies:
                    countries_and_movies[country] += 1
                else:
                    countries_and_movies[country] = 1

# Sort the dictionary by movie count in descending order
sorted_countries_movies = sorted(countries_and_movies.items(), key=lambda x: x[1], reverse=True)

# Get the top 5 countries and their movie counts
top_5_countries = sorted_countries_movies[:5]

# Separate the countries and counts for plotting
countries = [item[0] for item in top_5_countries]
movie_counts = [item[1] for item in top_5_countries]

# Create a bar plot to visualize the data
plt.figure(figsize=(10, 5))
plt.barh(countries, movie_counts, color='purple')
plt.xlabel("Number of Movies")
plt.ylabel("Country")
plt.title("Top 5 Countries with the Most Movies Released on Netflix")
plt.show()
