import csv
import matplotlib.pyplot as plt

csvFile = "bestSelling.csv"

# Dictionary to store the total units sold by each company
selling_console = {}

# Read the CSV file
with open(csvFile, mode="r", encoding="utf-8") as csv_file:
    csv_reader = csv.DictReader(csv_file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        company = row['Company']
        units_sold = row['UnitsSold']
        
        # Convert units sold to float and handle empty values
        if units_sold:
            units_sold = float(units_sold)
        else:
            units_sold = 0
        
        # If the company is already in the dictionary, add the units sold
        if company in selling_console:
            selling_console[company] += units_sold
        else:
            # Otherwise, add the company and initialize the units sold
            selling_console[company] = units_sold

# Get the top 5 companies by total units sold
top_5_companies = sorted(selling_console.items(), key=lambda x: x[1], reverse=True)[:5]

# Separate company names and total units sold for plotting
companies = [company for company, units_sold in top_5_companies]
units_sold = [units_sold for company, units_sold in top_5_companies]

# Plotting the data
plt.figure(figsize=(10, 6))
plt.barh(companies, units_sold, color='blue')
plt.xlabel('Units Sold (in millions)')
plt.ylabel('Company')
plt.title('Top 5 Companies by Total Units Sold')
plt.gca().invert_yaxis()
plt.show()