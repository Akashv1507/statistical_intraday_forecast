import argparse
import datetime as dt
from src.appConfig import getAppConfigDict
from src.intraDayRevision.intradayRevisionCreator import doIntradayRevision


configDict=getAppConfigDict()

currTime = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S')
# currTime = "2020-09-22 22:40:56"
parser = argparse.ArgumentParser()
parser.add_argument('--curr_time', help="Enter Start time in yyyy-mm-dd HH:MM:SS format",
                    default = currTime)

args = parser.parse_args()
currTime = dt.datetime.strptime(args.curr_time, '%Y-%m-%d %H:%M:%S')
currTime = currTime.replace(second=0, microsecond=0)

endTime = currTime
while (endTime.minute % 15) != 14:
    endTime = endTime - dt.timedelta(minutes=1)
    
startTime = endTime - dt.timedelta(hours=1 ,minutes=29)
print(startTime,endTime)
print(doIntradayRevision(startTime,endTime,configDict))

