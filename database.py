import pyrebase
import json

#데이터베이스 연결 스크립트
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
            "tel" : data['tel'],
            "price": data['price'],
            "reservation": data['reservation'],
            "img_path": "../static/image_upload/"+img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
            print(data,img_path)
            return True
        else:
            return False
        
    
    #리뷰 데이터 입력받기 닉네임 추가 버전
    def insert_review(self, review_name, data, review_img_path, review_nickname):
        review_info ={
            "review_name": review_name,
            "review_nickname": review_nickname,
            "review_star": data['review_star'],
            "review_string": data['review_string'],
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
        self.db.child("menu").push(menu_info)
        print(data,menu_img_path)
        return True
        
    #추천루트 데이터 입력받기    
    def insert_foodcourse(self,res_name1, data, course_img_path, course_nickname):
        foodcourse_info={
            "course_nickname": course_nickname,
            "res_name1": res_name1,
            "res_name2": data['res_name2'],
            "res_name3": data['res_name3'],
            "course_explain": data['course_explain'],
            "course_img_path": "../static/image_upload/"+course_img_path
        }

        #  #데이터베이스가 아예 비었을 때
        self.db.child("foodcourse").push(foodcourse_info)
        print(data,course_img_path)
        return True
        
        
    #식당 이름 중복 체크
    def restaurant_duplicate_check(self, name): 
        restaurants = self.db.child("restaurant").get() 
        for res in restaurants.each():
            value = res.val()
            if value['name'] == name: 
                return False
            return True
        
    #메뉴 중복 체크
    def menu_duplicate_check(self, menu_name): 
        menu = self.db.child("menu").get() 
        for res in menu.each():
            value = res.val()
            if value['menu_name'] == menu_name: 
                return False
            return True
        
    #식당 이름으로 데이터 받기    
    def get_restaurant_byname(self, name): 
        restaurants = self.db.child("restaurant").get() 
        target_value=""
        for res in restaurants.each():
            value = res.val()
            
            if value['name'] == name: 
                target_value=value
        return target_value
    
    #식당 이름으로 별점 평균 계산하기
    def get_avgrate_byname(self,name): 
        review = self.db.child("review").get() 
        rates=[]
        for res in review.each():
            value = res.val()
            if value['review_name'] == name:
                rates.append(float(value['review_star']))
        try:
            avg_star = sum(rates)/len(rates)
            return avg_star
        except ZeroDivisionError:
            return 0
    
    #레스토랑 정보 가져오기
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
        
    #식당 이름으로 메뉴 데이터 가져오기    
    def get_food_byname(self, restaurant_name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['restaurant_name'] == restaurant_name or value['restaurant_name'] == " ":
                target_value.append(value)
        return target_value    
        
        
    #식당 이름으로 리뷰 데이터 가져오기  
    def get_review_byname(self,name):
        review = self.db.child("review").get()
        target_value=[]
        for rev in review.each():
            value = rev.val()
            if value['review_name'] == name or value['review_name'] == " ": 
                target_value.append(value)
        return target_value
    
    #쩝쩝박사 코스 데이터 가져오기
    def get_foodcourse(self):
        foodcourse = self.db.child("foodcourse").get()
        target_value=[]
        for course in foodcourse.each():
            value = course.val()
            target_value.append(value)
        return target_value
    
    
    #회원가입 입력
    def insert_user(self, data, pw):
        user_info ={
            "id": data['id'],
            "pw": pw,
            "nickname": data['nickname'],
            "birth": data['birth']
            }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    
    #회원가입 아이디 중복체크
    def user_duplicate_check(self, id_string):
        users = self.db.child("user").get()
        print("users###",users.val())
        if str(users.val()) == "None": # first registration
            return True
        else:
            for res in users.each():
                value = res.val()
                if value['id'] == id_string:
                    return False
            return True

    
    #로그인
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        print(users)
        target_value=[]
        for res in users.each():
            value = res.val()
            if value['id'] == id_ and value['pw'] == pw_:
                return True
        return False
  

    #닉네임 세션을 위한 리턴 함수
    def find_nickname(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=""
        for res in users.each():
            value = res.val()
            if value['id'] == id_: 
                target_value=value['nickname']
        return target_value 

    #카테고리 이름으로 식당 데이터 가져오기
    def get_restaurants_bycategory(self, cate): 
        restaurants = self.db.child("restaurant").get() 
        target_value=[]
        for res in restaurants.each():
            value = res.val()
            if value['category'] == cate: 
                target_value.append(value)
        print("######target_value",target_value)
        return target_value
    