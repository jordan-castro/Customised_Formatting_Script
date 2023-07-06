# """
# Do conversion between file formats using https://cloudconvert.com
# """
import cloudconvert
import requests


def convert_file(input, output):
    with open('api.key', 'r') as key:
        api_key = key.read()
        cloudconvert.configure(api_key=api_key, sandbox=False)

        print(input, output)

        job = cloudconvert.Job.create(payload={
            "tasks": {
                'import-file': {
                    'operation': 'import/upload'
                },
                'docx-to-html': {
                    "operation": "convert",
                    "input_format": input.split('.')[-1],
                    "output_format": output.split('.')[-1],
                    "engine": "office",
                    # "engine": "libreoffice",
                    "input": [
                        "import-file"
                    ],
                    "filename": output
                },
                "export-file": {
                    "operation": "export/url",
                    "input": [
                        "docx-to-html"
                    ],
                    "inline": False,
                    "archive_multiple_files": False
                }
            }
        })

        # print(job)
        # Some error handling
        if job == None:
            exit('149811x2')

        # Upload the file to convert
        upload_task_data = job['tasks'][0]
        upload_task = cloudconvert.Task.find(id=upload_task_data['id'])
        res = cloudconvert.Task.upload(file_name=input, task=upload_task)
        res = cloudconvert.Task.find(id=upload_task_data['id'])

        # Get the exported result and download it
        export_data = job['tasks'][2]
        export_task = cloudconvert.Task.wait(id=export_data['id'])
        file = export_task.get("result").get("files")[0]
        # Get the url
        response = requests.get(file['url'])
        if response.status_code == 200:
            with open(file['filename'], 'wb') as cf:
                cf.write(response.content)
            return True
        else:
            return False
        

if __name__ == "__main__":
    # Test
    print("Testing conversion from .docx to .html and vice versa")
    docx_to_html = convert_file('test/Text_to_Format.docx', 'conversion_test.html')
    # if result:
    # and vice versa
    html_to_docx = convert_file('conversion_test.html', 'conversion_test.docx')