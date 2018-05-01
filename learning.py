import math
from tree import Tree

TEST_DATA = "noisy_train.ssv"
LABEL = 0  # label column
TREE = []
data = open(TEST_DATA)
new_data = data.read().splitlines()
matrix = []
for sub_data in new_data:
    matrix.append(sub_data.split())
feature_list = matrix[1][1:]
final_matrix = matrix[3:]
label_yes = 0
label_no = 0
for i in final_matrix:
    if i[0] == '0':
        label_no += 1
    else:
        label_yes += 1
# making a list that contain features and their attrs
feature_matrix = []
for finale in final_matrix:
    feature_matrix.append(finale[1:])
# making a list of lists that contain labels of each row
label_matrix = []
for m in final_matrix:
    label_matrix.append(m[0])


def entropy(n1, n2):
    total = n1 + n2
    ent = -(n1/total)*math.log(n1/total, 2) - (n2/total)*math.log(n2/total, 2)
    return ent


def gain(l_matrix, f_matrix, feature_list_g, feature, yes, no):
    e = entropy(yes, no)
    attr = {}
    for item in f_matrix:
        if item[feature_list_g.index(feature)] not in attr:
            if l_matrix[f_matrix.index(item)] == '0':
                attr[item[feature_list_g.index(feature)]] = {'no': 1}
            else:
                attr[item[feature_list_g.index(feature)]] = {'yes': 1}
        else:
            if l_matrix[f_matrix.index(item)] == '0':
                if 'no' in attr[item[feature_list_g.index(feature)]]:
                    attr[item[feature_list_g.index(feature)]]['no'] += 1
                else:
                    attr[item[feature_list_g.index(feature)]]['no'] = 1
            else:
                if 'yes' in attr[item[feature_list_g.index(feature)]]:
                    attr[item[feature_list_g.index(feature)]]['yes'] += 1
                else:
                    attr[item[feature_list_g.index(feature)]]['yes'] = 1
    ig = e
    for x in attr:
        if 'yes' in attr[x] and 'no' in attr[x]:
            ig = ig - (int(attr[x]['yes'])+int(attr[x]['no']))/(yes+no)*entropy(int(attr[x]['yes']), int(attr[x]['no']))
    return ig, attr


def find_root(lab_matrix, new_matrix, attr_list, yes_num, no_num):
    tup_list = {}
    for j in attr_list:
        temp = gain(lab_matrix, new_matrix, attr_list, j, yes_num, no_num)
        tup_list[temp[0]] = [j, temp[1]]
    root = max([q for q in tup_list])
    return tup_list[root]  # , root


def rebuild_matrix(feature, features_list, factor, main_matrix, label_list):
    feature_index = features_list.index(feature)
    features_list.remove(feature)
    new_matrix = []
    new_label = []
    for row in main_matrix:
        if row[feature_index] == factor:
            temp = row
            temp.pop(feature_index)
            new_matrix.append(temp)
            new_label.append(label_list[main_matrix.index(row)])
    return new_label, new_matrix, features_list


def build_tree(f_mat, f_list, l_list, ly, ln):
    builder = find_root(l_list, f_mat, f_list, ly, ln)
    temp_attr = [q for q in builder[1]]
    TREE.append([builder[0], temp_attr])
    for item in temp_attr:
        if 'yes' in builder[1][item] and 'no' in builder[1][item]:
            n_l, n_m, f_l = rebuild_matrix(builder[0], f_list, item, f_mat, l_list)
            TREE.append([builder[0], item, build_tree(n_m, f_l, n_l, builder[1][item]['yes'], builder[1][item]['no'])])
        else:
            if 'yes' in builder[1][item]:
                TREE.append([builder[0], item, True])
            else:
                TREE.append([builder[0], item, False])
    return TREE


a = build_tree(feature_matrix, feature_list, label_matrix, label_yes, label_no)
print(a)
# print(find_root(feature_matrix, feature_list, label_yes, label_no))
