import pandas as pd


class DataQualityLibrary:
    """
    A library of static methods for performing data quality checks on pandas DataFrames.

    This class is intended to be used in a PyTest-based testing framework to validate
    the quality of data in DataFrames. Each method performs a specific data quality
    check and uses assertions to ensure that the data meets the expected conditions.
    """

    @staticmethod
    def check_duplicates(target_data, column_names=None):
        if column_names:
            duplicates = target_data.duplicated(subset=column_names)
        else:
            duplicates = target_data.duplicated()
        assert not duplicates.any(), f"Found duplicates:\n{target_data[duplicates]}"

    @staticmethod
    def check_count(source_data, target_data):
        assert len(source_data) == len(target_data), \
            f"Row count mismatch: source_data={len(source_data)}, target_data={len(target_data)}"

    @staticmethod
    def check_data_completeness(source_data, target_data):
        pd.testing.assert_frame_equal(source_data.reset_index(drop=True),
                                      target_data.reset_index(drop=True))

    @staticmethod
    def check_dataset_is_not_empty(target_data):
        assert not target_data.empty, "Dataset is empty"

    @staticmethod
    def check_not_null_values(target_data, column_names=None):
        if column_names is None:
            column_names = target_data.columns
        for col in column_names:
            assert target_data[col].notnull().all(), f"NULL values found in column '{col}'"
