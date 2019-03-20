import requests
import json


class DanKe(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Cookie': 'UM_distinctid=167a1df2bd6310-090a6e7914ba9b-3a3a5d0c-100200-167a1df2bd7c81; TY_SESSION_ID=f7b0cde4-6501-46d8-8388-9302b0913870; Hm_lvt_814ef98ed9fc41dfe57d70d8a496561d=1544609017,1544790353,1544849351; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218839132591%22%2C%22%24device_id%22%3A%22167a1df2b9a190-0b0b9d741db65a-3a3a5d0c-1049088-167a1df2b9b499%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22platformType%22%3A%22M%22%2C%22pid%22%3A%22dankegongyu_customer%22%2C%22cid%22%3A%22bj%22%2C%22ucid%22%3A%22%22%2C%22uuid%22%3A%22%22%2C%22ssid%22%3A%22%22%2C%22lmei%22%3A%22%22%2C%22android_id%22%3A%22%22%2C%22idfa%22%3A%22%22%2C%22idfv%22%3A%22%22%2C%22mac_id%22%3A%22%22%7D%2C%22first_id%22%3A%22167a1df2b9a190-0b0b9d741db65a-3a3a5d0c-1049088-167a1df2b9b499%22%7D; externalHouseRecorderBankClose=true; CNZZDATA1271579284=2008552206-1544608853-%7C1544859121; Hm_lpvt_814ef98ed9fc41dfe57d70d8a496561d=1544863225; externalHouseRecorderPassengerClose=true; XSRF-TOKEN=eyJpdiI6IjRpaEZCS2lqREVKa1ZmT3JqN212anc9PSIsInZhbHVlIjoiM1ZLcmF2YytGQ0tvQ0hTaTlXZUZmSHpEbGtkZE95aVZSU1Z4RXhlaFBoR0F3UGpIK0NQOGU5UkpzMVJvdExtdTFUc0pVN1hWTGR0UmR3XC9wdHgzZ2dnPT0iLCJtYWMiOiJiNzEwY2ZhNzYyYjRkZDFiMTY4Y2E4OGY5NTg4N2MzNzk5ZWZiYTc1YTc0YWY0ODQ0MWQwZWE0Y2UyYTY2ZTQ2In0%3D; session=eyJpdiI6IlNnKzlhc1JuRVB1OXJJQlpWRmdMQUE9PSIsInZhbHVlIjoic1lYNGJIOGtHUExKSElEVTFRbloyeTY3aFhWazB0Q1dzZFE5QkFZbXFsdUo0ZUpHWjQ0RWFHMmxBaXQ0SjJva0l5ZXllcnRkT0xkRHZrYTJ5M0NJVWc9PSIsIm1hYyI6IjgyNTVlNjljZDBkNmI3ZTVkM2RmY2JhYmFjZjNkOTZhZWI1MmQxMThkYWYyMGZlYTVhODQ3YzU2OGY3YjI1MWQifQ%3D%3D; QINGCLOUDELB=91ae0dd9dfb0ce4e00b126ce03c3f9843f15cc784e02bc16683e0f9d6dfb723d|XBS+T|XBS3x'
        }
        self.csrf_token = 'EwjAEOgiY5aU5UlYY373lHHHyw1tCMuwgqE6HG1z'

    def check_phone(self, phone):
        headers = self.headers
        headers['X-CSRF-TOKEN'] = self.csrf_token
        url = 'https://www.dankegongyu.com/u/house-resource/check-phone'
        data = {'phoneNum': phone}
        response = requests.post(url, data=data, headers=headers)
        return response.content.decode() == '' or 'false' in response.content.decode()
        # 失败{"msg": null, "success": true, "data": null}
        # ''

    def get_data(self, city, xiaoqu, phone, doorplate):
        url = 'https://www.dankegongyu.com/u/house-resource/auto-xiaoqu-name?city={}&q={}'.format(city, xiaoqu)
        response = requests.get(url, headers=self.headers)
        # print(response.content.decode())
        if len(json.loads(response.content.decode())) == 0:
            return None
        xiaoqu_id = json.loads(response.content.decode())[0]['id']

        data = {
            '_token': self.csrf_token,
            'city': city,
            'xiaoqu_id': xiaoqu_id,
            'doorplate': doorplate,
            'landlord_phone': phone,
            'landlord_name': '',
            'record_bedroom_num': '',
            'record_keting_num': '',
            'record_toilet_num': '',
            'record_area': '',
            'recorder_note': '',
        }
        return data

    def insert(self, data):
        response = requests.post('https://www.dankegongyu.com/u/house-resource/insert', data=data, headers=self.headers)
        if '已提交' in response.content.decode():
            return True
        else:
            return False

    def run(self, item):
        city, xiaoqu, phone, doorplate = item['city'], item['xiaoqu'], item['phone'], item['doorplate']
        if not self.check_phone(phone):
            print('号码校验失败')
            return
        if not self.get_data(city, xiaoqu, phone, doorplate):
            print('小区不符合')
            return
        else:
            data = self.get_data(city, xiaoqu, phone, doorplate)
        if self.insert(data):
            print('导入成功')
        else:
            print('导入失败')

