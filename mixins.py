import os
import re
import subprocess
import tempfile
from itertools import groupby
import requests
import xlrd
from bs4 import BeautifulSoup
import xlwt
import pandas as pd
import pdfkit
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class essential:


    def pdftotext(self, pdf_file, count):
        with tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as temp_file:
            try:
                subprocess.call(['pdftotext', '-layout', pdf_file, temp_file.name])

                temp_file.seek(0)
                lines = temp_file.readlines()
                temp_file.seek(0)
                temp_file.writelines(line for line in lines if line.strip())
                temp_file.truncate()

                output_file_path = f"/home/user/pdf_to_text/pdftotext{count}.txt"
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    temp_file.seek(0)
                    output_file.write(temp_file.read())

                return output_file_path

            except Exception as e:
                print(e, "====================================")

    def pdf_downloader(self, url, count, new_pdf_folder):
        url = f"https://www.ginniemae.gov{url}"

        response = requests.get(url)

        if response.status_code == 200:
            pdf_content = response.content

            file_path = f"{new_pdf_folder}/file{count}.pdf"

            with open(file_path, "wb") as pdf_file:
                pdf_file.write(pdf_content)

            return file_path
        else:
            print(f"Failed to download the PDF. Status code: {response.status_code}")

    def text_value_extracter(self,text_file):

        filtered_data = []
        filter_name = []
        filter_remic = []


        content = open(text_file)
        content = content.readlines()

        for index in range(len(content)):

            transaction_details1 = re.compile(
                r'(?P<class_of_remic_securities>[A-Z()\d]+?)\s+\.\ ..*\s+(?P<orginal_principle_balance>\$?\s*[\d,]+)\s+(?P<intrest_rate>[\d,()\.%]+?[()\d]?)\s+(?P<principle_type>[A-Z()/\w]+?)\s+(?P<intrest_type>[A-Z()/\w]+)\s+(?P<cusip_number>\w*)\s+(?P<distribution_date>\w*\s+\d{4})\s*'
            )
            transaction_details2 = re.compile(
                r'(?P<class_of_remic_securities>[A-Z()\d]+?)\s+\.\ ..*\s+(?P<orginal_principle_balance>\$?\s*[\d,]+)\s+(?P<intrest_rate>[()\d]+)\s+(?P<principle_type>[A-Z()/\w]+?)\s+(?P<intrest_type>[A-Z/\w]+?)\s+(?P<cusip_number>\w*)\s+(?P<distribution_date>\w*\s+\d{4})\s*'
            )
            transaction_details3 = re.compile(
                r'(?P<class_of_remic_securities>[A-Z()\d]+?)\s+\.\ ..*\s+(?P<orginal_principle_balance>\$?\s+\d*\s*[\d,]+)\s+(?P<intrest_rate>[()\d]+)\s+(?P<principle_type>[A-Z()/\w]+?)\s+(?P<intrest_type>[A-Z/\w]+?)\s+(?P<cusip_number>\w*)\s+(?P<distribution_date>\w*\s+\d{4})\s*'
            )
            sponsor_name = re.compile(
                r'^Sponsor:(?P<sponsor_name>\s+[\w \. \s \& \,]+)\s*'
            )
            remic_trust = re.compile(
                r'^Ginnie Mae REMIC Trust(?P<remic_trust>\s+[\w \d \- \s]+)\s*'
            )
            txt = content[index]
            match1 = re.search(transaction_details1, txt)
            match2 = re.search(transaction_details2, txt)
            match3 = re.search(sponsor_name, txt)
            match4 = re.search(remic_trust, txt)
            match5 = re.search(transaction_details3, txt)
            if match5:
                filtered_data.append(match5.groupdict())
            elif match1:
                filtered_data.append(match1.groupdict())
            elif match2:
                filtered_data.append(match2.groupdict())
            elif match3:
                filter_name.append(match3.groupdict())
            elif match4:
                if not filter_remic:
                    filter_remic.append(match4.groupdict())

        return [filtered_data, filter_name, filter_remic]


