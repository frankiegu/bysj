import numpy as np
import os

data_path = "./data/"

def load_data(args):
    n_user, n_item, train_data, eval_data, test_data = load_rating(args)
    n_entity, n_relation, kg = load_kg(args)
    print('data loaded.')

    return n_user, n_item, n_entity, n_relation, train_data, eval_data, test_data, kg

def load_rating(args):
    print('reading rating file ...')

    # reading rating file
    rating_file = data_path + args.dataset + '/ratings_final'

    rating_np = np.loadtxt(rating_file + '.txt', dtype=np.int32)

    n_user = len(set(rating_np[:, 0]))
    n_item = len(set(rating_np[:, 1]))

    train_data, eval_data, test_data = dataset_split(rating_np)

    return n_user, n_item, train_data, eval_data, test_data

def dataset_split(rating_np):
    print('splitting dataset ...')

    # train:eval:test = 6:2:2
    eval_ratio = 0.1

    test_ratio = 0.1
    #35612  文件行数
    n_ratings = rating_np.shape[0]

    eval_indices = np.random.choice(list(range(n_ratings)), size=int(n_ratings * eval_ratio), replace=False)
    left = set(range(n_ratings)) - set(eval_indices)
    test_indices = np.random.choice(list(left), size=int(n_ratings * test_ratio), replace=False)
    train_indices = list(left - set(test_indices))
    # print(rating_np[train_indices])
    # exit()
    train_data = rating_np[train_indices]
    eval_data = rating_np[eval_indices]
    test_data = rating_np[test_indices]

    return train_data, eval_data, test_data

def load_kg(args):
    print('reading KG file ...')

    # reading kg file
    kg_file = data_path + args.dataset + '/kg_final'

    kg = np.loadtxt(kg_file + '.txt', dtype=np.int32)

    n_entity = len(set(kg[:, 0]) | set(kg[:, 2]))
    n_relation = len(set(kg[:, 1]))

    return n_entity, n_relation, kg
