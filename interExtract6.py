__author__ = 'Administrator'
from datetime import datetime

n_date = datetime.now().date()
print datetime.now().strftime('%Y-%m-%d %H:%M')

article_list = []  # ==list
all_list = []  # save all article sentence list   ==all
entity_pairss_list = []  # all entities in articles
inter_sentence_list = []  # inter sentence relation match list
inter_sentence_list_right = []  # inter sentence relation match list
relation_lists = []  # relation


class Title(object):
    def __init__(self, doc_id, type, content):
        self.doc_id = doc_id
        self.type = type
        self.content = content

    def get_doc_id(self):
        return self.doc_id

    def get_type(self):
        return self.type

    def get_content(self):
        return self.content


class Label(object):
    def __init__(self, doc_id, index_start, index_end, entity, type, ent_id):
        self.doc_id = doc_id
        self.index_start = index_start
        self.index_end = index_end
        self.entity = entity
        self.type = type
        self.ent_id = ent_id

    def get_doc_id(self):
        return self.doc_id

    def get_index_start(self):
        return self.index_start

    def get_index_end(self):
        return self.index_end

    def get_entity(self):
        return self.entity

    def get_type(self):
        return self.type

    def get_ent_id(self):
        return self.ent_id


class Relation(object):
    def __init__(self, doc_id, relation, chem_id, dis_id):
        self.doc_id = doc_id
        self.relation = relation
        self.chem_id = chem_id
        self.dis_id = dis_id

    def get_doc_id(self):
        return self.doc_id

    def get_relation(self):
        return self.relation

    def get_chem_id(self):
        return self.chem_id

    def get_dis_id(self):
        return self.dis_id


class Article(object):
    def __init__(self, title, abstract, label, relation):
        self.title = title
        self.abstract = abstract
        self.label = label
        self.relation = relation

    def get_title(self):
        return self.title

    def get_abstract(self):
        return self.abstract

    def get_label(self):
        return self.label

    def get_relation(self):
        return self.relation


def read(filename):
    f = open(filename)
    flag = True
    while flag:
        t_and_a = []
        label_list = []  # label list
        relation_list = []  # relation list
        for i in range(0, 2):
            t_and_a.append(f.readline())
        index_doc_id = t_and_a[0].find('|t|')
        doc_id = t_and_a[0][:index_doc_id]
        title_str = t_and_a[0][index_doc_id + 3:]
        abstract_str = t_and_a[1][index_doc_id + 3:]
        title = Title(doc_id, 'title', title_str)
        abstract = Title(doc_id, 'abstract', abstract_str)
        temp = f.readline()
        while temp != '\n':
            if not temp:  # read off the file
                break
            row = temp.split('\t')
            column2 = row[1]
            if column2 != 'CID':
                index_start = int(row[1])
                index_end = int(row[2])
                entity = str(row[3])
                type = row[4]
                ent_id = row[5].strip('\n')
                label = Label(doc_id, index_start, index_end, entity, type, ent_id)
                label_list.append(label)
            else:
                chem_id = str(row[2])
                dis_id = str(row[3])
                relation = Relation(doc_id, 'CID', chem_id, dis_id)
                relation_list.append(relation)
            temp = f.readline()
        article = Article(title, abstract, label_list, relation_list)
        article_list.append(article)
        flag = temp
    # for i in range(len(article_list)):
    # print article_list[i].get_title().get_content()
    f.close()


def write(article_list, filename):
    with open(filename, 'w+') as file:
        for num in xrange(len(article_list)):
            titles = article_list[num].get_title().get_content().strip('\n')
            abstracts = article_list[num].get_abstract().get_content().strip('\n')
            article = titles + ' ' + abstracts
            labels = article_list[num].get_label()
            file.write('article' + str(num) + ': ' + article + '\n')
            for i in xrange(len(labels)):
                doc_id = str(labels[i].get_doc_id())
                start = str(labels[i].get_index_start())
                end = str(labels[i].get_index_end())
                entity = str(labels[i].get_entity())
                type = str(labels[i].get_type())
                ent_id = str(labels[i].get_ent_id())
                file.write('Entity: ' + doc_id + '\t' + start + '\t' + end + '\t' +
                           entity + '\t' + type + '\t' + ent_id + '\n')
            relations = article_list[num].get_relation()
            for i in xrange(len(relations)):
                doc_id = relations[i].get_doc_id()
                relation = relations[i].get_relation()
                chem_id = relations[i].get_chem_id()
                dis_id = relations[i].get_dis_id()
                file.write('Relation: ' + doc_id + '\t' +
                           relation + '\t' + chem_id + '\t' + dis_id + '\n')


def search_index(article, position):
    index = article.find('. ', position)
    index1 = article.find('? ', position)
    if index1 != -1:
        if index1 < index:
            index = index1
    return index


