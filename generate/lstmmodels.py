import sys
import numpy as np

import torch
import torch.nn as nn
from torch.nn import functional as F
import torch.nn.utils.rnn as rnn_utils

# from trainer.utils import NUM_LABELS, IX_TO_LABEL


class FeedbackNN(nn.Module):
    """
    Neural network responsible for ingesting a tokenized student
    program, and spitting out a categorical prediction.

    We give you the following information:
        vocab_size: number of unique tokens
        num_labels: number of output feedback labels
    """

    def __init__(self, vocab_size, num_labels):
        super().__init__()
        # These modules define trainable parameters.
        self.embed_size = 20
        self.hidden_size = 50
        self.embed = nn.Embedding(vocab_size, self.embed_size)
        self.lstm = nn.LSTM(self.embed_size, self.hidden_size, bidirectional=False)
        self.fc = nn.Linear(self.hidden_size*52, num_labels)

    def forward(self, token_seq, token_length):
        """
        Forward pass for your feedback prediction network.

        @param token_seq: batch_size x max_seq_length
            Example: torch.Tensor([[0,6,2,3],[0,2,5,3], ...])
            These define your PADDED programs after tokenization.

        @param token_length: batch_size
            Example: torch.Tensor([4,4, ...])
            These define your unpadded program lengths.

        This function should return the following:
        @param label_out: batch_size x num_labels
            Each index in this tensor represents the likelihood of predicting
            1. Unlike IRT, this is a multilabel prediction program so we need
            to have a likelihood for every feedback. NOTE: this is NOT categorical
            since we can have multiple feedback at once.

            This will be given to F.binary_cross_entropy(...), just like IRT!
        """
        batch_size, max_seq_length = token_seq.shape # (100, 52)

        sorted_lengths, perm_idx = token_length.sort(0, descending=True)
        token_seq = token_seq[perm_idx]

        embed_seq = self.embed(token_seq)
        packed = rnn_utils.pack_padded_sequence(
            embed_seq,
            sorted_lengths.data.tolist() if batch_size > 1 else token_length.data.tolist(),
            batch_first=True
        )

        packed_output, hidden = self.lstm(packed)
        out, input_sizes = rnn_utils.pad_packed_sequence(packed_output, batch_first=True)
        _, unperm_idx = perm_idx.sort(0)
        out = out[unperm_idx]

        out = out.reshape(batch_size, -1)
        out = self.fc(out)
        out = torch.sigmoid(out)
        return out
