from sklearn.cluster import KMeans
import pandas as pd

# читаем датафрейм с тренировочной датой
df = pd.read_csv('dfs[3].csv')
# убираем айди из признаков
df_train = df.drop('Id', inplace=False, axis=1)

# выбрали кол-во кластеров как корень из кол-ва уникальных
num_neighbours = 72
# запускаем KMeans с тренировкой
kmeans = KMeans(n_clusters=num_neighbours,
                random_state=0).fit(df_train)
# получаем предикты для каждой строки (каждого инн)
preds = kmeans.predict(df_train)
# добавляем колонку кластер
df['cluster'] = preds
# создаём мапу между инн и его кластером
df_map = df[['Id', 'cluster']].copy()

# получаем названия колонок от датасета для тренировки
columns = list(df.columns)
# удаляем оттуда айди чтобы не мешало groupby
del columns[columns.index('Id')]
# получаем датафрейм только с нужными колонками
clusters = df[columns].copy()

# получаем суммарное кол-во покупок внутри каждой категории по кластерам
cluster_preference = clusters.groupby(['cluster']).sum()

# преобразуем датафрейм в словарь
cluster_dict = cluster_preference.to_dict(orient='records')

# инициализируем список для хранения топов по каждому кластеру
tops = []
# сортируем словарь по кол-ву покупок (каждую строку датафрейма, итерируя)
for i in cluster_dict:
    my_sort = {k: v for k, v in sorted(i.items(), key=lambda item: item[1])}
    # берём все ключи
    my_keys = list(my_sort.keys())
    # забираем топ 5 оттуда по макс кол-ву
    top_5 = my_keys[-5:]
    # кладём их в список для хранения топов
    tops.append(top_5)

# добавляем в датафрейм кластеров и его категорий топ категории для каждого
cluster_preference['top_categories'] = tops
# создаем пустую колонку с топами категорий для юзеров
df_map['top_categories'] = ''


def get_categories(idx):
    """
    По индексу датафрейма мапа, получаем его кластер
    по кластеру смотрим топ категорий и возвращаем их
    :param idx: int
    :return: list
    """
    cluster_id = df_map.loc[idx, 'cluster']
    vals = cluster_preference.loc[cluster_id, 'top_categories']
    return vals


# для каждого индекса в датафрейма мапа записываем в колонку топ категорий его кластера
for i in range(len(df_map)):
    df_map.loc[i, 'top_categories'] = str(get_categories(i))

# сохраняем получившийся файл мапа в csv
df_map.to_csv('dfs[3]_map.csv', index=False)
