import os
from django.shortcuts import render
from django.views import View
from .script import Scrap
from django.http import JsonResponse
import shutil



class DashBoard(View, Scrap):
    def get(
        self,
        request,
    ):
        return render(request, "index.html")

    def post(self, request):

        month = request.POST.get("month")
        year = request.POST.get("year")
        type = request.POST.get("type")
        file_path = ""
        folder = str(month)+str(year)
        if type == "Pdf":
            file_path = f"media/{folder}/{folder}_balance_summary.pdf"
        elif type == "Excel":
            file_path = f"media/{folder}/{folder}_data.xls"
            print(file_path)

        if os.path.exists(file_path):
            return JsonResponse({'file_path': file_path})

        else:
            datas = self.process_scrap(month, year)
            if datas is not None:
                filtered_data = datas[0]
                excel_folder = datas[3]
                test_folder = datas[1]
                pdf_folder = datas[2]

                if str(type) == "Pdf":
                    print("Generating Balance Summary...\n")
                    pdf = self.pdf_summarizer(filtered_data, month, year, excel_folder)
                    response_data = {'file_path': pdf}
                    shutil.rmtree(test_folder)
                    shutil.rmtree(pdf_folder)
                    print("Balance Summary is Generated...\n")
                    return JsonResponse(response_data)


                elif str(type) == "Excel":
                    print("Generating Excel file...\n")
                    excel = self.json_to_excel_converter(filtered_data, excel_folder, month, year)
                    response_data = {'file_path': excel}
                    shutil.rmtree(test_folder)
                    shutil.rmtree(pdf_folder)
                    print("Excel file Generated...\n")
                    return JsonResponse(response_data)


            else:
                return JsonResponse({"error": True})



