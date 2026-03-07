import requests

def search_around():
    url ="https://restapi.amap.com/v3/place/around"
    params = {
        'key': '859d19a94623ed25910d4a82df350c9f',
        'location': "108.65252,34.25134",
        'radius': 100000,
        'keywords': '星巴克',
        'city': '西安',
        'extensions': 'all',
        'page': 1,
        'offset': 10
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == '1':
                pois = data['pois']
                for poi in pois:
                    print(f"名称: {poi['name']}，地址:{poi['address']}，距离:{poi['distance']}米")
            else:
                print(f"请求失败，原因:{data['info']}")
        else:
            print(f"请求失败，状态码:{response.status_code}")
    except requests.RequestException as e:
        print(f"请求发生异常:{e}")

if __name__ == "__main__":
    search_around()