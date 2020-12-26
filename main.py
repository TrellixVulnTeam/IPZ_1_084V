from mainUI import *
import sys
import time
from socket import *


#Create UI app
app = QApplication(sys.argv)
Form = QWidget()
ui = Ui_Dialog_start()
ui.setupUi(Form)
Form.show()


#Logic
timenow = ''
startstop = True
status=''

def ErrorShow(error_type, error_code):
    print(error_type,error_code)
    ui.textBrowser_Error.show()
    ui.textBrowser_Error.setText(error_type+str(error_code))

def Login():
    Connect()
    global adminemode
    adminemode = False
    s.send('l'.encode())
    status=s.recv(1).decode()
    if status=='1':
        s.send(ui.lineEdit_user_id.text().encode())
    else:ErrorShow('Connection error','')
    status = s.recv(1).decode()
    if status== '1':
        s.send(ui.lineEdit_password.text().encode())
    status = s.recv(10).decode()
    if status=='1':
        pass
    elif status=='adm':
        adminemode=True

        ui.label_success.setText("Admin mode")
        ui.pushButton_Start.setEnabled(True)
        ui.pushButton_Admin.show()
        ui.pushButton_Admin.setEnabled(True)
        s.close()
        return adminemode
    else:
        ErrorShow('Connection error', '')

    if True:
        ui.pushButton_Start.setEnabled(True)
        ui.label_success.setText("Success")
    else:
        ui.label_success.setText("Unsuccess")

    s.close()

    return adminemode
def Admin_checkDate():
    Connect()
    adminmode
    if adminmode != True:
        return
    QDate = ui.calendarWidget.selectedDate()
    Date = "{0}.{1}.{2}".format(QDate.day(), QDate.month(), QDate.year())
    print("{0}.{1}.{2}".format(QDate.day(), QDate.month(), QDate.year()))

    s.send('a'.encode())
    status = s.recv(1).decode()
    if status == '1':
        s.send(Date.encode())
    else:
        ErrorShow('Connection error', '')
    status = s.recv(1).decode()
    if status == '1':
        pass
    else:
        ErrorShow('Connection error', '')

    s.close()
    return Date
adminmode = ui.pushButton_Login.clicked.connect(Login)
Date = ui.pushButton_Admin.clicked.connect(Admin_checkDate)


def ComeTW():
    Connect()
    global startstop
    qtimenow = QDateTime.currentDateTime()
    timenow=qtimenow.toString('dd.MM.yyyy')
    print(timenow)
    if startstop == True:
        ui.pushButton_Start.setText(QCoreApplication.translate("Dialog_start", u"Завершення роботи", None))
        ui.label_TimeR_St.setText("Розпочато роботу о " + timenow)
    else:
        ui.pushButton_Start.setText(QCoreApplication.translate("Dialog_start", u"\u0417\u0430\u0440\u0435\u0454\u0441\u0442\u0440\u0443\u0432\u0430\u0442\u0438 \u0441\u0442\u0430\u0440\u0442", None))
        ui.label_TimeR_St.setText("Завершено роботу о " + timenow)


    s.send('c'.encode())
    status = s.recv(1).decode()
    if status == '1':
        s.send(timenow.encode())
    else:
        ErrorShow('Connection error', '')
    status = s.recv(1).decode()
    if status == '1':
        startstops = str(int(startstop))
        s.send(startstops.encode())
    else:
        ErrorShow('Connection error', '')
    status = s.recv(1).decode()
    if status == '1':
        timenow_s=str(qtimenow.currentSecsSinceEpoch())
        s.send(timenow_s.encode())
    else:
        ErrorShow('Connection error', '')
    status = s.recv(1).decode()
    if status == '1':
        pass
    else:
        ErrorShow('Connection error', '')



    startstop = not startstop
    s.close()
ui.pushButton_Start.clicked.connect(ComeTW)

#Socket client side


def Connect():
    try:
        global s
        s = socket()
        s.connect(('localhost', 9999))
    except Exception as ex:
        ErrorShow('Conection Eror:\n',ex)
        ui.label_Connection.setText('Conection Error')
        s.close()
    else:
        ui.label_Connection.setText('Conected')






#Run main loop
if __name__ == '__main__':
    sys.exit(app.exec_())