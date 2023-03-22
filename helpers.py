import pandas as pd
import streamlit as st
from datetime import datetime
import re





month = datetime.today().month
day = datetime.today().day



storymch_logo = "https://storymachine.mocoapp.com/objects/accounts/a201d12e-6005-447a-b7d4-a647e88e2a4a/logo/b562c681943219ea.png"


filters = { 'Total Interaction: High to Low' : ['Total Interactions', False],
            'Total Interaction: Low to High' : ['Total Interactions', True],
            'Posts: Newest First': ['date',False],
            'Posts: Oldest First': ['date',True]}


mapper = { 'https://www.linkedin.com/company/amaneos/posts/?feedView=all' : 'Amaneos' ,
            'https://www.linkedin.com/company/asteriio/posts/?feedView=all': 'Asteri'  ,
         'https://www.linkedin.com/company/balcke-duerr/posts/?feedView=all': 'Balcke-Dürr Group',
        	'https://www.linkedin.com/company/cimos/posts/?feedView=all':'Cimos',
        	'https://www.linkedin.com/company/clecim/posts/?feedView=all':'Clecim',
        	'https://www.linkedin.com/company/donges-group/posts/?feedView=all':'Donges Group',
        	'https://www.linkedin.com/company/fasana-gmbh/posts/?feedView=all':'FASANA',
        	'https://www.linkedin.com/company/frigoscandia/posts/?feedView=all':'Frigoscandia',
        	'https://www.linkedin.com/company/ganter-group/posts/?feedView=all':'Ganter Group',
        	'https://www.linkedin.com/company/gemini-rail-group/posts/?feedView=all':'Gemini Rail Groups und ADComms',
        	'https://www.linkedin.com/company/guascorenergy/posts/?feedView=all':'Guascor Energy',
        	'https://www.linkedin.com/company/iinovis/posts/?feedView=all':'iinovis Group',
        	'https://www.linkedin.com/company/keeeper-gmbh/posts/?feedView=all':'keeeper Group',
        	'https://www.linkedin.com/company/kico-group/posts/?feedView=all':'Kico und ISH Group',
        	'https://www.linkedin.com/company/la-rochette-cartonboard/posts/?feedView=all':'La Rochette Cartonboard',
        	'https://www.linkedin.com/company/nem/posts/?feedView=all':'NEM Energy',
        	'https://www.linkedin.com/company/palmia-oy/posts/?feedView=all':'Palmia',
        	'https://www.linkedin.com/company/plati-spa/posts/?feedView=all':'Plati Group',
        	'https://www.linkedin.com/company/primotecsgroup/posts/?feedView=all':'PrimoTECS Group',
        	'https://www.linkedin.com/company/repartim/posts/?feedView=all':'Repartim Group',
        	'https://www.linkedin.com/company/sabo-maschinenfabrik-gmbh/posts/?feedView=all':'SABO',
        	'https://www.linkedin.com/company/special-melted-products-ltd/posts/?feedView=all':'Special Melted Products',
        	'https://www.linkedin.com/company/valtitubes/posts/?feedView=all':'VALTI',
            'https://www.linkedin.com/company/mutares/posts/?feedView=all': 'Mutares SE & CO.KGaA'}




@st.cache
def read_file(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['textContent'])
    df.drop(['connectionDegree', 'timestamp'], axis=1, inplace=True)
    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])
    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')
    
    return df



@st.cache
def read_file_sp(filename):
    df =pd.read_csv(filename)
    df = df.dropna(how='any', subset=['postContent'])
    # df.drop(['error', 'timestamp', 'sharedPostUrl','sharedPostProfileUrl',
    #         'sharedJobUrl','videoUrl','sharedPostCompanyUrl'], axis=1, inplace=True)

    df['postDate'] = df.postUrl.apply(getActualDate)
    df = df.dropna(how='any', subset=['postDate'])
    df['date'] =  pd.to_datetime(df['postDate'])

    df['company_name'] =  df.profileUrl.apply(lambda x : mapper[x])

    df.drop_duplicates(subset=['postUrl'], inplace=True)
    df = df.reset_index(drop=True)
    df['Total Interactions'] = df['likeCount'] + df['commentCount']
    df['likeCount'] = df['likeCount'].fillna(0)
    df['commentCount'] = df['commentCount'].fillna(0)
    df['Total Interactions'] = df['Total Interactions'].fillna(0)
    df['likeCount'] = df['likeCount'].astype(int)
    df['commentCount'] = df['commentCount'].astype(int)
    df['Total Interactions'] = df['Total Interactions'].astype(int)
    #df['Keyword']  = df['category']
    df['yy-dd-mm'] = pd.to_datetime(df.date).dt.strftime('%Y/%m/%d')
    
    return df






