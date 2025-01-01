import sys
import json
import socket
import argparse
import pandas as pd
from pprint import pprint

from utils import Utils
from dataset import Dataset

class SendPacket:
    def __init__(
        self,
        address: str = "127.0.0.1",
        port: str = 8888,
    ):
        self.address = address
        self.port = port

    def send_packet(self, packet):
        """
        Send packet to server.
        """
        try:
            # Create TCP client
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.address, self.port))

            # Convert json format and send to server
            packet_json = json.dumps(packet)
            client_socket.send(packet_json.encode("utf-8"))

        # Catch errors
        except Exception as e:
            print(f"Error in send_packet:\n{e}")
        finally:
            # Finally close the socket
            client_socket.close()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="Argument parser for sending data."
        )

        parser.add_argument(
            "--sending_cols",
            nargs="+",
            type=str,
            required=True,
            help="List of columns to send (e.g., --sending_cols col1 col2 col3).",
        )
        parser.add_argument(
            "--send_count",
            type=int,
            default=10000,
            help="Number of items to send (default: 10000).",
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

    # Initialize client class
    client = SendPacket(
        address=args.address,
        port=args.port,
    )

    # Init Utils class
    _utils = Utils()
    # Load configuration from json
    config_data = _utils.load_json_file(json_path="config.json")

    # Get dataset test path
    path_dataset_test = _utils.get_data_from_json("paths.dataset_test", config_data)
    # Get column names path
    path_column_names = _utils.get_data_from_json("paths.columns", config_data)

    # Read dataset
    read_dataset = Dataset()
    dataset = read_dataset.prepare_dataset(
        path_dataset_test, col_name_path=path_column_names
    )
    print(args.sending_cols)
    for i in range(args.send_count):
        packet = {}
        for col in args.sending_cols:
            packet[str(col)] = int(dataset[col].iloc[i])

        if args.debug == "True":
            print(f"Sending Packet {i}: {packet}")

        # Send packet to sever
        client.send_packet(packet)
