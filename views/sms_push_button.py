from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon

class SMSPushButton(QPushButton):
    '''
    自定义按钮
    '''
    def __init__(self, text = '', icon = QIcon(), parent = None):
        QPushButton.__init__(self, icon, text, parent)
