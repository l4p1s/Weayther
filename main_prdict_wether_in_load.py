import wether_api , Reverse_Geo_api , get_locations_information_api

# 出発地点と目的地を設定する
from_ = input("出発地点を入力してください   >>>>   ")
print("\n")
To_ = input("到着地点を入力してください   >>>   ")
print("\n")
per_time=10
all_loc_list_=get_locations_information_api.get_to_locations_info(from_ , To_)
for i_ in all_loc_list_:
    Reverse_Geo_api.return_locate_to_adress(i_[1] , i_[2])
    wether_api.predict_wether(i_[1], i_[2],i_[0])
    print("\n")

