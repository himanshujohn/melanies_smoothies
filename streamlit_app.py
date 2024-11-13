# Import python packages
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!.
    """
)

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberry", "Peaches"),
# )

# st.write("You favorite fruit is:", option)

# session = get_active_session()

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name on smoothie: ")
st.write("The name on your smoothie will be: ", name_on_order)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:"
    ,my_dataframe
    ,max_selections=5
)

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data = smoothiefroot_response.json())

if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    ingredients_string = ''

    for fruit_choose in ingredients_list:
        # ingredients_string += ', ' + fruit_choose
        ingredients_string += fruit_choose + ' '

    st.write(ingredients_string)

    my_insert_stmt = """ insert into SMOOTHIES.PUBLIC.ORDERS(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""  + name_on_order +  """');"""
    st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



    

