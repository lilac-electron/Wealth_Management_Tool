import openpyxl
from datetime import datetime, timedelta
import random

def is_payday(transaction_date, pay_day):
    #print(pay_day.day)
    #print(transaction_date.day)
    return transaction_date.day == pay_day.day

def generate_excel_file(file_path, num_transactions=600, outbound_frequency=0.7, pay_day=1, pay_day_amount=1400):
    # Create a new workbook and select the active sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    
    # Add headers
    headers = ["Date", "Description", "Money In", "Money Out", "Balance"]
    sheet.append(headers)
    
    # Generate diverse sample data
    transaction_date = datetime(2023, 1, 1)
    current_balance =
    
    for _ in range(num_transactions):
        # Generate a random date within a range
        transaction_date = transaction_date + timedelta(days=random.randint(0, 1))

        if is_payday(transaction_date, datetime(2023, transaction_date.month, pay_day)):
            current_balance += pay_day_amount
            sheet.append([transaction_date.strftime('%Y-%m-%d'), "Payday", pay_day_amount, 0, current_balance])
            
        
        # Determine if it's an inbound or outbound transaction
        if random.random() < outbound_frequency:
            transaction_date = transaction_date + timedelta(days=random.randint(0, 2))
            # Outbound transaction
            description = f"Expense {random.randint(1, 10)}"
            #money_out = random.randint(1, 500)
            money_out = random.randint(1, 70)
            money_in = 0
            current_balance -= money_out
        """else:
            # Inbound transaction
            description = f"Income {random.randint(1, 10)}"
            #money_in = random.randint(500, 1000)
            money_in = 1000
            money_out = 0
            current_balance += money_in"""
        
        # Append the transaction to the sheet
        sheet.append([transaction_date.strftime('%Y-%m-%d'), description, money_in, money_out, current_balance])
    
    # Save the workbook to the specified file path
    workbook.save(file_path)

# Specify the path where you want to save the Excel file
excel_file_path = 'generated_file_with_600_transactions_v4.xlsx'

# Call the function to generate the Excel file with 600 transactions
generate_excel_file(excel_file_path, num_transactions=600, outbound_frequency=0.97)

print(f"Excel file generated at: {excel_file_path}")
