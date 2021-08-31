import json
import csv


def read_jl_and_write_csv(filename):
    """
    Чтобы прочитать файл .jl, надо читать в цикле и каждую строку jl-файла переводить в питон-словарь(loads)
    Все это заворачиваем в список и получается список словарей.
    """
    with open(f'{filename}.jl', 'r') as f_1:
        lst = []
        lst1 = []
        for line in f_1:
            lst.append(json.loads(line))

        for i, v in enumerate(lst, 1):
            if i % 2 == 0:
                # print(v)
                lst1.append(v)

    with open(f'{filename}.csv', 'w', encoding='utf-8') as f_n:
        f_n_writer = csv.DictWriter(f_n, fieldnames=lst1[0].keys(),
                                    quoting=csv.QUOTE_NONNUMERIC)
        f_n_writer.writeheader()
        for d in lst1:
            f_n_writer.writerow(d)


read_jl_and_write_csv('hh')
