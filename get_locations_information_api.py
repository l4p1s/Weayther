import googlemaps
import datetime
import re

def get_to_locations_info(from_ , To_):
    # Google Maps PlatformのAPIキーを設定する
    gmaps = googlemaps.Client(key='AIzaSyDUG-TwY1fdbhXZdBgpNLuTcR504mpLTsM')
    # ルートを取得する
    now = datetime.datetime.now()
    directions_result = gmaps.directions(from_, To_, mode="driving", departure_time=now)
    #その他
    all_loc_list=[]
    count_minits=0
    first_flag_=True
    end_flag_=True
    per_time = 10

    # list内のデータ形式は
    # 最初と最後は、[出発時刻 , 出発地点のlat , lng] , [到着時刻 , 到着地点のlat , lng]
    # [天気を取得したい時間 , lat ,lng]
    for i in directions_result[0]['legs']:
        # pprint.pprint(i)
        if first_flag_: #最初の地点の情報を入れる。
            tmp_list=[]
            tmp_list.append(now.strftime("%Y-%m-%d:%H"))
            tmp_list.append(i['start_location']['lat'])
            tmp_list.append(i['start_location']['lng'])
            all_loc_list.append(tmp_list)
            first_flag_=False
        for step in i['steps']:
            duration_text = step['duration']['text']
            duration_text=duration_text.replace(' min', '').replace('s', '')
            duration_text=re.sub(r"\b\d+\s*hour(s)?\b", '', duration_text)
            change_int=int(duration_text)
            count_minits+=change_int
            loc_list=[]
            if(count_minits >= per_time):
                cur_time=now + datetime.timedelta(minutes=count_minits)
                loc_list.append(cur_time.strftime("%Y-%m-%d:%H"))
                loc_list.append(step['end_location']['lat'])
                loc_list.append(step['end_location']['lng'])
                count_minits=count_minits % per_time
                all_loc_list.append(loc_list)
        #最終地点を追加する。すでについかされていないかどうかをifで判定する。
        if (end_flag_ == True) and (first_flag_ == False):
            cur_time=now + datetime.timedelta(minutes=count_minits)
            loc_list.append(cur_time.strftime("%Y-%m-%d:%H"))
        if(all_loc_list[-1][1] != step['end_location']['lat']):
                loc_list.append(step['end_location']['lat'])
                loc_list.append(step['end_location']['lng'])
                all_loc_list.append(loc_list)
    return all_loc_list