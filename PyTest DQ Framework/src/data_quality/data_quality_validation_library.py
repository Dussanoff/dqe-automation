import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(df, column_names=None):
        if column_names:
            duplicates = df.duplicated(subset=column_names)
        else:
            duplicates = df.duplicated()
        assert not duplicates.any(), f"Found duplicates:\n{df[duplicates]}"

    @staticmethod
    def check_count(df1, df2):
        assert len(df1) == len(df2), f"Row count mismatch: df1={len(df1)}, df2={len(df2)}"

    @staticmethod
    def check_data_completeness(df1, df2):
        pd.testing.assert_frame_equal(df1.reset_index(drop=True), df2.reset_index(drop=True))

    @staticmethod
    def check_dataset_is_not_empty(df):
        assert not df.empty, "Dataset is empty"

    @staticmethod
    def check_not_null_values(df, column_names=None):
        if column_names is None:
            column_names = df.columns
        for col in column_names:
            assert df[col].notnull().all(), f"NULL values found in column '{col}'"
