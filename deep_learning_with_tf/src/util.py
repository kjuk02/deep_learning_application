from data import *
import datetime
import itertools
import hashlib
import matplotlib.pyplot as plt
import os
import _pickle
import random
from sklearn.metrics import confusion_matrix


# function: 입력 파일의 이름을 md5로 바꿔주는 함수
def convert_filename_to_md5(input_path):
    cnt = 0
    for path, _, files in os.walk(input_path):
        for file in files:
            file_md5 = get_md5(os.path.join(path, file))
            os.rename(os.path.join(path, file), os.path.join(path, file_md5+'.vir'))
            cnt += 1
            if cnt % 200 == 0:
                print(cnt)
    pass


# function: virussign 의 vir 파일을 fixed size vector(확장자: bin)로 변환하는 함수
# up-sampling / down-sampling 기술이 적용된다.
def convert_vir_to_bin(input_dir):
    print('conveert vir to bin start')
    fixed_file_size = int(16384)

    file_lists = os.listdir(input_dir)
    for file in file_lists:
        file_name, ext = os.path.splitext(file)
        # extension check
        if ext != '.vir':
            continue

        content = list(open(os.path.join(input_dir, file), 'rb').read())
        file_size = len(content)

        if file_size > fixed_file_size:  # down-sampling
            rest = file_size % fixed_file_size
            if rest == 0:
                convert_list = np.array(content)
            else:
                zero_padding_list = [0 for _ in range(rest, fixed_file_size)]
                convert_list = np.array(content + zero_padding_list)
            result_list = np.average(convert_list.reshape(len(convert_list)//fixed_file_size, fixed_file_size), axis=0)
        elif file_size < fixed_file_size:  # up-sampling
            blank_size = fixed_file_size - file_size
            for i in range(blank_size):
                content.append(content[i])
            result_list = np.array(content)
            pass
        else:
            result_list = np.array(content)
            pass

        result_list = [x / 255 for x in result_list]  # normalization to 255(max value)

        dst_path = input_dir.replace('raw', 'bin')

        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        with open(os.path.join(dst_path, file_name+'.bin'), 'wb') as f:
            _pickle.dump(result_list, f)

    print('{} end'.format(input_dir))
    pass


# function: 입력 파일에 대한 md5 hash value를 16진수로 반환하는 함수
def get_md5(path, block_size=8192):
    with open(path, 'rb') as f:
        hasher = hashlib.md5()
        buf = f.read(block_size)
        while buf:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()


# function: 입력 디렉토리가 존재하는지 확인하는 함수
def check_existing_dir(file_path):
    if not os.path.exists(os.path.normpath(os.path.abspath(file_path))):
        try:
            os.makedirs(file_path)
        except:
            pass
    pass


# function: 학습 모델의 예측 결과와 ground truth를 입력으로 받아 혼동 행렬를 그려주는 함수
def plot_confusion_matrix(step, y_true, y_pred, output_size):
    # check result directory
    result_dir = 'result'
    check_existing_dir(result_dir)

    print('plot confusion matrix start: ', end='')

    # compute confusion matrix
    cnf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)

    # configuration
    np.set_printoptions(precision=2)

    if output_size == 2:
        labels = ['benign', 'malware']
    else:
        # toy dataset label
        labels = ['Virus', 'Worm', 'Trojan', 'not-a-virus:Downloader', 'Trojan-Ransom', 'Backdoor']

    norm_flag = True
    plot_title = 'Confusion matrix'
    cmap = plt.cm.Blues

    if norm_flag:
        cnf_matrix = cnf_matrix.astype('float') / cnf_matrix.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    # plotting start
    plt.figure()
    plt.imshow(cnf_matrix, interpolation='nearest', cmap=cmap)
    plt.title(plot_title)
    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels, rotation=90)
    plt.xticks(tick_marks, labels)
    plt.yticks(tick_marks, labels)

    # information about each block's value
    fmt = '.3f' if norm_flag else 'd'
    thresh = cnf_matrix.max() / 2.
    for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        plt.text(j, i, format(cnf_matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

    ## insert legend information
    # import matplotlib.patches as mpatches
    # patches = [mpatches.Patch(color='white', label='G{num} = {group}'.format(num=i+1, group=labels[i])) for i in range(len(labels))]
    # plt.legend(handles=patches, bbox_to_anchor=(-0.60, 1), loc=2, borderaxespad=0.)

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.show()
    plt.savefig(os.path.join(result_dir, 'conf_matrix{}'.format(step)))
    print('--plot confusion matrix finish--')
    pass


# function:
def save_learning_result_to_csv(step, filenames=None, actuals=None, preds=None):
    # check result directory
    result_dir = 'result'
    check_existing_dir(result_dir)

    # delete upper directory
    filenames = [filename.split(os.sep)[-1] for filename in filenames]

    # save result as pickle file
    # if not (filenames is None and actuals is None and preds is None):
    #     with open(os.path.join(result_dir, 'learning_result{}.pickle'.format(step)), 'wb') as f:
    #         _pickle.dump(filenames, f)
    #         _pickle.dump(actuals, f)
    #         _pickle.dump(preds, f)

    # save result as csv file
    # with open(os.path.join(result_dir, 'learning_result{}.csv'.format(step)), 'w', newline='') as f:
    #     wr = csv.writer(f)
    #     for name, actual_label, pred_label in zip(filenames, actuals, preds):
    #         wr.writerow([name, actual_label, pred_label])

    # save result that gets wrong cases as csv file
    with open(os.path.join(result_dir, 'profiling{}.csv'.format(step)), 'w', newline='') as f:
        wr = csv.writer(f)
        for name, actual_label, pred_label in zip(filenames, actuals, preds):
            if actual_label != pred_label:
                wr.writerow([name, actual_label, pred_label])
    pass


# function: 입력 경로에 대한 모든 파일 경로를 리스트로 반환하는 함수
def walk_dir(input_path, ext):
    print('@ walk dir start')
    result = list()
    for path, dirs, files in os.walk(input_path):
        if len(dirs) == 0:
            print(path)
            for file in files:
                if ext == os.path.splitext(file)[-1][1:]:
                    file_path = os.path.join(path, file)  # store "file path"
                    result.append(file_path)
    print('@ walk dir finish')
    return result


# function: 시작일과 종료일 사이에 있는 모든 날짜를 반환하는 함수
def get_range_dates(start_date, end_date):
    date_form = '%Y%m%d'
    s = datetime.datetime.strptime(start_date, date_form).date()
    d = datetime.datetime.strptime(end_date, date_form).date()

    result_date = set()
    for day in range((d-s).days + 1):
        result_date.add((s + datetime.timedelta(days=day)).strftime(date_form))

    return result_date


# function:
def split_train_test_data(class_type, mal_path, ben_path, mal_train_start_date, mal_train_end_date,
                          mal_test_start_date, mal_test_end_date, ben_ratio, ext, fhs_flag):
    print('@ split train test data')

    mal_data = np.array(walk_dir(os.path.join(mal_path, 'fhs') if fhs_flag else mal_path, 'fhs' if fhs_flag else ext))
    mal_train_dates = get_range_dates(mal_train_start_date, mal_train_end_date)
    mal_test_dates = get_range_dates(mal_test_start_date, mal_test_end_date)
    mal_train_indices, mal_test_indices = list(), list()
    for cnt, data in enumerate(mal_data):
        file_name = os.path.splitext(os.path.basename(data))[0]
        upper_path = data.split(os.sep)[-2]
        if (file_name in mal_train_dates) or (upper_path in mal_train_dates):
            print('train: {}'.format(file_name))
            mal_train_indices.append(cnt)
        elif (file_name in mal_test_dates) or (upper_path in mal_test_dates):
            print('test: {}'.format(file_name))
            mal_test_indices.append(cnt)

    ben_data = np.array(walk_dir(ben_path, ext)) if class_type == 'BINARY' else list()
    ben_total_indices = np.arange(len(ben_data)); random.shuffle(ben_total_indices)
    ben_ratio_a, ben_ratio_b = ben_ratio.split(':')
    ben_ratio_number = int(ben_ratio_a)/(int(ben_ratio_a)+int(ben_ratio_b))
    no_ben_train_data = int(ben_ratio_number*len(ben_data))
    ben_train_indices, ben_test_indices = ben_total_indices[:no_ben_train_data], ben_total_indices[no_ben_train_data:]

    result_indices = list()
    result_indices.append((np.asarray(mal_train_indices), np.asarray(mal_test_indices)))
    if class_type == 'BINARY':
        result_indices.append((ben_train_indices, ben_test_indices))

    return mal_data, ben_data, result_indices