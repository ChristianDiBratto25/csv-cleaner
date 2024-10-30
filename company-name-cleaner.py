import pandas as pd
import re

def clean_company_name(name):
    """
    Remove common business suffixes and clean up company names.
    
    Args:
        name (str): Company name to clean
        
    Returns:
        str: Cleaned company name
    """
    # List of common business suffixes to remove
    suffixes = [
        r'\bInc\.?$',
        r'\bCo\.?$',
        r'\bCorp\.?$',
        r'\bLLC$',
        r'\bLtd\.?$',
        r'\bLimited$',
        r'\bPLC$',
        r'\bL\.?P\.?$',
        r'\bL\.?L\.?C\.?$',
        r'\bP\.?C\.?$',
        r'\bCompany$',
        r'\bCorporation$',
        r'\bIncorporated$',
    ]
    
    # Convert to string in case we get numerical input
    name = str(name).strip()
    
    # Remove each suffix
    for suffix in suffixes:
        name = re.sub(suffix, '', name, flags=re.IGNORECASE)
    
    # Clean up any remaining punctuation at the end
    name = re.sub(r'[,\.\s]+$', '', name)
    
    # Remove extra whitespace
    name = ' '.join(name.split())
    
    return name

def process_csv(input_file, output_file, company_column='company_name'):
    """
    Process a CSV file containing company names and clean them.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to save cleaned CSV file
        company_column (str): Name of the column containing company names
    """
    try:
        # Read the CSV file
        df = pd.read_csv(input_file)
        
        # Verify the company column exists
        if company_column not in df.columns:
            raise ValueError(f"Column '{company_column}' not found in CSV file")
        
        # Clean company names
        df[f'cleaned_{company_column}'] = df[company_column].apply(clean_company_name)
        
        # Save to new CSV file
        df.to_csv(output_file, index=False)
        print(f"Processed {len(df)} companies and saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Example with sample data
    sample_data = """company_name
Apple Inc.
Microsoft Corporation
Amazon.com, Inc.
Tesla, Inc.
Walmart Inc.
Netflix, Co.
Meta Platforms, Inc.
Alphabet Inc.
Toyota Motor Corporation
Samsung Electronics Co., Ltd."""
    
    # Save sample data to a temporary CSV
    with open('sample_companies.csv', 'w') as f:
        f.write(sample_data)
    
    # Process the sample file
    process_csv('sample_companies.csv', 'cleaned_companies.csv')
