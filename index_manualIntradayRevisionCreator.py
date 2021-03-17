"""index file for intraday revision
"""
import argparse
import datetime as dt
from src.appConfig import getAppConfigDict
from src.intraDayRevisionManual.intradayRevisionCreator import doIntradayRevision

configDict=getAppConfigDict()
count =0
endDate = dt.datetime.now() - dt.timedelta(days=2)
startDate = endDate 

# get start, end dates from command line
parser = argparse.ArgumentParser()
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter end date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))


args = parser.parse_args()
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')

startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0)
endDate = endDate.replace(hour=0, minute=0, second=0, microsecond=0)

startTime = startDate
endTime = endDate + dt.timedelta(hours=22, minutes=30)
while (startTime <= endTime):
    currRevisionStartTime= startTime
    currRevisionEndTime = startTime + dt.timedelta(hours=1, minutes=29)
    print(currRevisionStartTime,currRevisionEndTime)
    startTime= startTime + dt.timedelta(hours=1, minutes=30)
    isRevisionSuccess = doIntradayRevision(currRevisionStartTime, currRevisionEndTime,configDict)
    if isRevisionSuccess:
        count= count+1

noOfDays = (endDate-startDate).days
if count==noOfDays*16:
    print(f" revision successfull between {startTime} and {endTime} ")
else:
    print(f" revision unsuccessfull between {startTime} and {endTime} ")
