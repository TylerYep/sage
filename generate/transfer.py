"""Test on real data validation set!"""

import os
import torch
import pickle

from lstmmodels import FeedbackNN
from trainer.config import TRAINING_PARAMS, DATA_DIR, CHECKPOINT_DIR

import trainer


if __name__ == "__main__":
    real_data_path = os.path.join(DATA_DIR, 'transfer.pickle')
    checkpoint_path = os.path.join(CHECKPOINT_DIR, 'model_best.pth.tar')  # checkpoint.pth.tar

    results = trainer.transfer_pipeline(FeedbackNN, checkpoint_path, real_data_path)
    print(results)
