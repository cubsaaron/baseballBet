from pygameday import GameDayClient
from dateutil import parser
import datetime

database_uri = "sqlite:///gameday.db"
client = GameDayClient(database_uri, log_level="DEBUG", ingest_spring_training=False)

#client.process_date_range("2018-09-01", "2018-09-08")
client.process_date_range(datetime.datetime(2018,3,1), datetime.datetime(2018,10,10))

