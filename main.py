import numpy as np
import pandas as pd
import streamlit as st
import time
import datetime as dt

from helpers import *



st.set_page_config(layout='wide')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


logo, _ = st.columns(2)
with logo:
	st.image(storymch_logo, width=200)
   
st.markdown("<h1 style='text-align: center; color: green;'>Palantir: Community Management Dashboard</h1>", unsafe_allow_html=True)




## Filters to filter the dataframe

col1, col2, col3 = st.columns(3)

with col1:
	filter_day = st.number_input("Enter number to view posts for that number of days", min_value=1, max_value=30, value=7, step=1)
	if filter_day:
		st.success(f'Showing Posts from last {int(filter_day)} Days', icon="✅")

with col2:
	filter_Interactions = st.selectbox( "Filter by total interactions",
						('Total Interaction: High to Low',
						'Total Interaction: Low to High'))

with col3:
	filter_date = st.selectbox( "Filter by total Post date",
						('Posts: Newest First',
						'Posts: Oldest First'))


palantir_path = 'https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/xv0G0VRws9pU6ZsMf1uY2g/palantir_1.csv'

paula_cipi_path = 'https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/qmmv9cspSmqDQpn0QoRDdg/paula_cipi_1.csv'
jan_hie_path = 'https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/DpKxT9bGGT1HtVTj8BoFnA/jan_hiesserich.csv'
kath_brienne_path = 'https://phantombuster.s3.amazonaws.com/UhrenaxfEnY/w2Tf62a4RFxsvwk63Tbs8A/katharina_brienne.csv'




palantir_df_main = read_file(palantir_path)
paula_cipi_df_main = read_file(paula_cipi_path)
jan_hi_df_main = read_file(jan_hie_path)
kath_brienne_main = read_file(kath_brienne_path)



palantir_df = palantir_df_main[palantir_df_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]
paula_cipi_df = paula_cipi_df_main[paula_cipi_df_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]
jan_hi_df = jan_hi_df_main[jan_hi_df_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]
kath_brienne_df = kath_brienne_main[kath_brienne_main['date']>=(dt.datetime.now()-dt.timedelta(days=filter_day))]


palantir_df = palantir_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])
paula_cipi_df = paula_cipi_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])
jan_hi_df = jan_hi_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])
kath_brienne_df = kath_brienne_df.sort_values(by = ['yy-dd-mm','Total Interactions'], ascending=[ filters[filter_date][1], filters[filter_Interactions][1]])


Palantir, Paula_Cipi, Jan_Hiesserich, Kath_Brienne = st.tabs(['Palantir', 'Paula Cipierre', 'Jan Hiesserich', 'Katharina Brienne'])


with Palantir:

	palantir_df_copy = palantir_df.reset_index(drop=True)
	num_posts = palantir_df_copy.shape[0]
	st.write(f'Total number of posts found: ', str(num_posts))

	if  num_posts>0:
		splits = palantir_df_copy.groupby(palantir_df_copy.index // 3)
		for _, frames in splits:
			frames = frames.reset_index(drop=True)
			thumbnails = st.columns(frames.shape[0])
			for i, c in frames.iterrows():
				with thumbnails[i]:
					printFunction(i, c, frames)               
	else:
		printError()


with Paula_Cipi:
	

	paula_cipi_df = paula_cipi_df.reset_index(drop=True)
	paula_cipi_copy = paula_cipi_df.copy()
	num_posts = paula_cipi_copy.shape[0]
	st.write(f'Total number of posts found: ', str(num_posts))
	if  num_posts>0:
		splits = paula_cipi_copy.groupby(paula_cipi_copy.index // 3)
		for _, frames in splits:
			frames = frames.reset_index(drop=True)
			thumbnails = st.columns(frames.shape[0])
			for i, c in frames.iterrows():
				with thumbnails[i]:
					printFunction(i, c, frames)               
	else:
		printError()



with Jan_Hiesserich:
	
	jan_hi_df = jan_hi_df.reset_index(drop=True)
	jan_hi_df_copy = jan_hi_df.copy()
	num_posts = jan_hi_df_copy.shape[0]
	st.write(f'Total number of posts found: ', str(num_posts))

	if  num_posts>0:
		splits = jan_hi_df_copy.groupby(jan_hi_df_copy.index // 3)
		for _, frames in splits:
			frames = frames.reset_index(drop=True)
			thumbnails = st.columns(frames.shape[0])
			for i, c in frames.iterrows():
				with thumbnails[i]:
					printFunction(i, c, frames)               
	else:
		printError()


with Kath_Brienne:
	
	kath_brienne_df = kath_brienne_df.reset_index(drop=True)
	kath_brienne_df_copy = kath_brienne_df.copy()
	num_posts = kath_brienne_df_copy.shape[0]
	st.write(f'Total number of posts found: ', str(num_posts))

	if  num_posts>0:
		splits = kath_brienne_df_copy.groupby(kath_brienne_df_copy.index // 3)
		for _, frames in splits:
			frames = frames.reset_index(drop=True)
			thumbnails = st.columns(frames.shape[0])
			for i, c in frames.iterrows():
				with thumbnails[i]:
					printFunction(i, c, frames)               
	else:
		printError()


