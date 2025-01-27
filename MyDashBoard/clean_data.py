import Datas
import pandas as pd
import numpy as np
import re
def clean_map():
    n = 100
    data = Datas.data()
    l_datas = data.add_all_in_folder('data_sum')
    print(l_datas)
    for ii in l_datas:
        print(ii.split('_')[-1])
        if ii.split('_')[-1] != 'contract.csv':
            continue
        df1 = data.read_data(ii)
        df1 = df1.iloc[:,[1,2,10]]
        df1 = df1.dropna()
        size = df1.size
        size = size//n #fast & save ram
        mapping = Datas.cleandata(df1)
        for i in range(n-1):
            dfsub = df1[size*i:size*(i+1)]
            if i == n-2:
                dfsub = df1[size*i:]
            dfsub['subdep_id'] = dfsub['subdep_name'].replace(mapping)
            if not i:
                datass = dfsub
            if i:
                datass =  pd.concat([datass,dfsub],axis=0)
        datass.to_csv(f'use_data/{ii[:-4]}_clean.csv',encoding='utf-8',index=False)
        #datass.to_excel(f'clean_data1/{ii[:-4]}_clean.xlsx',encoding='utf-8',index = False)

def selec_class_T(n):
    mapdata_unique = {}
    data = Datas.data()
    l_data = data.add_all_in_folder('use_data')
    print(l_data)
    for ii in [l_data[3]]:
        df = data.read_data(ii)
        if df.count()["proj_name"] < 50000:
            n = 100
        if df.count()["proj_name"] > 160000:
            n = 300
        for i in df['subdep_id'].unique():
            if (df["subdep_id"] == i).sum() < n:
                df = df[df["subdep_id"] != i]
            else:
                drop_data = df.where(df['subdep_id'] == i).dropna()
                selec = min([len(drop_data.iloc[0]['subdep_name']),len(drop_data.iloc[-1]['subdep_name']),len(drop_data.iloc[-49]['subdep_name'])])
                mapdata_unique[i] = ''.join(np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec]))[(np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec])) == np.array(re.split('',drop_data.iloc[-1]['subdep_name'][:selec]))).tolist() and (np.array(re.split('',drop_data.iloc[0]['subdep_name'][:selec])) == np.array(re.split('',drop_data.iloc[-49]['subdep_name'][:selec]))).tolist()])
                class_name = ["โรงเรียน","กลุ่มงานเภสัชกรรม","กศน.","โรงพยาบาล","การประปาส่วนภูมิภาค","การไฟฟ้าส่วนภูมิภาค","ที่ทำการปกครองอำเภอ","ศูนย์พัฒนาเด็กเล็ก","สำนักงานเขตพื้นที่การศึกษา","องค์การบริหารส่วนตำบล","อุทยานแห่งชาติ","เทศบาลตำบล","สำนักงานสาธารณสุขอำเภอ","สำนักงานสาธารณสุข","เขตรักษาพันธุ์สัตว์ป่า"]
                for name in class_name:
                   if name in mapdata_unique[i]:
                        mapdata_unique[i] = name
     
        print(mapdata_unique)
        df['subdep_class'] = df['subdep_id'].replace(mapdata_unique)
        df.to_csv(f'use_data_by_class_T/{ii}',encoding='utf-8',index=False)

