
# coding: utf-8

# In[65]:


from lxml import etree
from collections import OrderedDict
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import numpy as np
sns.set()


# In[41]:


datamap=OrderedDict()
datamap["android"]="android.stackexchange.com"
# datamap["dba"]="dba.stackexchange.com"
# datamap["softwareEng"]="softwareengineering.stackexchange.com"
# datamap["serverfault"]= "serverfault.com"
# datamap["superuser"]="superuser.com"
# datamap["stackoverflow"]="stackoverflow.com-"


# In[59]:


def read_tags(filename):
    logtags=[]
    for row in open(filename,"r"):
        logtags.append(row.split(",")[0].strip().lower())   
    return logtags

def read_prog_lang(filename):
    data=OrderedDict()
    f=open(filename,"r")
    for l in f:
        row=l.split("\t")
        key=row[0].lower().strip()
        data[key]=[]
        for element in row[1].split(","):
            data[key].append(element.strip().lower())
    return data

def atleast_one(a, b):
    return not set(a).isdisjoint(b)

def refine_tags(tags):
    if tags!=None:
        l=tags.split('><')
        l=[i.replace('>','').replace('<','').lower() for i in l]
        return l
    else:
        return ["???"]

def init_data(taglist):
    data=OrderedDict()
    for tag in taglist:
        data[tag]=OrderedDict()
        for fname in datamap:
            data[tag][fname]=0
    return data


# In[49]:


logtags=list(set(read_tags("logging - Sheet3.csv")))

prog_tags=read_prog_lang("logging - Sheet4.tsv")

for i in prog_tags:
    logtags.extend(prog_tags[i])
logtags=list(set(logtags))

# del logtags[logtags.index("")]


# In[57]:


def common_tag_csv(data):
    f=open("Sheet-2.csv","w")
    f.write(",")
    for fname in datamap:
        f.write(fname+",")
    f.write("\n")
    for tag in data:
        f.write(tag+",")
        for element in data[tag]:
            f.write(str(data[tag][element])+",")
        f.write("\n")
    f.close()
    
    fr=open("Sheet-2.csv","r")
    fw=open("Modified-Sheet-2.csv","w")
    fw.write(fr.readline())
    for l in fr:
        row=l.split(",")
        temp=Counter(row)
        print(temp)
        if temp['0'] <=4:
            fw.write(l)
    fw.close()
    fr.close()
        
        


# In[51]:


def count_tags(taglist):
    data=init_data(taglist)
    #print(data)
    for fname in datamap:
        print(fname)
        if fname=="stackoverflow" and datamap[fname]=="stackoverflow.com-":
            datamap[fname]=datamap[fname]+"Tags"
        f=open("data/"+datamap[fname]+"/Tags.xml","rb")
        next(f)
        next(f)
        count=0
        for l in f:
            try:
                rows=etree.XML(l)  
                if  rows.get("TagName").lower() in taglist:
                    tagname=rows.get("TagName").lower()
                    question=rows.get("Count")
                    data[tagname][fname]=question
                    count=count+int(question)
                    #print(tagname,question)
            except:
                print(l)
               

        print(count)
    return data


# In[58]:


# data=count_tags(logtags)
# common_tag_csv(data)


# In[66]:


def plot_monthly_bargraph(plt,data,title,label,opr):
    # plt.close()
    # plt.clf()
    if opr==1:
        color='b'
    else:
        color='g'
    y=[data[i] for i in data]
    x=[i for i in range(len(data))]
    xticks=[i.split('-')[0] for i in data]
    plt.bar(x,y,label=label,color=color)
    gap=1
    plt.xticks(x[::gap],xticks[::gap],rotation=30)
    #plt.title(title.upper())
    plt.ylabel("No. of Questions")
    return plt
    # if opr==1:
    #     plt.savefig("Images/"+title+".png")
    # else:
    #     plt.show()
    # plt.clf()

    
def plot_monthly_cumgraph(plt,data,title,label,opr):
    if opr==1:
        color='b'
        marker=","
    else:
        color='g'
        marker="o"
    y=np.cumsum([data[i] for i in data])
    x=[i for i in range(len(data))]
    xticks=[i.split('-')[0] for i in data]
    plt.plot(x,y,color=color)
    plt.scatter(x,y,marker=marker,label=label,color=color)
    gap=1
    plt.xticks(x[::gap],xticks[::gap],rotation=30)
    #plt.title(title.upper())
    plt.ylabel("No. of Questions")
    # if opr==1:
    #     plt.savefig("Images/"+title+".png")
    # else:
    #     plt.show()
    # plt.clf()
    return plt

def init_o_data():
    data=OrderedDict()
    start_year=2008
    start_month=8
    end_year=2017
    end_month=12
    month=1
    for year in range(start_year,end_year+1):
       # for month in range(start_month,end_month+1):
            #print(year,month)
            temp=str(month)
            if len(temp)==1:
                temp="0"+temp
            data[str(year)]=0
        #start_month=1
    return data


# In[61]:


def distribute_posts(website,logtags):
    if fname=="stackoverflow" and datamap[fname]=="stackoverflow.com-":
        datamap[fname]=datamap[fname]+"Posts"   
    
    f=open("C:/Users/harshitgujral/Desktop/Stack/data/"+datamap[website]+"/Posts.xml","rb")
    next(f)
    next(f)
    data=init_o_data()
    data_all=init_o_data()
    count=0
    fr=open("ans."+fname+".txt","w")
    for l in f:
        try:
            row=etree.XML(l)      
            posttypeid=row.get("PostTypeId") 
            acceptedanswerID=row.get("AcceptedAnswerId")
            tags=refine_tags(row.get("Tags"))
            if posttypeid=="1":
                if atleast_one(tags,logtags):
                        date=row.get("CreationDate")
                        print(date)
                        key=date.split("T")[0][0:4]
                        if key not in data_all:
                            data_all[key]=0
                        data_all[key]+=1
            
            if posttypeid=="1" and acceptedanswerID!=None:
                # Means it has an accepted answer
                if atleast_one(tags,logtags):
                    # Atleast one logging tag

                    #print(tags)
                    date=row.get("CreationDate")
                    fr.write(acceptedanswerID+","+date+"\n")

                    key=date.split("T")[0][0:4]
                    if key not in data:
                        data[key]=0
                    data[key]+=1
        except:
            print(l)
    fr.close()
    return data, data_all


# In[68]:

for fname in list(datamap.keys()):
    data, data_all=distribute_posts(fname,logtags)


# for fname in list(datamap.keys()):
#     try:
#         data=pickle.load(open(fname+".pickle","rb"))
#         data_all=pickle.load(open(fname+".all.pickle","rb"))
#     except:
#         data, data_all=distribute_posts(fname,logtags)
    
#     plt=plot_monthly_bargraph(plt,data_all,fname+": Logging Questions","Total Logging Questions",1)
#     plt=plot_monthly_bargraph(plt,data,fname+": Logging Questions with selected answers","Total Logging Questions with accepted answer",0)
#     plt=plot_monthly_cumgraph(plt,data_all,fname+": Cummulative Logging Questions","Cummulative Logging Questions",1)
#     plt=plot_monthly_cumgraph(plt,data,fname+": Cummulative Logging Questions with selected answers","Cummulative Logging Questions with accepted answer",0)
#     plt.title(fname.upper())
#     plt.legend(loc='upper left')
#     plt.show()
#     pickle.dump(data,open(fname+".pickle","wb"))
#     pickle.dump(data_all,open(fname+".all.pickle","wb"))

