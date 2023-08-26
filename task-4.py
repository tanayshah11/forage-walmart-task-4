import sqlite3
import pandas as pd

# Connect to the SQLite database
conn = sqlite3.connect("your_database.db")
cursor = conn.cursor()

# Load spreadsheet 0 into DataFrame
df0 = pd.read_excel("spreadsheet_0.xlsx")

# Insert data from spreadsheet 0 into the database
df0.to_sql("Table_0", conn, if_exists='replace', index=False)

# Load spreadsheet 1 and 2 into DataFrames
df1 = pd.read_excel("spreadsheet_1.xlsx")
df2 = pd.read_excel("spreadsheet_2.xlsx")

# Merge df1 and df2 based on shipping identifier
merged_df = pd.merge(df1, df2, on="shipping_identifier")

# Determine the quantity of goods in the shipment
grouped_df = merged_df.groupby(["shipping_identifier"]).agg({"quantity": "sum"}).reset_index()

# Inserting into another table
for index, row in grouped_df.iterrows():
    sql_insert_query = """ INSERT INTO Table_1 (shipping_identifier, quantity, origin, destination)
                           VALUES (?, ?, ?, ?);"""
    
    # Prepare the values
    values = (row["shipping_identifier"], row["quantity"], row["origin"], row["destination"])
    
    # Execute the query
    cursor.execute(sql_insert_query, values)

# Commit the changes
conn.commit()

# Close the database connection
conn.close()
