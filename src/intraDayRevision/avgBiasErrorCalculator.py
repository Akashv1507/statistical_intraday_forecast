import pandas as pd
def calculateAvgBiasError(actualDemandDf:pd.core.frame.DataFrame, forecastedDemandDf:pd.core.frame.DataFrame)->float:
    biasErrorDf=pd.DataFrame() 
    biasErrorDf['biasError'] = (actualDemandDf['demandValue']-forecastedDemandDf['FORECASTED_DEMAND_VALUE'])/actualDemandDf['demandValue']
    avgBiasError = biasErrorDf['biasError'].mean()
    return avgBiasError
    # avgBiasErrorPercent = avgBiasError*100
    # print(biasErrorDf)
    # print(avgBiasError)
    # print(avgBiasErrorPercent)