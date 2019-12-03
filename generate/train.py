"""Train on synthetically generated data"""

import os
import pickle
import argparse

from lstmmodels import FeedbackNN
import trainer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', type=int, help='problem number')
    args = parser.parse_args()

    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    CHECKPOINT_DIR = os.path.join(os.path.dirname(__file__), 'checkpoints', f'cp{args.problem}')
    TRAINING_PARAMS = {
        'batch_size': 100,
        'epochs': 3,       # number of loops through synthetic data
        'lr': 3e-4,         # learning rate
        'seed': 1,
        'max_seq_len': 50,  # maximum number of tokens allowed in a single sequence
        'min_occ': 1,       # minimum number of occurences to add a token into the vocab
        'out_dir': CHECKPOINT_DIR,  # where to train the model
    }

    train_data_path = os.path.join(DATA_DIR, f'train_data_{args.problem}.pickle')
    val_data_path = os.path.join(DATA_DIR, f'val_data_{args.problem}.pickle')
    test_data_path = os.path.join(DATA_DIR, f'test_data_{args.problem}.pickle')

    trainer.train_pipeline(args.problem,
                           FeedbackNN,
                           train_data_path,
                           val_data_path,
                           test_data_path,
                           TRAINING_PARAMS)
