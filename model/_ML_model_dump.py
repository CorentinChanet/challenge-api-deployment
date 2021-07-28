import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RepeatedKFold

df = pd.read_csv("../static/raw_data.csv", index_col="Unnamed: 0")

for column in df.columns.to_list():
    df[column] = df[column].apply(lambda x:int(eval(str(x))) if x in ['True', 'False', True, False] else x)

df.drop(df[df.subtype.isin(['APARTMENT_BLOCK', 'APARTMENT_GROUP', 'HOUSE_GROUP'])].index, axis=0, inplace=True)

df.loc[df.kitchen.isin(['USA_SEMI_EQUIPPED', 'USA_UNINSTALLED']), 'kitchen'] = 0
df.rename(columns={'kitchen':'full_kitchen'}, inplace=True)

features = ['type', 'subtype', 'price', 'postalCode', 'condition', 'bedroomCount', 'netHabitableSurface']
df.drop_duplicates(subset=features, inplace=True)

df.dropna(subset=['price', 'netHabitableSurface', 'full_kitchen', 'condition'], inplace=True)

for column in ['hasTerrace','hasGarden', 'hasSwimmingPool']:
    df[column].fillna(0, inplace=True)

df = df.astype({'hasTerrace': int, 'hasGarden': int, 'full_kitchen': int})

codes = (("Brussels Capital Region", 1000, 1299),
          ("Walloon Brabant", 1300, 1499),
          ("Flemish Brabant", 1500, 1999),
          ("Antwerp", 2000, 2999),
          ("Flemish Brabant", 3000, 3499),
          ("Limburg", 3500, 3999),
          ("Liege", 4000, 4999),
          ("Namur", 5000, 5999),
          ("Hainaut", 6000, 6599),
          ("Luxembourg", 6600, 6999),
          ("Hainaut", 7000, 7999),
          ("Coast (West Flanders)", 8000,8499),
          ("West Flanders", 8500, 8999),
          ("East Flanders", 9000, 9999))


def find_province(postalCode):
    for _tuple in codes:
        if _tuple[1] <= postalCode <= _tuple[2]:
            return _tuple[0]
    return np.nan


province = df.postalCode.apply(find_province)
df['province'] = province

condition_binary = {'GOOD': 1, 'AS_NEW':1, 'TO_BE_DONE_UP':0, 'TO_RENOVATE':0, 'JUST_RENOVATED':1, 'TO_RESTORE':0}
df.condition = df.condition.apply(lambda x:condition_binary[x])

df.drop(['postalCode', 'locality', 'fireplaceExists', 'terraceSurface', 'gardenSurface', "isFurnished", 'facadeCount'], axis=1, inplace=True)

subtypes = pd.get_dummies(df.subtype, drop_first=False)
df.drop(['subtype', 'type'], axis=1, inplace=True)

provinces = pd.get_dummies(df.province, drop_first=False)
df.drop(['province'], axis=1, inplace=True)

df = pd.concat([df, subtypes, provinces], axis=1)

df = df.sort_values('price').iloc[9:-10,:]

target = np.log(np.array(df.price))
data = df.drop('price', axis=1)

estimator = RandomForestRegressor(random_state=0)
Kfolds = RepeatedKFold(n_splits=10, n_repeats=1, random_state=21)
params = {
    'min_samples_split': [2,4,6,8,10,12,14,16,18,20,25],
    'max_features': ['log2', 'auto', 'sqrt']
}


X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=0)
X_train = np.array(X_train)
X_test = np.array(X_test)

model = GridSearchCV(estimator, param_grid=params, cv=Kfolds, scoring='r2', n_jobs=-1, verbose=1).fit(X_train, y_train)

joblib.dump(model, 'model.pkl')

model_columns = list(data.columns)
joblib.dump(model_columns, 'model_columns.pkl')