import pandas as pd
import ast


cte_df = pd.read_excel("СТЕ.xlsx")
contract_df = pd.read_csv('contract_df_map.csv')
df = pd.read_csv('dfs[0]_map.csv')

#%%

def get_products(_id):
    cluster = df.loc[df['Id'] == _id]['cluster']
    cluster.item()
    categories = df.loc[df['Id'] == _id]['top_categories']
    return ast.literal_eval(categories.item())


def get_ids(cat):
    selected = cte_df.loc[cte_df['Код КПГЗ'] == cat]
    return list(selected['ID СТЕ'].values)


def calculate_quantity_of_each_id():
    groupby = contract_df.groupby(['cte_id'])['cte_quantity'].agg('sum')
    return groupby

#%%
all_ids = calculate_quantity_of_each_id()
all_ids['cte_id'] = all_ids.index
all_ids = all_ids[:-1]

products = get_products(7709043455)
ids = get_ids(products[0])
#%%
results = all_ids[all_ids['cte_id'] in ids]
#results = all_ids.loc[all_ids['cte_id'].isin(ids)]
#%%
results['cte_id'] = results.index


new_result = pd.DataFrame({'cte_id':results.index, 'cte_quantity':results.values}).to_dict('records')
sorted_dict = sorted(new_result, key=lambda k: k['cte_quantity'])
print(sorted_dict[-1]['cte_id'])