def article2list(article_list):
    for num in xrange(len(article_list)):
        sentence_list = []
        titles = article_list[num].get_title().get_content().strip('\n')
        abstracts = article_list[num].get_abstract().get_content().strip('\n')
        article = titles + ' ' + abstracts
        index = search_index(article, 0)
        if article[index + 2] != article[index + 2].lower():
            sentence_list.append(article[:index + 1])
        index2 = search_index(article, index + 1)
        while index2 != -1:
            if article[index2 + 2] != article[index2 + 2].lower():
                sentence_list.append(article[index + 2: index2 + 1])
            else:
                index2 = search_index(article, index2 + 1)
                continue
            index = index2
            index2 = search_index(article, index2 + 1)
        # index2 = article.find('.', index+1)  # add the last one sentence
        sentence_list.append(article[index + 2:])
        all_list.append(sentence_list)
    # print len(all_list)
    # print len(all_list[4])  #13sentences


def findEntityInEachSentence2list(allArticleList):  # article_list
    entity_pair_list = []  # one sentence include ent
    entity_pairs_list = []  # one article include ent

    for num in xrange(len(allArticleList)):
        titles = allArticleList[num].get_title().get_content().strip('\n')
        abstracts = allArticleList[num].get_abstract().get_content().strip('\n')
        article = titles + ' ' + abstracts
        # if num == 11:print article
        label_list = allArticleList[num].get_label()
        index = search_index(article, 0)
        if index != -1:
            while article[index + 2] == article[index + 2].lower():
                index = search_index(article, index + 1)
        number = 1  #The number of words in the sentence
        index2 = -2
        for i in xrange(len(label_list)):
            docid = label_list[i].get_doc_id()
            start = label_list[i].get_index_start()
            end = label_list[i].get_index_end()
            entity = str(label_list[i].get_entity())
            type = str(label_list[i].get_type())
            ent_id = str(label_list[i].get_ent_id())
            if ent_id == '-1':  #1.remove the corpus data row which entid=-1
                continue
            if index != -1:
                # if end < index + 1:
                # 	pass
                # else:
                while end > index + 1:
                    try:
                        entity_pairs_list.append(entity_pair_list)  # MemoryError!!
                    except Exception, e:
                        print 'Invalid input', e
                    # except(MemoryError),e:
                    # 	print 'error: ', e
                    finally:
                        print 'end:     ' + str(end)
                        print 'index+1: ' + str(index + 1)
                        print entity_pairs_list
                    entity_pair_list = []
                    number += 1
                    index2 = index
                    index = search_index(article, index2 + 1)
                    # if docid == '6466532':
                    # # 	print index	#922

                    if index != -1:
                        while article[index + 2] == article[index + 2].lower():
                            index = search_index(article, index + 1)
                            # if docid == '6466532':
                            # 	print index  # 922
                            if index == -1:
                                break
                        if index == -1:
                            break
                    else:
                        break
                # while index != -1:
                # 	if article[index + 2] == article[index + 2].lower():
                # 		index = search_index(article, index + 1)
                # 	else: break
            else:
                pass
            # ent = article[start:end]
            # entity = ent[0].lower() + ent[1:]  # 2.Let the first letters lowercase
            # entity_pair_list.append(str(docid) + "	" + str(start) + "	"
            # 						+ str(end) + "	" + entity + "	" + type + "	" + ent_id + "	" + str(
            # 	number))
            # the last step is important: remember append the last entitypair!
            ent = article[start:end]
            entity = ent[0].lower() + ent[1:]  # 2.Let the first letters lowercase
            entity_pair_list.append(str(docid) + "	" + str(start) + "	"
                                    + str(end) + "	" + entity + "	" + type + "	" + ent_id + "	" + str(
                number))
        entity_pairs_list.append(entity_pair_list)
        while index != len(article) - 1 and index != -1:
            index = search_index(article, index + 1)
            if index != -1:
                while article[index + 2] == article[index + 2].lower():
                    index = search_index(article, index + 1)
                    if index == -1:
                        index = len(article) - 1
                        break
            entity_pairs_list.append([])
        entity_pairss_list.append(entity_pairs_list)
        entity_pair_list = []
        entity_pairs_list = []
    # print len(entity_pairss_list[4])
    # print len(all_list[4])
    # for i in xrange(len(entity_pairss_list)):
    # 	print entity_pairss_list[i]


