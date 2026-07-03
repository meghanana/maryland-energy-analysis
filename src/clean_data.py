import pandas as pd
import os

def clean_energy_file(file_path, sheet_name, metric_name):
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=2)
    df = df[df['State'] == 'MD'].copy()
    
    if df.empty:
        return None
    
    year_columns = [col for col in df.columns if isinstance(col, (int, float)) and col > 1900]
    
    melted = df.melt(
        id_vars=['State'],
        value_vars=year_columns,
        var_name='Year',
        value_name='Value'
    )
    
    melted['Year'] = melted['Year'].astype(int)
    melted['Metric'] = metric_name
    melted = melted.sort_values('Year').reset_index(drop=True)
    
    return melted

def main():
    os.makedirs('data/processed', exist_ok=True)
    
    all_data = []
    
    print("Processing pr_avg_tot.xlsx...")
    sheets = {
        'Residential sector': 'Avg Price - Residential',
        'Commercial sector': 'Avg Price - Commercial',
        'Industrial sector': 'Avg Price - Industrial',
        'Transportation sector': 'Avg Price - Transportation',
        'Total': 'Avg Price - Total'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/pr_avg_tot.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nProcessing pr_ex_pa_ng.xlsx...")
    sheets = {
        'Petroleum prices': 'Price - Petroleum',
        'Petroleum expenditures': 'Expenditure - Petroleum',
        'Natural gas prices': 'Price - Natural Gas',
        'Natural gas expenditures': 'Expenditure - Natural Gas'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/pr_ex_pa_ng.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nProcessing pr_ex_cl_es.xlsx...")
    sheets = {
        'Coal prices': 'Price - Coal',
        'Coal expenditures': 'Expenditure - Coal',
        'Electricity prices': 'Price - Electricity',
        'Electricity expenditures': 'Expenditure - Electricity'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/pr_ex_cl_es.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nProcessing pr_ex_mg.xlsx...")
    sheets = {
        'Prices': 'Price - Other',
        'Expenditures': 'Expenditure - Other',
        'Expenditures per capita': 'Expenditure Per Capita - Other'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/pr_ex_mg.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nProcessing use_tot_realgdp.xlsx...")
    sheets = {
        'Total consumption': 'Total Consumption',
        'Real GDP': 'Real GDP',
        'Energy consumption per real GDP': 'Energy per GDP'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/use_tot_realgdp.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nProcessing expend_tot.xlsx...")
    sheets = {
        'Residential sector': 'Expenditure - Residential',
        'Commercial sector': 'Expenditure - Commercial',
        'Industrial sector': 'Expenditure - Industrial',
        'Transportation sector': 'Expenditure - Transportation',
        'Total': 'Expenditure - Total'
    }
    for sheet, metric in sheets.items():
        result = clean_energy_file('data/raw/expend_tot.xlsx', sheet, metric)
        if result is not None:
            all_data.append(result)
            print(f"  ✓ {metric}")
    
    print("\nCombining all metrics...")
    combined = pd.concat(all_data, ignore_index=True)
    
    output_path = 'data/processed/maryland_energy_clean.csv'
    combined.to_csv(output_path, index=False)
    
    print(f"\n✅ Success! Cleaned data saved to {output_path}")
    print(f"   Shape: {combined.shape[0]} rows × {combined.shape[1]} columns")
    print(f"\n   Sample of data:")
    print(combined.head(15))
    print(f"\n   Metrics included ({combined['Metric'].nunique()} total):")
    print(combined['Metric'].unique())

if __name__ == '__main__':
    main()