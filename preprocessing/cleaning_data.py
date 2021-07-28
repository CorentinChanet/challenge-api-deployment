import joblib
import pandas as pd

fields = joblib.load('/app/model/model_columns.pkl')


def _zip_to_province(item: dict):

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
             ("Coast (West Flanders)", 8000, 8499),
             ("West Flanders", 8500, 8999),
             ("East Flanders", 9000, 9999))

    for _tuple in codes:
        if _tuple[1] <= item['postalCode'] <= _tuple[2]:
            item[_tuple[0]] = 1
            item.pop('postalCode')
            return item
    raise ValueError(f"No Province in Belgium contains the following postal code: {item['postalCode']}")

def _vectorize(item: dict):
    df = pd.DataFrame(item, index=[0], columns=fields).fillna(0)
    df.replace(to_replace='Yes', value=1, inplace=True)
    df.replace(to_replace='No', value=0, inplace=True)
    df[item['subtype']] = 1
    return df

def preprocess(item: dict):
    item =_zip_to_province(item)
    item = _vectorize(item)
    return item
