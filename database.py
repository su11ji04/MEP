import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    
    def insert_restaurant(self, name, data, img_path):
        restaurant_info ={ 
            "name": data['name'],
            "category": data['category'],
            #"position": data['position'],
            "time": data['time'],
            "recommend_menu": data['recommend_menu'],
            "price": data['price'],
            "reservation": data['reservation'],
            "extra": data['extra'],
            "img_path": img_path
        }
        
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").child(name).set(restaurant_info)
            print(data,img_path)
            return True
        else:
            return False
        
        
        #self.db.child("restaurant").child(name).set(restaurant_info)
        #print(data,img_path)
        #return True

    def restaurant_duplicate_check(self, name): 
        restaurants = self.db.child("restaurant").get() 
        for res in restaurants.each():
            if res.key() == name: 
                return False
            return True