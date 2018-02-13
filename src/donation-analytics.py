
# coding: utf-8

# In[97]:


#JGJ JSR
import math
import pandas as pd
import heapq as hq
from datetime import datetime


# In[98]:


#reads a line at a time as a df, returns that df
def read_line(line):
    line = line.split("|")
    cols = ['CMTE_ID', 'NAME', 'ZIP_CODE', 'TRANSACTION_DT', 'TRANSACTION_AMT', 'OTHER_ID']
    df = pd.DataFrame(columns=cols)
    namedline = [line[n] for n in {0,7,10,13,14,15}] #index corr. to each cols value in line list
    df.loc[0] = [word if word != '' else "empty" for word in namedline] #replace by word empty if missing value
    return df


# In[99]:


#removes rows corr. to empty values entries in all columns except in OTHER_ID i.e. validate for emptiness
def remove_empty(df):
    for val in df.loc[0, df.columns != 'OTHER_ID']:
        if val=="empty":
            return None
    return df


# In[100]:


#removes non-MMDDYYYY formats of TRANSACTION_DT
def vali_date(df):
    if len(df.iloc[0]['TRANSACTION_DT']) !=8:
        return None
    try:
        pd.to_datetime(df.iloc[0]['TRANSACTION_DT'], format='%m%d%Y', errors='raise')
        return df.iloc[0]['TRANSACTION_DT']
    except:
        return None


# In[101]:


#remove rows corr. to non-empty values in OTHER_ID i.e. for non-individual contributions
def non_indi_contri(df):
    if df.iloc[0]['OTHER_ID']!="empty":
        return None
    else:
        return df


# In[102]:


#validate for zip code length and reduce it to first 5 digits
def check_zip(df):
    if len(df.iloc[0]['ZIP_CODE']) < 5:
        return None
    df.iloc[0]['ZIP_CODE'] = df.iloc[0]['ZIP_CODE'][:5]
    return df.iloc[0]['ZIP_CODE']


# In[103]:


#concatenating name and zip code to generate unique ID for each donor
def generate_uid(df):
    df['UID'] = df['NAME'] + df['ZIP_CODE']
    return df.iloc[0]['UID']


# In[104]:


#reduce date to 4-digit year
def reduce_date(df):
    df['TRANSACTION_YR'] = df.iloc[0]['TRANSACTION_DT'][4:] 
    return df.iloc[0]['TRANSACTION_YR']


# In[105]:


#rounds down below 0.5 and rounds up 0.5 and above; since python 3 rounds down at 0.5; for percentile
def rounder(x):
    if float(x) % 1 >= 0.5:
        x = math.ceil(x)
    else:
        x = round(x)
    return (int (x))


# In[106]:


#checks for repeated donors- can be to diff. orgs, check if different years and same unique id 
def map_data(df,repeated,nonrepeated):
    uid = df.iloc[0]['UID']
    yr = df.iloc[0]['TRANSACTION_YR']
    if (uid in repeated.keys()): #repeated but check for year
        if yr > repeated[uid]:
            return True
        else:
            return False
    if (uid in nonrepeated.keys()): #non-repeated but check for year
        if (yr>nonrepeated[uid]):
            repeated[uid] = nonrepeated[uid] #keep first-time donation year as threshold
            del nonrepeated[uid]
            return True
        else:
            return False
    #first entry, so in non-repeated
    nonrepeated[uid] = yr
    return False #added but not repeat donor


# In[107]:


