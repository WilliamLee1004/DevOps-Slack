import requests
import json
import bs4

#目標網站
URL = "https://www.darencademy.com/" 
#請求網站
r = requests.get(URL)

# 檢查回應。如果是200則成功請求
# print(r.status_code)
# print(r.elapsed.total_seconds())


# 取出網站「首頁」上的所有文章連結 
# 透過BeautiFul整理且用html.parser解析
root = bs4.BeautifulSoup(r.text,'html.parser')
#找到所有屬性class
ment = root.find_all('div',class_='item_content')

def slack_warning(msg):

    # HTTP POST Request
    s_url = '<webhook url>'

    dict_headers = {'Content-type': 'application/json'}

    dict_payload = {
        "text": msg}
    json_payload = json.dumps(dict_payload)

    rtn = requests.post(s_url, data=json_payload, headers=dict_headers)
    print(rtn.text)

    return None


#一個一個印出要的資料
for title in ment:
    print(title.a.string)  #取得文章標題
    print("https://www.darencademy.com/"+title.a.get("href"))  #取得文章連結
    

    URL = "https://www.darencademy.com/"+title.a.get("href")

    #請求網站
    r = requests.get(URL)

    print(r.status_code)
    print(r.elapsed.total_seconds())

    
    #檢查回應。如果不是200則發出告警
    if r.status_code  != 200:
        slack_warning("HTTP Status 異常!")
        print(r.status_code)
    
    #檢查回應時間。如果超過1秒則發出告警
    elif r.elapsed.total_seconds() > 1:
        slack_warning("回應超過 1 秒!")
        print(r.elapsed.total_seconds())

