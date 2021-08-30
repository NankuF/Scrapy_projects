import json
import csv


def read_jl_and_write_csv(filename):
    """
    Чтобы прочитать файл .jl, надо читать в цикле и каждую строку jl-файла переводить в питон-словарь(loads)
    Все это заворачиваем в список и получается список словарей.
    """
    with open(f'{filename}.jl', 'r') as f_1:
        lst = []
        for line in f_1:
            lst.append(json.loads(line))

    with open(f'{filename}.csv', 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.DictWriter(f_n, fieldnames=lst[0].keys(),
                                    quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writeheader()
        for d in lst:
            f_n_writer.writerow(d)


read_jl_and_write_csv('wb')
