import pandas as pd
import ast


class DataCleaning:
    def __init__(self,file_path:str,output_path:str):
        
        self.file_path = file_path
        self.output_path = output_path
        
    
    def new_car_details_cleaning(self):
        df = pd.read_excel(self.file_path)

        # Specify the columns containing dictionary string
        dict_columns = ['new_car_detail', 'new_car_overview', 'new_car_feature', 'new_car_specs']
        
        # Create an Excel writer to save each dictionary as a separate sheet
        #output_path = r'C:\Users\loges\Desktop\python\sample projects\GUVI\MLapp\data\delhi.xlsx'
        with pd.ExcelWriter(self.output_path) as writer:
            for col in dict_columns:
                # Check if the column exists in the DataFrame
                if col in df.columns:
                    # Convert each cell in the column from a dictionary string to an actual dictionary
                    try:
                        column_data = df[col].dropna().apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {})
                    except ValueError as e:
                        print(f"Error parsing column {col}: {e}")
                        continue  # Skip this column if there's an error

                    # Normalize each dictionary into a DataFrame and combine into a single DataFrame for the sheet
                    table_df = pd.json_normalize(column_data.tolist())

                    # Debug: print the head of the table to confirm data processing
                    print(f"Processed data for column {col}:\n", table_df.head())

                    # Write each table to a separate sheet
                    table_df.to_excel(writer, sheet_name=col, index=False)
                else:
                    print(f"Column '{col}' does not exist in the DataFrame.")

        # Output path to download the file
        print("Data written to:", self.output_path)
    
    
    def clean_and_expand_new_car_overview(self,sheet_name='new_car_overview', data_column='top'):
        """
        This function reads an Excel file, cleans the data, expands dictionary-like data into separate columns,
        and saves the cleaned data back to the same Excel file.

        Parameters:
        - file_path (str): The path to the Excel file.
        - sheet_name (str): The name of the sheet to process. Default is 'new_car_overview'.
        - data_column (str): The column containing dictionary-like data. Default is 'top'.
        """

        # Load the Excel file
        df = pd.read_excel(self.file_path, sheet_name=sheet_name)

        # Function to remove outer brackets from the data
        def remove_outer_brackets(value):
            if isinstance(value, str) and value.startswith('[') and value.endswith(']'):
                return value[1:-1]  # Remove first and last character (outer brackets)
            return value

        # Apply the function to remove outer brackets from the specified column
        df[data_column] = df[data_column].apply(remove_outer_brackets)

        # Function to parse each cell's dictionary-like data and convert it into a dictionary of columns
        def expand_data(cell_value):
            try:
                # Convert the string representation of dictionary list to actual Python list
                data_list = ast.literal_eval(cell_value)
                # Create a dictionary to hold the expanded data for each row
                expanded_row = {}
                # Extract 'key', 'value', and 'icon' for each item and set them in the expanded row
                for item in data_list:
                    key = item.get('key')
                    value = item.get('value')
                    icon = item.get('icon')
                    # Create columns for 'value' and 'icon' associated with each key
                    expanded_row[f'{key}'] = value
                    expanded_row[f'{key} Icon'] = icon
                return expanded_row
            except (ValueError, SyntaxError):
                return {}

        # Apply the function and expand each cell into separate columns
        expanded_data = df[data_column].apply(expand_data).apply(pd.Series)

        # Concatenate the expanded columns with the original DataFrame (excluding the original data column)
        df_cleaned = pd.concat([df.drop(columns=[data_column]), expanded_data], axis=1)

        # Write the cleaned DataFrame back to the same file, replacing the original sheet
        with pd.ExcelWriter(self.output_path , mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
            df_cleaned.to_excel(writer, sheet_name=sheet_name, index=False)

        print("The data has been expanded into columns and saved to the same file, with 'key' as column names and 'value' and 'icon' as data.")
    

    
    def clean_new_car_specs(self):
        """
        Cleans the 'new_car_specs' sheet in the given Excel file.
        - Converts JSON-like strings into structured data.
        - Flattens key-value pairs into separate columns.
        - Saves the cleaned data back to the same file.

        :param file_path: Path to the Excel file.
        """
        # Load the Excel file
        xls = pd.ExcelFile(self.file_path)
        
        # Load the 'new_car_specs' sheet
        df_specs = pd.read_excel(xls, sheet_name='new_car_specs')

        # Function to safely convert stringified lists/dicts to Python objects
        def safe_eval(val):
            try:
                return ast.literal_eval(val) if isinstance(val, str) else val
            except (SyntaxError, ValueError):
                return None

        # Apply transformation to 'top' and 'data' columns
        if 'top' in df_specs.columns:
            df_specs['top'] = df_specs['top'].apply(safe_eval)
        
        if 'data' in df_specs.columns:
            df_specs['data'] = df_specs['data'].apply(safe_eval)

        # Flatten 'top' column into separate columns if it contains data
        if df_specs['top'].notna().any():
            top_df = df_specs['top'].apply(lambda x: {d['key']: d['value'] for d in x} if isinstance(x, list) else {}).apply(pd.Series)
            df_specs = pd.concat([df_specs, top_df], axis=1)

        # Drop unneeded columns
        df_specs.drop(columns=['heading', 'commonIcon', 'top'], inplace=True, errors='ignore')

        # Save cleaned data back to the same file
        with pd.ExcelWriter(self.output_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_specs.to_excel(writer, sheet_name='new_car_specs', index=False)

        print("Data cleaning complete. File updated successfully.")


    def call(self):
        self.new_car_details_cleaning()
        self.clean_and_expand_new_car_overview()
        self.clean_new_car_specs()



def concat_features(file_path):
   
   # Path to your Excel file
    excel_file = file_path

    # Read all sheets into a dictionary of DataFrames
    all_sheets = pd.read_excel(excel_file, sheet_name=None)

    # Combine all sheets horizontally (side by side)
    combined_df = pd.concat(all_sheets.values(), axis=1)

    return combined_df



def concat_ll(dfs:list):
    
    combined_df = pd.DataFrame()

    for file in dfs:
        df = concat_features(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Save the combined DataFrame to a new Excel file
    combined_df.to_excel(r'C:\Users\loges\Documents\GitHub\ML-App\data\features\final_data.xlsx', index=False)