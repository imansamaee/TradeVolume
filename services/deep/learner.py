import pandas as pd
from keras.layers import Dense
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

from services.data.data_object import DataObject


class DeepLearner:

    def __init__(self, data_object, init=True):
        self.data_object: DataObject = data_object
        self.scaled_training_df = None
        self.scaled_testing_df = None
        self.model = None
        self.process_data()
        if init:
            self.create_model()
        else:
            self.model = keras.models.load_model(f"data/deep/overall/{self.data_object.symbol}_trained_model.h5")

    # noinspection PyTypeChecker
    def process_data(self):
        # Load training data set from CSV file
        training_data_df = self.data_object.df
        # Load testing data set from CSV file
        test_data_df = training_data_df

        # Data needs to be scaled to a small range like 0 to 1 for the neural
        # network to work well.
        scaler = MinMaxScaler(feature_range=(0, 1))

        # Scale both the training inputs and outputs
        scaled_training = scaler.fit_transform(training_data_df)
        scaled_testing = scaler.transform(test_data_df)

        # Create new pandas DataFrame objects from the scaled data
        scaled_training_df = pd.DataFrame(scaled_training, columns=training_data_df.columns.values)
        scaled_testing_df = pd.DataFrame(scaled_testing, columns=test_data_df.columns.values)

        # Save scaled data dataframes to new CSV files
        scaled_training_df.to_csv(f"data/deep/overall/{self.data_object.symbol}_scaled.csv", index=False)
        scaled_testing_df.to_csv(f"data/deep/overall/{self.data_object.symbol}_test_scaled.csv", index=False)
        self.scaled_training_df = scaled_training_df
        self.scaled_testing_df = scaled_testing_df
        return scaled_training_df, scaled_testing_df

    def create_model(self):
        training_data_df = self.scaled_testing_df
        X = training_data_df.drop('next_close', axis=1).values
        Y = training_data_df[['next_close']].values
        # Define the model
        model = Sequential()
        model.add(Dense(500, input_dim=training_data_df.shape[1] - 1, activation='relu'))
        model.add(Dense(500, activation='relu'))
        model.add(Dense(300, activation='relu'))
        model.add(Dense(1, activation='linear'))
        model.compile(loss="mean_squared_error", optimizer="adam")

        # Train the model
        model.fit(
            X,
            Y,
            epochs=350,
            verbose=0
        )

        # Load the separate test data set
        test_data_df = self.scaled_testing_df
        X_test = test_data_df.drop('next_close', axis=1).values
        Y_test = test_data_df[['next_close']].values

        test_error_rate = model.evaluate(X_test, Y_test, verbose=0)
        print("The mean squared error (MSE) for the test data set is: {}".format(test_error_rate))

        # Save the model to disk

        model.save(f"data/deep/overall/{self.data_object.symbol}_trained_model.h5")
        self.model = model
        print("Model saved to disk.")

    def predict_next_close(self, previous_index=0):
        main_df = self.data_object.df
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_training = scaler.fit_transform(main_df)
        scaled_training_df = pd.DataFrame(scaled_training, columns=main_df.columns.values)
        model = self.model
        X = scaled_training_df.iloc[-previous_index - 2:-previous_index - 1, :-1].values
        prediction = model.predict(X)
        # Grab just the first element of the first prediction (since we only have one)
        prediction = prediction[0][0]
        # Re-scale the data from the 0-to-1 range back to dollars
        # These constants are from when the data was originally scaled down to the 0-to-1 range
        prediction = prediction + scaler.min_[-1]
        prediction = prediction / scaler.scale_[-1]
        return prediction

    def next_change_percentage(self):
        return self.data_object.last / (self.predict_next_close() - self.data_object.last) * 100
