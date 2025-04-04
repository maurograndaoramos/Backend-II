import os
import time
import numpy as np
import pandas as pd
import multiprocessing
from functools import partial

def process_chunk(chunk,operations:list):
    result = chunk.copy()

    for operation in operations:
        numeric_cols = result.select_dtypes(include=[np.number]).columns
        if operation == "normalize":
            for col in numeric_cols:
                min_val = result[col].min()
                max_val = result[col].max()
                if max_val > min_val:
                    result[col] = (result[col]-min_val) / (max_val-min_val)
        elif operation == "fill_missing":
            for col in numeric_cols:
                result[col] = result[col].fillna(result[col].mean())
            cat_cols = result.select_dtypes(include=['object','category']).columns
            for col in cat_cols:
                result[col] = result[col].fillna(result[col].mode()[0] if not result[col].mode().empty() else "NA")
        elif operation == "add_features":
            for col in numeric_cols:
                result[f"{col}_squared"] = result[col] ** 2
                result[f"{col}_cubed"] = result[col] ** 3
        elif operation == "encode_categorical":
            cat_cols = result.select_dtypes(include=['object','category']).columns
            for col in cat_cols:
                if result[col].nunique() < 10:
                    dummies = pd.get_dummies(result[col],prefix=col)
                    result = pd.concat([result,dummies],axis=1)
                    result = result.drop(col,axis=1)
    time.sleep(0.1)
    return result


class DataProcessor:
    def __init__(self, num_processes):
        self.num_processes = num_processes or multiprocessing.cpu_count()
    
    def process_dataframe(self, df:pd.DataFrame, operations=None, chunks=None):
        operations = operations or ["normalize","fill_missing"]
        chunks = chunks or self.num_processes

        start = time.perf_counter()

        df_split = np.array_split(df,chunks)

        process_func = partial(process_chunk,operations=operations)

        with multiprocessing.Pool(processes=self.num_processes) as pool:
            results = pool.map(process_func,df_split)
        
        result_df = pd.concat(results)

        elapsed_time = time.perf_counter() - start

        return result_df
    
    def process_file(self, input_file, output_file, operations=None, chunks=None):
        df = pd.read_csv(input_file)

        result = self.process_dataframe(df, operations=operations,chunks=chunks)

        result.to_csv(output_file, index=False)

if __name__ == "__main__":

    sample_size = 10_000_000
    sample_data = pd.DataFrame({
        'numeric1': np.random.normal(0,1,sample_size),
        'numeric2': np.random.uniform(-100,100,sample_size),
        'category1':np.random.choice(["A","B","C",None],sample_size),
        'category2':np.random.choice(["Z","Y","Z","W"],sample_size)

    })
    sample_data.loc[np.random.choice(sample_size,1_000), 'numeric1'] = np.nan

    sample_data.to_csv("original.csv")

    processor = DataProcessor(num_processes=32)
    result_df = processor.process_dataframe(
        sample_data,
        operations=["normalize","add_features"]
    )
    
    result_df.to_csv("processed.csv")

    print(f"original shape: {sample_data.shape}")
    print(f"original shape: {result_df.shape}")