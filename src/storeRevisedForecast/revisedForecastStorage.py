import datetime as dt
from typing import List,Tuple
from src.storeRevisedForecast.fetchForecast import RevisedForecastedDemandFetchRepo
from src.storeRevisedForecast.storeForecastWithRevisionNo import RevisionInsertion

def storeRevisedForecast(startTime: dt.datetime, endTime: dt.datetime, revisionNo:str, configDict : dict )->bool:

    conString:str = configDict['con_string_mis_warehouse']
    print(revisionNo)

    obj_revisedForecastdDemandFetchRepo = RevisedForecastedDemandFetchRepo(conString)
    obj_revisionInsertion = RevisionInsertion(conString)

    data:List[Tuple] = obj_revisedForecastdDemandFetchRepo.fetchRevisedForecastedDemand(startTime, endTime, revisionNo)
    isRevisionStorageSuccess = obj_revisionInsertion.insertRevisedDemandForecast(data)

    return isRevisionStorageSuccess