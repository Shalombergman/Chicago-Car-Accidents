import csv
from database.connect import  db, injuries,accidents


def read_csv(csv_path):
   with open(csv_path, 'r') as file:
       csv_reader = csv.DictReader(file)
       for row in csv_reader:
           yield row



def init_accident_data():

    db.accidents.drop()
    db.injuries.drop()

    db.accidents.create_index([("beat_of_occurrence", 1)])
    db.accidents.create_index([("crash_date", 1)])


    for row in read_csv('../data/traffic_crashes.csv'):

        injury = {
            "injuries_total": int(row['INJURIES_TOTAL']),
            "injuries_fatal": int(row['INJURIES_FATAL'])
        }

        try:
            injuryId = injuries.insert_one(injury).inserted_id
        except Exception as e:
            print(f"Error inserting injury: {e}")

        accident = {
            "crash_date": row['CRASH_DATE'],
            "beat_of_occurrence": row['BEAT_OF_OCCURRENCE'],
            "injuries_id":injuryId ,
            "prim_contributory_cause": row['PRIM_CONTRIBUTORY_CAUSE']
        }
        try:

            db.accidents.insert_one(accident)
        except Exception as e:
            print(f"Error inserting accident: {e}")


init_accident_data()

