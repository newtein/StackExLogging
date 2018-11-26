
# coding: utf-8

# In[65]:


from lxml import etree
from collections import OrderedDict
from collections import Counter
import pickle
import numpy as np



# In[41]:


datamap=OrderedDict()
# datamap["android"]="android.stackexchange.com"
# datamap["dba"]="dba.stackexchange.com"
# datamap["softwareEng"]="softwareengineering.stackexchange.com"
# datamap["serverfault"]= "serverfault.com"
# datamap["superuser"]="superuser.com"
datamap["stackoverflow"]="C:/"


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

        
output_location = 'C:/Users/harshitgujral/Desktop/Stack/output/'

# In[51]:



def distribute_posts(website,logtags):
  
    f=open(datamap[website]+"/Posts.xml","rb")
    fo=open(output_location+"logging{}.csv".format(website),"w")

    next(f)
    next(f)
    for l in f:
        try:
            row=etree.XML(l)      
            posttypeid=row.get("PostTypeId") 
            acceptedanswerID=row.get("AcceptedAnswerId")
            tags=refine_tags(row.get("Tags"))
            Id=row.get("Id")
            if posttypeid=="1":
                if atleast_one(tags,logtags):
                        fo.write(Id+'\n')
                        
            
      
        except etree.XMLSyntaxError:
            # Used to skip last XML Tag '</post>' 
            print("Completed",website,l)

    fo.close()
    f.close()
    return 


# In[68]:

for fname in list(datamap.keys()):
    distribute_posts(fname,logtags)


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

