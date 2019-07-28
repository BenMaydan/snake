import pickle


def file(file_name, read_or_write, dump = None):
    """
    Reads file or dumps to a file
    :param file_name: Name of the file
    :param read_or_write: How to open the file
    :param dump: Data to dump
    :return: Depends on how the file was opened (rb or wb)
    """
    mapping = {
                'rb': lambda: pickle.load(f),
                'wb': lambda: pickle.dump(dump, f),
            }
    with open(file_name, read_or_write) as f:
        return mapping[read_or_write]()


default_data = {
                'id':{
                    'p1': {
                            'score': 0,
                            'direction': 'n',
                            'snake_list': []
                            },
                    'p2': {
                            'score': 0,
                            'direction': 'n',
                            'snake_list': []
                            },
                    'printable': []}}

print(file('games.pickle', 'rb'))
file('games.pickle', 'wb', default_data)
