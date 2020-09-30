import datetime as dt
from typing import List, Tuple
from src.blockwiseErrorStorage.actualDemandFetch import ActualDemandFetchRepo
from src.blockwiseErrorStorage.forecastFetch import ForecastedDemandFetchRepo
from src.blockwiseErrorStorage.blockwiseErrorCalculation import calculateMwError
from src.blockwiseErrorStorage.blockwiseMwErrorInsertion import MwErrorInsertion


def createBlockwiseError(startDate: dt.datetime, endDate: dt.datetime, revisionNo: str, configDict: dict) -> bool:
    """create blockwise mw error and blockwise mw error percentage/

    Args:
        startDate (dt.datetime): start date
        endDate (dt.datetime): end date
        revisionNo (str): revision number
        configDict (dict): application configuration

    Returns:
        bool: returns true if storage is successfull, else false
    """    

    con_string = configDict['con_string_mis_warehouse']
    obj_actualDemandFetchRepo = ActualDemandFetchRepo(con_string)
    obj_forecastedDemandFetchRepo = ForecastedDemandFetchRepo(con_string)
    obj_mwErrorInsertion = MwErrorInsertion(con_string)

    currDate = startDate
    insertSuccessCount = 0

    while currDate <= endDate:
        actualDemandDf = obj_actualDemandFetchRepo.fetchActualDemand(currDate, currDate)
        forecastedDemandDf = obj_forecastedDemandFetchRepo.fetchForecastedDemand(currDate, currDate, revisionNo)
        data:List[Tuple] = calculateMwError(actualDemandDf, forecastedDemandDf, revisionNo)
        isInsertionSuccess = obj_mwErrorInsertion.insertMwError(data)

        if isInsertionSuccess:
            insertSuccessCount = insertSuccessCount + 1

        # update currDate
        currDate += dt.timedelta(days=1)

    numOfDays = (endDate-startDate).days
    if insertSuccessCount == numOfDays +1 :
        return True
    else:
        return False