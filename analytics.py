import config
from classes import TotalStandings 
import pandas as pd


def get_analytics(submissions, data_type="month"):
    
    dataframe = pd.DataFrame.from_records([s.__dict__ for s in submissions])
    success_counts = dataframe[data_type][dataframe["status"] == "success"].value_counts()
    submissions_counts = dataframe[data_type].value_counts()
    return {"all": submissions_counts.to_json(), "success": success_counts.to_json(), "data_type": data_type}



