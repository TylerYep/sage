import os
import numpy as np

import torch
import torch.utils.data as data

from trainer.datasets import ProductionDataset
from preprocess import flatten_ast
from lstmmodels import FeedbackNN


def preprocess(nn_data):
    programs = []
    for ast in nn_data:
        code_list = flatten_ast(ast)
        code_str = ' '.join(code_list)
        programs.append(code_str)
    return np.array(programs)


def make_prediction(problem, programs):
    checkpoint_path = os.path.join(os.path.dirname(__file__), 'checkpoints', f'cp{problem}')
    checkpoint_path = os.path.join(checkpoint_path, 'model_best.pth.tar')

    device = torch.device('cpu')  # no CUDA support for now

    checkpoint = torch.load(checkpoint_path)
    config = checkpoint['config']

    model = FeedbackNN(vocab_size=checkpoint['vocab_size'],
                       num_labels=checkpoint['num_labels'])
    model.load_state_dict(checkpoint['state_dict'])  # load trained model
    model = model.eval()

    # reproducibility
    torch.manual_seed(config['seed'])
    np.random.seed(config['seed'])

    real_dataset = ProductionDataset(programs,
                                     vocab=checkpoint['vocab'],
                                     max_seq_len=config['max_seq_len'],
                                     min_occ=config['min_occ'])
    real_loader = data.DataLoader(real_dataset,
                                  batch_size=config['batch_size'],
                                  shuffle=False)

    pred_arr = []
    with torch.no_grad():
        for (token_seq, token_len) in real_loader:
            token_seq = token_seq.to(device)
            token_len = token_len.to(device)
            label_out = model(token_seq, token_len)
            pred_npy = torch.round(label_out).detach().numpy()
            pred_arr.append(pred_npy)
    return pred_arr[0]
