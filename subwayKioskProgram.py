import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
import copy
import pickle
import pandas as pd
import csv
import re

menu_list = [['에그마요', 4300], ['BMT', 5200], ['BLT', 5200], ['미트볼', 5200], ['햄', 4700], ['참치', 4800], ['K-BBQ', 6000],
             ['풀드포크', 5900]]
bread_list = ['화이트', '위트', '허니오트', '하티', '파마산 오레가노', '플랫브레드']
cheese_list = ['아메리칸치즈', '모짜렐라치즈', '슈레드치즈']
veg_list = ['양상추', '토마토', '오이', '피망', '양파', '피클', '올리브', '할라피뇨']
veg_amt = ['없음', '적음', '보통', '많음']
sauce_list = ['X', '랜치', '마요네즈', '스위트어니언', '허니머스타트', '스위트칠리', '바베큐', '핫칠리', '사우스웨스트', '머스타드', '홀스래디쉬', '올리브오일',
              '레드와인식초', '소금', '후추']
add_list = [['X', 0], ['더블업', 1800], ['베이컨비츠', 900], ['에그마요', 1600], ['오믈렛', 1200], ['베이컨', 900],
            ['페퍼로니', 900]]

set_list = ['X', 'O']  ##세트여부
veg_amt_gram = [0, 10, 30, 50]  #야채량 [없음, 적음, 보통, 많음]
sauce_gram = 30                 #샌드위치 하나당 소스양
#샌드위치 재료들의 재고량
bread_stock = [1000, 1000, 1000, 1000, 1000, 1000]  #['화이트', '위트', '허니오트', '하티', '파마산 오레가노', '플랫브레드']
cheese_stock = [1000, 1000, 1000]                   #['아메리칸치즈', '모짜렐라치즈', '슈레드치즈']
veg_stock = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]  #[양상추', '토마토', '오이', '피망', '양파', '피클', '올리브', '할라피뇨']
sauce_stock = [0, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000,1000]  #['X','랜치', '마요네즈', '스위트어니언', '허니머스타트', '스위트칠리', '바베큐', '핫칠리', '사우스웨스트', '머스타드', '홀스래디쉬', '올리브오일', '레드와인식초', '소금', '후추']

subway_green = "#008C15"
subway_yellow = "#FFC600"

TabStyleSheet = '''
QTabWidget {
    background-color: white;
    padding: 10px;
    margin:  10px;
}
QTabWidget::pane {
    border: 3px solid #008C15;
}
QTabBar {
    color: black;
    background-color:#FFC600
}
QTabBar::tab:top:selected {
    color: white;
    background-color:#008C15
}
'''

class InitialMenu(QWidget):  #가장 초기화면
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.subwayLbl = QLabel('SUBWAY')#서브웨이 로고 출력
        self.subwayLbl.sizeHint()
        self.subwayLbl.setPixmap(QtGui.QPixmap("./logo.png"))
        self.subwayLbl.setAlignment(Qt.AlignCenter)

        order_btn = QPushButton()
        order_btn.setStyleSheet("background-image : url(customer_order.png);"
                                "border : 0;")
        order_btn.setFixedSize(300,100)
        order_btn.clicked.connect(self.order)#주문버튼 출력

        oq_btn = QPushButton()
        oq_btn.setStyleSheet("background-image : url(order_manage.png);"
                             "border : 0;")
        oq_btn.setFixedSize(300, 100)
        oq_btn.clicked.connect(self.ordermanage_show)#주문확인 버튼 출력

        sm_btn = QPushButton()
        sm_btn.setStyleSheet("background-image : url(sales_manage.png);"
                             "border : 0;")
        sm_btn.setFixedSize(300, 100)
        sm_btn.clicked.connect(self.sale)#매출관리 버튼 출력

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(order_btn, QtCore.Qt.AlignHCenter)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(oq_btn, QtCore.Qt.AlignHCenter)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(sm_btn, QtCore.Qt.AlignHCenter)
        hbox3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.subwayLbl,QtCore.Qt.AlignCenter)
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def order(self):#메뉴 주문 창으로 이동
        ex.stk_w.setCurrentWidget(order_main)

    def sale(self):#매출 관리용 로그인 및 해당 창으로 이동
        self.limit = 0
        for i in range(5):
            self.limit += 1

            text, ok = QInputDialog.getText(self, '매출관리', '비밀번호를 입력해주세요.%d/5' % self.limit)

            if ok:
                self.load_pw()
                if str(text) in pw_dic:
                    QMessageBox.information(self, '로그인 성공', '로그인 되었습니다',
                                            QMessageBox.Yes, QMessageBox.Yes)

                    sale_management = MenuSaleWindow()
                    ex.stk_w.addWidget(sale_management)
                    ex.stk_w.setCurrentWidget(sale_management)
                    break

                elif self.limit < 5:
                    QMessageBox.information(self, '로그인 실패', '다시 입력해주세요.',
                                            QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, '로그인 실패', '입력횟수를 초과하였습니다.',
                                            QMessageBox.Yes, QMessageBox.Yes)
            else:
                break

    def load_pw(self):
        global pw_dic
        pw_dic = ['pw']

    def ordermanage_show(self):#주문관리창 로그인 및 실행 함수
        self.limit = 0
        for i in range(5):
            self.limit += 1

            text, ok = QInputDialog.getText(self, '주문관리', '비밀번호를 입력해주세요.%d/5' % self.limit)

            if ok:
                self.load_pw()
                if str(text) in pw_dic:
                    QMessageBox.information(self, '로그인 성공', '로그인 되었습니다',
                                            QMessageBox.Yes, QMessageBox.Yes)
                    order_manage.updateTable()
                    order_manage.setGeometry(100, 100, 1500, 800)
                    order_manage.setWindowTitle("주문관리")
                    order_manage.show()
                    break
                elif self.limit < 5:
                    QMessageBox.information(self, '로그인 실패', '다시 입력해주세요.',
                                            QMessageBox.Yes, QMessageBox.Yes)
                else:
                    QMessageBox.information(self, '로그인 실패', '입력횟수를 초과하였습니다.',
                                            QMessageBox.Yes, QMessageBox.Yes)
            else:
                break

