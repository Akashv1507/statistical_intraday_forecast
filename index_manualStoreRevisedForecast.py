"""index file for storing revisions
"""
import argparse
import datetime as dt
from src.appConfig import getAppConfigDict
from src.storeRevisedForecast.revisedForecastStorage import storeRevisedForecast

def manualStoreRevisedForecast(startTime: dt.datetime, endTime: dt.datetime):

    x = 11 # x should be in range 1 to 15
    currTime = endTime+dt.timedelta(x)
    configDict=getAppConfigDict()

    startTime = currTime.replace(hour=0, minute=0, second=0, microsecond=0)
    endTime = startTime + dt.timedelta(hours= 1, minutes= 30)

    #checking dt.now() falls in which revision
    revisionNo = 0 
    for i in range(1,17):
        if startTime <= currTime < endTime:
            revisionNo = i
            break
        else:
            startTime = startTime + dt.timedelta(hours= 1, minutes= 30)
            endTime = endTime + dt.timedelta(hours= 1, minutes= 30)

    startTime = currTime.replace(hour=0, minute=0, second=0, microsecond=0)
    endTime = startTime + dt.timedelta(hours= 23, minutes= 59)

    revisionNoStr = "R" + str(revisionNo)

    isRevisionStorageSuccess = storeRevisedForecast(startTime, endTime, revisionNoStr, configDict)
    if isRevisionStorageSuccess:
        print(f'revision number {revisionNoStr} storage successfull')
    else:
        print(f'revision number {revisionNoStr} storage unsuccessfull')


