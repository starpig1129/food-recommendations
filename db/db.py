from sqlalchemy import create_engine, select, update
from sqlalchemy.engine import Row
from sqlalchemy.orm import Session
from db.tables import *

URI = "sqlite:///database.sqlite"

class DB:
    def __init__(self) -> None:
        # 創建一個數據庫引擎，URI定義了數據庫的位置和類型
        self.engine = create_engine(URI, echo=True, future=True)
        # 在數據庫中創建表格，如果表格已存在則不會重複創建
        Base.metadata.create_all(self.engine)

    def getKeywords(self) -> list:
        # 定義查詢：選擇關鍵詞字段
        getCommand = select(Keywords.keyword)
        print(getCommand)

        with Session(self.engine) as session:
            result = session.execute(getCommand)
            # 提取查詢結果，以列表形式返回
            keywords_list = result.all()
            
        return keywords_list

    def checkKeyword(self, keyword: str):
        # 定義查詢：檢查某個關鍵詞是否存在
        getCommand = select(Keywords).where(Keywords.keyword == keyword)

        with Session(self.engine) as session:
            result = session.execute(getCommand)
            result_list = result.all()
        
        return result_list

    def storeKeyword(self, keyword: str) -> None:
        # 創建一個新的關鍵詞對象
        keyword_data = Keywords(keyword=keyword)

        with Session(self.engine) as session:
            # 新增關鍵詞到數據庫並提交
            session.add(keyword_data)
            session.commit()

    # 下列函數為未實現功能的占位符
    def storeModel(self):
        pass

    def getModelFromUser(self):
        pass

    def storeSearchRecord(self, discord_id: str, title: str, keyword: str, map_rate: str, tag: str, map_address: str) -> int:
        # 創建一個新的搜索紀錄對象
        searchRecord = SearchRecord(discord_id=discord_id, title=title, keyword=keyword, map_rate=map_rate, tag=tag, address=map_address, self_rate=0.5)

        with Session(self.engine) as session:
            # 新增搜索紀錄到數據庫並提交
            session.add(searchRecord)
            session.commit()
            return searchRecord.id

    def getSearchRecords(self, discord_id: str) -> list:
        # 定義查詢：選擇特定使用者的搜索紀錄
        getCommand = select(SearchRecord).where(SearchRecord.discord_id == discord_id)

        with Session(self.engine) as session:
            searchRecords = session.execute(getCommand)
            searchRecords_all = searchRecords.all()

        return searchRecords_all

    def updateRecordRate(self, id: int, new_rate: float) -> bool:
        with Session(self.engine) as session:
            # 通過ID查找特定的搜索紀錄
            record: SearchRecord = session.get(SearchRecord, id)
            
            print(f"Debug: record: {record}")

            # 如果未找到記錄，返回 False
            if record is None:
                return False 

            # 更新該記錄的評價並提交
            record.self_rate = new_rate
            session.commit()

            return True