class OrderMain(QWidget):#메뉴주문클래스
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        global login_id, custom_list

        self.subwayLbl = QLabel('SUBWAY')
        self.subwayLbl.resize(650, 174)
        self.subwayLbl.setPixmap(QtGui.QPixmap("./logo.png"))
        self.subwayLbl.setAlignment(Qt.AlignCenter)

        menu_btn = QPushButton()
        menu_btn.setStyleSheet("background-image : url(order.png);"
                                "border : 0;")
        menu_btn.setFixedSize(300, 100)
        menu_btn.clicked.connect(self.choose_menu)#메뉴 주문 버튼

        login_btn = QPushButton()
        login_btn.setStyleSheet("background-image : url(Login.png);"
                               "border : 0;")
        login_btn.setFixedSize(300, 100)
        login_btn.clicked.connect(self.login)#회원 로그인 버튼

        home = QPushButton()
        home.setStyleSheet("background-image: url(home.png);"
                           "border : 0;")
        home.setFixedSize(80,80)
        home.clicked.connect(self.back_home)#홈 버튼

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(menu_btn, QtCore.Qt.AlignHCenter)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(login_btn, QtCore.Qt.AlignHCenter)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(home, QtCore.Qt.AlignHCenter)
        hbox3.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.subwayLbl, QtCore.Qt.AlignCenter)
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def back_home(self):
        global current_order
        if (len(current_order) >= 1) or OrderMain.is_login(self):
            reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제되고 로그아웃됩니다. 계속하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                current_order = []
                OrderMain._logout(self)
                ex.stk_w.setCurrentWidget(initialize)
            else:
                OrderMain.cancel(self)
        else:
            ex.stk_w.setCurrentWidget(initialize)


    #아이디 입력창
    def login(self):
        global login_id, custom_list
        #로그인 상태인 경우 로그아웃 묻기
        if self.is_login():
            reply = QMessageBox.information(self, '로그아웃', '이미 로그인 상태입니다 로그아웃 하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.logout()
            else:
                self.cancel()

        #로그인 상태가 아닌경우
        else:
            text, ok = QInputDialog.getText(self, '아이디 입력창', '아이디를 입력해주세요')

            if ok:
                self.load_id()
                if str(text) in id_dic:
                    sucmsg = QMessageBox.information(self, '로그인 성공', '로그인 되었습니다',
                                                     QMessageBox.Yes, QMessageBox.Yes)
                    login_id = str(text)
                    custom_list = id_dic[login_id]  #개인메뉴 불러오기
                else:
                    falmsg = QMessageBox.information(self, '로그인 실패', '존재하지 않는 아이디입니다',
                                                     QMessageBox.Yes, QMessageBox.Yes)

    def logout(self):
        global login_id, custom_list
        if len(current_order) == 0:
            sucmsg = QMessageBox.information(self, '로그아웃 성공', '로그아웃 되었습니다', QMessageBox.Yes, QMessageBox.Yes)
        custom_list = []
        login_id = ''

    def cancel(self):
        pass

    def load_id(self):
        global id_dic
        file = open("id_DB", "rb")
        id_dic = pickle.load(file)

    #데이터베이스에 id 저장
    def store_id(self):
        global id_dic
        file = open("id_DB", "wb")
        pickle.dump(id_dic, file)
        file.close()

    #로그인 상태 판별
    def is_login(self):
        global login_id, custom_list
        if len(login_id) == 0:
            return False
        if len(login_id) > 0:
            return True

    #로그아웃
    def _logout(self):
        global custom_list, login_id
        custom_list = []
        login_id = ''

    def choose_menu(self):
        select_menu_refresh = ChooseMenu()
        ex.stk_w.addWidget(select_menu_refresh)
        ex.stk_w.setCurrentWidget(select_menu_refresh)


class ChooseMenu(QWidget):#메뉴선택 클래스
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.temp_order = []
        self.index = 0
        self.initUI()

    def initUI(self):
        global login_id, custom_list
        self.setStyleSheet("background-color : white;")
        self.tab1 = QWidget()  #프리셋
        self.tab2 = QWidget()  #직접선택
        self.tab3 = QWidget()  #개인메뉴

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab1, '프리셋 메뉴')
        self.tabs.addTab(self.tab2, '직접 선택')
        if OrderMain.is_login(self):
            self.tabs.addTab(self.tab3, '개인 메뉴')

        vbox = QVBoxLayout()
        grid = QGridLayout()

        self.home = QPushButton()
        self.home.setStyleSheet("background-image: url(home.png);"
                                "border : 0 ")
        self.home.setFixedSize(80,80)
        self.home.clicked.connect(self.back_home)

        self.subwayLbl2 = QLabel()
        self.subwayLbl2.setPixmap(QtGui.QPixmap("./subway.png"))
        self.sizeHint()
        grid.addWidget(self.home,0,0,1,2)
        grid.addWidget(self.subwayLbl2,0,1,2,5)

        vbox.addLayout(grid)

        #프리셋 메뉴 레이아웃
        self.tab1.layout = QVBoxLayout(self)

        self.btnlayout = QVBoxLayout()

        # 일반버튼
        self.btn1 = QPushButton("이전", self)
        self.btn1.setStyleSheet("background-color : #D0CECE;")
        self.btn1.clicked.connect(self.back)

        self.btn2 = QPushButton("다음", self)
        self.btn2.setStyleSheet("background-color : #D0CECE;")
        self.btn2.clicked.connect(self.next)

        # 레이아웃 설정
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn1)
        hbox.addStretch(1)
        hbox.addWidget(self.btn2)

        # 스크롤박스
        self.tab1.layout.addWidget(self.createLayout_Pre_Container())
        self.tab1.layout.addWidget(self.basket())
        self.tab1.layout.addLayout(hbox)
        self.tab1.setLayout(self.tab1.layout)

        #직접선택 레이아웃
        self.tab2.layout = QVBoxLayout(self)

        self.btn3 = QPushButton("이전", self)
        self.btn3.setStyleSheet("background-color : #D0CECE;")
        self.btn3.clicked.connect(self.back)

        self.btn4 = QPushButton("다음", self)
        self.btn4.setStyleSheet("background-color : #D0CECE;")
        self.btn4.clicked.connect(self.next)

        # 레이아웃 설정
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.btn3)
        hbox2.addStretch(1)
        hbox2.addWidget(self.btn4)

        self.tab2.layout.addWidget(self.createLayout_S_container())
        self.tab2.layout.addWidget(self.basket())

        P_hbox = QHBoxLayout()

        self.tab2.layout.addLayout(P_hbox)
        self.tab2.layout.addLayout(hbox2)
        self.tab2.setLayout(self.tab2.layout)

        #개인메뉴 레이아웃
        self.tab3.layout = QVBoxLayout(self)

        self.btn8 = QPushButton('개인메뉴에서 삭제', self)
        self.btn8.setStyleSheet("background-color : " + subway_yellow + ";")
        self.btn8.clicked.connect(self.delete_custom)

        # 일반버튼
        self.btn9 = QPushButton("이전", self)
        self.btn9.setStyleSheet("background-color : #D0CECE;")
        self.btn9.clicked.connect(self.back)

        self.btn10 = QPushButton("다음", self)
        self.btn10.setStyleSheet("background-color : #D0CECE;")
        self.btn10.clicked.connect(self.next)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.btn9)
        hbox3.addStretch(1)
        hbox3.addWidget(self.btn10)

        # 개인메뉴 출력 스크롤박스
        self.C_checkboxes = []  # 개인메뉴삭제용
        self.sltbtns = []  # 개인메뉴 주문하기용
        self.tab3.layout.addWidget(self.createLayout_C_container())
        self.tab3.layout.addWidget(self.basket())

        for i, sltbtn in enumerate(self.sltbtns):
            self.sltbtns[i].clicked.connect(self.select_custom)

        self.tab3.layout.addWidget(self.btn8)
        self.tab3.layout.addLayout(hbox3)
        self.tab3.setLayout(self.tab3.layout)
        self.layout.addLayout(vbox)
        self.layout.addWidget(self.tabs)
        self.setLayout(vbox)
        self.tabs.setStyleSheet(TabStyleSheet)


    def basket(self):#장바구니 생성 함수
        groupbox = QGroupBox('장바구니')
        groupbox.setFixedHeight(100)
        grid = QGridLayout()

        for i in range(len(current_order)):
            line = i // 8
            txt = menu_list[current_order[i][0]][0]
            menuTxt = QLabel(txt, self)
            grid.addWidget(menuTxt, line, i % 8)

        groupbox.setLayout(grid)

        return groupbox

    def refresh_choose_menu(self):#창 새로고침 함수
        select_menu_refresh = ChooseMenu()
        ex.stk_w.addWidget(select_menu_refresh)
        ex.stk_w.setCurrentWidget(select_menu_refresh)
        select_menu_refresh.tabs.setCurrentIndex(self.index)

    def Add_ing(self):#선택된 재료 식별 함수
        li = []
        #라디오버튼 식별
        if self.b0.isChecked():
            self.temp_order.append(0)
        elif self.b1.isChecked():
            self.temp_order.append(1)
        elif self.b2.isChecked():
            self.temp_order.append(2)
        elif self.b3.isChecked():
            self.temp_order.append(3)
        elif self.b4.isChecked():
            self.temp_order.append(4)
        elif self.b5.isChecked():
            self.temp_order.append(5)
        if self.c0.isChecked():
            self.temp_order.append(0)
        elif self.c1.isChecked():
            self.temp_order.append(1)
        elif self.c2.isChecked():
            self.temp_order.append(2)
        if self.le_0.isChecked():
            self.temp_order.append(0)
        elif self.le_1.isChecked():
            self.temp_order.append(1)
        elif self.le_2.isChecked():
            self.temp_order.append(2)
        elif self.le_3.isChecked():
            self.temp_order.append(3)
        if self.to_0.isChecked():
            self.temp_order.append(0)
        elif self.to_1.isChecked():
            self.temp_order.append(1)
        elif self.to_2.isChecked():
            self.temp_order.append(2)
        elif self.to_3.isChecked():
            self.temp_order.append(3)
        if self.cu_0.isChecked():
            self.temp_order.append(0)
        elif self.cu_1.isChecked():
            self.temp_order.append(1)
        elif self.cu_2.isChecked():
            self.temp_order.append(2)
        elif self.cu_3.isChecked():
            self.temp_order.append(3)
        if self.pe_0.isChecked():
            self.temp_order.append(0)
        elif self.pe_1.isChecked():
            self.temp_order.append(1)
        elif self.pe_2.isChecked():
            self.temp_order.append(2)
        elif self.pe_3.isChecked():
            self.temp_order.append(3)
        if self.on_0.isChecked():
            self.temp_order.append(0)
        elif self.on_1.isChecked():
            self.temp_order.append(1)
        elif self.on_2.isChecked():
            self.temp_order.append(2)
        elif self.on_3.isChecked():
            self.temp_order.append(3)
        if self.pi_0.isChecked():
            self.temp_order.append(0)
        elif self.pi_1.isChecked():
            self.temp_order.append(1)
        elif self.pi_2.isChecked():
            self.temp_order.append(2)
        elif self.pi_3.isChecked():
            self.temp_order.append(3)
        if self.ol_0.isChecked():
            self.temp_order.append(0)
        elif self.ol_1.isChecked():
            self.temp_order.append(1)
        elif self.ol_2.isChecked():
            self.temp_order.append(2)
        elif self.ol_3.isChecked():
            self.temp_order.append(3)
        if self.ja_0.isChecked():
            self.temp_order.append(0)
        elif self.ja_1.isChecked():
            self.temp_order.append(1)
        elif self.ja_2.isChecked():
            self.temp_order.append(2)
        elif self.ja_3.isChecked():
            self.temp_order.append(3)
        #체크박스 식별
        if self.s1.isChecked():
            li.append(1)
        if self.s2.isChecked():
            li.append(2)
        if self.s3.isChecked():
            li.append(3)
        if self.s4.isChecked():
            li.append(4)
        if self.s5.isChecked():
            li.append(5)
        if self.s6.isChecked():
            li.append(6)
        if self.s7.isChecked():
            li.append(7)
        if self.s8.isChecked():
            li.append(8)
        if self.s9.isChecked():
            li.append(9)
        if self.s10.isChecked():
            li.append(10)
        if self.s11.isChecked():
            li.append(11)
        if self.s12.isChecked():
            li.append(12)
        if self.s13.isChecked():
            li.append(13)
        if self.s14.isChecked():
            li.append(14)
        if len(li) == 0:
            li.append(0)
        self.temp_order.append(li)

        li = []
        #추가메뉴 체크박스 식별
        if self.a1.isChecked():
            li.append(1)
        if self.a2.isChecked():
            li.append(2)
        if self.a3.isChecked():
            li.append(3)
        if self.a4.isChecked():
            li.append(4)
        if self.a5.isChecked():
            li.append(5)
        if len(li) == 0:
            li.append(0)
        self.temp_order.append(li)
        #세트여부 판단(주문확인에서 메뉴 수정시)
        if self.mode == 1:
            if self.set_1.isChecked():
                self.temp_order.append(0)
            elif self.set_2.isChecked():
                self.temp_order.append(1)
            self.dialog.close()
        else:
            self.dialog.close()
            self.Ask_set()

    def is_login(self):
        global login_id, custom_list
        if len(login_id) == 0:
            return False
        if len(login_id) > 0:
            return True

    def Selecting(self, n, mode=0):#재료 직접 선택창 실행 및 구성 함수
        self.temp_order = []
        self.temp_order.append(n)
        self.mode = mode
        self.index = 1

        self.dialog = QDialog()
        self.dialog.setWindowTitle('재료선택')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(400, 600)
        self.dialog.setStyleSheet("background-color: white;")
        self.ok_btn = QPushButton('완료')
        self.ok_btn.setStyleSheet("background-color : "+ subway_yellow+";")

        grid = QGridLayout()
        grid.addWidget(self.B_Group(), 0, 0)
        grid.addWidget(self.C_Group(), 0, 1)
        grid.addWidget(self.Lettuce(), 2, 0)
        grid.addWidget(self.Tomato(), 2, 1)
        grid.addWidget(self.Cucumber(), 3, 0)
        grid.addWidget(self.Pepper(), 3, 1)
        grid.addWidget(self.Onion(), 4, 0)
        grid.addWidget(self.Pickled(), 4, 1)
        grid.addWidget(self.Olive(), 5, 0)
        grid.addWidget(self.Jalapeno(), 5, 1)
        grid.addWidget(self.S_Group(), 6, 0)
        grid.addWidget(self.A_Group(), 6, 1)

        if self.mode == 1:
            grid.addWidget(self.Set_Group(), 7, 0)

        grid.addWidget(self.ok_btn, 7, 1)
        self.ok_btn.clicked.connect(self.Add_ing)
        self.dialog.setLayout(grid)
        self.dialog.show()

    def B_Group(self):#빵 선택 그룹박스 생성 함수
        groupbox = QGroupBox('빵 선택')

        self.b0 = QRadioButton('화이트')
        self.b1 = QRadioButton('위트')
        self.b2 = QRadioButton('허니오트')
        self.b3 = QRadioButton('하티')
        self.b4 = QRadioButton('파마산오레가노')
        self.b5 = QRadioButton('플랫브레드')
        self.b_group = [self.b0, self.b1, self.b2, self.b3, self.b4, self.b5]
        self.b0.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.b0)
        vbox.addWidget(self.b1)
        vbox.addWidget(self.b2)
        vbox.addWidget(self.b3)
        vbox.addWidget(self.b4)
        vbox.addWidget(self.b5)
        groupbox.setLayout(vbox)

        return groupbox

    def C_Group(self):#치즈 선택 그룹박스 생성 함수
        groupbox = QGroupBox('치즈 선택')

        self.c0 = QRadioButton('아메리칸 치즈')
        self.c1 = QRadioButton('모짜렐라 치즈')
        self.c2 = QRadioButton('슈레드 치즈')
        self.c_group = [self.c0, self.c1, self.c2]
        self.c0.setChecked(True)

        vbox = QVBoxLayout()
        vbox.addWidget(self.c0)
        vbox.addWidget(self.c1)
        vbox.addWidget(self.c2)

        groupbox.setLayout(vbox)

        return groupbox

    def Lettuce(self):#양상추 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.le_0 = QRadioButton('없음')
        self.le_1 = QRadioButton('조금')
        self.le_2 = QRadioButton('보통')
        self.le_3 = QRadioButton('많이')
        self.le_group = [self.le_0, self.le_1, self.le_2, self.le_3]
        self.le_0.setChecked(True)

        grid = QGridLayout()

        grid.addWidget(QLabel('양상추'), 0, 0)
        grid.addWidget(self.le_0, 0, 1)
        grid.addWidget(self.le_1, 0, 2)
        grid.addWidget(self.le_2, 0, 3)
        grid.addWidget(self.le_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Tomato(self):#토마토 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.to_0 = QRadioButton('없음')
        self.to_1 = QRadioButton('조금')
        self.to_2 = QRadioButton('보통')
        self.to_3 = QRadioButton('많이')
        self.to_group = [self.to_0, self.to_1, self.to_2, self.to_3]
        self.to_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('토마토'), 0, 0)
        grid.addWidget(self.to_0, 0, 1)
        grid.addWidget(self.to_1, 0, 2)
        grid.addWidget(self.to_2, 0, 3)
        grid.addWidget(self.to_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Cucumber(self):#오이 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.cu_0 = QRadioButton('없음')
        self.cu_1 = QRadioButton('조금')
        self.cu_2 = QRadioButton('보통')
        self.cu_3 = QRadioButton('많이')
        self.cu_group = [self.cu_0, self.cu_1, self.cu_2, self.cu_3]
        self.cu_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('오이'), 0, 0)
        grid.addWidget(self.cu_0, 0, 1)
        grid.addWidget(self.cu_1, 0, 2)
        grid.addWidget(self.cu_2, 0, 3)
        grid.addWidget(self.cu_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Pepper(self):#피망 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.pe_0 = QRadioButton('없음')
        self.pe_1 = QRadioButton('조금')
        self.pe_2 = QRadioButton('보통')
        self.pe_3 = QRadioButton('많이')
        self.pe_group = [self.pe_0, self.pe_1, self.pe_2, self.pe_3]
        self.pe_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('피망'), 0, 0)
        grid.addWidget(self.pe_0, 0, 1)
        grid.addWidget(self.pe_1, 0, 2)
        grid.addWidget(self.pe_2, 0, 3)
        grid.addWidget(self.pe_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Onion(self):#양파 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.on_0 = QRadioButton('없음')
        self.on_1 = QRadioButton('조금')
        self.on_2 = QRadioButton('보통')
        self.on_3 = QRadioButton('많이')
        self.on_group = [self.on_0, self.on_1, self.on_2, self.on_3]
        self.on_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('양파'), 0, 0)
        grid.addWidget(self.on_0, 0, 1)
        grid.addWidget(self.on_1, 0, 2)
        grid.addWidget(self.on_2, 0, 3)
        grid.addWidget(self.on_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Pickled(self):#피클 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.pi_0 = QRadioButton('없음')
        self.pi_1 = QRadioButton('조금')
        self.pi_2 = QRadioButton('보통')
        self.pi_3 = QRadioButton('많이')
        self.pi_group = [self.pi_0, self.pi_1, self.pi_2, self.pi_3]
        self.pi_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('피클'), 0, 0)
        grid.addWidget(self.pi_0, 0, 1)
        grid.addWidget(self.pi_1, 0, 2)
        grid.addWidget(self.pi_2, 0, 3)
        grid.addWidget(self.pi_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Olive(self):#올리브 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.ol_0 = QRadioButton('없음')
        self.ol_1 = QRadioButton('조금')
        self.ol_2 = QRadioButton('보통')
        self.ol_3 = QRadioButton('많이')
        self.ol_group = [self.ol_0, self.ol_1, self.ol_2, self.ol_3]
        self.ol_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('올리브'), 0, 0)
        grid.addWidget(self.ol_0, 0, 1)
        grid.addWidget(self.ol_1, 0, 2)
        grid.addWidget(self.ol_2, 0, 3)
        grid.addWidget(self.ol_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def Jalapeno(self):#할라피뇨 양 선택 그룹박스 함수
        groupbox = QGroupBox('')

        self.ja_0 = QRadioButton('없음')
        self.ja_1 = QRadioButton('조금')
        self.ja_2 = QRadioButton('보통')
        self.ja_3 = QRadioButton('많이')
        self.ja_group = [self.ja_0, self.ja_1, self.ja_2, self.ja_3]
        self.ja_0.setChecked(True)
        grid = QGridLayout()

        grid.addWidget(QLabel('할라피뇨'), 0, 0)
        grid.addWidget(self.ja_0, 0, 1)
        grid.addWidget(self.ja_1, 0, 2)
        grid.addWidget(self.ja_2, 0, 3)
        grid.addWidget(self.ja_3, 0, 4)

        groupbox.setLayout(grid)
        return groupbox

    def S_Group(self):#소스 선택 그룹박스 함수
        groupbox = QGroupBox('소스 선택')
        grid = QGridLayout()

        self.s1 = QCheckBox('랜치')
        self.s2 = QCheckBox('마요네즈')
        self.s3 = QCheckBox('스위트어니언')
        self.s4 = QCheckBox('허니머스타드')
        self.s5 = QCheckBox('스위트칠리')
        self.s6 = QCheckBox('바베큐')
        self.s7 = QCheckBox('핫칠리')
        self.s8 = QCheckBox('사우스웨스트')
        self.s9 = QCheckBox('머스타드')
        self.s10 = QCheckBox('홀스래디쉬')
        self.s11 = QCheckBox('올리브오일')
        self.s12 = QCheckBox('레드와인식초')
        self.s13 = QCheckBox('소금')
        self.s14 = QCheckBox('후추')
        self.s_group = [self.s1, self.s2, self.s3, self.s4, self.s5, self.s6, self.s7,
                        self.s8, self.s9, self.s10, self.s11, self.s12, self.s13, self.s14]

        grid.addWidget(self.s1, 0, 0)
        grid.addWidget(self.s2, 0, 1)
        grid.addWidget(self.s3, 1, 0)
        grid.addWidget(self.s4, 1, 1)
        grid.addWidget(self.s5, 2, 0)
        grid.addWidget(self.s6, 2, 1)
        grid.addWidget(self.s7, 3, 0)
        grid.addWidget(self.s8, 3, 1)
        grid.addWidget(self.s9, 4, 0)
        grid.addWidget(self.s10, 4, 1)
        grid.addWidget(self.s11, 5, 0)
        grid.addWidget(self.s12, 5, 1)
        grid.addWidget(self.s13, 6, 0)
        grid.addWidget(self.s14, 6, 1)
        groupbox.setLayout(grid)
        return groupbox

    def A_Group(self):#추가메뉴 선택 그룹박스 함수
        groupbox = QGroupBox('추가메뉴 선택')
        grid = QGridLayout()

        self.a1 = QCheckBox('더블업(+1800원)')
        self.a2 = QCheckBox('베이컨비츠(+900원)')
        self.a3 = QCheckBox('에그마요(+1600원)')
        self.a4 = QCheckBox('오믈렛(+1200원)')
        self.a5 = QCheckBox('베이컨(+900원)')
        self.a6 = QCheckBox('페퍼로니(+900원)')
        self.a_group = [self.a1, self.a2, self.a3, self.a4, self.a5, self.a6]

        grid.addWidget(self.a1, 0, 0)
        grid.addWidget(self.a2, 0, 1)
        grid.addWidget(self.a3, 1, 0)
        grid.addWidget(self.a4, 1, 1)
        grid.addWidget(self.a5, 2, 0)
        grid.addWidget(self.a6, 2, 1)

        groupbox.setLayout(grid)
        return groupbox

    def Set_Group(self):#세트 여부 창 생성 함수
        groupbox = QGroupBox('')
        grid = QGridLayout()

        self.set_1 = QRadioButton('단품')
        self.set_2 = QRadioButton('세트\n+2200원')

        self.set_group = [self.set_1, self.set_2]

        grid.addWidget(QLabel('세트선택'), 0, 0)
        grid.addWidget(self.set_1, 0, 1)
        grid.addWidget(self.set_2, 0, 2)

        groupbox.setLayout(grid)
        return groupbox

    def Preset(self, n):#프리셋메뉴 선택창 생성 함수
        if n == 0:#에그마요프리셋
            self.pre_0 = [0, 5, 0, 3, 3, 3, 3, 3, 3, 3, 3, [3, 5, 10], [5]]
            self.pre_1 = [0, 5, 0, 3, 3, 3, 3, 3, 3, 3, 3, [1, 5], [5]]
        elif n == 1:#BMT프리셋
            self.pre_0 = [1, 0, 0, 3, 3, 3, 3, 3, 1, 3, 3, [5], [3, 5]]
            self.pre_1 = [1, 4, 1, 3, 3, 0, 3, 3, 2, 3, 3, [1, 5], [5]]
        elif n == 2:#BLT프리셋
            self.pre_0 = [2, 2, 0, 3, 3, 3, 3, 3, 1, 3, 3, [2, 5], [0]]
            self.pre_1 = [2, 4, 1, 3, 3, 0, 3, 3, 2, 3, 3, [1, 5], [5]]
        elif n == 3:#미트볼프리셋
            self.pre_0 = [3, 5, 0, 0, 0, 0, 2, 2, 0, 2, 2, [1, 14], [0]]
            self.pre_1 = [3, 4, 1, 2, 0, 0, 1, 2, 2, 3, 3, [1, 7], [3]]
        elif n == 4:#햄프리셋
            self.pre_0 = [4, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, [1, 2], [0]]
            self.pre_1 = [4, 4, 1, 2, 3, 1, 2, 3, 1, 2, 3, [4, 5], [1]]
        elif n == 5:#참치프리셋
            self.pre_0 = [5, 1, 0, 1, 2, 1, 3, 1, 0, 1, 1, [1, 7], [5]]
            self.pre_1 = [5, 5, 1, 2, 3, 1, 2, 3, 1, 2, 3, [4, 8], [2]]
        elif n == 6:#K-BBQ프리셋
            self.pre_0 = [6, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, [2, 9], [6]]
            self.pre_1 = [6, 5, 0, 2, 3, 1, 2, 3, 1, 2, 3, [5, 10, 13], [3]]
        elif n == 7:#풀드포크프리셋
            self.pre_0 = [7, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, [3, 11], [0]]
            self.pre_1 = [7, 5, 2, 2, 3, 1, 2, 3, 1, 2, 3, [6, 12], [4]]

        sauce0 = ''
        sauce1 = ''
        addon0 = ''
        addon1 = ''

        for i in range(len(self.pre_0[11])):
            sauce0 = sauce0 + ' ' + sauce_list[self.pre_0[11][i]]
        for i in range(len(self.pre_1[11])):
            sauce1 = sauce1 + ' ' + sauce_list[self.pre_1[11][i]]

        for i in range(len(self.pre_0[12])):
            addon0 = addon0 + ' ' + add_list[self.pre_0[12][i]][0]
        for i in range(len(self.pre_1[12])):
            addon1 = addon1 + ' ' + add_list[self.pre_1[12][i]][0]

        if addon0 == 'X':
            addon0 = '추가재료 없음'
        if addon1 == 'X':
            addon1 = '추가재료 없음'

        self.dialog = QDialog()
        self.dialog.setWindowTitle('프리셋 선택')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.setStyleSheet("background-color: white;")
        self.dialog.resize(600, 400)
        grid = QGridLayout()
        self.dialog.setLayout(grid)
        self.index = 0

        self.P0_btn = QPushButton("프리셋 1", self.dialog)
        self.P0_btn.setStyleSheet("background-color :" + subway_yellow + ";")
        self.P1_btn = QPushButton("프리셋 2", self.dialog)
        self.P1_btn.setStyleSheet("background-color : " + subway_yellow + ";")

        self.P0_btn.setMaximumSize(150, 150)
        self.P0_btn.setMinimumSize(150, 150)
        self.P1_btn.setMaximumSize(150, 150)
        self.P1_btn.setMinimumSize(150, 150)

        grid.addWidget(self.P0_btn, 0, 0)
        grid.addWidget(self.P1_btn, 1, 0)
        #프리셋 내용 출력
        grid.addWidget(QLabel(
            '메뉴: ' + menu_list[self.pre_0[0]][0] + ' | 빵: ' + bread_list[self.pre_0[1]] + ' | 치즈: ' + cheese_list[
                self.pre_0[2]] + '\n' +
            veg_list[0] + '(' + veg_amt[self.pre_0[3]] + '), ' + veg_list[1] + '(' + veg_amt[self.pre_0[4]] + '), ' +
            veg_list[2] + '(' + veg_amt[self.pre_0[5]] + '), ' + veg_list[3] + '(' + veg_amt[self.pre_0[6]] + ')\n' +
            veg_list[4] + '(' + veg_amt[self.pre_0[7]] + '), ' + veg_list[5] + '(' + veg_amt[self.pre_0[8]] + '), ' +
            veg_list[6] + '(' + veg_amt[self.pre_0[9]] + '), ' + veg_list[7] + '(' + veg_amt[self.pre_0[10]] + ')\n' +
            '소스: ' + sauce0 + ' | 추가메뉴: ' + addon0), 0, 1)
        grid.addWidget(QLabel(
            '메뉴: ' + menu_list[self.pre_1[0]][0] + ' | 빵: ' + bread_list[self.pre_1[1]] + ' | 치즈: ' + cheese_list[
                self.pre_1[2]] + '\n' +
            veg_list[0] + '(' + veg_amt[self.pre_1[3]] + '), ' + veg_list[1] + '(' + veg_amt[self.pre_1[4]] + '), ' +
            veg_list[2] + '(' + veg_amt[self.pre_1[5]] + '), ' + veg_list[3] + '(' + veg_amt[self.pre_1[6]] + ')\n' +
            veg_list[4] + '(' + veg_amt[self.pre_1[7]] + '), ' + veg_list[5] + '(' + veg_amt[self.pre_1[8]] + '), ' +
            veg_list[6] + '(' + veg_amt[self.pre_1[9]] + '), ' + veg_list[7] + '(' + veg_amt[self.pre_1[10]] + ')\n' +
            '소스: ' + sauce1 + ' | 추가메뉴: ' + addon1), 1, 1)

        self.P0_btn.clicked.connect(lambda: self.P_clicked(0))
        self.P1_btn.clicked.connect(lambda: self.P_clicked(1))

        self.dialog.show()

    def P_clicked(self, n):#프리셋 선택 판독 함수
        if n == 0:
            self.temp_order = self.pre_0
        elif n == 1:
            self.temp_order = self.pre_1
        self.dialog.close()
        self.Ask_set()

    def Ask_set(self):#세트여부 질문 함수
        self.dialog = QDialog()
        self.dialog.setWindowTitle('세트 여부')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        self.dialog.resize(400, 200)
        self.dialog.setStyleSheet("background-color: white;")
        grid = QGridLayout()
        self.dialog.setLayout(grid)

        self.btn0 = QPushButton("단품", self.dialog)
        self.btn0.setStyleSheet("background-color : " + subway_yellow + ";")
        self.btn1 = QPushButton("세트\n+2200원", self.dialog)
        self.btn1.setStyleSheet("background-color : " + subway_yellow + ";")

        self.btn0.setMaximumSize(150, 150)
        self.btn0.setMinimumSize(150, 150)
        self.btn1.setMaximumSize(150, 150)
        self.btn1.setMinimumSize(150, 150)

        grid.addWidget(self.btn0, 0, 0)
        grid.addWidget(self.btn1, 0, 1)

        self.btn0.clicked.connect(lambda: self.O_final(0))
        self.btn1.clicked.connect(lambda: self.O_final(1))

        self.dialog.show()

    def O_final(self, n):#주문 내용을 current_order 변수에 전달하는 함수
        self.temp_order.append(n)
        self.dialog.close()
        current_order.append(self.temp_order)
        self.refresh_choose_menu()

    def createLayout_Pre_Container(self):#프리셋 메뉴 컨테이너
        self.menus = QScrollArea(self)
        self.menus.setWidgetResizable(True)

        self.widgets = []
        self.widget = QWidget()
        self.menus.setWidget(self.widget)
        self.layout_area = QGridLayout(self.widget)

        self.menu0_btn = QPushButton() #에그마요( menu_list[0][0])
        self.menu0_btn.setStyleSheet("background-image: url(eggmayo.png);"
                                     "border : 0 ;")
        self.menu0_btn.sizeHint()
        self.menu0_btn.clicked.connect(lambda: self.Preset(0))

        self.menu1_btn = QPushButton() #BMT (menu_list[1][0])
        self.menu1_btn.setStyleSheet("background-image: url(bmt.png);"
                                     "border : 0 ;")
        self.menu1_btn.sizeHint()
        self.menu1_btn.clicked.connect(lambda: self.Preset(1))

        self.menu2_btn = QPushButton()#이탈리안 BLT (menu_list[2][0])
        self.menu2_btn.setStyleSheet("background-image: url(blt.png);"
                                     "border : 0 ;")
        self.menu2_btn.sizeHint()
        self.menu2_btn.clicked.connect(lambda: self.Preset(2))

        self.menu3_btn = QPushButton()#미트볼 (menu_list[3][0])
        self.menu3_btn.setStyleSheet("background-image: url(meatball.png);"
                                     "border : 0 ;")
        self.menu3_btn.sizeHint()
        self.menu3_btn.clicked.connect(lambda: self.Preset(3))

        self.menu4_btn = QPushButton()#햄 (menu_list[4][0])
        self.menu4_btn.setStyleSheet("background-image: url(ham.png);"
                                     "border : 0 ;")
        self.menu4_btn.sizeHint()
        self.menu4_btn.clicked.connect(lambda: self.Preset(4))

        self.menu5_btn = QPushButton()#참치 (menu_list[5][0])
        self.menu5_btn.setStyleSheet("background-image: url(tuna.png);"
                                     "border : 0 ;")
        self.menu5_btn.sizeHint()
        self.menu5_btn.clicked.connect(lambda: self.Preset(5))

        self.menu6_btn = QPushButton()#kbbq (menu_list[6][0])
        self.menu6_btn.setStyleSheet("background-image: url(kbbq.png);"
                                     "border : 0 ;")
        self.menu6_btn.sizeHint()
        self.menu6_btn.clicked.connect(lambda: self.Preset(6))

        self.menu7_btn = QPushButton()#풀드포크 (menu_list[7][0])
        self.menu7_btn.setStyleSheet("background-image: url(pulledpork.png);"
                                     "border : 0 ;")
        self.menu7_btn.sizeHint()
        self.menu7_btn.clicked.connect(lambda: self.Preset(7))

        self.buttons = [self.menu0_btn, self.menu1_btn, self.menu2_btn, self.menu3_btn, self.menu4_btn, self.menu5_btn,
                        self.menu6_btn, self.menu7_btn]

        for i in range(len(self.buttons)):
            tp_widget = self.buttons[i]
            tp_widget.setMaximumSize(200, 200)
            tp_widget.setMinimumSize(200, 200)
            self.widgets.append(tp_widget)
            if i % 2 == 0:
                self.layout_area.addWidget(tp_widget, i // 2, i % 2)
            else:
                self.layout_area.addWidget(tp_widget, i // 2, i % 2)

        return self.menus

    def createLayout_S_container(self):#직접선택 컨테이너
        self.menus = QScrollArea(self)
        #self.orders.setFixedWidth(480)
        self.menus.setWidgetResizable(True)

        self.widgets = []
        self.widget = QWidget()
        self.menus.setWidget(self.widget)
        self.layout_area = QGridLayout(self.widget)

        self.menu0_btn = QPushButton()  #에그마요( menu_list[0][0])
        self.menu0_btn.setStyleSheet("background-image: url(eggmayo.png);"
                                     "border : 0 ;")
        self.menu0_btn.sizeHint()
        self.menu0_btn.clicked.connect(lambda: self.Selecting(0))

        self.menu1_btn = QPushButton()  #BMT (menu_list[1][0])
        self.menu1_btn.setStyleSheet("background-image: url(bmt.png);"
                                     "border : 0 ;")
        self.menu1_btn.sizeHint()
        self.menu1_btn.clicked.connect(lambda: self.Selecting(1))

        self.menu2_btn = QPushButton()  #이탈리안 BLT (menu_list[2][0])
        self.menu2_btn.setStyleSheet("background-image: url(blt.png);"
                                     "border : 0 ;")
        self.menu2_btn.sizeHint()
        self.menu2_btn.clicked.connect(lambda: self.Selecting(2))

        self.menu3_btn = QPushButton()  #미트볼 (menu_list[3][0])
        self.menu3_btn.setStyleSheet("background-image: url(meatball.png);"
                                     "border : 0 ;")
        self.menu3_btn.sizeHint()
        self.menu3_btn.clicked.connect(lambda: self.Selecting(3))

        self.menu4_btn = QPushButton()  #햄 (menu_list[4][0])
        self.menu4_btn.setStyleSheet("background-image: url(ham.png);"
                                     "border : 0 ;")
        self.menu4_btn.sizeHint()
        self.menu4_btn.clicked.connect(lambda: self.Selecting(4))

        self.menu5_btn = QPushButton()  #참치 (menu_list[5][0])
        self.menu5_btn.setStyleSheet("background-image: url(tuna.png);"
                                     "border : 0 ;")
        self.menu5_btn.sizeHint()
        self.menu5_btn.clicked.connect(lambda: self.Selecting(5))

        self.menu6_btn = QPushButton()  #kbbq (menu_list[6][0])
        self.menu6_btn.setStyleSheet("background-image: url(kbbq.png);"
                                     "border : 0 ;")
        self.menu6_btn.sizeHint()
        self.menu6_btn.clicked.connect(lambda: self.Selecting(6))

        self.menu7_btn = QPushButton()  #풀드포크 (menu_list[7][0])
        self.menu7_btn.setStyleSheet("background-image: url(pulledpork.png);"
                                     "border : 0 ;")
        self.menu7_btn.clicked.connect(lambda: self.Selecting(7))

        self.buttons = [self.menu0_btn, self.menu1_btn, self.menu2_btn, self.menu3_btn, self.menu4_btn, self.menu5_btn,
                        self.menu6_btn, self.menu7_btn]

        for i in range(len(self.buttons)):
            tp_widget = self.buttons[i]
            tp_widget.setMaximumSize(200, 200)
            tp_widget.setMinimumSize(200, 200)
            self.widgets.append(tp_widget)
            if i % 2 == 0:
                self.layout_area.addWidget(tp_widget, i // 2, i % 2)
            else:
                self.layout_area.addWidget(tp_widget, i // 2, i % 2)

        return self.menus

    def select_custom(self):#개인메뉴 주문
        global id_dic, custom_list, login_id

        self.index = 2
        for i, sltbtn in enumerate(self.sltbtns):
            if self.sltbtns[i].isChecked():
                current_order.append(custom_list[i][1])
                self.refresh_choose_menu()
                self.sltbtns[i].toggle()

    def delete_custom(self):#개인메뉴 삭제
        global id_dic, custom_list, login_id

        self.del_list = []
        for i, checkbox in enumerate(self.C_checkboxes):
            if checkbox.isChecked():
                self.del_list.append(i)
        self.del_list.sort(reverse=True)

        if len(self.del_list) == 0:
            msg = QMessageBox.information(self, '개인메뉴 삭제 실패', '선택된 개인메뉴가 없습니다', QMessageBox.Yes, QMessageBox.Yes)
        else:
            reply = QMessageBox.information(self, '개인메뉴 삭제', '해당메뉴를 개인메뉴에서 삭제하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                for i in self.del_list:
                    self.C_widgets[i].setParent(None)
                    del self.C_checkboxes[i]  #위젯삭제
                    del id_dic[login_id][i]
                    OrderMain.store_id(self)  # id DB 파일출력
                sucmsg = QMessageBox.information(self, '개인메뉴 삭제 성공', '개인메뉴를 삭제하였습니다',
                                                 QMessageBox.Yes, QMessageBox.Yes)
            else:
                pass

    def createLayout_C_menu(self, n):#개인메뉴 주문 위젯
        widget = QWidget()

        #체크박스
        checkbox = QtWidgets.QCheckBox()
        self.C_checkboxes.append(checkbox)

        #개인메뉴명
        txt = custom_list[n][0]
        menuTxt = QLabel(txt, self)

        #세부사항
        sauce = ''
        for i in custom_list[n][1][11]:
            sauce += sauce_list[i] + ' '
        addon = ''
        for j in custom_list[n][1][12]:
            addon += add_list[j][0] + ' '
        price = 0
        price += menu_list[custom_list[n][1][0]][1]
        for i in custom_list[n][1][12]: #추가메뉴 가격 추가
            price += add_list[i][1]
        if custom_list[n][1][13] == 1:  # 세트일 경우 2200원 추가
            price += 2200
        txt2 = ('가격: ' + str(price) + ' | 메뉴: ' + menu_list[custom_list[n][1][0]][0] + ' | 빵: ' + bread_list[custom_list[n][1][1]]
                + ' | 치즈: ' + cheese_list[custom_list[n][1][2]] + '\n' + '양상추(' + veg_amt[custom_list[n][1][3]] + '), '
                + '토마토(' + veg_amt[custom_list[n][1][4]] + '), ' + '오이(' + veg_amt[custom_list[n][1][5]] + '), '
                + '피망(' + veg_amt[custom_list[n][1][6]] + '),\n' + '양파(' + veg_amt[custom_list[n][1][7]] + '), '
                + '피클(' + veg_amt[custom_list[n][1][8]] + '), ' + '올리브(' + veg_amt[custom_list[n][1][9]] + '), '
                + '할라피뇨(' + veg_amt[custom_list[n][1][10]] + ')\n'
                + '소스: ' + sauce + ' | 추가메뉴: ' + addon + ' | 세트: ' + set_list[custom_list[n][1][13]])

        detailTxt = QLabel(txt2, self)

        #주문버튼
        sltbtn = QPushButton('주문하기')
        sltbtn.setStyleSheet("background-color : " + subway_yellow + ";")
        sltbtn.setCheckable(True)
        self.sltbtns.append(sltbtn)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(menuTxt, 2)
        hbox1.addWidget(sltbtn, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(detailTxt)

        hbox = QHBoxLayout()
        hbox.addWidget(checkbox, 1)
        hbox.addLayout(vbox, 7)

        widget.setLayout(hbox)

        return widget

    def createLayout_C_container(self):#개인메뉴 포함 컨테이너
        global custom_list
        self.C_menu = QScrollArea(self)
        self.C_menu.setWidgetResizable(True)

        self.C_widgets = []
        self.C_widget = QWidget()
        self.C_menu.setWidget(self.C_widget)
        self.C_layout_area = QVBoxLayout(self.C_widget)
        for i in range(len(custom_list)):
            C_widget = self.createLayout_C_menu(i)
            self.C_widgets.append(C_widget)
            self.C_layout_area.addWidget(C_widget)

        self.C_layout_area.addStretch(1)

        return self.C_menu

    def back(self):#뒤로가기
        global current_order
        if (len(current_order) >= 1) or OrderMain.is_login(self):
            if OrderMain.is_login(self) :
                reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제되고 로그아웃됩니다. 계속하시겠습니까?',
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            else:
                reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제됩니다. 계속하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                current_order = []
                OrderMain._logout(self)
                ex.stk_w.setCurrentWidget(order_main)
            else:
                OrderMain.cancel(self)
        else :
            ex.stk_w.setCurrentWidget(order_main)

    def next(self):#메뉴 주문에서 주문 확인으로 넘기기
        if current_order != []:
            order_confirm_refresh = OrderConfirm()
            ex.stk_w.addWidget(order_confirm_refresh)
            ex.stk_w.setCurrentWidget(order_confirm_refresh)
        else:
            reply = QMessageBox.information(self, '', '하나 이상의 메뉴를 선택해주세요',
                                            QMessageBox.Yes, QMessageBox.Yes)

    def back_home(self):
        global current_order
        if (len(current_order) >= 1) or OrderMain.is_login(self) :
            reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제되고 로그아웃됩니다. 계속하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                current_order = []
                OrderMain._logout(self)
                ex.stk_w.setCurrentWidget(initialize)
            else:
                OrderMain.cancel(self)
        else:
            ex.stk_w.setCurrentWidget(initialize)

class OrderConfirm(QWidget):#주문확인 클래스
    def __init__(self, parent=None):
        super(OrderConfirm, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.total_price = 0
        self.del_list = []
        self.tp_list = current_order
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white;")
        j = 1
        for i in current_order:
            j += 1

        self.tab1 = QWidget()  #주문확인 탭
        self.tab2 = QWidget()  #결제 탭

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab1, '주문확인')
        self.tabs.addTab(self.tab2, ' 결제 ')

        VBOX = QVBoxLayout()
        grid = QGridLayout()
        self.home = QPushButton()
        self.home.setStyleSheet("background-image: url(home.png);"
                                "border : 0 ")
        self.home.setFixedSize(80, 80)
        self.home.clicked.connect(self.back_home)

        self.subwayLbl2 = QLabel()
        self.subwayLbl2.setPixmap(QtGui.QPixmap("./subway.png"))
        self.sizeHint()
        grid.addWidget(self.home, 0, 0, 1, 2)
        grid.addWidget(self.subwayLbl2, 0, 1, 2, 5)

        VBOX.addLayout(grid)

        #주문확인 레이아웃
        self.tab1.layout = QVBoxLayout(self)

        self.in_btn = QPushButton('개인메뉴 추가', self)
        self.in_btn.setStyleSheet("background-color : " + subway_yellow +";")
        self.in_btn.clicked.connect(self.insert_custom)

        self.del_btn = QPushButton('주문 삭제', self)
        self.del_btn.clicked.connect(self.delete_menu)
        self.del_btn.setStyleSheet("background-color : " + subway_yellow + ";")

        self.back_btn = QPushButton('주문추가/돌아가기', self)
        self.back_btn.clicked.connect(self.refresh_choose_menu)
        self.back_btn.setStyleSheet("background-color : " + subway_yellow + ";")

        #레이아웃 설정
        hbox = QHBoxLayout()
        hbox.addWidget(self.in_btn)
        hbox.addWidget(self.del_btn)

        #주문출력스크롤박스
        self.checkboxes = []  #개인메뉴추가, 삭제 메뉴 선택용
        self.modbtns = []  #수정메뉴 선택용
        self.tab1.layout.addWidget(self.createLayout_Container())

        for i, modbtn in enumerate(self.modbtns):
            self.modbtns[i].clicked.connect(self.mod_menu)  #수정하기 선택 시

        self.tab1.layout.addLayout(hbox)
        self.tab1.layout.addWidget(self.back_btn)
        self.tab1.setLayout(self.tab1.layout)

        #결제 레이아웃
        self.tab2.layout = QVBoxLayout(self)

        self.here_btn = QPushButton('매장 식사', self)
        self.here_btn.setStyleSheet("background-color : "+ subway_yellow+";")
        self.here_btn.setCheckable(True)

        self.go_btn = QPushButton('포장', self)
        self.go_btn.setStyleSheet("background-color : " + subway_yellow + ";")
        self.go_btn.setCheckable(True)

        self.pay_btn = QPushButton('결제하기', self)
        self.pay_btn.setStyleSheet("background-color : "+ subway_yellow+";")

        self.here_btn.clicked.connect(self.togo)
        self.go_btn.clicked.connect(self.togo)
        self.pay_btn.clicked.connect(self.pay)

        self.tab2.layout.addWidget(self.createLayout_P_container())

        self.total_price_Lbl = QLabel('총가격: ' + str(self.total_price), self)
        font1 = self.total_price_Lbl.font()
        font1.setPointSize(11)
        self.total_price_Lbl.setFont(font1)

        P_hbox = QHBoxLayout()

        P_hbox.addWidget(self.here_btn)
        P_hbox.addWidget(self.go_btn)


        self.tab2.layout.addWidget(self.total_price_Lbl)
        self.tab2.layout.addLayout(P_hbox)
        self.tab2.layout.addWidget(self.pay_btn)
        self.tab2.setLayout(self.tab2.layout)

        self.layout.addLayout(VBOX)
        self.layout.addWidget(self.tabs)
        self.setLayout(VBOX)
        self.tabs.setStyleSheet(TabStyleSheet)

    def mod_menu(self):#주문 수정
        self.mod_li = []

        for i, modbtn in enumerate(self.modbtns):
            if self.modbtns[i].isChecked():
                self.modbtns[i].toggle()
                self.mod_num = i

        self.mod_window = ChooseMenu()
        self.mod_window.Selecting(current_order[self.mod_num][0], 1)

        #기존 선택내역 보여주기
        self.mod_window.b_group[current_order[self.mod_num][1]].setChecked(True)  #빵
        self.mod_window.c_group[current_order[self.mod_num][2]].setChecked(True)  #치즈선택
        self.mod_window.le_group[current_order[self.mod_num][3]].setChecked(True)  #양상추
        self.mod_window.to_group[current_order[self.mod_num][4]].setChecked(True)  #토마토
        self.mod_window.cu_group[current_order[self.mod_num][5]].setChecked(True)  #오이
        self.mod_window.pe_group[current_order[self.mod_num][6]].setChecked(True)  #피망
        self.mod_window.on_group[current_order[self.mod_num][7]].setChecked(True)  #양파
        self.mod_window.pi_group[current_order[self.mod_num][8]].setChecked(True)  #피클
        self.mod_window.ol_group[current_order[self.mod_num][9]].setChecked(True)  #올리브
        self.mod_window.ja_group[current_order[self.mod_num][10]].setChecked(True)   #할라피뇨

        for j in current_order[self.mod_num][11]:  #소스
            if j == 0:
                break
            else:
                self.mod_window.s_group[j - 1].setChecked(True)
        for j in current_order[self.mod_num][12]:  #추가메뉴
            if j == 0:
                pass
            else:
                self.mod_window.a_group[j - 1].setChecked(True)

        self.mod_window.set_group[current_order[self.mod_num][13]].setChecked(True)  #세트
        self.mod_window.ok_btn.clicked.connect(self.mod_done)

    def mod_done(self):#수정완료 함수
        mod_li = self.mod_window.temp_order
        current_order[self.mod_num] = mod_li
        self.refresh_confirm_menu()

    def insert_custom(self):#개인메뉴 추가
        global id_dic, custom_list, login_id
        self.menu_num = []  #개인메뉴에 저장될 메뉴번호
        self.new_custom = []  #개인메뉴에 저장될 메뉴
        flag = 0
        if not OrderMain.is_login(self):
            reply = QMessageBox.information(self, '개인메뉴 추가', '로그인하셔야 사용가능한 메뉴입니다.\n로그인하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                OrderMain.login(self)
            else:
                pass
        elif OrderMain.is_login(self):
            for i, checkbox in enumerate(self.checkboxes):
                if checkbox.isChecked():
                    self.menu_num.append(i)
            self.menu_num.sort(reverse=True)

            if len(self.menu_num) == 0: #선택된 메뉴가 없는 경우
                msg = QMessageBox.information(self, '개인메뉴 추가', '선택된 메뉴가 없습니다',
                                                QMessageBox.Yes, QMessageBox.Yes)

            for i in self.menu_num:
                # 기존 개인메뉴와의 중복 검토
                for j in custom_list:
                    if j[1] == current_order[i]:
                        fail_msg = QMessageBox.information(self, '개인메뉴 저장 실패', '해당메뉴는 이미 개인메뉴에 저장되어 있습니다',
                                                           QMessageBox.Yes, QMessageBox.Yes)
                        flag = 1
                if flag == 0:
                    name, ok = QInputDialog.getText(self, '개인메뉴 이름', '개인메뉴의 이름을 입력해주세요')
                    # 개인메뉴 이름 중복 검토
                    for j in custom_list:
                        if j[0] == name :
                            fail_msg = QMessageBox.information(self, '개인메뉴 저장 실패', '이미 존재하는 개인메뉴 이름입니다',
                                                                   QMessageBox.Yes, QMessageBox.Yes)
                            flag = 1
                    if ok and flag == 0:
                        self.new_custom.append(name)
                        self.new_custom.append(current_order[i])
                        id_dic[login_id].append(self.new_custom)
                        OrderMain.store_id(self)  #id DB 파일출력
                        suc_msg = QMessageBox.information(self, '개인메뉴 저장 성공', '해당메뉴를 개인메뉴에 저장 하였습니다',
                                                          QMessageBox.Yes, QMessageBox.Yes)
                        self.new_custom = []  #초기화
           

    def togo(self): #매장/포장 선택 함수
        if self.here_btn.isChecked():
            self.here_btn.setStyleSheet("background-color : "+ subway_green+"; color: white")
            self.go_btn.setStyleSheet("background-color : "+ subway_yellow+";")
            self.here_btn.toggle()
        elif self.go_btn.isChecked():
            self.here_btn.setStyleSheet("background-color : "+ subway_yellow+";") 
            self.go_btn.setStyleSheet("background-color : "+ subway_green+"; color: white")
            self.go_btn.toggle()



    def pay(self):#결제(매장, 포장여부 선택 확인 후 진행) 함수
        global current_order
        global ordercount
        self.tp_list = current_order

        here_color = self.here_btn.palette().button().color()
        go_color = self.go_btn.palette().button().color()

        om_list = copy.deepcopy(current_order)
        
        if here_color.name() == "#008c15" or go_color.name() == "#008c15":
            reply = QMessageBox.information(self, '결제하기', '결제가 완료되었습니다.',
                                            QMessageBox.Yes, QMessageBox.Yes)
            if here_color.name() == "#008c15":
                om_list.append(0) #매장: 0

            elif go_color.name() == "#008c15":
                om_list.append(1) #포장: 1

            ordercount += 1
            queue.enqueue(om_list)  # 주문관리 큐에 추가

            for i in range(len(self.tp_list)):

                self.tp_list[i].insert(0, datetime.today().strftime("%y%m%d"))
                self.tp_list[i].append(self.price_list[i])
                total_order.append(self.tp_list[i])

            OrderMain.logout(self)
            current_order = []

            ex.stk_w.setCurrentWidget(order_main)

        else:#매장/포장 선택하지 않은 경우
            reply = QMessageBox.information(self, '결제하기', '매장 또는 포장을 선택해주세요.',
                                            QMessageBox.Yes, QMessageBox.Yes)
        #결제 후 주문데이터 데이터베이스에 저장
        order_file = open('order_DB.csv', 'r')
        csv_data = csv.reader(order_file)
        db_data = []
        for line in csv_data:
            db_data.append(line)
        # csv 파일을 불러오면 datatypq을 str -> int 로 변환
        for i in range(len(db_data)):
            for j in range(1, len(db_data[0])):
                if j == 12 or j == 13:
                    str_data = str(db_data[i][j])
                    int_data = re.findall("\d+", str_data)
                    db_data[i][j] = int_data
                    for k in range(len(db_data[i][j])):
                        db_data[i][j][k] = int(db_data[i][j][k])
                else:
                    db_data[i][j] = int(db_data[i][j])
        order_file.close()
        #불러온 데이터베이스에 새로운 데이터 추가
        db_list = db_data
        for i in range(len(total_order)):
            db_list.append(total_order[i])
        csvfile = open('order_DB.csv', 'w', newline="")
        csvwriter = csv.writer(csvfile)
        for row in db_list:
            csvwriter.writerow(row)
        csvfile.close()

    def delete_menu(self):#주문메뉴삭제
        self.del_list = []
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.isChecked():
                self.del_list.append(i)
        self.del_list.sort(reverse=True)

        if self.del_list == []:
            reply = QMessageBox.information(self, '주문삭제', '선택된 메뉴가 없습니다.',
                                            QMessageBox.Yes, QMessageBox.Yes)        
        

        for i in self.del_list:
            #주문확인 레이아웃 수정
            self.widgets[i].setParent(None)
            del self.checkboxes[i]
            del self.widgets[i]
            del self.modbtns[i]

            #결제 레이아웃 수정
            self.P_widgets[i].setParent(None)
            del self.P_widgets[i]
            del current_order[i]#current_order에서 삭제

            #총가격 수정
            self.total_price -= self.price_list[i]
            del self.price_list[i]
        self.total_price_Lbl.setText('총가격: ' + str(self.total_price))

        j = 1
        for i in current_order:
            j += 1

        if len(current_order) == 0:
            reply = QMessageBox.information(self, '주문삭제', '주문내역이 없어 메뉴선택 단계로 돌아갑니다.',
                                            QMessageBox.Yes, QMessageBox.Yes)
            self.refresh_choose_menu()

    def createLayout_Order(self, n):#주문메뉴별 위젯
        widget = QWidget()

        #체크박스
        checkbox = QtWidgets.QCheckBox()
        self.checkboxes.append(checkbox)

        #메뉴이미지
        menuimages = [QtGui.QPixmap("./eggmayo2.png"), QtGui.QPixmap("./bmt2.png"), QtGui.QPixmap("./blt2.png"), 
                  QtGui.QPixmap("./meatball2.png"), QtGui.QPixmap("./ham2.png"), QtGui.QPixmap("./tuna2.png"),
                  QtGui.QPixmap("./kbbq2.png"), QtGui.QPixmap("./pulledpork2.png")]
        menu = current_order[n][0]
        menuimages[menu] = menuimages[menu].scaledToWidth(130, Qt.SmoothTransformation)
        menuLb =QLabel()

        menuLb.setPixmap(menuimages[menu])



        #메뉴명
        txt = menu_list[current_order[n][0]][0]
        menuTxt = QLabel(txt, self)
        font1 = menuTxt.font()
        font1.setPointSize(11)
        menuTxt.setFont(font1)

        #세부사항
        sauce = ''
        for i in current_order[n][11]:
            sauce += sauce_list[i] + ' '
        addon = ''
        for j in current_order[n][12]:
            addon += add_list[j][0] + ' '
        price = 0
        price += menu_list[current_order[n][0]][1]
        for k in current_order[n][12]:  # 추가메뉴 가격 추가
            price += add_list[k][1]
        if current_order[n][13] == 1:  # 세트일 경우 2200원 추가
            price += 2200
        txt2 = ('가격: ' + str(price) + ' | 빵: ' + bread_list[current_order[n][1]]
                + ' | 치즈: ' + cheese_list[current_order[n][2]] + '\n' + '양상추(' + veg_amt[current_order[n][3]] + '), '
                + '토마토(' + veg_amt[current_order[n][4]] + '), ' + '오이(' + veg_amt[current_order[n][5]] + '), '
                + '피망(' + veg_amt[current_order[n][6]] + '),\n' + '양파(' + veg_amt[current_order[n][7]] + '), '
                + '피클(' + veg_amt[current_order[n][8]] + ')' + '올리브(' + veg_amt[current_order[n][9]] + '), '
                + '할라피뇨(' + veg_amt[current_order[n][10]] + ')\n'
                + '소스: ' + sauce + '\n추가메뉴: ' + addon + ' | 세트: ' + set_list[current_order[n][13]])
        detailTxt = QLabel(txt2, self)
        font2 = detailTxt.font()
        font2.setPointSize(9)
        detailTxt.setFont(font2)

        #수정버튼
        modbtn = QPushButton('수정하기')
        modbtn.setStyleSheet("background-color : " + subway_yellow + ";")
        modbtn.setCheckable(True)
        self.modbtns.append(modbtn)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(menuTxt, 2)
        hbox1.addWidget(modbtn, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addWidget(detailTxt)

        hbox = QHBoxLayout()
        hbox.addWidget(checkbox, 1)
        hbox.addWidget(menuLb, 2)
        hbox.addLayout(vbox, 7)

        widget.setLayout(hbox)

        return widget

    def createLayout_Container(self):#주문메뉴 포함 컨테이너
        self.orders = QScrollArea(self)
        self.orders.setWidgetResizable(True)

        self.widgets = []
        self.widget = QWidget()
        self.orders.setWidget(self.widget)
        self.layout_area = QVBoxLayout(self.widget)

        for i in range(len(current_order)):
            tp_widget = self.createLayout_Order(i)
            self.widgets.append(tp_widget)
            self.layout_area.addWidget(tp_widget)
        self.layout_area.addStretch(1)

        return self.orders

    def createLayout_P_order(self, n):#결제 메뉴별 위젯
        widget = QWidget()
        tp_price = 0

        #메뉴명
        txt = menu_list[current_order[n][0]][0]
        menuTxt = QLabel(txt, self)

        #메뉴별 가격
        tp_price += menu_list[current_order[n][0]][1]
        for i in current_order[n][12]: #추가메뉴 가격 추가
            tp_price += add_list[i][1]
        if current_order[n][13] == 1: #세트일 경우 2200원 추가
            tp_price += 2200
        self.total_price += tp_price
        menu_price = QLabel('메뉴가격: ' + str(tp_price), self)
        self.price_list.append(tp_price)

        vbox = QVBoxLayout()
        vbox.addWidget(menuTxt)
        vbox.addWidget(menu_price)

        widget.setLayout(vbox)

        return widget

    def createLayout_P_container(self):#결제확인용 주문메뉴 컨테이너
        self.P_orders = QScrollArea(self)
        #self.orders.setFixedWidth(480)
        self.P_orders.setWidgetResizable(True)

        self.price_list = []
        self.P_widgets = []
        self.P_widget = QWidget()
        self.P_orders.setWidget(self.P_widget)
        self.C_layout_area = QVBoxLayout(self.P_widget)

        for i in range(len(current_order)):
            tp_widget = self.createLayout_P_order(i)
            self.P_widgets.append(tp_widget)
            self.C_layout_area.addWidget(tp_widget)

        self.C_layout_area.addStretch(1)

        return self.P_orders

    def refresh_choose_menu(self):#메뉴선택 새로고침
        select_menu_refresh = ChooseMenu()
        ex.stk_w.addWidget(select_menu_refresh)
        ex.stk_w.setCurrentWidget(select_menu_refresh)

    def refresh_confirm_menu(self):#주문확인 새로고침
        order_confirm_refresh = OrderConfirm()
        ex.stk_w.addWidget(order_confirm_refresh)
        ex.stk_w.setCurrentWidget(order_confirm_refresh)

    def back_home(self):
        global current_order
        if (len(current_order) >= 1) or OrderMain.is_login(self) :
            reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제되고 로그아웃됩니다. 계속하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                current_order = []
                OrderMain._logout(self)
                ex.stk_w.setCurrentWidget(initialize)
            else:
                OrderMain.cancel(self)
        else:
            ex.stk_w.setCurrentWidget(initialize)

    def is_login(self):#로그인 상태 판별
        global login_id, custom_list
        if len(login_id) == 0:
            return False
        if len(login_id) > 0:
            return True

    def load_id(self):
        global id_dic
        file = open("id_DB", "rb")
        id_dic = pickle.load(file)


class MyMain(QWidget):#초기화면 실행 함수
    def __init__(self):
        super().__init__()
        self.stk_w = QStackedWidget(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("SUBWAY KIOSK")
        self.setStyleSheet("background-color: white;")
        widget_box = QVBoxLayout()

        #전환화면추가
        self.stk_w.addWidget(initialize)
        self.stk_w.addWidget(order_main)
        self.stk_w.addWidget(order_confirm)
        self.stk_w.addWidget(select_menu)

        widget_box.addWidget(self.stk_w)

        self.setLayout(widget_box)

        self.setGeometry(300, 50, 700, 800)
        self.show()


class OrderQueue():#주문관리
    def __init__(self):
        self.orders = []
        self.front_index = 0
        self.length = 0

    def __len__(self):
        return len(self.orders)

    def enqueue(self, orderdata):

        togo = orderdata[-1]  #포장여부

        for i in range(len(orderdata) - 1):
            self.orders.append(self.change_string(orderdata[i], togo))
            self.length += 1

    def dequeue(self):
        if len(self.orders) == 0 or self.front_index == len(self.orders):#주문내역이 없음 확인
            return None
        else:
            data = self.orders[self.front_index]
            self.front_index += 1
            self.length -= 1
            return data

    def is_togo(self,n):
        return n

    def change_string(self, orderdata,togo):
        data = []
        vegetable = ""
        sauce = ""
        add = ""
        global ordercount

        data.append(0) # 체크박스 들어갈 공간
        data.append(str(ordercount))

        data.append(menu_list[orderdata[0]][0])#메뉴이름
        data.append(bread_list[orderdata[1]])#빵종류
        data.append(cheese_list[orderdata[2]][:-2])#치즈

        # 야채관련 정보
        for i in range(8):
            if orderdata[i + 3] == 0:
                amount = ""
            elif orderdata[i + 3] == 1:
                amount = "(소)"
            elif orderdata[i + 3] == 2:
                amount = "(중)"
            else:
                amount = "(다)"

            if i == 0:
                vegetable = vegetable + veg_list[i] + amount
            else:
                vegetable = vegetable + ", " + veg_list[i] + amount

        data.append(vegetable)

        #소스 정보
        for i in orderdata[11]:
            if i == orderdata[11][-1]:
                sauce = sauce + sauce_list[i]
            else:
                sauce = sauce + sauce_list[i] + ', '
        data.append(sauce)

        #추가메뉴 정보
        for i in orderdata[12]:
            if i == orderdata[12][-1]:
                add = add + add_list[i][0]
            else:
                add = add + add_list[i][0] + ' '
        data.append(add)

        #세트여부
        if orderdata[13] == 0:
            data.append('O')
        else:
            data.append('X')

        if togo == 1:
            data.append('O')
        else:
            data.append('X')
        return data

    def return_queue(self, order_data):

        if self.front_index > 0:
            self.orders[self.front_index - 1] = order_data
            self.front_index -= 1
            self.length += 1

        else:
            self.orders.insert(0, order_data)

class DoneList():#조리완료 처리 클래스
    def __init__(self):
        self.done = []
        self.length = 0

    def __len__(self):
        return (len(self.orders))

    def pop(self, n):
        if len(self.done) == 0:
            return None
        else:
            x = self.done[n]
            del self.done[n]
            self.length -= 1
            return x

    def append(self, orderdata):
        self.length += 1
        self.done.append(orderdata)

class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df = df

        #테이블 형태 설정
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        self.setHorizontalHeaderLabels(('완료', '주문번호', '메뉴', '빵', '치즈', '채소', '소스', '추가메뉴', '세트','포장'))

        #데이터 삽입
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                item = MyQTableWidgetItemCheckBox()  #정렬을 위해 checkbox와 함께 item 삽입
                self.setItem(i, 0, item)
                chbox = MyCheckBox(item)
                self.setCellWidget(i, 0, chbox)
                chbox.stateChanged.connect(self.__checkbox_change)
                self.setItem(i, j, QTableWidgetItem(self.df.iloc[i, j]))

        self.sortByColumn(0, Qt.AscendingOrder)  #체크박스 열을 기준으로 정렬
        self.setSortingEnabled(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.resizeColumnsToContents()
        self.setColumnWidth(0, 20)

    def __checkbox_change(self, checkvalue):
        chbox = self.sender()

class MyCheckBox(QCheckBox):
    def __init__(self, item):
        super().__init__()
        self.item = item
        self.mycheckvalue = 0
        self.stateChanged.connect(self.__checkbox_change)
        self.stateChanged.connect(self.item.my_setdata)#checked 여부로 정렬을 하기위한 data 저장

    def __checkbox_change(self, checkvalue):
        self.mycheckvalue = checkvalue

        r = self.get_row()

        x = len(checked)
        if self.mycheckvalue == 2:
            checked.append(r + x)
        else:
            checked.pop()

    def get_row(self):
        return self.item.row()

class MyQTableWidgetItemCheckBox(QTableWidgetItem):
    def __init__(self):
        super().__init__()
        self.setData(Qt.UserRole, 0)

    def __lt__(self, other):
        return self.data(Qt.UserRole) < other.data(Qt.UserRole)

    def my_setdata(self, value):
        self.setData(Qt.UserRole, value)

class OrderManage(QtWidgets.QMainWindow):#주문관리 메인 화면
    def __init__(self, parent=None):
        super(OrderManage, self).__init__(parent)

        self.centralwidget = QtWidgets.QWidget(self)
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.no_waiting = QtWidgets.QLabel(self.centralwidget)#대기 메뉴 수 / 완료 메뉴 수
        self.no_waiting.setStyleSheet("background-color :" + subway_yellow + ";"
                                     "border-radius : 3px;")

        self.btn_finish = QtWidgets.QPushButton(self.centralwidget)#조리완료
        self.btn_finish.setText("조리 완료")
        self.btn_finish.clicked.connect(self.finish_click)

        self.filter = QComboBox(self.centralwidget)
        self.filter.addItem('조리중')
        self.filter.addItem('조리 완료')
        self.filter.activated[str].connect(self.filterOn)

        df = pd.DataFrame(queue.orders)
        self.table = TableWidget(df)

        self.grid = QtWidgets.QGridLayout(self.centralwidget)
        self.grid.addWidget(self.title, 0, 1, 1, 2)
        self.grid.addWidget(self.no_waiting, 1, 0, 1, 1)
        self.grid.addWidget(self.filter, 1, 2, 1, 1)
        self.grid.addWidget(self.btn_finish, 1, 3, 1, 1)
        self.grid.addWidget(self.table, 2, 0, 1, 4)

        self.setCentralWidget(self.centralwidget)
        self.title.setText("주문 관리")
        self.title.setPixmap(QtGui.QPixmap("./om.png"))
        self.title.setAlignment(Qt.AlignCenter)
        self.no_waiting.setText("주문 대기 메뉴 :" + str(queue.length))

    def setDoneTable(self):#조리 완료 필터 선택시, donelist 출력 화면
        df = pd.DataFrame(done.done)#데이터를 donelist로 변경
        self.table = TableWidget(df)
        self.grid.addWidget(self.table, 2, 0, 1, 4)
        self.no_waiting.setText("조리 완료 메뉴 :" + str(done.length))
        self.grid.addWidget(self.no_waiting, 1, 0, 1, 1)

        self.btn_cancel = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cancel.setText("취소")
        self.grid.addWidget(self.btn_cancel, 1, 3, 1, 1)
        self.btn_cancel.clicked.connect(self.cancel)

        checked.clear()#checked 리스트 초기

    def updateTable(self):#화면 업데이트
        df = pd.DataFrame(queue.orders[queue.front_index:])

        self.table = TableWidget(df)
        self.grid.addWidget(self.table, 2, 0, 1, 4)
        self.table.setSortingEnabled(True)
        self.no_waiting.setText("주문 대기 메뉴 :" + str(queue.length))
        self.grid.addWidget(self.no_waiting, 1, 0, 1, 1)
        self.btn_finish = QtWidgets.QPushButton(self.centralwidget)

        self.btn_finish.setText("조리 완료")
        self.btn_finish.clicked.connect(self.finish_click)
        self.grid.addWidget(self.btn_finish, 1, 3, 1, 1)
        checked.clear()

    def keyPressEvent(self, e):
        queue.enqueue(order_data[0])
        self.updateTable()

    def finish_click(self):
        for i in range(len(checked)):
            x = queue.dequeue()
            done.append(x)
        self.updateTable()

    def filterOn(self, text):#콤보박스 바뀌면 필터를 통해 화면 전환
        if text == '조리 완료':
            self.setDoneTable()
        else:
            self.updateTable()

    def cancel(self):#취소 버튼
        n = len(checked)
        for i in range(n, 0, -1):
            x = done.pop(checked[i - 1])
            queue.return_queue(x)
        self.setDoneTable()

class PandasModel(QtCore.QAbstractTableModel):#매출관리클래스
    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df.copy()

    def toDataFrame(self):
        return self._df.copy()
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):#데이터의 열 관리
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if not index.isValid():
            return QtCore.QVariant()

        return QtCore.QVariant(str(self._df.iloc[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            value = value.toPyObject()
        else:
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)


    def sort(self, column, order):#데이터프레임 정렬
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()

class MaterialQuantityWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MaterialQuantityWindow, self).__init__(parent)
        self.centralwidget = QtWidgets.QWidget(self)#위젯 형태 설정
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.view = QtWidgets.QTableView(self.centralwidget)#데이터프레임 출력할 테이블
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)#직접입력 필터링 박스
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.title = QtWidgets.QLabel(self.centralwidget)

        #필터링 직접입력하는 곳 레이아웃
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label.setText("직접입력 ")
        self.set_material_quantity_dataframe()

        #데이터프레임 열 이름 클릭시 정렬되게 변수기능 추가
        self.comboBox.addItems(["{0}".format(col) for col in self.model._df.columns])#필터링 종류 열 계산
        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)#직접입력칸 인덱스 설정
        self.horizontalHeader = self.view.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)#필터 클릭시 인덱스 출력

    #재고관리 데이터프레임 구하는 함수
    def get_material_cal(self):

        order_data = sale_db  #order_DB의 데이터 복사
        material_quantity_data = []#재료량 추가할 데이터
        filter_quantity_sum = []#재료량 합산

        #빵 재고 계산
        for i in range(len(bread_list)):
            count = 0
            for j in range(len(order_data)):
                if bread_list[i] == bread_list[order_data[j][2]]:
                    count += 1
                    temp_data = ['빵(' + str(bread_list[i]) + ')', order_data[i][0], '1개',
                                 str(bread_stock[i] - count) + '개']
                    material_quantity_data.append(temp_data)
            bread_stock[i] = bread_stock[i] - count
            filter_quantity_sum.append(
                ['빵(' + str(bread_list[i]) + ')', '', "판매량=" + str(count) + '개', '재고량=' + str(bread_stock[i]) + '개'])

        #치즈 재고계산
        for i in range(len(cheese_list)):
            count = 0
            for j in range(len(order_data)):
                if cheese_list[i] == cheese_list[order_data[j][3]]:
                    count += 1
                    temp_data = ['치즈(' + str(cheese_list[i]) + ')', order_data[i][0], '1장',
                                 str(cheese_stock[i] - count) + '장']
                    material_quantity_data.append(temp_data)
            cheese_stock[i] = cheese_stock[i] - count
            filter_quantity_sum.append(
                ['치즈(' + str(cheese_list[i]) + ')', '', "판매량=" + str(count) + '장',
                 '재고량=' + str(cheese_stock[i]) + '장'])  #판매량 및 재고량 리스트에 추가

        #야채재고계산
        for i in range(4, 12):
            count = 0
            for j in range(len(order_data)):
                if order_data[j][i] != 0:
                    temp_data = ['채소(' + str(veg_list[i - 4]) + ')', order_data[j][0],
                                 str(veg_amt_gram[order_data[j][i]]) + 'g',
                                 str(veg_stock[i - 4] - veg_amt_gram[order_data[j][i]]) + 'g']
                    material_quantity_data.append(temp_data)
                    count += veg_amt_gram[order_data[j][i]]
                    veg_stock[i - 4] -= veg_amt_gram[order_data[j][i]]

            filter_quantity_sum.append(['채소(' + str(veg_list[i - 4]) + ')', '', "판매량=" + str(count) + 'g',
                                        '재고량=' + str(veg_stock[i - 4]) + 'g'])  #판매량 및 재고량 리스트에 추가

        #소스재고계산
        for i in range(len(sauce_list)):
            count = 0
            for j in range(len(order_data)):
                for k in range(len(order_data[j][12])):
                    if sauce_list[i] == sauce_list[order_data[j][12][k]]:
                        temp_data = ['소스(' + str(sauce_list[i]) + ')', order_data[j][0], str(sauce_gram) + 'g',
                                     str(sauce_stock[i] - sauce_gram) + 'g']
                        material_quantity_data.append(temp_data)
                        count += sauce_gram
                        sauce_stock[i] -= sauce_gram
            filter_quantity_sum.append(
                ['소스(' + str(sauce_list[i]) + ')', '', "판매량=" + str(count) + 'g',
                 '재고량=' + str(sauce_stock[i]) + 'g'])  #판매량 및 재고량 리스트에 추가

        #각 재고별 판매량 및 재고량 리스트에 추가
        for i in range(len(filter_quantity_sum)):
            material_quantity_data.append(filter_quantity_sum[i])
        df_material_quantity = pd.DataFrame(data=material_quantity_data,
                                            columns=[' 재  료 ( 필  터 ) ', ' 날     짜 ', ' 판   매   량 ',
                                                     ' 재   고   량 '])  #리스트 데이프레임화

        sale_db.clear() #sale_db초기화해준다.
        return df_material_quantity
    
    def set_material_quantity_dataframe(self):#데이터프레임 pyqt에 맞게 변경 및 출력
        df_material_quantity = self.get_material_cal()
        self.model = PandasModel(df_material_quantity)  #데이터프레임을 PandasModel을 통해 pyqt에 적합한 형태로 변환
        self.proxy = QtCore.QSortFilterProxyModel(self)  #필터모델 데이터프레임화
        self.proxy.setSourceModel(self.model)
        self.view.setModel(self.proxy)  #view에 데이터프레임 추가
        self.view.resizeColumnsToContents()

    #필터링에 필요한 검색조건 열들 갯수및 종류 계산 함수
    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):
        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        #필터링 전체 검색 및 slot설정
        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    #필터링 검색을 위한 slot 기능
    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp("",
                                      QtCore.Qt.CaseInsensitive,
                                      QtCore.QRegExp.RegExp
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    #필터링 인덱스 값들 맵핑
    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(stringAction,
                                      QtCore.Qt.CaseSensitive,
                                      QtCore.QRegExp.FixedString
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    #필터링 텍스트 변경가능
    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterRegExp(search)

    #직접입력 콤모박스 열 계산
    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)


class MenuSaleWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MenuSaleWindow, self).__init__(parent)
        self.centralwidget = QtWidgets.QWidget(self)#위젯 형태 설정
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.view = QtWidgets.QTableView(self.centralwidget)#데이터프레임 출력할 테이블
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)#직접입력 필터링 박스
        self.label = QtWidgets.QLabel(self.centralwidget)

        self.set_order_db() #주문데이터 데이터베이스 set

        #탭추가 및 구분
        tabs = QTabWidget()
        tabs.addTab(self.menu_sale_ui(), '메뉴매출')
        tabs.addTab(MaterialQuantityWindow(), '재고관리')
        self.setCentralWidget(tabs)#QMainWindow 추가
        tabs.setStyleSheet(TabStyleSheet)

        self.home = QPushButton(self)
        self.home.setStyleSheet("background-image: url(home_small.png);"
                                "border : 0 ")
        self.home.move(650, 0) 
        self.home.setFixedSize(20, 20)
        self.home.clicked.connect(self.back_home)

    #매출관리 출력을 위한 주문데이터 세팅 수정사항
    def set_order_db(self):
        order_file = open('order_DB.csv', 'r')
        csv_data = csv.reader(order_file)
        for line in csv_data:
            sale_db.append(line)
        #csv 파일을 불러오면 datatype str -> int로 변환
        for i in range(len(sale_db)):
            for j in range(1,len(sale_db[0])):
                if j == 12 or j == 13:
                    str_data = str(sale_db[i][j])
                    int_data = re.findall("\d+", str_data)
                    sale_db[i][j] = int_data
                    for k in range(len(sale_db[i][j])):
                        sale_db[i][j][k] = int(sale_db[i][j][k])
                else:
                    sale_db[i][j] = int(sale_db[i][j])

        order_file.close()

    def back_home(self):#홈버튼
        global current_order
        if (len(current_order) >= 1) or OrderMain.is_login(self) :
            reply = QMessageBox.information(self, '돌아가기', '장바구니 내역이 삭제되고 로그아웃됩니다. 계속하시겠습니까?',
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                current_order = []
                OrderMain._logout(self)
                ex.stk_w.setCurrentWidget(initialize)
            else:
                OrderMain.cancel(self)
        else:
            ex.stk_w.setCurrentWidget(initialize)
    
    def get_menu_sale_data(self):#메뉴매출 데이터프레임 구하는 함수
        order_data = sale_db #order_DB 데이터 복사
        filter_sale_sum = []
        menu_sale_data = [] #메뉴매출을 위한 데이터
        total_count = 0
        total_sale = 0
        date_data = []  #날짜별 매출 계산을 위한 리스트
        
        for i in range(len(order_data)):
            date_data.append(order_data[i][0])#모든 날짜를 모음
        data_set = set(date_data)#집합으로 정의해 중복제거
        date_data = list(data_set)
        date_data.sort()#중복제거한 데이터 다시 시간순으로

        #날짜/메뉴 데이터 숫자데이터를 글자데이터로 변환
        for i in range(len(date_data)):
            temp_sale = 0
            count = 0
            for j in range(len(order_data)):
                if date_data[i] == order_data[j][0]:
                    temp_sale += order_data[j][len(order_data[j]) - 1]#매출액 합산 식, 마지막 인덱스는 매출액
                    temp_data = [order_data[j][0], menu_list[order_data[j][1]][0], bread_list[order_data[j][2]],
                                 cheese_list[order_data[j][3]], set_list[order_data[j][14]],
                                 add_list[order_data[j][13][0]][0],
                                 str(order_data[j][15]) + '원']#매출액 합산 식, 마지막 인덱스는 매출액
                    menu_sale_data.append(temp_data)
                    count += 1
            total_sale += temp_sale
            total_count += count
            filter_sale_sum.append([date_data[i], '', '', '', '', "판매량=" + str(count) + '개',
                                    "매출액=" + str(temp_sale) + '원'])#메뉴별 총 판매량 매출액 데이터
        #메뉴에 따른 판매량 매출액 계산
        for i in range(len(menu_list)):
            temp_sale = 0
            count = 0
            for j in range(len(order_data)):
                if menu_list[i][0] == menu_list[order_data[j][1]][0]:
                    temp_sale += order_data[j][len(order_data[j]) - 1]#매출액 합산 식, 마지막 인덱스는 매출액
                    count += 1

            filter_sale_sum.append(['', menu_list[i][0], '', '', '', "판매량=" + str(count) + '개',
                                    "매출액=" + str(temp_sale) + '원'])#메뉴별 총 판매량 매출액 데이터

        for i in range(len(filter_sale_sum)):
            menu_sale_data.append(filter_sale_sum[i])
        menu_sale_data.append(['', '', '', '', '', "총 판매량=" + str(total_count) + '개', "총 매출액=" + str(total_sale) + '원'])

        df_menu_sale = pd.DataFrame(data=menu_sale_data, columns=['날 짜 (필 터)', '메 뉴(필 터)', '빵', '치 즈', '세 트', '추 가 메 뉴',
                                                                  '매 출 액'])#리스트데이터 데이터프레임으로 변환

        return df_menu_sale

    def menu_sale_ui(self):
        #필터링 직접입력하는 곳 레이아웃
        self.setCentralWidget(self.centralwidget)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.view, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.comboBox, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label.setText("직접입력 ")
        self.set_menu_sale_dataframe()
        #데이터프레임 열 이름 클릭시 정렬되는 함수들
        self.comboBox.addItems(["{0}".format(col) for col in self.model._df.columns])
        self.lineEdit.textChanged.connect(self.on_lineEdit_textChanged)
        self.comboBox.currentIndexChanged.connect(self.on_comboBox_currentIndexChanged)
        self.horizontalHeader = self.view.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)

        menu_sale_tab = QtWidgets.QTableView(self.centralwidget)
        menu_sale_tab.setLayout(self.gridLayout)
        return menu_sale_tab
    
    def set_menu_sale_dataframe(self):#데이터프레임 pyqt에 맞게 변경 및 출력
        df_menu_sale = self.get_menu_sale_data()
        self.model = PandasModel(df_menu_sale)  #데이터프레임을 PandasModel을 통해 pyqt에 적합한 형태로 변환
        self.proxy = QtCore.QSortFilterProxyModel(self)  #필터모델 데이터프레임화
        self.proxy.setSourceModel(self.model)
        self.view.setModel(self.proxy)  #view에 데이터프레임 추가
        self.view.resizeColumnsToContents()

    #필터링에 필요한 검색조건 열들 갯수및 종류 계산 함수
    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):

        self.logicalIndex = logicalIndex
        self.menuValues = QtWidgets.QMenu(self)
        self.signalMapper = QtCore.QSignalMapper(self)
        self.comboBox.blockSignals(True)
        self.comboBox.setCurrentIndex(self.logicalIndex)
        self.comboBox.blockSignals(True)

        valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()

        #필터링 전체 검색 및 slot설정
        actionAll = QtWidgets.QAction("All", self)
        actionAll.triggered.connect(self.on_actionAll_triggered)
        self.menuValues.addAction(actionAll)
        self.menuValues.addSeparator()
        for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
            action = QtWidgets.QAction(actionName, self)
            self.signalMapper.setMapping(action, actionNumber)
            action.triggered.connect(self.signalMapper.map)
            self.menuValues.addAction(action)
        self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
        headerPos = self.view.mapToGlobal(self.horizontalHeader.pos())
        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

        self.menuValues.exec_(QtCore.QPoint(posX, posY))

    #필터링 검색을 위한 slot 기능
    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp("",
                                      QtCore.Qt.CaseInsensitive,
                                      QtCore.QRegExp.RegExp
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    #필터링 인덱스 값들 맵핑
    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(stringAction,
                                      QtCore.Qt.CaseSensitive,
                                      QtCore.QRegExp.FixedString
                                      )

        self.proxy.setFilterRegExp(filterString)
        self.proxy.setFilterKeyColumn(filterColumn)

    #필터링 텍스트 변경가능
    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(text,
                                QtCore.Qt.CaseInsensitive,
                                QtCore.QRegExp.RegExp
                                )

        self.proxy.setFilterRegExp(search)

    #직접입력 콤모박스 열 계산
    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self.proxy.setFilterKeyColumn(index)  #필터 인덱스 세팅



queue = OrderQueue()
done = DoneList()
checked = []
temp = []
ordercount = 0
current_order = []
total_order = []
sale_db = []
id_dic = {}#id DB, 파일 입출력으로 저장
login_id = ''#로그인 된 아이디 저장, 로그인 상태 판별
custom_list = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    initialize = InitialMenu()
    select_menu = ChooseMenu()
    order_confirm = OrderConfirm()
    order_main = OrderMain()
    order_manage = OrderManage()

    ex = MyMain()
    sys.exit(app.exec_())
