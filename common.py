import configparser as cp
import os

class Config(object):
    '''
    配置文件读写
    '''
    def __init__(self, path = ''):
        object.__init__(self)
        
        self._config_parser = cp.ConfigParser()
        
        if not path:
            self._path = 'config.ini'
        else:
            self._path = path
        
        if os.path.exists(self._path):
            self._config_parser.read(self._path)
            self._window_title = self._config_parser['window']['title']
            self._window_icon = self._config_parser['window']['icon']
            self._window_is_full_screen = self._config_parser['window']['is_full_screen']
            self._window_width = int(self._config_parser['window']['width'])
            self._window_height = int(self._config_parser['window']['height'])
            self._window_x = int(self._config_parser['window']['x'])
            self._window_y = int(self._config_parser['window']['y'])
            self._database_name = self._config_parser['database']['name']
        else:    
            self._window_title = '出入库管理系统'
            self._window_icon = 'resources/icons/main.png'
            self._window_is_full_screen = 0
            self._window_x = 100
            self._window_y = 100
            self._window_width = 640
            self._window_height = 480
            self._database_name = 'sms.db'
            
    def get_window_title(self):
        return self._window_title
        
    def set_window_title(self, text):
        self._window_title = text
        
    def get_window_icon(self):
        return self._window_icon
        
    def set_window_icon(self, icon):
        self._window_icon = icon
        
    def get_window_is_full_screen(self):
        return int(self._window_is_full_screen)
        
    def set_window_is_full_screen(self, stat):
        self._window_is_full_screen = str(stat)
        
    def get_window_width(self):
        return self._window_width
        
    def set_window_width(self, width):
        self._window_width = width
        
    def get_window_height(self):
        return self._window_height
        
    def set_window_height(self, height):
        self._window_height = height
        
    def get_window_x(self):
        return self._window_x
        
    def set_window_x(self, x):
        self._window_x = x
        
    def get_window_y(self):
        return self._window_y
    
    def set_window_y(self, y):
        self._window_y = y
        
    def get_database_name(self):
        return self._database_name
        
    def set_database_name(self, name):
        self._database_name = name
        
    def update(self):
        self._config_parser['window'] = {}
        self._config_parser['window']['title'] = self._window_title
        self._config_parser['window']['icon'] = self._window_icon
        self._config_parser['window']['is_full_screen'] = self._window_is_full_screen
        self._config_parser['window']['width'] = str(self._window_width)
        self._config_parser['window']['height'] = str(self._window_height)
        self._config_parser['window']['x'] = str(self._window_x)
        self._config_parser['window']['y'] = str(self._window_y)
        self._config_parser['database'] = {}
        self._config_parser['database']['name'] = self._database_name
        with open(self._path, 'w') as config_file:
            self._config_parser.write(config_file)
       
       
#全局配置对象
config = None

#配置对象获取函数
def get_config():
    global config
    if not config:
        config = Config()
    return config
