from sklearn.cluster import KMeans
import pandas as pd
import json
import ast
import numpy as np
# читаем датафрейм с тренировочной датой
df = pd.read_csv('dfs[0]_map.csv')
#%%
cte_df = pd.read_excel("СТЕ.xlsx")
contract_df = pd.read_excel("Контракты.xlsx")

# %%
def get_products(_id):
    cluster = df.loc[df['Id'] == _id]['cluster']
    cluster.item()
    categories = df.loc[df['Id'] == _id]['top_categories']
    return ast.literal_eval(categories.item())


list_categories = get_products(7709043455)

def get_ids(cat):
    selected = cte_df.loc[cte_df['Код КПГЗ'] == cat]
    return list(selected['ID СТЕ'].values)

#%%
get_ids('01.20.03.04.04.01')
#%%
contract_df.columns
#%%
"""
for index, row in contract_df.iterrows():
    contract_df.loc[index, 'cte_id'] = json.loads(contract_df.loc[index].СТЕ)[0]['Id']
"""
#%%
"""
for index, row in contract_df.iterrows():
    js = json.loads(contract_df.loc[index].СТЕ)[0]
    contract_df.loc[index, 'cte_quantity'] = js['Quantity']
    contract_df.loc[index, 'cte_id'] = js['Id']
"""
#%%
contract_df_cte = contract_df['СТЕ'].copy()
contract_df_cte_values = contract_df_cte.values

contract_df_cte_values = [json.loads(val)[0] for val in contract_df_cte_values]
contract_df_cte_values_id = [val['Id'] for val in contract_df_cte_values]
contract_df_cte_values_quantity = [val['Quantity'] for val in contract_df_cte_values]

#%%
contract_df['cte_id'] = contract_df_cte_values_id
#%%
contract_df['cte_quantity'] = contract_df_cte_values_quantity
#%%
contract_df.to_csv('contract_df_map.csv', index=False)

#%%
contract_df = pd.read_csv('contract_df_map.csv')
#%%

def calculate_quantity_of_each_id():
    groupby = contract_df.groupby(['cte_id'])['cte_quantity'].agg('sum')
    return groupby
#%%

calculate_quantity_of_each_id()
#%%
json.loads(contract_df.loc[0].СТЕ)[0]['Id']

#%%


products = get_products(7709043455)
ids = get_ids(products[0])
#%%
all_ids = calculate_quantity_of_each_id()
all_ids['cte_id'] = all_ids.index
print(all_ids)
#%%
len(all_ids)
#%%
all_ids = all_ids[:-1]
#%%
#results = all_ids[all_ids['cte_id'] in ids]
results = all_ids.loc[all_ids['cte_id'].isin(ids)]
#%%
results = results[:-1]
print((results))
#%%
results['cte_id'] = results.index
#%%
results.idxmax()
#%%
new_result = pd.DataFrame({'cte_id':results.index, 'cte_quantity':results.values}).to_dict('records')
#%%
new_result.idmax()
#%%
new_result
#%%
sorted_dict = sorted(new_result, key=lambda k: k['cte_quantity'])
#%%
sorted_dict[-1]['cte_id']
