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

def incremental_credit(label,matrix,Classify):


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
    collect={}
    pool=[]
    for ind in test:
        pool.append(ind)
        if clf.predict(matrix[ind])==label[ind]:
            score=0.5
        else:
            score=1.0
        try:
            collect[label[ind]][ind]=score
        except:
            collect[label[ind]]={ind:score}

        if len(pool)==step_count*100:
            num=int(len(pool)/len(set(label)))
            add=[]
            for ll in collect:
                add.extend(list(np.array(collect[ll].keys())[np.argsort(collect[ll].values())][-num:]))

            test_new=list(set(test)-set(pool))
            clf=Classify(label[train+add],matrix[train+add])
            prediction=clf.predict(matrix[test_new])
            dict_tmp=evaluate(label[test_new],prediction)
            for key in dict_tmp:
                dict[key][str(100+step_count*100)]=dict_tmp[key]
            step_count=step_count+step
            if step_count>total:
                break
    return dict

def incremental_wrong(label,matrix,Classify):


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
    wrong=[]
    pool=[]
    for ind in test:
        pool.append(ind)
        if not clf.predict(matrix[ind])==label[ind]:
            wrong.append(ind)


        if len(pool)==step_count*100:

            test_new=list(set(test)-set(pool))
            clf=Classify(label[train+wrong],matrix[train+wrong])
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
    classifiers = [do_SVM, do_KNN, do_MNB]
    c_name = ['SVM_','KNN_','MNB_']
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

def _test2(filename,method):
    filepath='../Cleaned_Data/'
    filetype='.txt'
    Classify=do_SVM
    repeats=10

    exp={"wrong": incremental_wrong, "brutal": incremental2, "credit": incremental_credit}
    experiment=exp[method]
    label,matrix=preprocess(filepath+filename+filetype)
    result={}

    for i in xrange(repeats):
        dict_tmp=experiment(label,matrix,Classify)
        dict_add(result,dict_tmp)
        print(str(i)+" finished")
    with open('./dump/'+method+'_'+filename+'.pickle', 'wb') as handle:
        pickle.dump(result, handle)
    #save(result,c_name[c_id]+filename)

def draw_all():
    ## to get the results
    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']
    # for dataset in datalist:
    #     # f = _test2(dataset)
    #     for i in xrange(len(classifiers)):
    #         f = _test(dataset,i)

    # load the results and pic them for different folders.
    # for what in c_name:
    #     draw(what)
    # load the resultsa dn pic them for different classifiers.




def run_test():
    ## to get the results
    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']
    methods=["wrong","brutal","credit"]
    for method in methods:
        for dataset in datalist:
            _test2(dataset,method)
        draw(method)
    draw3()

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
        with open('./dump/'+what+'_'+filename+'.pickle', 'rb') as handle:
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

def draw_inc():
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)

    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']


    plt.figure()
    result={}
    methods=["wrong","brutal","credit"]
    Y={}
    X=range(len(datalist))
    for method in methods:
        Y[method]=[]
        for filename in datalist:
            with open('./dump/'+method+'_'+filename+'.pickle', 'rb') as handle:
                result[filename] = pickle.load(handle)
            tmp=result[filename]['F_M']['1000']
            Y[method].append(tmp)
        line,=plt.plot(X,map(np.median,Y[method]),label=method+" median")
        plt.plot(X,map(iqr,Y[method]),"-.",color=line.get_color(),label=method+" iqr")
    plt.yticks(np.arange(0,1.1,0.1))
    plt.xticks(X, datalist, rotation=70)
    plt.ylabel("F_M score")
    plt.xlabel("Data sets")
    plt.legend(bbox_to_anchor=(0.35, 1), loc=1, ncol = 1, borderaxespad=0.)
    plt.savefig("../Results/semi_methods_half.eps")
    plt.savefig("../Results/semi_methods_half.png")

def draw3():
    font = {'family' : 'normal',
            'weight' : 'bold',
            'size'   : 20}

    plt.rc('font', **font)
    paras={'lines.linewidth': 5,'legend.fontsize': 20, 'axes.labelsize': 30, 'legend.frameon': False,'figure.autolayout': True,'figure.figsize': (16,8)}
    plt.rcParams.update(paras)

    datalist=['beck-s','farmer-d','kaminski-v','kitchen-l','lokay-m','sanders-r','williams-w3']


    plt.figure()
    result={}
    for classifier in c_name:
        Y_100 = list()
        for filename in datalist:
            with open('./dump/'+classifier+'_'+filename+'.pickle', 'rb') as handle:
                result[filename] = pickle.load(handle)
            tmp = result[filename]['F_M']
            tmp100 = np.median(tmp['100'])
            t = Y_100 + [tmp100]
            Y_100 = t
        line,=plt.plot(range( len(datalist) ),Y_100,label=classifier)

    plt.xticks(range( len(datalist) ), (datalist))
    plt.yticks(np.arange(0,1.0,0.2))
    plt.ylabel("F_M score")
    plt.xlabel("Training Folder")
    plt.legend(bbox_to_anchor=(0.35, 1), loc=1, ncol = 1, borderaxespad=0.)

    plt.savefig("../Results/comp_classifier.eps")
    plt.savefig("../Results/comp_classifier.png")




if __name__ == '__main__':
    eval(cmd())
