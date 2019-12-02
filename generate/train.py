"""Train on synthetically generated data"""

import os
import pickle

from lstmmodels import FeedbackNN
from config import TRAINING_PARAMS, DATA_DIR, CURR_PROBLEM

import trainer


if __name__ == "__main__":
    train_data_path = os.path.join(DATA_DIR, f'train_data_{CURR_PROBLEM}.pickle')
    val_data_path = os.path.join(DATA_DIR, f'val_data_{CURR_PROBLEM}.pickle')
    test_data_path = os.path.join(DATA_DIR, f'test_data_{CURR_PROBLEM}.pickle')

    trainer.train_pipeline(FeedbackNN, train_data_path, val_data_path, test_data_path, TRAINING_PARAMS)
