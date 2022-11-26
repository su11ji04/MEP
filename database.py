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
            "name": name,
            "category": data['category'],
            #"position": data['position'],
            "time": data['time'],
            "recommend_menu": data['recommend_menu'],
            "price": data['price'],
            "reservation": data['reservation'],
            "extra": data['extra'],
            "img_path": "../static/image_upload/"+img_path
        }
        """ 
        #데이터베이스가 아예 비었을 때
        self.db.child("restaurant").push(restaurant_info)
        print(data,img_path)
        return True
        """
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
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
            value = res.val()
            if value['name'] == name: 
                return False
            return True
        
    def get_restaurant_byname(self, name): 
        restaurants = self.db.child("restaurant").get() 
        target_value=""
        for res in restaurants.each():
            value = res.val()
            
            if value['name'] == name: 
                target_value=value
        return target_value
        
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
        
        
        
        
        