import streamlit as st             
from pytrends.request import TrendReq
from GoogleNews import GoogleNews
from googletrans import Translator
import pandas as pd 
import re
import numpy as np

def main():

    def list_str(input_list):
        output_str = ' '.join(input_list) 
        return output_str
    
    @st.cache
    def get_related(df):
        if df.size > 0:
            related = ""
            for q in df.head(3)['query'].unique():
                related += q + ', '
            return(re.sub(r',\s$', '', related))
        else:
            return("No related queries found")

    @st.cache
    def get_top(country):
        ds = pytrend.trending_searches(pn=country.lower())
        ds.columns = ['trends']
        return ds.head(10).trends.unique()

    @st.cache
    def get_news(term):
        # detect the language
        translator = Translator()
        lan = translator.detect(term)
        lan = re.sub(r'Detected\(lang=(..), confidence=.+\)', r'\1', str(lan))
        # get news
        googlenews=GoogleNews(lang=lan)
        googlenews.search(term)
        result=googlenews.result()
        df = pd.DataFrame(result)
        try:
            df = df[['title', 'media', 'link']].head(1)
            title = list_str(df.title.unique())
            link = list_str(df.link.unique())
            return(f"{title} [link]({link})")
        except KeyError:
            return("No related news found")
    
    st.title("Daily TOP 10 Search Trends")
    st.write("Check and compare daily search trends, related queries and news in two countries")

    pytrend = TrendReq()

    # create columns to input countries
    col_one, col_two = st.columns(2)

    with col_one:
        country_one = st.text_input("Incert country name", value="Ukraine")

    with col_two:
        country_two = st.text_input("Incert country name", value="russia")

    # create two columns for data output
    col_one, col_two = st.columns(2)

    with col_one:
        
        st.write(f'Search trends in {country_one}')
        
        tops_one = get_top(country_one)

        for t in tops_one:

            with st.expander(f'{np.where(tops_one == t)[0] + 1} {t}'):

                if st.checkbox('Show related queries', key=f'{t}one'):
                    pytrend.build_payload(kw_list=[t])
                    related_queries = pytrend.related_queries()
                    rising = pd.DataFrame(data=related_queries.get(t).get('rising'))
                    st.write(get_related(rising))

                if st.checkbox('Show related news', key=f'{t}one'):
                    st.write(get_news(t))

    with col_two:
        
        st.write(f'Search trends in {country_two}')
        
        tops_two = get_top(country_two)

        for t in tops_two:

            with st.expander(f'{np.where(tops_two == t)[0] + 1} {t}'):

                if st.checkbox('Show related queries', key=f'{t}two'):
                    pytrend.build_payload(kw_list=[t])
                    related_queries = pytrend.related_queries()
                    rising = pd.DataFrame(data=related_queries.get(t).get('rising'))
                    st.write(get_related(rising))

                if st.checkbox('Show related news', key=f'{t}two'):
                    st.write(get_news(t))


if __name__ == '__main__':
    main()
