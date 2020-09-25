import datetime as dt
from typing import List, Tuple
from src.fetchers.demandDataFetcher import fetchDemandDataFromApi
from src.intraDayRevision.forecastedDemandFetcher import ForecastedDemandFetchRepo
from src.intraDayRevision.avgBiasErrorCalculator import calculateAvgBiasError
from src.intraDayRevision.forecastedDemandFetchForRevision import ForecastedDemandFetchForRevisionRepo
from src.intraDayRevision.revisedForecastedDemandInsertion import RevisedDemandForecastInsertionRepo

def doIntradayRevision(startTime: dt.datetime, endTime: dt.datetime, configDict : dict):

    conString:str = configDict['con_string_mis_warehouse']
    obj_forecastedDemandFetchRepo = ForecastedDemandFetchRepo(conString)
    obj_forecastedDemandFetchForRevisionRepo = ForecastedDemandFetchForRevisionRepo(conString)
    obj_revisedForecastInsertionRepo = RevisedDemandForecastInsertionRepo(conString)

    isRevisionSuccessCount = 0
    # listOfEntity =['WRLDCMP.SCADA1.A0046945','WRLDCMP.SCADA1.A0046948','WRLDCMP.SCADA1.A0046953','WRLDCMP.SCADA1.A0046957','WRLDCMP.SCADA1.A0046962','WRLDCMP.SCADA1.A0046978','WRLDCMP.SCADA1.A0046980','WRLDCMP.SCADA1.A0047000']
    listOfEntity =['WRLDCMP.SCADA1.A0047000']
    for entity in listOfEntity:
        #fetch last 6 block actual demand
        actualDemandDf = fetchDemandDataFromApi(startTime,endTime,entity,configDict)
        
        #fetch last 6 block forecaste demand
        forecastedDemandDf = obj_forecastedDemandFetchRepo.fetchForecastedDemand(startTime,endTime,entity)
        
        #calculate avg bias error
        avgBiasError = calculateAvgBiasError(actualDemandDf, forecastedDemandDf)
       
        # avgbiasErrorPercentage = avgBiasError*100
        if abs(avgBiasError*100)>1:
            # do revision in next time blocks from B+3
            revisedForecastData :List[Tuple] = obj_forecastedDemandFetchForRevisionRepo.fetchForecastedDemandForRevision(startTime, endTime, entity, avgBiasError)
            # insert revised forecasted demand in db
            isRevisionSuccess = obj_revisedForecastInsertionRepo.insertRevisedDemandForecast(revisedForecastData)
        if isRevisionSuccess:
            isRevisionSuccessCount = isRevisionSuccessCount +1
    
    if isRevisionSuccessCount == 8:
        return True
    else:
        return False


            