from __future__ import print_function, division
from func import *
import pickle
import cPickle
from demos import cmd
import matplotlib.pyplot as plt

classifiers = [do_SVM, do_KNN, do_DT]
c_name = ['SVM_','KNN_','DT_']

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
    XX=map(str,range(100,100+total*100,step*100))

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
                dict[key][str(100+step_count*100)]=dict_tmp[key]
            step_count=step_count+step
            if step_count>total:
                break
    return dict

def _test(filename, classifier_id):
    filepath='../Cleaned_Data/'
    filetype='.txt'
    # classifiers = [do_SVM, do_KNN, do_MNB]
    # c_name = ['SVM_','KNN_','MNB_']
    # **** spicify the classifier below.  ****
    #c_id = 2
    # ****************************************
    Classify=classifiers[classifier_id] #do_SVM
    repeats=10
    experiment=incremental2

    label,matrix=preprocess(filepath+filename+filetype)
    result={}

    for i in xrange(repeats):
        dict_tmp=experiment(label,matrix,Classify)
        dict_add(result,dict_tmp)
        print(str(i)+" finished")
    with open('./dump/'+c_name[classifier_id]+'_'+filename+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)

def _test2(filename):
    filepath='../Cleaned_Data/'
    filetype='.txt'
    # classifiers = [do_SVM, do_KNN, do_MNB]
    # c_name = ['SVM_','KNN_','MNB_']
    # **** spicify the classifier below.  ****
    c_id = 2
    # ****************************************
    Classify=classifiers[c_id] #do_SVM
    repeats=10
    experiment=incremental2

    label,matrix=preprocess(filepath+filename+filetype)
    result={}

    for i in xrange(repeats):
        dict_tmp=experiment(label,matrix,Classify)
        dict_add(result,dict_tmp)
        print(str(i)+" finished")
    with open('./dump/'+c_name[c_id]+'_'+filename+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)
    #save(result,c_name[c_id]+filename)

def col_result():
    ## to get the results
    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']
    # for dataset in datalist:
    #     # f = _test2(dataset)
    #     for i in xrange(len(classifiers)):
    #         f = _test(dataset,i)

    # load the results and pic them for different folders.
    for what in c_name:
        draw(what)
    # load the resultsa dn pic them for different classifiers.
    draw2()

def draw(what):
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)

    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']


    plt.figure()
    result={}
    for filename in datalist:
        with open('./dump/'+what+'__'+filename+'.pickle', 'rb') as handle:
            result[filename] = pickle.load(handle)
        tmp=result[filename]['F_M']
        ind=np.argsort(map(int,tmp.keys()))
        X=np.array(tmp.keys())[ind]
        Y=np.array(tmp.values())[ind]
        line,=plt.plot(X,map(np.median,Y),label=filename+" median")
        plt.plot(X,map(iqr,Y),"-.",color=line.get_color(),label=filename+" iqr")
    plt.xticks(np.arange(100,1100,100))
    plt.yticks(np.arange(0,1.0,0.2))
    plt.ylabel("F_M score")
    plt.xlabel("Training Size")
    plt.legend(bbox_to_anchor=(0.35, 1), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("../Results/semi_" + what + ".eps")
    plt.savefig("../Results/semi_" + what + ".png")

def draw2():
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)

    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']


    plt.figure()
    result={}
    Y_ave = []
    # Y_total = []
    for classifier in c_name:
        for filename in datalist:
            with open('./dump/'+classifier+'_'+filename+'.pickle', 'rb') as handle:
                result[filename] = pickle.load(handle)
            tmp=result[filename]['F_M']
            if(tmp.__contains__('1100')):
                tmp.pop('1100')
            ind=np.argsort(map(int,tmp.keys()))
            X=np.array(tmp.keys())[ind]
            Y=np.array(tmp.values())[ind]
            if Y_ave == []:
                Y_ave = map(np.median,Y)
            else:
                tmp = map(np.median,Y)
                Y_ave = np.add(Y_ave, tmp)
            # if Y_total == [] :
            #     Y_total = Y
            # else:
            #     Y_total = np.add(Y_total, Y)
        Y_ave = map(lambda x:x/10.0,Y_ave)
        # Y_total = map(lambda x:x/10.0,Y_total)
        line,=plt.plot(X,map(np.median,Y_ave),label=classifier+" median")
        # plt.plot(X,map(iqr,Y_total),"-.",color=line.get_color(),label=classifier+" iqr")
    plt.yticks(np.arange(0,1.0,0.2))
    plt.ylabel("F_M score")
    plt.xlabel("Training Size")
    plt.legend(bbox_to_anchor=(0.35, 1), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("../Results/semi_classifier.eps")
    plt.savefig("../Results/semi_classifier.png")




if __name__ == '__main__':
    eval(cmd())
