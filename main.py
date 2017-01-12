#!/usr/bin/python
# -*- coding: utf-8 -*-
# coding=utf-8
import function

depend_file = r'corpus/train/train_One.gdep'
train_file = r'corpus/train/CDR_Train_One.txt'


# 从 train_One.gdep 文件中，读取出所有单词和它所依赖的单词的数组下标
words, position = function.get_pos_word(depend_file)
# 构建一棵依赖树,返回node数组和根节点所在数组下标
trees, root_index = function.construct_tree(words, position)
# 从file中获取所有的句子，存至sentences数组中
sentences, word_pair, flags = function.get_all_sentences(train_file)


# 计算节点的高度
def Hight(node):
    len = 0
    while node:
        len += 1
        node = node.parent
    return len


'''
    查找两个节点到最近公共祖先节点之间的路径
'''


def GetLastCommonAncestor(w1, w2, flag, tree):
    left_path = []
    right_path = []
    word1, word2 = w1, w2
    node1, node2 = None, None
    '''
    有些词在句子中是连词（多个词组成），但是在关系依赖树被拆分了，无法匹配！
    如：alpha-methyldopa(√)、[3H]-naloxone(×)-->-naloxone
    所以，暂时以连词的最后一个词作为匹配对象...
    '''
    if ' ' in w1:
        word1 = word1.split()[-1]
    if w1.find('-') != -1 and w1.find('[') != -1:
        word1 = word1.split('-')[-1]
        word1 = '-'+word1
    if ' ' in w2:
        word2 = word2.split()[-1]
    if w2.find('-') != -1 and w2.find('[') != -1:
        word2 = word2.split('-')[-1]
        word2 = '-'+word2

    for i in range(len(tree)):
        if tree[i].value == word1:
            node1 = tree[i]
        if tree[i].value == word2:
            node2 = tree[i]
    if node1 in [None] and node2 in [None]:
        print '节点为空'
    len1 = Hight(node1)
    len2 = Hight(node2)
    while len1 > len2:
        left_path.append(node1.value + '↑')
        node1 = node1.parent
        len1 -= 1
    while len1 < len2:
        right_path.append('↓' + node2.value)
        node2 = node2.parent
        len2 -= 1

    while node1 and node2 and node1 != node2:
        left_path.append(node1.value + '↑')
        right_path.append('↓' + node2.value)
        node1 = node1.parent
        node2 = node2.parent

    if node1 == node2 and node1 not in [None]:
        left_path.append(node1.value)  # 根节点进来
        right_path.reverse()  # 逆转右边的数组
        for i in range(len(right_path)):
            left_path.append(right_path[i])
        relation = ''
        for i in range(len(left_path)):
            relation += left_path[i]
        print ('0' if flag == 'false' else '1') + '  %s 和 %s 的依赖关系是:  %s' % (w1, w2, relation)
    else:
        print ('0' if flag == 'false' else '1') + '  %s 和 %s :no common parent!!' % (word1, word2)


'''
    查找两个节点到-根节点-之间的路径
'''


def get_relation_path(w1, w2, node):
    left_path = []
    right_path = []
    for i in range(len(node)):
        if node[i].value == w1:
            temp = node[i]
            while True:
                if temp.parent:
                    if temp.parent.value != w2:
                        left_path.append(temp.value + '↑')
                        temp = temp.parent
                    else:
                        relation = ''
                        left_path.append(temp.value)
                        for j in range(len(left_path)):
                            relation += left_path[j]
                        print '%s 和 %s 的依赖关系是:  %s' % (w1, w2, relation)
                        return
                else:
                    break
            left_path.append(temp.value)
            break

    for i in range(len(node)):
        if node[i].value == w2:
            temp = node[i]
            while True:
                if temp.parent:
                    right_path.append('↓' + temp.value)
                    temp = temp.parent
                else:
                    break
            right_path.reverse()  # 逆转右边的数组
            for i in range(len(right_path)):
                left_path.append(right_path[i])
            break

    # print map(lambda x: x, [left_path[y] for y in range(len(left_path))])
    relation = ''
    for i in range(len(left_path)):
        relation += left_path[i]
    print ' %s 和 %s 的依赖关系是:  %s' % (w1, w2, relation)


def main():
    for i in range(len(word_pair)):
        tree = trees[i]
        for j in range(len(word_pair[i])):
            w1, w2 = word_pair[i][j]
            flag = flags[i][j]
            # get_relation_path(w1, w2, node)
            GetLastCommonAncestor(w1, w2, flag, tree)
        print '\n'


if __name__ == "__main__":
    main()
    # str = '[3H]-naloxone'
    # if str.find('-') != -1 and str.find('[') != -1 :
    # word1 = str.split('-')[-1]
    # print word1













