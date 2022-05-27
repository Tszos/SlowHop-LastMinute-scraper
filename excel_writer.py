import xlsxwriter
from scrap import scrap_slowhop
from openpyxl import Workbook
from openpyxl.utils import get_column_letter

scrap = scrap_slowhop()
header_list = ['miejsce', 'nazwa', 'opis', 'wielkość', 'nowa cena', 'stara cena', 'oszczędność', 'zameldowanie',
               'wymeldowanie', 'zdjęcie', 'strona']


def create_excel(workbook_name: str, worksheet_name: str, headders_list: list, data: list, thresh=0.5):
    workbook = xlsxwriter.Workbook(workbook_name + '.xlsx')
    worksheet = workbook.add_worksheet(worksheet_name)
    bold = workbook.add_format({'bold': True})
    green_bg = workbook.add_format({'bg_color': '#6AA121', 'border': 1})
    for i, h in enumerate(headders_list):
        worksheet.write(0, i, str(h).capitalize(), bold)

    for index1, e in enumerate(data):
        for index2, h in enumerate(headders_list):
            savings = e.get('oszczędność')
            reference = e.get('stara cena')
            if type(reference) == float:
                threshold = reference * thresh
            if type(savings) == float and type(reference) == float and savings > threshold:
                worksheet.write(index1 + 1, index2, e[h], green_bg)
            else:
                worksheet.write(index1 + 1, index2, e[h])
                worksheet.autofilter('A1')

    workbook.close()


if __name__ == '__main__':
    create_excel('SlowHopeLastMinutes', 'Last_minute', header_list, scrap)

