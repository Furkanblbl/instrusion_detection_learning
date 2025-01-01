import os
import sys
import pandas as pd


class Dataset:
    def __init__(self, path_dataset: str, path_col_names: str):
        self.dataset = self.prepare_dataset(path_dataset, col_name_path=path_col_names)

    @classmethod
    def read_csv_file(self, path: str) -> pd.DataFrame:
        try:
            # If file doesn't csv file exit the program
            if not path.endswith(".txt"):
                print(f"Model file doesn't ends with 'csv': {path}")
                sys.exit(0)

            # Read and return csv file
            return pd.read_csv(path)

        # Catch error
        except Exception as e:
            print(f"Error in __read_csv_file function:\n{e}")
            sys.exit(0)

    @classmethod
    def read_columns_from_file(self, col_file_path: str) -> list:
        try:
            # Must be list before return
            col_names = []

            # Read column names from file
            with open(col_file_path, "r") as f:
                lines = f.readlines()
                for curr_col_name in lines:
                    # Remove whitespaces
                    curr_col_name = curr_col_name.strip()

                    # Appen main list
                    col_names.append(str(curr_col_name))

            # Return, if read any col names. Otherwise return None
            return col_names if len(col_names) > 0 else None

        except Exception as e:
            print(f"Error in __read_columns_from_file function:\n{e}")
            return None

    @classmethod
    def set_col_names(self, dataset: pd.DataFrame, col_names: list) -> pd.DataFrame:
        try:
            # Column names can't be None
            if col_names == None:
                print(f"Column names can't be None")
                sys.exit(0)

            # Set column names
            dataset.columns = col_names

            # Return new dataset
            return dataset

        # If catch any error, exit the program
        except Exception as e:
            print(f"Error in set_col_names function:\n{e}")
            sys.exit(0)

    @classmethod
    def prepare_dataset(self, path_dataset: str, col_name_path: str):
        dataset = self.read_csv_file(path=path_dataset)
        col_names = self.read_columns_from_file(col_file_path=col_name_path)
        dataset_with_col_names = self.set_col_names(
            dataset=dataset, col_names=col_names
        )

        return dataset_with_col_names

    @property
    def get_dataset(self):
        """Getter function for dataset

        Returns:
            pd.DataFrame: Dataset
        """
        return self.dataset