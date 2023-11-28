import os

import xlwt
from xlrd import open_workbook
from xlutils.copy import copy


class Json_To_Excel:
    def json_to_excel_converter(self, json_data, excel_folder, month, year):
        datas = json_data


        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("sheet1")

        headers = ["Name", "Remic Trust", "Class of remmic Securities", "Orginal Principle Balance", "Interest rate", "Principal Type",
                   "Interest Type", "CUSIP number", "Final Distribution Date"]
        count = 0
        style1 = xlwt.easyxf('font:bold 1; align: horiz center;')
        style2 = xlwt.easyxf('align: horiz center, vert center;')
        style3 = xlwt.easyxf('align: horiz center; align: vertical top;')
        style3.borders.top = 100

        sheet.row(0).height_mismatch = True  # Enable height mismatch
        sheet.row(0).height = 20 * 20

        row_height_in_points = 20  # Set the desired row height in points
        row_height_in_twips = int(row_height_in_points * 20)




        for head in headers:
            sheet.write(0, count, head, style1)
            sheet.col(count).width = 30 * 256
            count += 1


        position1 = 1
        filter_remic = datas[2]["filter_remic"]
        count1 = 0
        data = [item for sublist in filter_remic for item in sublist if item]
        for i in datas[0]["filtered_data"]:
            for j in range(len(i)):
                sheet.write(position1, 1, data[count1].get('remic_trust', ''), style3)
                sheet.row(position1).height_mismatch = True
                sheet.row(position1).height = row_height_in_twips
                position1 += 1
            count1 += 1

        position2 = 1
        filter_name = datas[1]["filter_name"]
        count2 = 0
        data = [item for sublist in filter_name for item in sublist if item]
        for i in datas[0]["filtered_data"]:
            for j in range(len(i)):
                sheet.write(position2, 0, data[count2].get('sponsor_name', ''), style3)
                sheet.row(position2).height_mismatch = True
                sheet.row(position2).height = row_height_in_twips
                position2 += 1
            count2 += 1



        position = 1
        for members in datas[0]["filtered_data"]:
            for member in members:
                sheet.write(position, 2, member.get("class_of_remic_securities", ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 3, member.get('orginal_principle_balance', ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 4, member.get('intrest_rate', ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 5, member.get('principle_type', ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 6, member.get('intrest_type', ''), style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 7, member.get('cusip_number', ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 8, member.get('distribution_date', ''),style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                position += 1
        sheet.col(1).width = 4000
        sheet.col(4).width = 4000
        sheet.col(5).width = 4500
        sheet.col(6).width = 4500
        sheet.col(7).width = 4700
        sheet.col(8).width = 5500
        file_path = f"{excel_folder}/{month + str(year)}_data.xls"
        workbook.save(file_path)
        return file_path