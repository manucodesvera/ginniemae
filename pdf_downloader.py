import json
import random
import time

import requests

servers = [
    "https://filetools11.pdf24.org/client.php",
    "https://filetools17.pdf24.org/client.php",
    "https://filetools19.pdf24.org/client.php",
    "https://filetools20.pdf24.org/client.php",
    "https://filetools14.pdf24.org/client.php"
]


class TestExtracter:
    def get_random_servers(self):
        """
        get the random proxi from the list ips.
        Returns:
                proxi
        """
        return random.choice(servers)

    def create_text_file(self, pdf_file, count, new_text_folder):
        retry = 0
        file_path = f"{new_text_folder}/textfile{count}.txt"
        content = self.pdf_download_request(pdf_file, self.get_random_servers())
        if content:
            with open(file_path, 'wb') as file:
                file.write(content)
            return file_path
        else:
            if retry > 3:
                print("=====================SOMETHING WENT WRONG===========================")
                return None
            else:
                self.create_text_file(pdf_file, count, new_text_folder)
                retry += 1


    def file_upload_request(self, pdf_file,server):
        params = {
            'action': 'upload',
        }

        filedata = {
            'file': open(f'{pdf_file}', 'rb')
        }

        response = requests.post(f'{server}', params=params, files=filedata)

        data = response.json()
        return data


    def pdf_convert_request(self,pdf_file,server):
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json; charset=UTF-8',
            'Origin': 'https://tools.pdf24.org',
            'Referer': 'https://tools.pdf24.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }

        params = {
            'action': 'convertPdfTo',
        }

        data = self.file_upload_request(pdf_file,server)

        json_data = {
            'files': [
                {
                    'file': f'{data[0]["file"]}',
                    'size': data[0]['size'],
                    'name': f'{data[0]["name"]}',
                    'ctime': f'{data[0]["ctime"]}',
                    'host': f'{data[0]["host"]}',
                },
            ],
            'outputFileType': 'txt',
        }

        response = requests.post(f'{server}', params=params, headers=headers, json=json_data)

        json_data = response.json()

        return json_data



    def pdf_download_request(self, pdf_file,server):

        cookies = {
            '_ga': 'GA1.1.1647596621.1700544196',
            '__gads': 'ID=daf152396cd20381:T=1700544196:RT=1700560948:S=ALNI_MZCABeP7GFKQJTIAs4A_eho8mYUfQ',
            '__gpi': 'UID=00000c9043d849cf:T=1700544196:RT=1700560948:S=ALNI_MbjfdEA0odiKpWAfoUVFf6lsTCMxQ',
            '_ga_J5BFLTV8SB': 'GS1.1.1700560946.5.1.1700561026.49.0.0',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga=GA1.1.1647596621.1700544196; __gads=ID=daf152396cd20381:T=1700544196:RT=1700560948:S=ALNI_MZCABeP7GFKQJTIAs4A_eho8mYUfQ; __gpi=UID=00000c9043d849cf:T=1700544196:RT=1700560948:S=ALNI_MbjfdEA0odiKpWAfoUVFf6lsTCMxQ; _ga_J5BFLTV8SB=GS1.1.1700560946.5.1.1700561026.49.0.0',
            'Referer': 'https://tools.pdf24.org/',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
        }
        jobId = self.pdf_convert_request(pdf_file,server)
        time.sleep(5)
        params = {
            'mode': 'download',
            'action': 'downloadJobResult',
            'jobId': jobId['jobId'],
        }

        response = requests.get(f'{server}', params=params, cookies=cookies, headers=headers)
        if response.status_code == 200:
            return response.content


