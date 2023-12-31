import os
import re
import sys
import time
from excelcreator import Json_To_Excel
from mixins import essential, PdfSummarizer
from pdf_downloader import TestExtracter
from pdf_scraper import get_pdfs

folder = "media"

class Scrap(essential,Json_To_Excel,TestExtracter,PdfSummarizer):



    def process_scrap(self,month,year):
        print("===============================PROCESS STARTED==============================")
        if not os.path.exists(folder):
            # Create the folder
            os.makedirs(folder)
        folder_name = str(month) + str(year)
        new_folder_path = os.path.join(folder, folder_name)

        os.makedirs(new_folder_path, exist_ok=True)

        new_text_folder = os.path.join(new_folder_path, 'text')
        new_pdf_folder = os.path.join(new_folder_path, 'pdf')

        os.makedirs(new_text_folder, exist_ok=True)
        os.makedirs(new_pdf_folder, exist_ok=True)

        filtered_data = []
        context1 = {}
        context2 = {}
        context3 = {}

        pdf_links = get_pdfs(year, month)
        if pdf_links:
            count1 = 0
            print("Started PDFs Downloading...\n")
            for pdf_link in pdf_links:
                count1 += 1
                self.pdf_downloader(pdf_link, count1, new_pdf_folder)

            """ created pdfs """

            print(f"{len(pdf_links)} PDFs Downloaded...\n")
            files = [f for f in os.listdir(new_pdf_folder) if os.path.isfile(os.path.join(new_pdf_folder, f))]
            files.sort(key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])  # Sort files based on numerical suffix


            count2 = 0
            print("Text file conversion Started...\n")
            for pdf_name in files:
                count2 += 1
                pdf_path = os.path.join(new_pdf_folder, pdf_name)
                if os.path.isfile(pdf_path):
                    self.create_text_file(pdf_path, count2, new_text_folder)

            """ text file created """

            print("Text file conversion complete...\n")
            text_files = [f for f in os.listdir(new_text_folder) if os.path.isfile(os.path.join(new_text_folder, f))]
            text_files.sort(key=lambda x: [int(s) if s.isdigit() else s for s in re.split(r'(\d+)', x)])

            li = [[], [], []]
            for text_name in text_files:
                text_path = os.path.join(new_text_folder, text_name)
                if os.path.isfile(text_path):
                    datas = self.text_value_extracter(text_path)
                    time.sleep(2)
                    if datas:
                        li[0].append(datas[0])
                        li[1].append(datas[1])
                        li[2].append(datas[2])

            context1["filtered_data"] = li[0]
            context2["filter_name"] = li[1]
            context3["filter_remic"] = li[2]

            filtered_data.append(context1)
            filtered_data.append(context2)
            filtered_data.append(context3)

            """ extracted values """

            return [filtered_data, new_folder_path]
        else:
            os.rmdir(new_pdf_folder)
            os.rmdir(new_text_folder)
            os. rmdir(new_folder_path)
            os.rmdir(folder)
            sys.exit()







start_time = time.time()
b1 = Scrap()
month = sys.argv[1]
month = month.capitalize()
year = sys.argv[2]
export_type = sys.argv[3]
export_type = export_type.capitalize()
datas = b1.process_scrap(month, year)
filtered_data = datas[0]
excel_folder = datas[1]

if str(export_type) == "Pdf":
    print("Generating Balance Summary...\n")
    b1.pdf_summarizer(filtered_data, month, year, excel_folder)
    print("Balance Summary is Generated...\n")

elif str(export_type) == "Excel":
    print("Generating Excel file...\n")
    b1.json_to_excel_converter(filtered_data, excel_folder, month, year)
    print("Excel file Generated...\n")

else:

    print("================================INVALID FILE FORMAT================")

end_time = time.time()
elapsed_time = end_time - start_time
in_minutes = elapsed_time/60
in_minutes = round(in_minutes, 2)
print("**************************PROCESS COMPLETED*************************")
print(f"Elapsed Time: {in_minutes} minutes")





