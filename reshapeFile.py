import pandas as pd
from datetime import datetime

def normalize_date(date_str):
    """
    Normalize the date to be on the first of the next month.
    """
    # Try different date formats if necessary
    for date_format in ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d']:
        try:
            date_obj = datetime.strptime(date_str, date_format)
            year = date_obj.year
            month = date_obj.month
            # Increment month and adjust year if necessary
            if month == 12:
                month = 1
                year += 1
            else:
                month += 1
            return datetime(year, month, 1).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None  # Return None if no format matches

def convert_to_number(value):
    """
    Convert values with abbreviations to actual numbers.
    T -> Trillion, B -> Billion, M -> Million, K -> Thousand
    """
    if pd.isna(value):
        return value

    if value[-1] == 'T':
        return float(value[:-1]) * 10**12
    elif value[-1] == 'B':
        return float(value[:-1]) * 10**9
    elif value[-1] == 'M':
        return float(value[:-1]) * 10**6
    elif value[-1] == 'k':
        return float(value[:-1]) * 10**3
    else:
        return float(value)

def transform_stock_data(input_file, output_file):
    # Load the data
    data = pd.read_csv(input_file)

    # Rename 'Unnamed: 0' column to 'Statistic'
    data = data.rename(columns={'Unnamed: 0': 'Statistic'})

    # Columns to pivot
    pivot_cols = ['As of Date: 1/20/2024Current', '9/30/2023', '6/30/2023', '3/31/2023', '12/31/2022',
                  '10/31/2023', '7/31/2023', '4/30/2023', '1/31/2023', '10/31/2022',
                  'As of Date: 1/19/2024Current', '11/30/2023', '8/31/2023', '5/31/2023',
                  '2/28/2023', '11/30/2022']

    # Perform the pivot
    pivoted_data = data.melt(id_vars=['Ticker', 'Statistic'], value_vars=pivot_cols,
                             var_name='Date', value_name='Value')

    # Remove "As of Date:" from the 'Date' column
    pivoted_data['Date'] = pivoted_data['Date'].str.replace('As of Date: ', '')
    pivoted_data['Date'] = pivoted_data['Date'].str.replace('Current', '')

    # Convert values in 'Value' column to actual numbers
    pivoted_data['Value'] = pivoted_data['Value'].apply(convert_to_number)

    # Remove rows with NaN values in 'Value' column
    pivoted_data = pivoted_data.dropna(subset=['Value'])

    # Update the date to be the first of the month
    pivoted_data['Date'] = pivoted_data['Date'].apply(lambda x: normalize_date(x))

    # Save the transformed data to a new CSV file
    pivoted_data.to_csv(output_file, index=False)

# Example usage
input_file = 'stock_data.csv'  # Replace with your input file path
output_file = 'snp500_statistics.csv'  # Replace with your desired output file path

transform_stock_data(input_file, output_file)
