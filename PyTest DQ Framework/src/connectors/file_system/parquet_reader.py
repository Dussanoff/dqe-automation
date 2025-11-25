import os
import pandas as pd

class ParquetReader:
    def process(self, path, include_subfolders=False):
        dfs = []

        if include_subfolders:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(".parquet"):
                        full_path = os.path.join(root, file)
                        dfs.append(pd.read_parquet(full_path))
        else:
            for file in os.listdir(path):
                full_path = os.path.join(path, file)
                if file.endswith(".parquet") and os.path.isfile(full_path):
                    dfs.append(pd.read_parquet(full_path))

        if not dfs:
            raise ValueError(f"No parquet files found in {path}")

        return pd.concat(dfs, ignore_index=True)
