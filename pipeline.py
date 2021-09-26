import pandas as pd
import numpy as np
import json

df = pd.read_excel("СТЕ.xlsx")
contract_df = pd.read_excel("Контракты.xlsx")


def get_season(value):
    doy = value.timetuple().tm_yday
    # "day of year" ranges for the northern hemisphere
    spring = range(80, 172)
    summer = range(172, 264)
    fall = range(264, 355)
    # winter = everything else

    if doy in spring:
        season = 'spring'
    elif doy in summer:
        season = 'summer'
    elif doy in fall:
        season = 'fall'
    else:
        season = 'winter'
    return season


contract_df = contract_df[contract_df['Дата заключения контракта'].notna()]
contract_df['season'] = contract_df['Дата заключения контракта'].apply(get_season)

ans = [y for x, y in contract_df.groupby('season', as_index=False)]
#%%
#ans[0].loc[ans[0][0, 'season']]
ans[3].head()
#%%

def get_cte_id(idx):
    js = json.loads(contract_df.loc[idx].СТЕ)[0]
    _id = js['Id']
    if _id is None: return None, None
    quantity = js['Quantity']
    _id = json.loads(contract_df.loc[idx].СТЕ)[0]['Id']
    row = df.loc[df['ID СТЕ'] == _id]
    category = row['Код КПГЗ']
    return category.item(), quantity


categories = df['Код КПГЗ'].unique()
df_new = pd.DataFrame(columns=categories)
ids = contract_df['ИНН заказчика'].unique()
df_new['Id'] = ids
df_new = df_new.fillna(0)

dfs = [df_new.copy(), df_new.copy(), df_new.copy(), df_new.copy()]

for i in range(len(dfs)):

    for index, row in ans[i].iterrows():
        _id = row['ИНН заказчика']
        cat, quan = get_cte_id(index)
        if cat is None or quan is None:
            continue
        idx = int(dfs[i].index[dfs[i]['Id'] == _id].tolist()[0])
        dfs[i].loc[idx, cat] += quan

        if index % 10000 == 0:
            print(index)
    dfs[i].to_csv(f'dfs[{i}].csv', index=False)
#%%
len(ans)