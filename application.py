from flask import Flask, render_template, request, redirect, url_for
from database import DBhandler
import sys
application = Flask(__name__)
DB = DBhandler()


@application.route("/") #메인 화면
def hello():
    #return render_template("index.html")
    return redirect(url_for('list_restaurants')) #12주차 강의자료-8@application.route("/") #메인 화면

@application.route("/1") #임시
def hellotemp():
    return render_template("index.html")

@application.route("/write_review") #리뷰 작성 화면
def write_review():
    return render_template("Review_Write.html")

@application.route("/view_review") #리뷰 조회 화면
def view_review():
    return render_template("Review_Check.html")

@application.route("/write_mep") #맛집 등록 화면
def write_mep():
    return render_template("mep_registration.html")

@application.route("/add_menu") #메뉴 등록 화면
def add_menu():
    return render_template("Add_Menu.html")

@application.route("/show_menu") #메뉴 보기 화면
def show_menu():
    return render_template("Show_Menu.html")

@application.route("/result") #맛집 등록 입력값 출력 result 화면
def result():
    return render_template("result.html")

@application.route("/JoinUs") #회원가입 화면
def JoinUs():
    return render_template("JoinUs.html")

@application.route("/login") #로그인 화면
def login():
    return render_template("login_index.html")

@application.route("/food_course") #추천루트게시판 화면
def food_course():
    return render_template("foodcourse.html")

@application.route("/korea") #한식 화면
def view_korea():
    return render_template("korea_index.html")

@application.route("/china") #중식 화면
def view_china():
    return render_template("china_index.html")

@application.route("/japan") #일식 화면
def view_japan():
    return render_template("japan_index.html")

@application.route("/west") #양식 화면
def view_west():
    return render_template("western_index.html")

@application.route("/fast") #패스트푸드 화면
def view_fast():
    return render_template("fastfood_index.html")

@application.route("/dessert") #디저트 화면
def view_desert():
    return render_template("dessert_index.html")

@application.route("/mep_page") #맛집 세부 화면
def view_mep():
    return render_template("mep_page.html")

    
#@application.route("/submit_review/<name>/")
#def review_submit():
#   data = DB.get_restaurant_byname(str(name))
#  print('####data:', data)
# return True
    

#result.html 에서 메뉴등록화면으로 보내기
@application.route("/submit_result_html", methods=['POST'])
def result_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/{}".format(image_file.filename))
    data=request.form
    print(data)
    return render_template("Add_Menu.html", data=data)


#맛집 등록 화면 입력값 보내기
@application.route("/submit_registration", methods=['POST'])
def mep_registration_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data['review_name'], data, image_file.filename):
        return render_template("result.html", data=data, image_path="./static/image_upload/"+image_file.filename)
    else:
        return "Restaurant name already exist!"


#회원가입 화면 입력값 보내기
@application.route("/submit_JoinUs", methods=['POST'])
def JoinUs_submit():
    data=request.form
    print(data)
    #return render_template("JoinUs.html", data=data)

#로그인 화면 입력값 보내기
@application.route("/submit_login", methods=['POST'])
def login_submit():
    data=request.form
    print(data)
    #return render_template("login_index.html", data=data)

#추천루트 게시판 입력값 보내기
@application.route("/submit_foodcourse", methods=['POST'])
def reg_foodcourse_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data = request.form
    print(data)
    #return render_template("foodcourse.html", data=data)

    
# #메뉴 등록 화면 입력값 보내기
# @application.route("/submit_menu", methods=['POST'])
# def add_menu_submit():
#     image_file=request.files["file"]
#     image_file.save("./static/image_upload/{}".format(image_file.filename))
#     data=request.form
    
#     if DB.insert_menu(data['menu_name'], data, image_file.filename):
#         return render_template("Show_Menu.html", data=data, menu_image_path="./static/image_upload/"+image_file.filename)
#     else:
#         return "Menu name already exist!"



#12주차 강의자료 10페이지
@application.route("/list") 
def list_restaurants():
    page = request.args.get("page", 0, type=int)
    limit = 9
    
    start_idx = limit*page
    end_idx = limit*(page+1)
    data = DB.get_restaurants() #read the table 
    tot_count = len(data)
    data = dict(list(data.items())[start_idx:end_idx]) 
    # url_for('list_restaurants', page=i)
    
    return render_template(
        "list.html",
        datas=data.items(), 
        total=tot_count,
        limit=limit,
        page=page,
        page_count=int((tot_count/10)+1)
    )


#12주차 강의자료 18페이지
@application.route('/dynamicurl/<variable_name>/')
def DynamicUrl(variable_name): 
    return str(variable_name)

          
#12주차 강의자료 20페이지
@application.route("/mep_page/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    #avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    return render_template("mep_page.html", data=data) #, avg_rate=avg_rate)

#상세화면->리뷰조회화면으로 옮기는
@application.route("/review_check/<name>/")
def review_check(name):
    data = DB.get_restaurant_byname(str(name))
    #avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    return render_template("Review_Check.html", data=data)

#리뷰조회화면 -> 리뷰작성화면 
@application.route("/review_write/<name>/")
def review_write(name):
    data = DB.get_restaurant_byname(str(name))
    #avg_rate = DB.get_avgrate_byname(str(name))
    print("####data:",data)
    return render_template("Review_Write.html", data=data)

#12주차 강의자료 26페이지
#맛집 세부 화면에서 대표메뉴 화면으로 넘어가기
@application.route("/show_menu/<name>/")
def view_menu(name):
    # data = DB.get_restaurant_byname(str(name))
    # print('####data:', data)
    # tot_count = len(data)
    # return render_template("Show_Menu.html", datas=data.items(), total=tot_count)
    data = DB.get_food_byname(str(name))
    tot_count = len(data)
    return render_template("Show_Menu.html", datas=data, total=tot_count)
    

#메뉴 등록 화면 동적라우팅
@application.route("/add_menu/<name>/")
def mep_add_menu(name):
    data = DB.get_restaurant_byname(str(name))
    print("####data:",data)
    return render_template("Add_Menu.html", data=data)

#메뉴 등록 화면 입력값 보내기
@application.route("/submit_show_menu", methods=['POST'])
def menu_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data = request.form
    
    print(data)
    if DB.insert_menu(data['menu_name'], data, image_file.filename):
        #return render_template("Show_Menu.html", data=data, menu_image_path="./static/image_upload/"+image_file.filename)
        return render_template("Show_Menu.html", data=data, menu_image_path="./static/image_upload/"+image_file.filename)
    else:
        return "Menu name already exist!"
    # return render_template("Show_Menu.html", data=data)
    
    
#리뷰 등록 화면 입력값 보내기
@application.route("/submit_review", methods=['POST'])
def submit_review():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data = request.form
    
    if DB.insert_review(data['review_name'], data, image_file.filename):
        return render_template("Review_Check.html", data=data, review_img_path="./static/image_upload/"+image_file.filename)
    else:
        return "Restaurant name already exist!"  

    
if __name__ == "__main__":
    application.run(host='0.0.0.0', debug= True)