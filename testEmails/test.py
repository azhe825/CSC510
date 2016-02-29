from __future__ import print_function, division
from func import *
import pickle
import cPickle
from demos import cmd

def no_incremental(label,matrix,Classify):
    train,test=split_data(label)
    clf=Classify(label[train],matrix[train])
    prediction=clf.predict(matrix[test])
    return evaluate(label[test],prediction)

def dict_add(old,new):
    if not type(new) == type({}):
        try:
            old.append(new)
        except:
            old=[new]
    else:
        for key in new:
            if key in old:
                pass
            elif type(new[key])==type({}):
                old[key]={}
            else:
                old[key]=[]
            dict_add(old[key],new[key])
    return old


def incremental(label,matrix,Classify):

    def check_pool(pool,step_count):
        return all([len(pool[key])>=step_count for key in pool])


    step_count=1
    step=1
    total=5
    pool={}
    dict={}
    for key in set(label):
        pool[key]=[]
        dict[key]={}
    dict['F_M']={}
    XX=map(str,range(10,10+total,step))

    train,test=split_data(label)
    clf=Classify(label[train],matrix[train])
    prediction=clf.predict(matrix[test])
    dict_tmp=evaluate(label[test],prediction)
    for key in dict:
        dict[key][XX[0]]=dict_tmp[key]

    shuffle(test)
    collect=[]
    for ind in test:
        collect.append(ind)
        try:
            pool[label[ind]].append(ind)
        except:
            pool[label[ind]]=[ind]
        if check_pool(pool,step_count):
            # add=[]
            # for key in pool:
            #     add.extend(list(np.random.choice(pool[key],step_count,replace=False)))
            add=collect
            test_new=list(set(test)-set(collect))
            clf=Classify(label[train+add],matrix[train+add])
            prediction=clf.predict(matrix[test_new])
            dict_tmp=evaluate(label[test_new],prediction)
            for key in dict_tmp:
                dict[key][str(10+step_count)]=dict_tmp[key]
            step_count=step_count+step
            if step_count>total:
                break
    return dict

def incremental2(label,matrix,Classify):


    step_count=1
    step=1
    total=10
    dict={}
    for key in set(label):
        dict[key]={}
    dict['F_M']={}
    XX=map(str,range(10,10+total,step))

    train,test=split_data(label)
    clf=Classify(label[train],matrix[train])
    prediction=clf.predict(matrix[test])
    dict_tmp=evaluate(label[test],prediction)
    for key in dict:
        dict[key][XX[0]]=dict_tmp[key]

    shuffle(test)
    collect=[]
    for ind in test:
        collect.append(ind)

        if len(collect)==step_count*100:
            add=collect

            test_new=list(set(test)-set(collect))
            clf=Classify(label[train+add],matrix[train+add])
            prediction=clf.predict(matrix[test_new])
            dict_tmp=evaluate(label[test_new],prediction)
            for key in dict_tmp:
                dict[key][str(10+step_count)]=dict_tmp[key]
            step_count=step_count+step
            if step_count>total:
                break
    return dict



def _test(filename):
    filepath='../Cleaned_Data/'
    filetype='.txt'
    classifiers = [do_SVM, do_KNN]
    c_name = ['SVM_','KNN_']
    # **** spicify the classifier below.  ****
    c_id = 0
    Classify=classifiers[c_id] #do_SVM
    repeats=10
    experiment=incremental2

    label,matrix=preprocess(filepath+filename+filetype)
    result={}

    for i in xrange(repeats):
        dict_tmp=experiment(label,matrix,Classify)
        dict_add(result,dict_tmp)
    print(result)
    print(result['F_M'])
    save(result,c_name[c_id]+filename)


if __name__ == '__main__':
    eval(cmd())