class PdfSummarizer:

    def pdf_summarizer(self, json_data, month, year, excel_folder):
        pdf_path = f"{excel_folder}/{str(month)+str(year)}_summary.pdf"
        principle_types = []
        datas = json_data

        for members in datas[0]["filtered_data"]:
            for member in members:
                if member.get("principle_type"):
                    principle_types.append(member["principle_type"].strip())

        filtered_types = []
        for item in principle_types:
            if item not in filtered_types:
                filtered_types.append(item)

        li = []
        for members in datas[0]["filtered_data"]:
            for member in members:
                if member.get("principle_type").strip() in filtered_types:
                    li.append({f"{member['principle_type']}": member["orginal_principle_balance"]})

        sorted_data = sorted(li, key=lambda x: list(x.keys())[0])

        grouped_data = {key: [d[key] for d in group] for key, group in
                        groupby(sorted_data, key=lambda x: list(x.keys())[0])}





        out_put = []
        count = 0
        for key in grouped_data:
            for data in grouped_data[key]:
                filtered_data = data.replace(",", "")
                filtered_data = filtered_data.replace("$", "")
                filtered_data = filtered_data.replace(" ", "").strip()
                count = int(filtered_data) + count
            formatted_count = "{:,}".format(count)
            out_put.append({f"{key}": formatted_count})
            count = 0

        self.tem_excel_creation(out_put, pdf_path)


    def tem_excel_creation(self,out_put, pdf_path):

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("sheet1")


        headers = ["Print Type", "Balance"]

        style1 = xlwt.easyxf('font:bold 1; align: horiz center;')
        style2 = xlwt.easyxf('align: horiz center, vert center;')


        sheet.row(0).height_mismatch = True  # Enable height mismatch
        sheet.row(0).height = 20 * 20

        row_height_in_points = 20  # Set the desired row height in points
        row_height_in_twips = int(row_height_in_points * 20)



        count = 0
        for head in headers:
            sheet.write(0, count, head, style1)
            sheet.col(count).width = 30 * 256
            count += 1

        position = 1
        for dictionary in out_put:
            for key, value in dictionary.items():
                sheet.write(position, 0, key, style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
                sheet.write(position, 1, value, style2)
                sheet.row(position).height_mismatch = True
                sheet.row(position).height = row_height_in_twips
            position += 1
        workbook.save("data.xlsx")

        self.excel_to_pdf("data.xlsx", pdf_path)

    def excel_to_pdf(self, excel_file, pdf_path):

        df = pd.read_excel(excel_file, header=0)
        # Convert DataFrame to HTML and save it to a file
        df_html = df.to_html(index=False, header=True, classes='table table-striped', justify='center', escape=False, index_names=False)

        # Add a heading to the HTML file
        heading = "<h1 style='background-color: #d3d3d3; text-align: center; font-style: italic;'>Summary</h1>"
        html_content = f"{heading}\n{df_html}"
        print(html_content)

        # Adjust the CSS styles to fill the entire page
        html_content = html_content.replace(
            "<table",
            "<table style='width: 80%; border-collapse: collapse; border: 1px solid black; text-align: center;  margin: auto;'"
        )
        html_content = html_content.replace("<th", "<th style='font-size: 40px; font-weight: bold; background-color: #d3d3d3; font-family: 'Times New Roman';")
        html_content = html_content.replace("<td", "<td style='font-size: 30px;'")


        # Save the modified HTML content back to the file
        with open("file.html", "w") as file:
            file.write(html_content)

        # Convert HTML to PDF using pdfkit with custom options
        options = {
            "page-size": "A4",  # Set the paper size (A4, A3, etc.)
            "margin-top": "0mm",
            "margin-right": "0mm",
            "margin-bottom": "0mm",
            "margin-left": "0mm",
        }

        pdfkit.from_file("file.html", pdf_path, options=options)  # to pdf
        os.remove(excel_file)
        os.remove("file.html")



