# encoding:utf-8
import time
import fileinput
from datetime import datetime


# n_date = datetime.now().date()
# print datetime.now().strftime('%Y-%m-%d %H:%M')

# how much words?
def count_words(file):
    with open(file) as f:
        text = f.readline()
        words = text.split()
        count = len(words)
    return count


# how much lines in a very big file?
def count_lines(file2):
    row = 0
    with open(file2) as f:
        while True:
            line = f.readline()
            if not line: break
            row += 1
        return row


def count_lines1(f):
    row = 0
    while True:
        line = f.readline()
        if not line: break
        row += 1
    return row


# how much lines in a file?--file iterator
def count_lines2(file1):
    row = 0
    with open(file1) as f:
        for line in f:
            # process(line)
            row += 1
    return row


# 将train和test的cue位置文件内容缩减
def label2txt(txt, file_pos, corpus):
    with open(txt, 'w+') as r:
        with open(file_pos) as p:
            with open(corpus) as f:
                for line in p:  # 文件迭代器
                    words = line.split('---')
                    for i in range(len(words)):
                        if i in [0, 1, 6]:
                            r.write(words[i] + ' ')
                    r.write('\n')


'''
    从 train_One.gdep 文件中，读取出所有单词 words 和它所依赖的单词的数组下标 position
'''


def get_pos_word(file):
    lines = []
    position = []
    words = []
    with open(file) as f:
        w = []
        p = []
        while True:
            line = f.readline()
            if not line: break
            if line != '\n':
                w.append(line.split()[1])
                p.append(line.split()[-2])
            else:
                words.append(w)
                position.append(p)
                w = []
                p = []
        words.append(w)
        position.append(p)
    # for i in range(len(lines)):
    # line = lines[i]
    #     # print "number: %3s word: %12s  depend: %3s style: %5s" % (line[0], line[1], line[-2], line[-1])
    #     words.append(line[1])
    #     position.append(line[-2])
    return words, position


'''
    构建一棵依赖树,返回node数组和根节点所在数组下标
'''
from multi_tree import TreeNode


def construct_tree(words, position):
    tree = []
    node = []
    root_index = []
    for i in range(len(words)):  # 先获得所有的单词节点
        for k in range(len(words[i])):
            node.append(TreeNode(words[i][k]))

        for j in range(len(position[i])):  # 通过position判断依赖关系，形成依赖树
            index = int(position[i][j])
            # next = position[index-1]
            if index != 0:  # 根节点
                node[index - 1].add_child(node[j])
            else:
                root_index.append(j)
        tree.append(node)
        # node[root_index[i]].show(0)  # 展示依赖树
        node = []
    return tree, root_index


'''
    从file中获取所有的句子，存至sentences数组中
    从file中获取有关系的实体对，存至word_pair数组中
'''


def get_all_sentences(file):
    sentences = []  # 存放语料的所有句子
    word_pair = []  # 存放句子中有关系的实体对
    flags = []  # 存放实体对的关系的真假标签
    rows = count_lines(file)
    with open(file) as f:
        first_line = f.readline()
        # line = line.split()[1:]
        line = first_line.split()
        line[len(line) - 1] = line[len(line) - 1][:-1]  # 去掉句子中最后一个单词的句号
        line.append('.')
        sentences.append(line)
        word = []
        flag = []
        while True:
            line = f.readline()
            if not line: break
            if line != '\n':
                if line.split()[2] != 'CID':
                    continue
                else:
                    row = line.split()
                    w1 = first_line[int(row[3]) + 10:int(row[4]) + 10]
                    w2 = first_line[int(row[6]) + 10:int(row[7]) + 10]
                    flag.append(row[-1])
                    word.append([w1, w2])
            else:
                flags.append(flag)
                word_pair.append(word)
                flag = []
                word = []
                first_line = f.readline()
                line = first_line.split()
                try:
                    line[len(line) - 1] = line[len(line) - 1][:-1]  # list index out of range
                except:
                    pass
                line.append('.')
                sentences.append(line)
        flags.append(flag)
        word_pair.append(word)
    return sentences, word_pair, flags


if __name__ == "__main__":
    # 从file中获取所有的句子，存至sentences数组中
    sentences, word_pair, flags = get_all_sentences(r'corpus/CDR_TrainSentence.txt')