#calculates running percentile only for added and repeated donors using heaps
def running_percentile_calculator(df,prank,min_heap,max_heap):
    #atleast one line in data stream
    df['TRANSACTION_AMT'] = df['TRANSACTION_AMT'].astype('float64')
    amt = df.iloc[0]['TRANSACTION_AMT']
    if (len(max_heap) == 0):
        hq.heappush(max_heap,-amt)
    elif (len(max_heap) != 0 and -amt > max_heap[0]): #comparing new element to be inserted with previous percentile
        hq.heappush(max_heap,-amt)
    else:
        hq.heappush(min_heap,amt)
    #rebalancing the heaps since we want len(max_heap)=prank
    while(True):
        if(len(max_heap)<prank):
            hq.heappush(max_heap, -hq.heappop(min_heap))
        elif(len(max_heap)>prank):
            hq.heappush(min_heap, -hq.heappop(max_heap))
        else:
            break
    return -max_heap[0] #since dividing in ratio of percentile


# In[108]:


#checks for repeat donors and return all corr. details
def repeat_donor_amount(df,output,process_data,nums,pval,quart,idx,min_heap,max_heap):
    df['TRANSACTION_AMT'] = df['TRANSACTION_AMT'].astype('float64') #astype('float64') #simplistic assumption or #df.round()
    if (process_data): #added only if successive year entry encountered, repeat_donor if same UID
        cmte = df.iloc[0]['CMTE_ID']
        uid = df.iloc[0]['UID']
        amt = df.iloc[0]['TRANSACTION_AMT']
        yr = df.iloc[0]['TRANSACTION_YR']
        zip = uid[-5:]
        uniq = cmte+zip+yr
        #nearest rank-method for percentile where prank is ordinal rank
        prank = math.ceil(quart[0][0]*0.01*idx) #prank is calculated only for data streamed so far
        if(uniq in output.keys() and uniq in nums.keys()):
            output[uniq] = output[uniq] + amt
            nums[uniq] = nums[uniq] + 1
        else:
            output[uniq] = amt
            nums[uniq] = 1
        cum_amt = output[uniq]
        percnt = running_percentile_calculator(df,prank,min_heap,max_heap) #call only if added and repeated donor
        numcount = nums[uniq]
        if cum_amt.is_integer() :
            return (cmte,zip,yr,rounder(percnt),(int (cum_amt)),numcount)
        else:
            return (cmte,zip,yr,rounder(percnt),(float ("{0:.2f}".format(cum_amt))),numcount)
    else:
        return None


# In[109]:


#where all the streaming happens! performs the donation analysis
def donation_analysis(file_path):
    rqdcols = ['CMTE_ID', 'ZIP_CODE', 'TRANSACTION_YR', 'PERCENTILE', 'CUMULATIVE_CONTRIBUTIONS','COUNTER']
    nums = dict()
    output = dict()
    repeated = dict()
    nonrepeated = dict()
    pval = pd.Series()
    min_heap = []
    max_heap = []
    idx = 0
    quart = pd.read_csv('input/percentile.txt',header=None) #can change percentile value for each run
    if ('StreamedData' in vars()) == False:
        StreamedData = pd.DataFrame(columns= rqdcols)
    with open(file_path) as content:
        for x in content:
            line = read_line(x)
            dfline = remove_empty(line) 
            if (dfline is None): #if has empty values
                continue                
            if (vali_date(dfline) is None): #if the date is invalid
                continue
            if (non_indi_contri(dfline) is None): #if not just individual contributor
                continue
            if (check_zip(dfline) is None): #if zipcode is invalid
                continue
            uid = generate_uid(dfline)
            year = reduce_date(dfline)
            process_data = map_data(dfline,repeated,nonrepeated) #map the dfline data
            idx = idx + 1
            rda = repeat_donor_amount(dfline,output,process_data,nums,pval,quart,idx,min_heap,max_heap) #check for repeated donor
            if (rda is None): #if not both added and repeated
                idx = idx - 1
                continue
            dat = pd.Series(rda, rqdcols)
            StreamedData = StreamedData.append(dat, ignore_index=True)
    StreamedData.to_csv('output/repeat_donors.txt', sep='|',index=False,header=False)
    return (StreamedData)


# In[111]:


if __name__ == "__main__":
    lineInfo = donation_analysis("input/itcont.txt")

