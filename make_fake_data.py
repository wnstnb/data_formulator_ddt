from faker import Faker
import pandas as pd
import random
from dateutil.relativedelta import relativedelta

fake = Faker()

num_records = 2000  # Number of customer records to generate

data = []
for _ in range(num_records):
    data.append({
        'CustomerID': fake.unique.random_number(digits=5),
        'Name': fake.name(),
        'AccountType': random.choice(['Checking', 'Savings', 'Credit Card']),
        'Balance': round(random.uniform(100, 100000), 2),  # Balance between $100 and $100,000
        'TransactionCount': random.randint(1, 50),  # Number of transactions
        'Region': fake.state(),
        'JoinDate': fake.date_this_decade(),  # Date joined the bank
        'IsActive': random.choice([True, False]),
        'CreditScore': random.choice([None, random.randint(300, 850)])  # Credit score with None values
    })

df = pd.DataFrame(data)
df.to_csv('data/bank_data.csv', index=False)

print("CSV file 'bank_data.csv' created successfully.")


# --- Monthly Balance Data ---
monthly_balances = []
for _, row in df.iterrows():
    customer_id = row['CustomerID']
    join_date = pd.to_datetime(row['JoinDate'])
    current_date = pd.to_datetime(fake.date_this_year()) # End at this year for simplicity
    end_of_month = join_date

    while end_of_month <= current_date:
        # Simulate balance fluctuations (can be positive or negative)
        balance_change = round(random.uniform(-1000, 5000), 2)  # Change up to +/- $5000
        balance = round(row['Balance'] + balance_change,2)
        if balance < 0:
          balance = 0

        monthly_balances.append({
            'CustomerID': customer_id,
            'MonthEndDate': end_of_month.strftime('%Y-%m-%d'),  # Format as string for CSV
            'Balance': balance
        })

        end_of_month += relativedelta(months=1) # Get next month

monthly_balances_df = pd.DataFrame(monthly_balances)
monthly_balances_df.to_csv('data/monthly_balances.csv', index=False)
print("CSV file 'monthly_balances.csv' created successfully.")


# --- Transaction Data ---
transactions = []
for _, row in df.iterrows():
    customer_id = row['CustomerID']
    join_date = pd.to_datetime(row['JoinDate'])

    # Randomly decide if this customer has transactions (about 70% chance)
    has_transactions = random.random() < 0.7

    if has_transactions:
        num_transactions = random.randint(1, 30)  # Up to 30 transactions
        for _ in range(num_transactions):
            transaction_date = fake.date_between(start_date=join_date, end_date='today')
            transaction_type = random.choice(['Withdrawal', 'Deposit', 'Transfer', 'Payment', 'Fee'])
            description = fake.sentence(nb_words=5)  # Short description
            amount = round(random.uniform(-2000, 2000), 2)  # Amount between -$2000 and $2000

            transactions.append({
                'CustomerID': customer_id,
                'TransactionDate': transaction_date.strftime('%Y-%m-%d'),  # Format date
                'TransactionType': transaction_type,
                'Description': description,
                'Amount': amount
            })

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv('data/transactions.csv', index=False)
print("CSV file 'transactions.csv' created successfully.")