def rule1(sj1, entities_in_current_sentence, entityk):
    # Determine whether there is a co-occurrence between C and D
    original_type = entityk.split('\t')[4]
    for x in xrange(len(sj1)):
        entitykx = sj1[x]
        next_type = entitykx.split('\t')[4]
        next_entity = entitykx.split('\t')[3]
        next_id = entitykx.split('\t')[5]
        current_id = entityk.split('\t')[5]
        if original_type != next_type:
            if next_entity not in entities_in_current_sentence:
                if inter_sentence_list == []:
                    if original_type == 'Chemical':
                        relation_l = entityk.split('\t')
                        relation_r = entitykx.split('\t')
                    else:
                        relation_l = entitykx.split('\t')
                        relation_r = entityk.split('\t')
                    relation_l = relation_l[0] + '\t' + 'CID' + '\t' + relation_l[1] + '\t' + relation_l[2] + '\t' + \
                                 relation_l[-2] + '\t'
                    relation_r = relation_r[1] + '\t' + relation_r[2] + '\t' + relation_r[-2]
                    inter_sentence_list.append(relation_l)
                    inter_sentence_list_right.append(relation_r)
                else:
                    # 4. Filter the row with the same id.Can not stop?
                    temp = []
                    for i in xrange(len(inter_sentence_list)):
                        chem_id = inter_sentence_list[i].split('\t')[4]
                        dis_id = inter_sentence_list_right[i].split('\t')[2]
                        temp.append([chem_id, dis_id])
                    if [current_id, next_id] not in temp:
                        if [next_id, current_id] not in temp:
                            if original_type == 'Chemical':
                                relation_l = entityk.split('\t')
                                relation_r = entitykx.split('\t')
                            else:
                                relation_l = entitykx.split('\t')
                                relation_r = entityk.split('\t')
                            relation_l = relation_l[0] + '\t' + 'CID' + '\t' + relation_l[1] + '\t' + relation_l[
                                2] + '\t' + relation_l[-2] + '\t'
                            relation_r = relation_r[1] + '\t' + relation_r[2] + '\t' + relation_r[-2]
                            inter_sentence_list.append(relation_l)
                            inter_sentence_list_right.append(relation_r)
                        # existing_relation.append([left_id, right_id])
            else:
                continue  # cooccurrence
        else:
            continue

        # print inter_sentence_list + inter_sentence_list_right


def rule2(current_sentence, article):  # 3. find later two sentence:set distance = 2
    if current_sentence + 2 < len(article):
        sj1 = article[current_sentence + 1]
        sj2 = article[current_sentence + 2]
    elif current_sentence + 1 < len(article):
        sj1 = article[current_sentence + 1]
        sj2 = []
    else:
        sj1 = []
        sj2 = []
    return [sj1, sj2]


def inter_sentence_match(entity_pairss_list):
    existing_relation = []
    # print entity_pairss_list[79][0][0].split('\t')[0]	########19308880
    for i in xrange(len(entity_pairss_list)):
        article_level_entity = entity_pairss_list[i]
        # if i==79: print article_level_entity
        temp = inter_sentence_list
        for j in xrange(len(article_level_entity)):
            sentence_level_entity = article_level_entity[j]
            # if i==79 and j==2: print sentence_level_entity
            # ['19308880\t0\t9\tconfusion\tDisease\tD003221\t1', '19308880\t55\t68\tvalproic acid\tChemical\tD014635\t1']
            entities_in_sentence = []
            for z in xrange(len(sentence_level_entity)):
                entity = sentence_level_entity[z].split('\t')[3]
                entities_in_sentence.append(entity)
            sj1 = rule2(j, article_level_entity)[0]
            sj2 = rule2(j, article_level_entity)[1]
            for k in xrange(len(sentence_level_entity)):
                entityk = sentence_level_entity[k]
                # if i == 79: print entityk
                rule1(sj1, entities_in_sentence, entityk)
                rule1(sj2, entities_in_sentence, entityk)
        existing_relation = []  # not sure!!

    for i in xrange(len(inter_sentence_list)):
        print inter_sentence_list[i] + '\t' + inter_sentence_list_right[i]


def get_relation_sentence(inter_sentence_list):
    list = []
    for i in xrange(len(inter_sentence_list)):
        left = inter_sentence_list[i]
        right = inter_sentence_list_right[i]
        list.append(left + right)
        if i + 1 < len(inter_sentence_list):
            left1 = inter_sentence_list[i + 1]
            if left.split('\t')[0] != left1.split('\t')[0]:  # whether in same article
                relation_lists.append(list)
                list = []
    relation_lists.append(list)
    doc_id = []
    for i in xrange(len(relation_lists)):
        doc_id.append(relation_lists[i][0].split('\t')[0])
    for j in xrange(len(article_list)):
        doc_in = article_list[j].get_relation()[0].get_doc_id()
        if doc_in not in doc_id:
            print str(j) + '	' + doc_in
            relation_l = 'dontknow' + '\t' + 'CID' + '\t' + '11' + '\t' + '22' + '\t' + '-22' + '\t'
            relation_r = '00' + '\t' + '22' + '\t' + '-22'
            # inter_sentence_list.insert(j, relation_l)
            # inter_sentence_list_right.insert(j, relation_r)
            relation_lists.insert(j, [relation_l + relation_r])


