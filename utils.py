import pickle


def make_pickle(list, file_name):
    with open(file_name, "wb") as f:
        pickle.dump(list, f)


def check_num(i):
    try:
        int(i)
        return True
    except:
        return False
