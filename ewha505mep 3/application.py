from flask import Flask, render_template, request
import sys
application = Flask(__name__)


@application.route("/") #메인 화면
def hello():
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

@application.route("/result") #맛집 등록 입력값 출력 result 화면
def result():
    return render_template("result.html")




#리뷰 등록 화면 입력값 보내기
@application.route("/submit_review", methods=['POST'])
def reg_review_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/"+image_file.filename)
    data = request.form
    print(data)
    #return render_template("Review_Check.html", data=data)
    
#맛집 등록 화면 입력값 보내기
@application.route("/submit_registration", methods=['POST'])
def mep_registration_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/{}".format(image_file.filename))
    data=request.form
    print(data)
    return render_template("result.html", data=data)

#메뉴 등록 화면 입력값 보내기
@application.route("/submit_menu", methods=['POST'])
def Add_Menu_submit():
    image_file=request.files["file"]
    image_file.save("./static/image_upload/{}".format(image_file.filename))
    data=request.form
    print(data)
    #return render_template("Add_Menu.html", data=data)

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug= True)

    
