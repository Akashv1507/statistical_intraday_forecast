import cx_Oracle
import datetime as dt
from typing import List, Tuple


class RevisedDemandForecastInsertionRepo():
    """repository to push revised forecasted demand of entities to db.
    """

    def __init__(self, con_string: str) -> None:
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string

    def insertRevisedDemandForecast(self, data: List[Tuple]) -> bool:
        """Insert blockwise revisedDemandForecast of entities to db
        Args:
            self : object of class 
            data (List[Tuple]): (timestamp, entityTag, forecastedDemand)
        Returns:
            bool: return true if insertion is successful else false
        """
        
        # making list of tuple of timestamp(unique),entityTag based on which deletion takes place before insertion of duplicate

        existingRows = [(x[0],x[1]) for x in data]

        try:
            
            connection = cx_Oracle.connect(self.connString)
            isInsertionSuccess = True

        except Exception as err:
            print('error while creating a connection', err)
        else:
            try:
                cur = connection.cursor()
                try:
                    cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS' ")
                    del_sql = "DELETE FROM dayahead_demand_forecast WHERE time_stamp = :1 and entity_tag=:2"
                    cur.executemany(del_sql, existingRows)
                    insert_sql = "INSERT INTO dayahead_demand_forecast(time_stamp,ENTITY_TAG,forecasted_demand_value) VALUES(:1, :2, :3)"
                    cur.executemany(insert_sql, data)
                except Exception as e:
                    print("error while insertion/deletion->", e)
                    isInsertionSuccess = False
            except Exception as err:
                print('error while creating a cursor', err)
                isInsertionSuccess = False
            else:
                connection.commit()
        finally:
            cur.close()
            connection.close()
        return isInsertionSuccess