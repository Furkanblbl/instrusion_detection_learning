#!/usr/bin/env python3
import os
import json


class Utils:
    def load_json_file(self, json_path):
        """
        Load JSON file.
        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not a JSON file.
        """
        # Check if the file exists
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Config file not found: {json_path}")

        # Check if the file has a `.json` extension
        if not json_path.endswith(".json"):
            raise ValueError(f"Invalid file type: {json_path}. Expected a JSON file.")

        # Load the JSON content
        try:
            with open(json_path, "r") as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {json_path}. Error: {str(e)}")

    def get_data_from_json(self, key, json_data, default=None):
        """
        Get a value from the configuration. Supports nested keys with dot notation.
        The default parameter is used to return a default value in case a key
        is not present in the configuration file.

        Example: config.get("paths.log_directory")
        """
        keys = key.split(".")
        value = json_data
        try:
            for k in keys:
                value = value[k]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f"Key not found in configuration: {key}")
        return value
