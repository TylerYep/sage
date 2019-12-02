import os
import pickle
import numpy as np
from codeDotOrg import pseudoCodeToTree
from trainer.utils import OPEN_BRACKET, END_BRACKET
from trainer.utils import train_test_split
from trainer.labels import get_label_to_ix # LABEL_TO_IX, NUM_LABELS


def flatten_ast(ast):
    r"""Neural nets cannot take trees as input. For simplicity, we
    can flatten the tree into a string.

    @param ast: abstract syntax tree
    """
    flat = [OPEN_BRACKET, ast.rootName]
    for child in ast.children:
        if child:
            flat += flatten_ast(child)
    flat.append(END_BRACKET)
    return flat


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('problem', type=int, help='problem number')
    parser.add_argument(
        'raw_data_path', type=str,
        help='pickle file of {"program": [...], "label": [[...],[...],...]}',
    )
    args = parser.parse_args()
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR)
    print('DATA_DIR is accessible.')

    LABEL_TO_IX, IX_TO_LABEL, NUM_LABELS = get_label_to_ix(args.problem)

    with open(args.raw_data_path, 'rb') as fp:
        data = pickle.load(fp)

    num = len(data)
    programs, labels = [], []
    for i in range(num):
        code, label = data[i]['code'], data[i]['label']
        ast = pseudoCodeToTree.parse(code)
        code_list = flatten_ast(ast)
        code_str = ' '.join(code_list)
        programs.append(code_str)
        label_vec = np.zeros(NUM_LABELS)
        for lab in label:
            label_vec[LABEL_TO_IX[lab]] = 1
        labels.append(label_vec)
    programs = np.array(programs)
    labels = np.array(labels)

    train_list, val_list, test_list = train_test_split(
        [programs, labels], train_frac=0.8, val_frac=0.1, test_frac=0.1)

    train_programs, train_labels = train_list[0], train_list[1]
    val_programs, val_labels = val_list[0], val_list[1]
    test_programs, test_labels = test_list[0], test_list[1]

    train_data = {'program': train_programs, 'label': train_labels}
    val_data = {'program': val_programs, 'label': val_labels}
    test_data = {'program': test_programs, 'label': test_labels}

    with open(os.path.join(DATA_DIR, f'train_data_{args.problem}.pickle'), 'wb') as fp:
        pickle.dump(train_data, fp)

    with open(os.path.join(DATA_DIR, f'val_data_{args.problem}.pickle'), 'wb') as fp:
        pickle.dump(val_data, fp)

    with open(os.path.join(DATA_DIR, f'test_data_{args.problem}.pickle'), 'wb') as fp:
        pickle.dump(test_data, fp)

    # process the real student data

    # with open(os.path.join(DATA_DIR, 'real-data-500.pk'), 'rb') as fp:
    #     real_data = pickle.load(fp)

    # num = len(real_data['program'])
    # new_labels = []
    # for i in range(num):
    #     label = real_data['label'][i]
    #     label_vec = np.zeros(NUM_LABELS)
    #     for lab in label:
    #         try:
    #             label_vec[LABEL_TO_IX[lab]] = 1
    #         except:
    #             continue
    #     new_labels.append(label_vec)
    # new_labels = np.array(new_labels)

    # real_data = {'program': real_data['program'], 'label': new_labels}
    # with open(os.path.join(DATA_DIR, 'transfer.pickle'), 'wb') as fp:
    #     pickle.dump(real_data, fp)

if __name__ == "__main__":
    main()
