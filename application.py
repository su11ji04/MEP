from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import DBhandler
import hashlib
import math
import sys
application = Flask(__name__)
application.secret_key = 'secret_key'
DB = DBhandler()


# @application.route("/1") #임시
# def hellotemp():
#     return render_template("index.html")


#index 화면
@application.route("/") 
def list_restaurants2():
    page = request.args.get("page", 0, type=int)
    limit = 12
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    data = DB.get_restaurants() #read the table
    tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx])
    valuelist = list(data.values())
    avgratelist = []
    for i in range(len(data.values())):
        avgratelist.append(DB.get_avgrate_byname(str(valuelist[i].get('name'))))      
    return render_template(
        "index.html",
        datas=data.items(), 
        total=tot_count,
        limit=limit,
        page=page,
        page_count=int((tot_count/10)+1),
        avgratelist=avgratelist
    )


#리뷰 작성 화면
@application.route("/write_review") 
def write_review():
    return render_template("Review_Write.html")


#리뷰 조회 화면
@application.route("/view_review") 
def view_review():
    return render_template("Review_Check.html")


#맛집 등록 화면
@application.route("/write_mep") 
def write_mep():
    return render_template("mep_registration.html")


#메뉴 등록 화면
@application.route("/add_menu") 
def add_menu():
    return render_template("Add_Menu.html")


#메뉴 보기 화면
@application.route("/show_menu") 
def show_menu():
    return render_template("Show_Menu.html")


#회원가입 화면
@application.route("/JoinUs") 
def JoinUs():
    return render_template("JoinUs.html")


#로그인 화면
@application.route("/login") 
def login():
    return render_template("login_index.html")


#카테고리 한식 화면
@application.route("/korea") 
def view_korea():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("한식")

    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("korea_index.html", datas=data, avgratelist=avgratelist)


#카테고리 중식 화면
@application.route("/china") 
def view_china():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("중식")

    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("china_index.html", datas=data, avgratelist=avgratelist)


#카테고리 일식 화면
@application.route("/japan") 
def view_japan():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("일식")

    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("japan_index.html", datas=data, avgratelist=avgratelist)


#카테고리 양식 화면
@application.route("/west") 
def view_west():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("양식")
    
    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("western_index.html", datas=data, avgratelist=avgratelist)
  
    
#카테고리 패스트푸드 화면
@application.route("/fast") 
def view_fast():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("패스트푸드")
    
    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("fastfood_index.html", datas=data, avgratelist=avgratelist)


#카테고리 디저트 화면
@application.route("/dessert") 
def view_desert():
    page = request.args.get("page", 0, type=int)
    data = DB.get_restaurants_bycategory("디저트")
    
    avgratelist = []
    for i in range(len(data)):
        avgratelist.append(DB.get_avgrate_byname(data[i].get('name')))
    print(avgratelist)
    return render_template("dessert_index.html", datas=data, avgratelist=avgratelist)


#회원가입 화면
@application.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data,pw_hash):
        return render_template('login_index.html')
    else:
        flash("해당 ID로는 가입할 수 없습니다!")
        return render_template("JoinUs.html")

    
#로그인 화면
@application.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    print(id_)
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    print(pw_hash)
    if DB.find_user(id_,pw_hash):
        session['id']=id_
        nickname = DB.find_nickname(id_, pw_hash)
        session['nickname']=nickname
        return redirect(url_for('list_restaurants2'))
    else:
        flash("잘못된 ID 또는 PW 입니다!")
        return render_template("login_index.html")  

    
#로그아웃
@application.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('list_restaurants2'))


#12주차 강의자료 18페이지 <동적 라우팅>
@application.route('/dynamicurl/<variable_name>/')
def DynamicUrl(variable_name): 
    return str(variable_name)


#맛집 등록 화면 입력값 보내기
@application.route("/submit_registration", methods=['POST'])
def mep_registration_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return mep_add_menu(data['name'])
    else:
        return "해당 맛집이 이미 존재합니다!"
    

#맛집 세부 화면
@application.route("/mep_page")
def view_mep():
    return render_template("mep_page.html")

            
#맛집 세부 화면 식당 이름별로 동적 라우팅
@application.route("/mep_page/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    return render_template("mep_page.html", data=data , avg_rate=avg_rate)


#대표 메뉴 화면 식당 이름별로 동적 라우팅
@application.route("/show_menu/<name>/")
def view_menu(name):
    data = DB.get_food_byname(str(name))
    print("####data:",data)
    tot_count = len(data)
    return render_template("Show_Menu.html", data=data, total=tot_count, name=name)


#대표 메뉴 화면에서 메뉴 등록 화면으로 넘어가기 동적 라우팅
@application.route("/add_menu/<name>/", methods=['POST'])
def mep_add_menu(name):
    data = DB.get_food_byname(str(name))
    print("####data:",data)
    tot_count = len(data)
    return render_template("Add_Menu.html", data=data, total=tot_count, name=name)


#메뉴 등록 화면 데이터베이스 저장하기
@application.route("/submit_show_menu", methods=['POST'])
def menu_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data2 = request.form
    data = DB.get_food_byname(data2['restaurant_name'])
    tot_count = len(data)
    
    if DB.insert_menu(data2['menu_name'], data2, image_file.filename):
        return view_menu(data2['restaurant_name'])
    else:
        return "해당 메뉴가 이미 존재합니다!"
    
    
#리뷰조회 화면 식당 이름별로 동적 라우팅
@application.route("/review_check/<name>/")
def review_check(name):
    data = DB.get_review_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    tot_count = len(data)
    return render_template("Review_Check.html", data=data, total=tot_count, avg_rate=avg_rate, name=name)


#리뷰조회화면에서 리뷰작성화면으로 넘어가기 동적 라우팅
@application.route("/review_write/<name>/")
def review_write(name):
    data = DB.get_restaurant_byname(str(name))
    #avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    tot_count=len(data)
    return render_template("Review_Write.html", data=data, total=tot_count, name=name)
 
    
#추천루트 게시판 화면
@application.route("/food_course", methods=['POST'])
def foodcourse_submit():       
    image_file=request.files["file"]
    if not image_file:
        data2=DB.get_foodcourse()
        return render_template("foodcourse.html", data=data2)
    else:
        image_file.save("./static/image_upload/"+image_file.filename)
        data = request.form
        if DB.insert_foodcourse(data['res_name1'], data, image_file.filename, data['course_nickname']):
            data2=DB.get_foodcourse()
            return render_template("foodcourse.html", data=data2, image_path="./static/image_upload/"+image_file.filename)
        else:
            return "Restaurant name already exist!" 
        
        
#닉네임 넘겨주기
@application.route("/submit_review", methods=['POST'])
def submit_review():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data = request.form
    tot_count=len(data)    
    
    if DB.insert_review(data['review_name'], data, image_file.filename, data['review_nickname']):
        return review_check(data['review_name'])
    else:
        return "Restaurant name already exist!" 

    
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug= True)