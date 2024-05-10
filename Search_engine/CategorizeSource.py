import csv

def categorize_csv(filename):
    categorized_data = {}

    # Open the CSV file and read its contents
    with open(filename, 'r', encoding='utf-8', errors='replace') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file
        for row in reader:
            # Extract the value from column
            source_ = row['Source website']
            
            # Create a new list for this source if it doesn't exist in the categorized data
            if source_ not in categorized_data:
                categorized_data[source_] = []
            
            # Append the current row to the list corresponding to its source
            categorized_data[source_].append(row)
    
    return categorized_data

def return_new_csv(categorized_data, output_filename):
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Link', 'Source website', 'Website link', 'Title', 'Description', 'Author', 'Published date', 'Type', 'Image']  # Adjust fieldnames as needed
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Write categorized data to the CSV file
        for source_, rows in categorized_data.items():
            for row in rows:
                writer.writerow(row)

# Specify the correct path to CSV file
filename = 'Search_engine/newBlockchaintablechangeUpdated.csv'
categorized_data = categorize_csv(filename)
output_filename = 'Sources.csv'
return_new_csv(categorized_data, output_filename)
