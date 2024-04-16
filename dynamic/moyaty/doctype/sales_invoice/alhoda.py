

from sqlalchemy import create_engine

import urllib.parse
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};"
                                 "SERVER=151.106.39.110;"
                                 "DATABASE=NopDB19-1-2022;"
                                 "UID=Dynamic;"
                                 "PWD=DBs@DyNamic434548")


con = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))