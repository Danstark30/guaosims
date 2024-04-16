import pandas as pd
import json
"""
This module is usefull to convert arrays in a panda's data frame
"""


def gen_csv(new_columns=[], data=[]):
    """
    This method convert an array in a csv file
    Args:
    - new_columns: name of the columns
    - data: array with data
    return:
            A csv string
    """
    new_df = pd.DataFrame(data, columns=new_columns)
    new_csv = new_df.to_csv()

    return json.dumps(new_csv)
