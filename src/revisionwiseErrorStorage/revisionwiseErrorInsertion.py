import cx_Oracle
import datetime as dt
from typing import List, Tuple

class RevisionwiseErrorInsertion():
    """repository to push revision wise  mean abs error, RMSE, MAE, MAPE of entities with revision number to db.
    """

    def __init__(self, con_string: str) -> None:
        """initialize connection string
        Args:
            con_string ([type]): connection string 
        """
        self.connString = con_string

    def insertRevisionwiseError(self, data: List[Tuple]) -> bool:
        """Insert MAE, MAPE, RMSE, RMSE%  of entities with revision number to db
        Args:
            self : object of class 
            data (List[Tuple]): (dateKey, entityTag, revisionNo, mae, mape, rmse, rmse%)
        Returns:
            bool: return true if insertion is successful else false
        """
        
        # making list of tuple of dateKey,entityTag,revision_no based on which deletion takes place before insertion of duplicate

        existingRows = [(x[0],x[1],x[2]) for x in data]

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
                    del_sql = "DELETE FROM revisionwise_error_store WHERE date_key = :1 and entity_tag=:2 and revision_no =:3"
                    cur.executemany(del_sql, existingRows)
                    insert_sql = "INSERT INTO revisionwise_error_store(date_key, ENTITY_TAG, revision_no, mae, mape, rmse, rmse_percentage) VALUES(:1, :2, :3, :4, :5, :6, :7)"
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
            # print("revisionwise mae , mape, rmse, rmse_percentage error with revision no. storage complete")
        return isInsertionSuccess