from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.t_categories import TCategories
from database.t_items import TItems
from common import get_config

db_session = None
def get_database_session(enable_echo = False):
    global db_session
    if not db_session:
        config = get_config()
        db_url = 'sqlite:///%s' % config.get_database_name()
        db_engine = create_engine(db_url, echo = enable_echo)
        #创建表
        TCategories.metadata.create_all(db_engine)
        TItems.metadata.create_all(db_engine)
        Session = sessionmaker(bind = db_engine)
        db_session = Session()
    return db_session
        


