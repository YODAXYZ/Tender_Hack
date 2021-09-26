import pandas as pd
import ast

cte_df = pd.read_excel("СТЕ.xlsx")
contract_df = pd.read_csv('contract_df_map.csv')
df = pd.read_csv('dfs[0]_map.csv')


# %%

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


# %%

def get_result(_id):
    all_ids = calculate_quantity_of_each_id()
    products = get_products(_id)
    res_pr = []
    for pr in products:
        ids = get_ids(pr)
        results = pd.DataFrame({'cte_id': all_ids.index, 'cte_quantity': all_ids.values})
        results = results.loc[results['cte_id'].isin(ids)]
        new_result = results.to_dict('records')
        sorted_dict = sorted(new_result, key=lambda k: k['cte_quantity'])
        res_pr.append(int(sorted_dict[-1]['cte_id']))
    return res_pr

# %%
result_dt = pd.DataFrame(columns=['id', 'cte'])
result_dt['id'] = contract_df['ИНН заказчика'].unique()
result_dt['cte'] = result_dt['id'].apply(get_result)
# %%
result_dt.to_csv('result_map.csv', index=False)


# %%
def get_name(_id):
    return str([cte_df.loc[cte_df['ID СТЕ'] == _id_cte]['Название СТЕ'].item() for _id_cte in _id])

# %%
result_dt['name'] = result_dt['cte'].apply(get_name)
#%%
result_dt.to_csv('result_map_names.csv', index=False)
#%%
def get_recommendations(ИНН):
    return result_dt.loc[result_dt['id']==ИНН]['name']
#%%
get_recommendations(7732004550)