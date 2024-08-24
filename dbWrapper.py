import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

class DBWrapper:
    
    def __init__(self):
        load_dotenv()
        self.cluster = os.getenv('CLUSTER')
        self.pwd = os.getenv('PASSWORD')
        self.server = MongoClient(f'mongodb+srv://{self.cluster}:{self.pwd}@{self.cluster}.wa7nrsi.mongodb.net/?retryWrites=true&w=majority&appName={self.cluster}')
        self.db = self.server.welcome_home
        # self.tz = timezone(timedelta(hours=+8))
        
    def insert_data(self, pred_result, confidence, act_result):
        
        time = datetime.now()
        data = {
            "time": time,
            "pred_result": pred_result,
            "confidence": confidence,
            "act_result": act_result,
            }
	
        doc_id = self.db.face_recog_result.insert_one(data)
        print(doc_id)
