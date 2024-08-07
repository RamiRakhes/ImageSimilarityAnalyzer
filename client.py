import requests

def upload_image(file_path):
    url = "http://127.0.0.1:5001/api/search"
    files = {'file': open(file_path, 'rb')}
    data = {'top_k': 10}
    response = requests.post(url, files=files, data=data)
    print(response.json())

if __name__ == "__main__":
    upload_image('test.jpg')
