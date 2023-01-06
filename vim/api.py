import requests
import base64
url = "http://frappe.local:8000**/api/method/frappe.auth.get_logged_user**"
headers = {
    'Authorization': "token " %base64.b64encode(5b4eac6850857df:33dc9ff5369c457)
}
response = requests.request("GET", url, headers=headers)
