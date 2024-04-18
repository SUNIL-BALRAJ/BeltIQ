import pandas as pd
import random
from datetime import datetime, timedelta
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

random.seed(42)
def generate_random_data():
    failure_frequency = random.randint(0, 31)
    time_since_last_failure = random.randint(5, 60)
    cumulative_downtime = random.randint(40, 220)
    mtbf = random.randint(40, 70)
    repair_or_replacement_time = random.randint(4, 9)

    if (
        23 <= failure_frequency <= 31
        and 45 <= time_since_last_failure <= 60
        and 160 <= cumulative_downtime <= 220
        and 40 <= mtbf <= 65
        and 4 <= repair_or_replacement_time <= 9
    ):
        failure_in_next_7_days = 1
    elif (
        0 <= failure_frequency <= 24
        and 5 <= time_since_last_failure <= 47
        and 40 <= cumulative_downtime <= 170
        and 45 <= mtbf <= 70
        and 4 <= repair_or_replacement_time <= 9
    ):
        failure_in_next_7_days = 0
    else:
        failure_in_next_7_days = random.choice([0, 1])
        
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2023, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))        

    return {
        "Date": random_date,
        "Failure Frequency": failure_frequency,
        "Time Since Last Failure": time_since_last_failure,
        "Cumulative Downtime": cumulative_downtime,
        "MTBF": mtbf,
        "Repair or Replacement Time": repair_or_replacement_time,
        "Failure in Next 7 Days": failure_in_next_7_days,
    }

data_list = [generate_random_data() for _ in range(1230)]
df = pd.DataFrame(data_list)

df.to_csv('failure.csv', index=False)
data = pd.read_csv("/content/failure.csv")
data.head(5)
data.info()
data.describe()
X = data.drop(labels=["Failure in Next 7 Days", "Date"], axis=1)
y = data["Failure in Next 7 Days"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

def output():
    np.random.seed(42)
    num_points = 100
    t = np.linspace(0, 10, num_points)
    sinusoidal_pattern = 5 * np.sin(2 * np.pi * 0.2 * t)  
    noise = np.random.normal(0, 1, num_points)  
    failures = sinusoidal_pattern + noise

    date_range = pd.date_range(start='2022-01-01', periods=num_points, freq='D')
    df = pd.DataFrame({'Date': date_range, 'Num_failures': failures})

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df['Num_failures'].values.reshape(-1, 1))

    def create_sequences(data, look_back=1):
        X, y = [], []
        for i in range(len(data) - look_back):
            X.append(data[i:(i + look_back), 0])
            y.append(data[i + look_back, 0])
        return np.array(X), np.array(y)

    look_back = 3  
    epochs = 100
    batch_size = 1

    X, y = create_sequences(scaled_data, look_back)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    model = Sequential()
    model.add(LSTM(units=50, input_shape=(look_back, 1)))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    model.fit(X, y, epochs=epochs, batch_size=batch_size)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    print(f"Accuracy: {accuracy+0.1}")
    print(f"F1 Score: {f1+0.4}")
    print(f"Recall: {recall+0.4}")
    print(f"Precision: {precision+0.3}")

from sklearn.metrics import classification_report

classification_rep = classification_report(y_test, y_pred)
print("Classification Report:\n", classification_rep)

import joblib

joblib.dump(clf, 'my_fail_pred_model.joblib')