def getActualDate(url):
    a= re.findall(r"\d{19}", url)
    a = int(''.join(a))
    a = format(a, 'b')
    first41chars = a[:41]
    ts = int(first41chars,2)
    actualtime = datetime.fromtimestamp(ts/1000).strftime("%Y-%m-%d %H:%M:%S %Z")
    return actualtime



def printFunction(i, rows, dataframe):
   
    if not pd.isnull(rows['companyUrl']):
        st.subheader(rows.companyName)
        st.write('Company Account')
      
        st.info(rows['textContent'])
        st.write('Total Interactions 📈:  ',rows['Total Interactions'])
        st.write('Likes 👍:  ',rows['likeCount']) 
        st.write('Comments 💬:  ',rows['commentCount'])
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['companyUrl']) #linktoProfile


    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile




def printFunction_search(i, rows, dataframe):
   
    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.fullName[i])
        st.write('Personal Account')
        st.write(rows['title']) #postType
        st.write('-----------')
       
        st.info(rows['textContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    



def printFunction_posts(i, rows, dataframe):
    if not pd.isnull(rows['profileUrl']):
        #st.image(rows['profileImgUrl'], width=150)
        st.subheader(dataframe.company_name[i])
        #st.write('Personal Account')
        st.write(rows['type']) #postType
        st.write('-----------')
       
        st.info(rows['postContent'])  #postrowsontent
        st.write('Total Interactions 📈:  ',rows['Total Interactions']) #totInterarowstions
        st.write('Likes 👍:  ',rows['likeCount']) #totInterarowstions
        st.write('Comments 💬:  ',rows['commentCount']) #totInterarowstions
        #st.write('Arowstion 📌:  ',rows['arowstion']) #totInterarowstions
        st.write('Publish Date & Time 📆:         ',rows['postDate']) #publishDate
        with st.expander('Link to this Post 📮'):
                st.write(rows['postUrl']) #linktoPost
        with st.expander('Link to  Profile 🔗'):
                st.write(rows['profileUrl']) #linktoProfile
    





def printError():
    st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
    st.subheader('Oops... No new post found in last Hours.')


def printAccountInfo(dataframe, option):
    dataframe_copy = dataframe[dataframe.Branche == option]
    dataframe_copy = dataframe_copy.reset_index(drop=True)
    num_post = dataframe_copy.shape[0]
    if num_post>0:
        splits = dataframe_copy.groupby(dataframe_copy.index//3)
        for _,frame in splits:
            frame = frame.reset_index(drop=True)
            thumbnail = st.columns(frame.shape[0])
            for i, row in frame.iterrows():
                with thumbnail[i]:
                    st.subheader(row['Account_Name'])
                    if not pd.isnull(row['imgUrl']):
                        st.image(row['imgUrl'])
                    st.info(row['postContent'])
                    st.write('Publish Date & Time 📆:         ',row['postDate'])
                    st.write('Total Interactions 📈:  ',row['Total Interactions'])
                    st.write('Likes 👍:  ',row['likeCount']) #totInteractions
                    st.write('Comments 💬:  ',row['commentCount']) #totInteractions
                    with st.expander('Link to this Post 📮'):
                        st.write(row['postUrl']) #linktoPost
                    with st.expander('Link to  Profile 🔗'):
                        st.write(row['profileUrl']) #linktoProfile
    else:
        st.image('https://img.freepik.com/premium-vector/hazard-warning-attention-sign-with-exclamation-mark-symbol-white_231786-5218.jpg?w=2000', width =200)
        st.subheader('Oops... No new post found for the selection.')

