from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_csv('dfs[3].csv')
df_train = df.drop('Id', inplace=False, axis=1)

num_neighbours = 72
kmeans = KMeans(n_clusters=num_neighbours,
                             random_state=0).fit(df_train)
preds = kmeans.predict(df_train)
df['cluster'] = preds
df_map = df[['Id', 'cluster']].copy()

columns = list(df.columns)
del columns[columns.index('Id')]
clusters = df[columns].copy()

cluster_preference = clusters.groupby(['cluster']).sum()

cluster_dict = cluster_preference.to_dict(orient='records')

tops = []
for i in cluster_dict:
    my_sort = {k: v for k, v in sorted(i.items(), key=lambda item: item[1])}
    my_keys = list(my_sort.keys())
    top_5 = my_keys[-5:]
    tops.append(top_5)

cluster_preference['top_categories'] = tops
df_map['top_categories'] = ''


def get_categories(idx):
    cluster_id = df_map.loc[idx, 'cluster']
    vals = cluster_preference.loc[cluster_id, 'top_categories']
    return vals


for i in range(len(df_map)):
    df_map.loc[i, 'top_categories'] = str(get_categories(i))

df_map.to_csv('dfs[3]_map.csv', index=False)
#%%
df.head()