import os

from utils import Utils
from dataset import Dataset
from kmeans import KMeanAlogriths

attacks = [
    [
        "apache2",
        "back",
        "land",
        "neptune",
        "mailbomb",
        "pod",
        "processtable",
        "smurf",
        "teardrop",
        "udpstorm",
        "worm",
    ],
    ["ipsweep", "mscan", "nmap", "portsweep", "saint", "satan"],
    ["buffer_overflow", "loadmdoule", "perl", "ps", "rootkit", "sqlattack", "xterm"],
    [
        "ftp_write",
        "guess_passwd",
        "http_tunnel",
        "imap",
        "multihop",
        "named",
        "phf",
        "sendmail",
        "snmpgetattack",
        "snmpguess",
        "spy",
        "warezclient",
        "warezmaster",
        "xclock",
        "xsnoop",
    ],
]


# Defining main function
def main():
    # Init Utils class
    _utils = Utils()
    # Load configuration from json
    config_data = _utils.load_json_file(json_path="config.json")

    # Get dataset path
    path_dataset = _utils.get_data_from_json("paths.dataset", config_data)
    # Get dataset test path
    path_dataset_test = _utils.get_data_from_json("paths.dataset_test", config_data)
    # Get column names path
    path_column_names = _utils.get_data_from_json("paths.columns", config_data)
    # Get kmeans_model save directory path
    path_kmeans_save = _utils.get_data_from_json("paths.kmeans_model", config_data)

    print(f"path_dataset: {path_dataset}")
    print(f"path_column_names: {path_column_names}")
    print(f"path_kmeans_save: {path_kmeans_save}")

    # Read dataset
    read_dataset = Dataset()
    dataset = read_dataset.prepare_dataset(
        path_dataset, col_name_path=path_column_names
    )
    dataset_test = read_dataset.prepare_dataset(
        path_dataset_test, col_name_path=path_column_names
    )

    kmean = KMeanAlogriths(
        dataset=dataset,
        dataset_test=dataset_test,
        attacks=attacks,
        test_size=0.6,
        n_clusters=2,
        path_model_save=os.path.join(path_kmeans_save, "model1.pkl"),
        numeric_features=["duration", "src_bytes", "dst_bytes"],
    )
    # Train kmean model and save
    kmean.kmean_training


if __name__ == "__main__":
    main()
