import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
    
    
    #식당정보 데이터 입력받기
    def insert_restaurant(self, name, data, img_path):
        restaurant_info ={ 
            "name": name,
            "category": data['category'],
            "position": data['position'],
            "time": data['time'],
            "recommend_menu": data['recommend_menu'],
            "price": data['price'],
            "reservation": data['reservation'],
            "extra": data['extra'],
            "img_path": "../static/image_upload/"+img_path,
            # "menu":{
            #     "menu_name": data['menu_name'],
            #     "menu_price": data['menu_price'],
            #     "menu_info": data['menu_info'],
            #     #"menu_img_path": "../static/image_upload/"+menu_img_path
            # }
            # "review":{     
            #}
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
            print(data,img_path)
            return True
        else:
            return False
        
    #리뷰 데이터 입력받기
    def insert_review(self, review_name, data, review_img_path):
        review_info ={
            "review_name": review_name,
            "review_star": data['review_star'],
            "review_string": data['review_string'],
            "review_hash": data['review_hash'],
            "review_img_path": "../static/image_upload/"+review_img_path
            
        }
        self.db.child("review").push(review_info)
        print(data,review_img_path)
        return True
        
    #대표메뉴 데이터 입력받기 
    def insert_menu(self, menu_name, data, menu_img_path):
        menu_info ={ 
            "menu_name": menu_name,
            "menu_price": data['menu_price'],
            "menu_info": data['menu_info'],
            "menu_img_path": "../static/image_upload/"+menu_img_path,
            "restaurant_name": data['restaurant_name']
        }

        
        """
         #데이터베이스가 아예 비었을 때
        self.db.child("menu").push(menu_info)
        print(data,menu_img_path)
        return True
        """
        
        if self.menu_duplicate_check(menu_name):
            self.db.child("menu").push(menu_info)
            print(data, menu_img_path)
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
        
    def menu_duplicate_check(self, menu_name): 
        menu = self.db.child("menu").get() 
        for res in menu.each():
            value = res.val()
            if value['menu_name'] == menu_name: 
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
    
    #12주차 강의자료-22page
    def get_avgrate_byname(self,name): 
        reviews = self.db.child("review").get() 
        rates=[]
        for res in reviews.each():
            value = res.val()
            if value['res_name'] == name: 
                     rates.append(float(value['rate']))
            return sum(rates)/len(rates)
        
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
        
    def get_food_byname(self, restaurant_name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            
            #if value['restaurant_name'] == menu_name:
            if value['restaurant_name'] == restaurant_name:
                target_value.append(value)
        return target_value    
        
    def get_review_byname(self,restaurant_name):
        review = self.db.child("review").get().val()
        return review
        