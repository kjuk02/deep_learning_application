import os

# CPU COUNT
CPU_COUNT = 10

# SCRIPT CONTROLLER OPTION
ANALYSIS_FLAG = 0
SAVE_FH_FLAG = 1

# IDB/OPS OPTION
FILE_CLASS = 'contest'  # malware, benignware, kisa_test_2018

# FH OPTION
'''
(b): basic block, (f): function, (p): process
(o): opcode seq, (a): api call seq, (s): string
(n): n-gram, (v): v-gram
(r): frequency, (c): content
'''
FH_TYPE = 'fh_fovc'  # counter(r), content(c), p(process), a(apics)
N_GRAM = 'v'
FH_CONTENT_BOUNDARY = 65536  # 2^8, 2^16, 2^32, 2^64
MAX_VECTOR_SIZE_BIT = 12
MAX_VECTOR_SIZE = (1 << MAX_VECTOR_SIZE_BIT)

# IDA 경로
# IDA_PATH = os.path.normpath('C:/Program Files/IDA 7.0/idat64.exe')
# IDA_TIME_OUT = 180

# 데이터셋 기본 경로
# BASE_PATH = os.path.normpath(os.path.abspath('D:/working_board/toy_dataset'))
BASE_PATH = os.path.normpath(os.path.abspath('D:/working_board/kisa_dataset'))

# ZIP FILE PATH
# ZIP_FILE_PATH = os.path.normpath(os.path.abspath('{0}/{1}/zipfile'.format(BASE_PATH, FILE_CLASS)))

# 입력 파일 경로
# INPUT_FILE_PATH = os.path.normpath(os.path.abspath('{0}/{1}/vir'.format(BASE_PATH, FILE_CLASS)))

# idb(i64) 저장 경로
# IDB_PATH = os.path.normpath(os.path.abspath('{0}/{1}/idb'.format(BASE_PATH, FILE_CLASS)))

# ida python script 저장 경로
# IDA_PYTHON_SCRIPT_PATH = os.path.normpath(os.path.abspath('./ida_script/ida_opcode.py'))

############################ OPS ############################
# OPS_PATH = os.path.normpath(os.path.abspath('{0}/{1}/ops'.format(BASE_PATH, FILE_CLASS)))
# ACS_PATH = os.path.normpath(os.path.abspath('{0}/{1}/acs'.format(BASE_PATH, FILE_CLASS)))
# STR_PATH = os.path.normpath(os.path.abspath('{0}/{1}/str'.format(BASE_PATH, FILE_CLASS)))
KISA_REPORT_PATH = os.path.normpath(os.path.abspath('{0}/{1}/ida_report'.format(BASE_PATH, FILE_CLASS)))
FH_INPUT_PATH = os.path.normpath(os.path.abspath(KISA_REPORT_PATH))

############################ FH ############################
FH_PATH = os.path.normpath(os.path.abspath('{0}/{1}/{2}/{3}/{4}'.format(BASE_PATH, FILE_CLASS, FH_TYPE, N_GRAM, MAX_VECTOR_SIZE)))


# function #
def create_file_list(root):
    ret_list = []
    for path, dirs, files in os.walk(root):
        if len(dirs) == 0:
            print('create file path: {}'.format(os.path.split(path)[-1]))
            for file in files:
                full_file_path = os.path.join(path, file)
                ret_list.append(full_file_path)
    return ret_list
