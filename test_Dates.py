from datetime import datetime
import calendar

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
            return datetime(year, month, 1).strftime('%m/%d/%Y')
        except ValueError:
            continue
    return None  # Return None if no format matches

# Example usage
example_date = "1/30/2023"
normalized_date = normalize_date(example_date)
print(normalized_date)
