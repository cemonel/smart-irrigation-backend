import time
import datetime

import pandas as pd
from scipy.signal import argrelextrema
import numpy
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.pipeline import Pipeline


from django.core.management.base import BaseCommand
from smart_irrigation.data.models import Data
from smart_irrigation.plant.models import Plant


def decide_irrigation():
    data = list(Data.objects.filter(plant_id=1))
    train_data = data[:-5]  # Old data for training. This is for test purposes this should be up to last manual irrigation.
    new_data = data[-5:]  # seconds last 5 minutes data
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

    #  Extract as Json
    with open('temp.json', 'w') as f:
        f.write(irrigation_data.to_json(orient='records', lines=True))

    del irrigation_data['time']
    del irrigation_data['epoch_time']
    del new_data['time']
    del new_data['epoch_time']

    # Soil-Moisture Percentage Calculation
    max_soil_moisture = irrigation_data['soil_moisture'].max()
    old_max_soil_moisture = max_soil_moisture
    irrigation_data['soil_moisture'] = irrigation_data['soil_moisture'].apply(lambda x: max_soil_moisture - x)
    max_soil_moisture = irrigation_data['soil_moisture'].max()
    min_soil_moisture = irrigation_data['soil_moisture'].min()

    # Soil-Moisture Percentage Calculation
    new_data['soil_moisture'] = new_data['soil_moisture'].apply(lambda x: old_max_soil_moisture - x)

    irrigation_data['soil_moisture'] = irrigation_data['soil_moisture'].apply(lambda x: (x / max_soil_moisture) * 100)
    new_data['soil_moisture'] = new_data['soil_moisture'].apply(lambda x: (x / max_soil_moisture) * 100)

    # Mark local minimum points
    n = 50  # number of points to be checked before and after

    # irrigation_data = irrigation_data.loc[:,~irrigation_data.rows.duplicated()] #  Removes duplicate columns
    irrigation_data = irrigation_data[~irrigation_data.index.duplicated()]
    irrigation_data['min'] = irrigation_data.iloc[argrelextrema(irrigation_data.soil_moisture.values, numpy.less_equal, order=n)[0]]['soil_moisture']
    threshold_value = irrigation_data.mean(axis=0, skipna=True)[3]
    print("Threshold value:" + str(threshold_value.item()))
    irrigation_data["boolean"] = irrigation_data["min"]
    irrigation_data.drop(columns=['min'], inplace=True)
    irrigation_data["boolean"].fillna(0, inplace=True)

    for index, i in enumerate(irrigation_data["soil_moisture"]):
        if i < threshold_value:
            irrigation_data["boolean"][index] = 1
        else:
            irrigation_data["boolean"][index] = 0

    irrigation_data.dropna(inplace=True)
    irrigation_data_boolean = irrigation_data['boolean']
    irrigation_data.drop(columns=['boolean'], inplace=True)
    # pd.set_option('display.max_rows', irrigation_data_boolean.shape[0] + 1) # Uncomment to see every row
    # print(irrigation_data_boolean.describe())

    pipeline = Pipeline([
        ('classifier', GradientBoostingClassifier()),
    ])

    pipeline.fit(irrigation_data, irrigation_data_boolean)
    print("Fitting:")
    print(new_data)
    predictions = pipeline.predict(new_data)
    count = 0

    for i in predictions:  # More than 5 irrigate
        if i == 1:
            count = count + 1

    if count >= 5:
        print('Irrigation Time.')
        plant = Plant.objects.get(id=1)
        plant.status = Plant.STATUS_IRRIGATE
        plant.last_irrigation_date = datetime.datetime.now()
        plant.irrigation_count = plant.irrigation_count + 1
        plant.save()


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):
        while True:
            plant = Plant.objects.get(id=1)
            if plant.machine_learning and plant.irrigation_count > plant.max_manual_irrigation_for_machine_learning:
                print("Deciding...")
                decide_irrigation()
                time.sleep(600)
            print("Waiting for enough irrigation. Current Irrigation: " + plant.irrigation_count)
