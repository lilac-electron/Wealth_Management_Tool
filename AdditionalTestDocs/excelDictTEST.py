import pandas as pd

def excel_to_dict(file_path):
    # Read the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Initialize an empty dictionary to store sheet data
    excel_dict = {}
    
    # Iterate through each sheet in the Excel file
    for sheet_name in xls.sheet_names:
        # Read the sheet into a DataFrame
        df = pd.read_excel(xls, sheet_name)
        
        # Convert the DataFrame to a dictionary and add it to the excel_dict
        excel_dict[sheet_name] = df.to_dict(orient='records')
    
    return excel_dict

# Example usage:
file_path = 'example.xlsx'  # Replace 'example.xlsx' with your Excel file path
result = excel_to_dict(file_path)
print(result['Credits'][0]['Mortgage'])
print(result)