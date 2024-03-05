import pandas as pd

def create_excel_file(file_path, sheet_data):
    # Create a Pandas Excel writer using xlsxwriter as the engine
    writer = pd.ExcelWriter(file_path)
    
    # Iterate through the sheet data
    for sheet_name, column_names in sheet_data.items():
        # Create a DataFrame with column names
        df = pd.DataFrame(columns=column_names)
        
        # Fill the DataFrame with zeros below the column names
        for col in column_names:
            df[col] = [0]
        
        # Write the DataFrame to the Excel file
        df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    # Save the Excel file
    writer._save()

# Example usage:
file_path = 'exampleCreation.xlsx'
sheet_data = {
    'credits': ['Mortgage', 'Rent', 'Car Payment'],  # List for 'credits' sheet
    'assets': ['Asset1', 'Asset2', 'Asset3'],      # List for 'assets' sheet
    'retirement': ['Retirement1', 'Retirement2'],  # List for 'retirement' sheet
    'savings': ['Savings1', 'Savings2', 'Savings3'] # List for 'savings' sheet
}

create_excel_file(file_path, sheet_data)
print(f'Excel file "{file_path}" created successfully.')