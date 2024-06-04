import pandas as pd
import os

CURRENTPATH = os.path.dirname(os.path.abspath(__file__))


# Load the data from your Excel file
df = pd.read_csv(CURRENTPATH + '\EmbeddingResult.csv')

# Group the data by 'Payload' and calculate the mean for specified columns
grouped_df = df.groupby('Payload').agg({
    'BitSequenceLength': 'size',  # Counts the number of samples per group
    'OriginalBitChange': 'mean',
    'OptimizedBitChange': 'mean',
    'OptimizedNum': 'mean',
    'TimeTaken': 'mean'
}).rename(columns={'BitSequenceLength': 'Number of Samples'})

# Reset index to make 'Payload' a column again if it becomes the index after grouping
grouped_df.reset_index(inplace=True)

# Save the new dataframe to an Excel file
grouped_df.to_excel(CURRENTPATH + '\EmbeddingResultAggregate.xlsx', index=False)

print("Excel file has been created with the summarized data.")
