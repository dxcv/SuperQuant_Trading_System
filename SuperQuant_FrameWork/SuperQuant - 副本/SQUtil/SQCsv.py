# coding:utf-8


import csv

def SQ_util_save_csv(data, name, column=None, location=None):
    # 重写了一下保存的模式
    # 增加了对于可迭代对象的判断 2017/8/10
    """
    SQ_util_save_csv(data,name,column,location)

    将list保存成csv
    第一个参数是list
    第二个参数是要保存的名字
    第三个参数是行的名称(可选)
    第四个是保存位置(可选)

    @yutiansut
    """
    assert isinstance(data, list)
    if location is None:
        path = './' + str(name) + '.csv'
    else:
        path = location + str(name) + '.csv'
    with open(path, 'w', newline='') as f:
        csvwriter = csv.writer(f)
        if column is None:
            pass
        else:
            csvwriter.writerow(column)

        for item in data:

            if isinstance(item, list):
                csvwriter.writerow(item)
            else:
                csvwriter.writerow([item])


if __name__ == '__main__':
    SQ_util_save_csv(['a', 'v', 2, 3], 'test')
    SQ_util_save_csv([['a', 'v', 2, 3]], 'test2')

