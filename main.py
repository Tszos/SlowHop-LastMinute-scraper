from src.config import EXCEL_HEADER_LIST
from src.excel_writer import create_excel
from src.scrap import scrap_slowhop

if __name__ == '__main__':
    create_excel('SlowHopeLastMinutes', 'Last_minute', EXCEL_HEADER_LIST, scrap_slowhop())