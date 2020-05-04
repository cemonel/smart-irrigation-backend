import time
import datetime

import pandas as pd
from scipy.signal import argrelextrema
import numpy
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline


from django.core.management.base import BaseCommand, CommandError
from smart_irrigation.data.models import Data


def decide_irrigation():
    data = list(Data.objects.all())
    train_data = data[:-150]  # Old data for training
    new_data = data[-150:]  # 150*2 seconds last 5 minutes data
    irrigation_data_ = []
    new_data_ = []

    for datum in train_data:
        date = datetime.datetime.fromtimestamp(datum.epoch).strftime('%Y-%m-%d %H:%M:%S')
        irrigation_data_.append([date, datum.soil_moisture, datum.air_temperature, datum.air_humidity, datum.epoch])

    for datum in new_data:
        date = datetime.datetime.fromtimestamp(datum.epoch).strftime('%Y-%m-%d %H:%M:%S')
        new_data_.append([date, datum.soil_moisture, datum.air_temperature, datum.air_humidity, datum.epoch])

    irrigation_data = pd.DataFrame(irrigation_data_,
                                   columns=['time', 'soil_moisture', 'air_temperature', 'air_humidity', 'epoch_time'])

    new_data = pd.DataFrame(new_data_,
                                columns=['time', 'soil_moisture', 'air_temperature', 'air_humidity', 'epoch_time'])

    irrigation_data.dropna(inplace=True)
    new_data.dropna(inplace=True)

    irrigation_data.set_index(irrigation_data['time'], inplace=True)
    new_data.set_index(new_data['time'], inplace=True)

    # #  Extract as Json
    # with open('temp.json', 'w') as f:
    #     f.write(irrigation_data.to_json(orient='records', lines=True))

    del irrigation_data['time']
    del irrigation_data['epoch_time']
    del new_data['time']
    del new_data['epoch_time']

    # Soil-Moisture Percentage Calculation
    max_soil_moisture = irrigation_data['soil_moisture'].max()
    irrigation_data['soil_moisture'] = irrigation_data['soil_moisture'].apply(lambda x: max_soil_moisture - x)
    max_soil_moisture = irrigation_data['soil_moisture'].max()
    min_soil_moisture = irrigation_data['soil_moisture'].min()

    # Soil-Moisture Percentage Calculation
    new_data_max_soil_moisture = new_data['soil_moisture'].max()
    new_data['soil_moisture'] = new_data['soil_moisture'].apply(lambda x: new_data_max_soil_moisture - x)
    new_data_max_soil_moisture = new_data['soil_moisture'].max()
    min_soil_moisture = new_data['soil_moisture'].min()

    irrigation_data['soil_moisture'] = irrigation_data['soil_moisture'].apply(lambda x: (x / max_soil_moisture) * 100)
    new_data['soil_moisture'] = new_data['soil_moisture'].apply(lambda x: (x / new_data_max_soil_moisture) * 100)

    # Mark local minimum points
    n = 50  # number of points to be checked before and after

    irrigation_data['min'] = irrigation_data.iloc[argrelextrema(irrigation_data.soil_moisture.values, numpy.less_equal, order=n)[0]]['soil_moisture']
    irrigation_data["boolean"] = irrigation_data["min"]
    irrigation_data.drop(columns=['min'], inplace=True)
    irrigation_data["boolean"].fillna(0, inplace=True)
    irrigation_data.loc[irrigation_data["boolean"] != 0, "boolean"] = 1
    irrigation_data.dropna(inplace=True)
    irrigation_data_boolean = irrigation_data['boolean']
    irrigation_data.drop(columns=['boolean'], inplace=True)
    # pd.set_option('display.max_rows', irrigation_data_boolean.shape[0] + 1) # Uncomment to see every row
    # print(irrigation_data_boolean.describe())

    pipeline = Pipeline([
        ('classifier', GradientBoostingClassifier()),
    ])

    pipeline.fit(irrigation_data, irrigation_data_boolean)
    print("fit oldu")
    predictions = pipeline.predict(new_data)
    print(predictions)


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        while True:
            decide_irrigation()
            time.sleep(600)
