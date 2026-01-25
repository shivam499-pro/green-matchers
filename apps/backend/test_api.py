import requests 
import json 
 
# Test job search 
print('Testing job search...') 
response = requests.get('http://127.0.0.1:8000/api/jobs/search?query=solar+engineer') 
print(f'Status: {response.status_code}') 
print(f'Response: {response.text}') 
 
# Test career recommendations 
print('Testing career recommendations...') 
response = requests.get('http://127.0.0.1:8000/api/career/recommendations?skills=python,renewable+energy') 
print(f'Status: {response.status_code}') 
print(f'Response: {response.text}') 
