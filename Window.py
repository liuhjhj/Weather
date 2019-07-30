# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import Get_City
import re
import html_parser


class get_city(QThread):    # 调用子线程获取城市列表及链接
    add_city_name = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(get_city, self).__init__(parent)
        self.url = 'https://www.tianqi.com/chinacity.html'

    def run(self):
        cities = Get_City.paser_page(self.url)
        for city in cities:
            a = re.compile(r'/.*?/">')
            b = re.compile(r'[\u4E00-\u9FA5]+')
            city_ = re.findall(a, city)
            city_name = re.findall(b, city)
            self.add_city_name.emit(''.join(city_)[0:-2], ''.join(city_name))


class get_weather(QThread):  # 调用子线程爬取天气信息
    weather_signal = pyqtSignal(dict)

    def __init__(self, name, parent=None):
        super(get_weather, self).__init__(parent)
        self.url = 'https://www.tianqi.com' + name

    def run(self):
        text = Get_City.get_page(self.url)
        if text == 'Error' or text is None:
            return
        weather_data = html_parser.parser(text.encode('UTF-8'))
        if weather_data is None or len(weather_data) == 0:
            return
        self.weather_signal.emit(weather_data)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap("b0.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.city = {}
        self.city['请选择城市'] = '请输入城市'
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(MainWindow)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.choos_city_label = QtWidgets.QLabel(MainWindow)
        self.choos_city_label.setObjectName("choos_city_label")
        self.horizontalLayout.addWidget(self.choos_city_label)
        self.comboBox = QtWidgets.QComboBox(MainWindow)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.currentTextChanged.connect(self.show_infor)
        self.horizontalLayout.addWidget(self.comboBox)
        self.query_btn = QtWidgets.QPushButton(MainWindow)
        self.query_btn.setObjectName("query_btn")
        self.horizontalLayout.addWidget(self.query_btn)
        self.exit_btn = QtWidgets.QPushButton(MainWindow)
        self.exit_btn.setObjectName("exit_btn")
        self.horizontalLayout.addWidget(self.exit_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.weather_infor_listWidget = QtWidgets.QListWidget(MainWindow)
        self.weather_infor_listWidget.setObjectName("weather_imfor_listWidget")
        self.verticalLayout.addWidget(self.weather_infor_listWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.query_btn.clicked.connect(self.query_weather)
        self.retranslateUi(MainWindow)
        self.exit_btn.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "今日天气查询"))
        self.choos_city_label.setText(_translate("MainWindow", "选择城市:"))
        self.query_btn.setText(_translate("MainWindow", "获取城市列表"))
        self.exit_btn.setText(_translate("MainWindow", "退出"))
        self.comboBox.addItem('请选择城市')

    def query_weather(self):  # 获取城市列表(与按钮绑定)
        self.thread = get_city()
        self.thread.add_city_name.connect(self.add)
        self.thread.start()
        self.query_btn.setEnabled(False)

    # 为combobox添加项目及设置数据集合将城市与对应的拼音对应(与get_city.add_city_name信号绑定)
    def add(self, pinyin, name):
        self.comboBox.addItem(name)
        self.city[name] = pinyin

    def show_infor(self):  # 显示天气信息(与combobox绑定)
        if self.comboBox.currentText() != '请选择城市':
            self.weather_infor_listWidget.clear()
            self.show_thread = get_weather(
                self.city[self.comboBox.currentText()])
            self.show_thread.weather_signal.connect(self.add_infor)
            self.show_thread.start()

    def add_infor(self, weather_data):  # 添加天气条目(与get_weather.weather_signal绑定)
        if self.comboBox.currentText() != '请选择城市':
            self.weather_infor_listWidget.addItem(self.comboBox.currentText())
            self.weather_infor_listWidget.addItem(weather_data['tem'])
            self.weather_infor_listWidget.addItem(weather_data['air'])
            self.weather_infor_listWidget.addItem(weather_data['humidity'])
            self.weather_infor_listWidget.addItem(weather_data['day'])


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

#
'''
在https://www.tianqi.com/chinacity.html获取城市列表及对应链接
具体天气信息网址:https://www.tianqi.com/lanzhou/(兰州的天气)
一次查询天气的过程为:
点击按钮执行
query_weather获取城市列表
调用
get_city()子线程(获取城市列表和链接)
通过信号槽调用
self.add()将城市名字和拼音相对应
再点击combobox中的item
调用
self.show_infor()
开启
get_weather()子线程(解析出天气信息)
通过信号槽调用
self.add_infor()展示解析到的天气信息
一次查询过程执行完毕
'''