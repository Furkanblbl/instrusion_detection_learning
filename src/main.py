from utils import Utils
from dataset import Dataset


# Defining main function
def main():
    # Init Utils class
    _utils = Utils()
    # Load configuration from json
    config_data = _utils.load_json_file(json_path="config.json")

    # Get dataset path
    path_dataset = _utils.get_data_from_json("paths.dataset", config_data)
    # Get column names path
    path_column_names = _utils.get_data_from_json("paths.columns", config_data)
    # Get kmeans_model save directory path
    path_kmeans_save = _utils.get_data_from_json("paths.kmeans_model", config_data)

    # Read dataset
    read_dataset = Dataset(path_dataset=path_dataset, path_col_names=path_column_names)
    # Get dataset
    dataset = read_dataset.get_dataset


if __name__ == "__main__":
    main()
