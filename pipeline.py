import pandas as pd
import json

# Читаем эксель файлы
df = pd.read_excel("СТЕ.xlsx")
contract_df = pd.read_excel("Контракты.xlsx")


def get_season(value):
    """
    parse datetime into season of year
    :param value: datetime
    :return: str
    """
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


# убираем нан строки и добавляем столбец сезон
contract_df = contract_df[contract_df['Дата заключения контракта'].notna()]
contract_df['season'] = contract_df['Дата заключения контракта'].apply(get_season)

# создаём 4 датафрейма для 4 моделей мл
ans = [y for x, y in contract_df.groupby('season', as_index=False)]


def get_cte_id(idx):
    """
    by index of contract dataframe, gets it's CTE
    and finds corresponding category
    also returns it's quantity in contract dataframe
    :param idx: int
    :return: str, int
    """
    js = json.loads(contract_df.loc[idx].СТЕ)[0]
    _id = js['Id']
    if _id is None:
        return None, None
    quantity = js['Quantity']
    _id = json.loads(contract_df.loc[idx].СТЕ)[0]['Id']
    row = df.loc[df['ID СТЕ'] == _id]
    category = row['Код КПГЗ']
    return category.item(), quantity


# находим все уникальные коды КПГЗ, создаем пустой датафрейм с такими колонками
categories = df['Код КПГЗ'].unique()
df_new = pd.DataFrame(columns=categories)
# нахоим все уникальные ИНН заказчика и вставляем эту колонку и пустой датафрейм с ключом Id
ids = contract_df['ИНН заказчика'].unique()
df_new['Id'] = ids
# заменяем все нанки на нули, далее их будем заполнять кол-вом покупок в этой категории
df_new = df_new.fillna(0)

# создаём 4 пустых датафрейма для 4 сезонов года
dfs = [df_new.copy(), df_new.copy(), df_new.copy(), df_new.copy()]


def create_train_datasets():
    """
    Для каждого пустого датафрейма
    итерируем таблицы времён года
    забираем ИНН
    по индексу строки получаем категорию и кол-во в этой строке
    ищем индекс в новом пустом датафрейме с инн как у заказчика
    для этого индекса и этой категории записываем кол-во в данной строке
    :return:
    """
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


# %%
create_train_datasets()
