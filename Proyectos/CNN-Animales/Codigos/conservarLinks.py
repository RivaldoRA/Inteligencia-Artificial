import pandas as pd

# Define the file path
file_path = './Datasets/multimedia.txt'

try:
    # Use read_csv and specify the delimiter as '\t' (tab)
    df = pd.read_csv(file_path, sep='\t')

    # The data is now stored in a pandas DataFrame called 'df'
    print("✅ File successfully loaded!")
    print("\n--- First 5 Rows of the Data ---\n")
    print(df.head())

    # https://inaturalist-open-data.s3.amazonaws.com, only keep the ones with this format
    # The prefix we are looking for in the 'identifier' column
    s3_prefix = 'https://inaturalist-open-data.s3.amazonaws.com'

    # 1. Create a boolean mask: True for rows that start with the prefix, False otherwise
    mask = df['identifier'].str.startswith(s3_prefix, na=False)

    # 2. Filter the entire DataFrame using the mask, and then select the 'identifier' column
    filtered_identifiers = df[mask]['identifier']

    # Assuming 'filtered_df' is the result of your filtering operation:
    # filtered_df = df[df['identifier'].str.startswith('https://inaturalist-open-data.s3.amazonaws.com')]

    # Define the output file name
    output_file_name = 'gatos.tsv'

    # Save the filtered DataFrame to a new TSV file
    filtered_identifiers.to_csv(
        output_file_name,
        sep='\t',     # Use tab as the delimiter for TSV
        index=False   # Do not write the pandas row index to the file
    )

    # 3. Print the result
    print(filtered_identifiers)

    # print("\n--- Data Types of the Columns ---\n")
    # print(df.dtypes)

except FileNotFoundError:
    print(f"❌ Error: The file '{file_path}' was not found. Please check the path.")
except Exception as e:
    print(f"❌ An error occurred while reading the file: {e}")