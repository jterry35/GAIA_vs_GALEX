# \ Cluster name (Ex: Berkeley 12)
# |        ra       |         dec       |
# |       double    |        double     |
#  ################  ###################


import os
import csv


# Set the directory path containing the CSV files
input_dir = r"C:\Workspace\GAIA_vs_GALEX\data\Galex"
output_dir = r"C:\Workspace\GAIA_vs_GALEX\IPACFormated"
RA_COL = "ra"
DEC_COL = "dec"

def max_column_length(reader, column_name):
    max_length = 0
    # Iterate over each row in the CSV file
    for row in reader:
        # Get the value from the specified column
        value = row[column_name]
        
        # Update the maximum length if the value is longer
        if len(value) > max_length:
            max_length = len(value)
    
    return max_length

def center_values(value1, value2, width):
    # Calculate the number of spaces to pad on each side of each value
    padding = (width - len(value1) - len(value2) - 2) // 2
    
    # Build the padded values with spaces on each side
    padded_value1 = f"{' ' * padding}{value1}{' ' * padding}"
    padded_value2 = f"{' ' * padding}{value2}{' ' * padding}"
    
    # If the width is odd, add an extra space on the right side of the second value
    if len(padded_value1) + len(padded_value2) + 2 < width:
        padded_value2 += ' '
    
    # Concatenate the two padded values with pipe characters
    centered_values = f"|{padded_value1}|{padded_value2}|"
    
    return centered_values

def writeIPACFile(name, contents):
    filename = "{}.txt".format(name)

    # Create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, filename), "w") as outfile:
        for element in contents:
            outfile.write(element + "\n")

# Iterate over each file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(input_dir, filename)
        
        # Open the CSV file and extract the values from the specified columns
        with open(filepath, "r") as csvfile:
            reader = csv.DictReader(csvfile)

            # get the longest value in each of the columns
            decColWidth = max_column_length(reader, DEC_COL)
            raColWidth = max_column_length(reader, RA_COL)
            max_decimals = max(decColWidth, raColWidth)

            filename_without_extension = os.path.splitext(filename)[0]

            # reset the file back to the beggining
            csvfile.seek(0)

            # move the reader to row 1.. skipping the header row
            next(reader)

            output = []
            output.append("\\ {}".format(filename_without_extension))
            output.append("| {:^{width}} | {:^{width}} |".format("ra", "dec", width=decColWidth))
            output.append("| {:^{width}} | {:^{width}} |".format("double", "double", width=decColWidth))
        
            for row in reader:
                # get the values from each column
                ra = row[RA_COL]
                dec = row[DEC_COL]

                # create the formatted string with the values of ra and dec
                output.append("  {:^{width}}   {:^{width}}  ".format(ra, dec, width=decColWidth))

            writeIPACFile(filename_without_extension, output)

