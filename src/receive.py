import os
import sys
import socket
import joblib
import argparse
import numpy as np
import pandas as pd
from scipy.stats import zscore

from utils import Utils
from dataset import Dataset


class ReceivePacket:
    def __init__(
        self,
        kmean_model,
        cols: list[str],
        address: str = "127.0.0.1",
        port: str = 8888,
    ):
        self.address = address
        self.cols = cols
        self.port = port
        self.kmeans_model = kmean_model

    def preprocess_packet(self, packet: dict, cols: list[str]):
        """
        Conver packet format by the kmeans models
        """
        # Convert as pandas from dict
        data = pd.get_dummies(pd.DataFrame([packet]))
        # Get just related cols
        numeric_data = data[cols]
        # Return packet data
        return numeric_data

    def detect_anomaly(self, processed_data, indeks):
        """
        Anomali detection with KMeans models
        """
        try:
            prediction = self.kmeans_model.predict(processed_data)
            cluster_centers = self.kmeans_model.cluster_centers_
            distances = np.linalg.norm(cluster_centers - processed_data.values, axis=0)

            if np.min(distances) > 2900 and np.min(distances) <= 3000:
                print(
                    f"Detect Anomali : {indeks}: {np.min(distances)}, "
                    f"{int(processed_data['duration'].iloc[0])}, "
                    f"{int(processed_data['src_bytes'].iloc[0])}, "
                    f"{int(processed_data['dst_bytes'].iloc[0])}"
                )

            else:
                print(
                    f"Normal         : {np.min(distances)}, "
                    f"{int(processed_data['duration'].iloc[0])}, "
                    f"{int(processed_data['src_bytes'].iloc[0])}, "
                    f"{int(processed_data['dst_bytes'].iloc[0])}"
                )
        # Catch errors
        except Exception as e:
            print(f"Error in detect_anomaly:\n{e}")

    def start_server(self):
        """
        Start TCP server
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.address, self.port))
        server_socket.listen(5)

        # For print visualization
        indeks = 0

        # Start loop for listen
        while True:
            client_socket, addr = server_socket.accept()
            try:
                data = client_socket.recv(1024).decode("utf-8")

                # Convert json
                # todo: be careful to eval, it's dangerous. So, we must change it
                packet = eval(data)

                # Procces data
                processed_data = self.preprocess_packet(packet, self.cols)

                # Detect anomali
                is_anomaly = self.detect_anomaly(processed_data, indeks)
                indeks += 1

            except Exception as e:
                print(f"Error in start_server: {e}")
            finally:
                client_socket.close()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Argument parser for sending data."
        )

        parser.add_argument(
            "--address",
            type=str,
            default="127.0.0.1",
            help="Address to send data to (default: 127.0.0.1).",
        )
        parser.add_argument(
            "--port",
            type=int,
            default=8888,
            help="Port to send data to (default: 8888).",
        )
        parser.add_argument(
            "--cols",
            nargs="+",
            type=str,
            required=True,
            help="List of columns to send (e.g., --cols col1 col2 col3).",
        )
        parser.add_argument(
            "--model",
            type=str,
            required=True,
            default="../kmeans-model/kmeans_model.pkl",
            help="Kmean model path (e.g., --model ../kmeans-model/model.pkl).",
        )
        parser.add_argument(
            "--debug",
            type=str,
            default="True",
            help="Debug mode, only True or False. (default: True)",
        )

        # Take all args
        args = parser.parse_args()

    # If catch any error, exit the program
    except Exception as e:
        print(f"Error in parser:\n{e}")
        sys.exit(0)

    if args.model.endswith(".pkl") and os.path.exists(args.model):
        # Load kmeans model from path
        kmeans_model = joblib.load(args.model)
        # Initialize client class
        server = ReceivePacket(
            kmean_model=kmeans_model,
            cols=args.cols,
            address=args.address,
            port=args.port,
        )

        server.start_server()
    else:
        print(f"Check model file path. It is not exist or unsupported file format")