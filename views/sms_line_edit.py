from PyQt5.QtWidgets import QLineEdit

class SMSLineEdit(QLineEdit):
    '''
    自定义编辑框
    '''
    def __init__(self, parent = None):
        QLineEdit.__init__(self, parent)
        self.setPlaceholderText('请输入关键字...')
