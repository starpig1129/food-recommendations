import datetime
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserPref(Base):
    __tablename__ = "user_pref"  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵，自動增長
    discord_id = Column(String)  # Discord 用戶ID
    model_uri = Column(String)  # 模型URI，應存儲URI
    last_update = Column(String)  # 最後更新時間，應考慮使用日期時間型態

class SearchRecord(Base):
    __tablename__ = "search_record"  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵，自動增長
    date = Column(String)  # 搜索日期，應考慮使用日期時間型態
    discord_id = Column(String)  # Discord 用戶ID
    title = Column(String)  # 搜索標題
    tag = Column(String)  # 搜索標籤
    address = Column(String)  # 搜索位置
    keyword = Column(String)  # 搜索關鍵詞
    map_rate = Column(String)  # 地圖評價，若為數字應考慮使用數值型態
    self_rate = Column(Float)  # 自我評價

    def __init__(self, discord_id:str, title:str, keyword:str, tag:str, address:str, map_rate:str, self_rate:float):
        self.discord_id = discord_id
        self.keyword = keyword
        self.title = title
        self.tag = tag
        self.address = address
        self.map_rate = map_rate
        self.self_rate = self_rate
        self.date = str(datetime.datetime.now().timestamp())  # 建立日期時間戳

class Keywords(Base):
    __tablename__ = "keywords"  # 表名
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主鍵，自動增長
    keyword = Column(String)  # 關鍵詞
    add_date = Column(String)  # 添加日期，應考慮使用日期時間型態

    def __init__(self, keyword:str):
        self.keyword = keyword
        self.add_date = str(datetime.datetime.now().timestamp())  # 建立日期時間戳
