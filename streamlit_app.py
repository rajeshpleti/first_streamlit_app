import streamlit
import pandas
import snowflake.connector 
import requests
from urllib.error import URLError

streamlit.title('welcome mallika')
streamlit.header('brekfastmenu')
streamlit.text('🌕 omega')
streamlit.text('🥙 kale')
streamlit.text( '🐔 hard')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)


# code function 
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
   
streamlit.header('Fruityvice and Fruity advice')   
try: 
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
         streamlit.error("please select fruit to get information.")
   else: 
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error() 
    
    
# streamlit.write('The user entered ', fruit_choice)
# new section 





streamlit.stop()

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# write your own comment -what does the next line do? 
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# write your own comment - what does this do?
streamlit.dataframe(fruityvice_normalized)


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load ist contains:")
streamlit.dataframe(my_data_row)



add_my_fruit = streamlit.text_input('What fruit would u like to add?','jackfruit')
streamlit.write('thanks for adding ', add_my_fruit)
# new section 

my_cur.execute(" insert into fruit_load_list values ('from streamlit')")