def result_of_extraction():
    good_entity = []
    good_relation = []

    def get_start_list(entity_pair_list):
        for a in xrange(len(entity_pair_list)):
            good_entity.append('Entity: ' + str(entity_pair_list[a]) + '\n')
            start_index = str(entity_pair_list[a]).split('\t')[1]
            start_list.append(start_index)

    def add_entity(file):
        for i in xrange(len(good_entity)):
            file.write(good_entity[i])
        # def add_entity(file, entity_pair_list):
        # for a in xrange(len(entity_pair_list)):

    # 		file.write('Entity: ' + str(entity_pair_list[a]) + '\n')
    # 		start_index = str(entity_pair_list[a]).split('\t')[1]
    # 		start_list.append(start_index)

    def judge_relation(relation_lists, true_relation):
        true_relations = []
        for i in range(len(true_relation)):
            a = true_relation[i].get_chem_id().strip('\n')
            b = true_relation[i].get_dis_id().strip('\n')
            true_relations.append([a, b])
        for x in xrange(len(relation_lists)):
            start1 = relation_lists[x].split('\t')[2]
            start2 = relation_lists[x].split('\t')[5]
            chem_id = relation_lists[x].split('\t')[4]
            dis_id = relation_lists[x].split('\t')[7]
            # print [chem_id, dis_id]
            if start1 in start_list and start2 in start_list:
                if [chem_id, dis_id] in true_relations:
                    good_relation.append('Relation: ' + relation_lists[x] + '\t' + '1' + '\n')
                else:
                    good_relation.append('Relation: ' + relation_lists[x] + '\t' + '0' + '\n')
            else:
                continue
        return good_relation


    def add_relation(file):
        for i in xrange(len(good_relation)):
            file.write(good_relation[i])

    start_list = []  # save start index to list
    with open('f.txt', 'w') as f:
        for num in xrange(len(all_list)):
            # print str(num + 1) + 'th article\'s sentences number is :' + str(len(all_list[num]))
            sentence_list = all_list[num]
            true_relation = article_list[num].get_relation()
            for i in xrange(len(sentence_list)):
                if i + 2 < len(sentence_list):
                    for j in range(i + 1, i + 3):
                        if entity_pairss_list[num][i] == [] and entity_pairss_list[num][j] == []:
                            continue
                        get_start_list(entity_pairss_list[num][i])
                        get_start_list(entity_pairss_list[num][j])
                        # print good_entity
                        if judge_relation(relation_lists[num], true_relation) == []:
                            start_list = []
                            good_entity = []
                            good_relation = []
                            continue
                        # print good_relation
                        f.write('Sentence1: ' + sentence_list[i] + '\n')
                        f.write('Sentence2: ' + sentence_list[j] + '\n')
                        add_entity(f)
                        add_relation(f)
                        start_list = []
                        good_entity = []
                        good_relation = []
                        f.write('\n')

                elif i + 1 < len(sentence_list):
                    if entity_pairss_list[num][i] == [] and entity_pairss_list[num][i + 1] == []:
                        continue
                    get_start_list(entity_pairss_list[num][i])
                    get_start_list(entity_pairss_list[num][i + 1])
                    # print good_entity
                    if judge_relation(relation_lists[num], true_relation) == []:
                        start_list = []
                        good_entity = []
                        good_relation = []
                        continue
                    f.write('Sentence1: ' + sentence_list[i] + '\n')
                    f.write('Sentence2: ' + sentence_list[i + 1] + '\n')
                    add_entity(f)
                    add_relation(f)
                    start_list = []
                    good_entity = []
                    good_relation = []
                    f.write('\n')
                else:
                    continue

# read('s.txt')
# read('test.txt')
# read('test1.txt')
# read('test2.txt')
read('F:\Python Location\untitled\CDR_TrainDevSet.PubTabor.txt')
# write(article_list, 'f.txt')
article2list(article_list)
findEntityInEachSentence2list(article_list)
inter_sentence_match(entity_pairss_list)
get_relation_sentence(inter_sentence_list)
# supplement_relation(relation_lists)

print 'have ' + str(len(relation_lists)) + ' article relation.'
print 'Article\'s amount is : ' + str(len(all_list)) + '\n'

result_of_extraction()

with open('inter_relation.txt', 'w+') as ie:
    ie.write('each article\'s relation pair:' + '\n')
    for i in xrange(len(relation_lists)):
        ie.write(str(relation_lists[i]) + '\n')
        #lack of 19308880 relation??


