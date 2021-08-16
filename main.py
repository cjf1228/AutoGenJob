import os
import time
import pattern

FileNameDic = dict(pattern_dsr='', dbr_info='', output_dsr='',ary_dbr_file=[])

def GetAllFile():

    strCwd = os.getcwd()

    FileNameDic['pattern_dsr'] = os.path.join(strCwd, 'pattern.dsr')
    FileNameDic['dbr_info'] = os.path.join(strCwd, 'dbrinfo.ini')

    tmpData = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    FileNameDic['output_dsr'] = os.path.join(os.getcwd(), "批量作业" + tmpData + ".dsr")

    if not os.path.exists(FileNameDic['pattern_dsr']):
        print("错误::::::::::::::::::::文件 pattern.dsr 不存在")
    if not os.path.exists(FileNameDic['dbr_info']):
        print("错误::::::::::::::::::::文件 dbrinfo.ini 不存在")

    if os.path.exists(FileNameDic['output_dsr']):
        os.remove(FileNameDic['output_dsr'])

def read_file_line():
    strPath = ''

    f_file = open(FileNameDic['dbr_info'], 'r', encoding='utf-8')
    lines = f_file.readlines()
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        elif line.startswith('path='):
            strPath=line.replace('path=','')
        elif line.endswith('.dbr'):
            FileNameDic['ary_dbr_file'].append(os.path.join(strPath,line))

    f_file.close()


def get_entry_item():
    str_name = '转换'
    str_entries = ''
    str_hops = ''

    ary_dbr_file = FileNameDic['ary_dbr_file']
    for index in range(len(ary_dbr_file)):
        str_entry = pattern.str_entry_pattern
        str_hop = pattern.str_hop_pattern

        str_hop_name1 = f'{str_name} {index}'

        if index == len(ary_dbr_file) - 1:
            str_hop_name2 = f'成功'
        else:
            str_hop_name2 = f'{str_name} {index + 1}'

        str_entry = str_entry.replace("%%%1", str_hop_name1)
        str_entry = str_entry.replace("%%%2", ary_dbr_file[index])
        str_entry = str_entry.replace("%%%3", str((index + 1) * 100))

        str_hop = str_hop.replace("%%%1", str_hop_name1)
        str_hop = str_hop.replace("%%%2", str_hop_name2)

        str_entries = str_entries + str_entry + '\r\n'
        str_hops = str_hops + str_hop  + '\r\n'


    return  str_entries,str_hops


def write_to_dsr(str_entries, str_hops):
    f_file = open(FileNameDic['pattern_dsr'], 'r', encoding='utf-8')
    str_buf = f_file.read()
    f_file.close()

    str_buf = str_buf.replace("%%%1", str_entries)
    str_buf = str_buf.replace("%%%2", str_hops)

    f_file = open(FileNameDic['output_dsr'], 'w', encoding='utf-8')
    f_file.write(str_buf)
    f_file.close()


def Main():
    GetAllFile()
    read_file_line()
    str_entries,str_hops = get_entry_item()
    write_to_dsr(str_entries, str_hops)


print('运行开始-----------')
Main()
print('运行结束----------')
