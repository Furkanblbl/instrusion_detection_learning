import os
import sys
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class KMeanAlogriths:
    def __init__(
        self,
        dataset: pd.DataFrame,
        dataset_test: pd.DataFrame,
        attacks: list = None,
        test_size: float = 0.6,
        n_clusters: int = 2,
        path_model_save: str = "../kmeans-model/model.pkl",
        numeric_features: list = ["duration", "src_bytes", "dst_bytes"],
    ):
        self.dataset = dataset
        self.dataset_test = dataset_test
        self.test_size = test_size
        self.numeric_features = numeric_features
        self.n_clusters = n_clusters
        self.path_model_save = path_model_save
        self.attacks = attacks

    def map_dataset(self, dataset: pd.DataFrame, flag: str = "attack_flag"):
        is_attack = dataset.attack.map(lambda a: 0 if a == "normal" else 1)
        dataset[flag] = is_attack
        return dataset

    def map_attack(self, attack):
        try:
            if self.attacks is not None:
                attack_type = 0
                for idx, curr_attacks in enumerate(self.attacks):
                    if attack in curr_attacks:
                        attack_type = idx + 1
                        pass
                return attack_type

        except Exception as e:
            print(f"Error in map_attack:\n{e}")
            sys.exit(0)

    def make_map_attack(self, dataset: pd.DataFrame, col_name: str = "attack_map"):
        attack_map = dataset.attack.apply(self.map_attack)
        dataset[col_name] = attack_map
        return dataset

    def prepare_training(
        self,
        dataset: pd.DataFrame,
        dataset_test: pd.DataFrame,
        flag: str = "attack_flag",
        col_name: str = "attack_map",
    ):
        dataset = self.map_dataset(dataset=dataset, flag=flag)
        dataset_test = self.map_dataset(dataset=dataset_test, flag=flag)

        dataset = self.make_map_attack(dataset=dataset, col_name=col_name)
        dataset_test = self.make_map_attack(dataset=dataset_test, col_name=col_name)

        # Get just numeric features, dataset and test dataset
        return dataset[self.numeric_features], dataset, dataset_test

    @property
    def kmean_training(self):
        to_fit, dataset, dataset_test = self.prepare_training(
            dataset=self.dataset,
            dataset_test=self.dataset_test,
            flag="attack_flag",
            col_name="attack_map",
        )

        binary_y = dataset["attack_flag"]
        multi_y = dataset["attack_map"]

        binary_train_X, binary_val_X, binary_train_y, binary_val_y = train_test_split(
            to_fit, binary_y, test_size=self.test_size
        )
        multi_train_X, multi_val_X, multi_train_y, multi_val_y = train_test_split(
            to_fit, multi_y, test_size=self.test_size
        )

        model = KMeans(n_clusters=self.n_clusters)
        model.fit(multi_train_X, multi_train_y)
        prediction = model.predict(multi_val_X)

        # Save model result
        joblib.dump(model, self.path_model_save)

        print(accuracy_score(prediction, multi_val_y))

        print(accuracy_score(prediction, binary_val_y))