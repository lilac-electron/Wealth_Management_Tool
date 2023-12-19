#import pandas as pd
#df = pd.read_excel('example.xlsx', sheet_name='Sheet1')
#print(df)

import openpyxl

def read_excel_file(file_path):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)
    
    # Assuming the data is in the first sheet (you can modify this accordingly)
    sheet = workbook.active
    
    # Dictionary to store the extracted data
    data_list = []
    
    # Iterate through rows starting from the second row (assuming the first row is headers)
    for row in sheet.iter_rows(min_row=6, values_only=True):
        date, description, money_in, money_out, balance = row
        
        # Add money_in, money_out, and balance to the dictionary
        data_list.append((date, money_in, money_out, balance, description))
        #print(len(data_list))
    
    return data_list

# Example usage
file_path = 'Statement_2023.xlsx'
result_list = read_excel_file(file_path)

# Print the result
total_out = 0
total_in = 0
total_balance = 0
for data_tuple in result_list:
    date, money_in, money_out, balance, description = data_tuple
    #print(f"Date: {date}, Money In: {money_in}, Money Out: {money_out}, Balance: {balance}, Description: {description}")
    #print (str(money_in))
    total_in += float(money_in) if money_in is not None else 0
    total_out += float(money_out) if money_out is not None else 0
    total_balance += float(balance) if balance is not None else 0

print(total_in)
print(total_out)
print(total_in-total_out)
print(balance)