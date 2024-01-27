import json
import streamlit as st
import pandas as pd
import requests
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image



#CREATE DATAFRAMES FROM SQL
#sql connection

mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="1234",
      database="phonepedata"
    )
mycursor=mydb.cursor(buffered=True)


#Aggregated_transaction
mycursor.execute("select * from aggregated_transaction")
mydb.commit()
table1 = mycursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_Type", "Transaction_Count", "Transaction_Amount"))

#Aggregated_user
mycursor.execute("select * from aggregated_user")
mydb.commit()
table2 = mycursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_Count", "Percentage"))

#Map_transaction
mycursor.execute("select * from map_transaction;")
mydb.commit()
table3 = mycursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_Count", "Transaction_Amount"))

#Map_user
mycursor.execute("select * from map_user;")
mydb.commit()
table4 = mycursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUsers", "AppOpens"))

#Top_transaction
mycursor.execute("select * from top_transaction;")
mydb.commit()
table5 = mycursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_Count", "Transaction_Amount"))

#Top_user
mycursor.execute("select * from top_user;")
mydb.commit()
table6 = mycursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns([2,2],gap="large")
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_Count", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 400, 
                        title= "TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_Amount", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 400,
                        title= "TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)

def Aggre_Transaction_Year(df, year, quarter):
    aiy= df[(df["Years"] == year) & (df["Quarter"] == quarter)]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    aiyg.reset_index(inplace= True)
    col1,col2=st.columns([2,2],gap="large")
    with col1:
        fig_india_1 = px.choropleth(
        aiyg,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_Amount',
        color_continuous_scale= "Sunsetdark",
        range_color= (aiyg["Transaction_Amount"].min(),aiyg["Transaction_Amount"].max()),
        hover_data= ['Transaction_Amount'],title = "TRANSACTION AMOUNT",
        fitbounds= "locations",width =500, height= 500)

        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)
    
    with col2:
        fig_india_1 = px.choropleth(
        aiyg,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='States',
        color='Transaction_Count',
        color_continuous_scale= "Sunsetdark",
        range_color= (aiyg["Transaction_Count"].min(),aiyg["Transaction_Count"].max()),
        hover_data= ['Transaction_Count'],title = "TRANSACTION COUNT",
        fitbounds= "locations",width=500, height= 500)

        fig_india_1.update_geos(visible =False)
        st.plotly_chart(fig_india_1)


    return aiy

def Aggre_user_plot_1(df,year,quarter):
    aguy= df[(df["Years"] == year) & (df["Quarter"] == quarter)]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_Count", title="BRANDS AND TRANSACTION COUNT",
                       hover_data=["Brands","Transaction_Count"],
                    width=800,color_discrete_sequence=px.colors.sequential.Oranges_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_Count", hover_data= ["Brands","Transaction_Count","Percentage"],
                      width=800,title="BRANDS AND TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_Count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_Count", markers= True,
                           width=800, title="BRANDS AND TRANSACTION COUNT")
    st.plotly_chart(fig_scatter_1)

def map_tran_plot_1(df,year,quarter,state):
    miys= df[(df["Years"] == year) &(df["Quarter"]==quarter) & (df["States"] == state)]
    miys.reset_index(drop= True, inplace= True)

    miysg= miys.groupby("Districts")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns([2,2],gap="large")
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_Amount",
                              width=450, height=500, title= "SELECTED STATE DISTRICTS AND TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "Districts", values= "Transaction_Count",
                              width=450, height= 500, title= "SELECTED STATE DISTRICTS AND TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)
    return miys
        
def map_user_plot_1(df, year,quarter,state):
    muy= df[(df["Years"] == year) & (df["Quarter"] == quarter) & (df["States"] == state)]
    muy.reset_index(drop= True, inplace= True)

    muyg= pd.DataFrame(muy.groupby(["States","Districts"])[["RegisteredUsers", "AppOpens"]].sum())
    muyg.reset_index(inplace= True)

    col1,col2= st.columns([2,2], gap="large")
    with col1:
        fig_map_user_plot_1= px.bar(muyg, x= "Districts", y= "RegisteredUsers",barmode="group",color="Districts",
                                    width=500,height=400,
                                    title= " DISTRICTS OF SELECTED STATE AND ITS REGISTERED USERS", 
                                    hover_data=["States","Districts","RegisteredUsers"],
                                    color_discrete_sequence= px.colors.sequential.Viridis_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_1= px.bar(muyg, x= "Districts", y= "AppOpens",barmode="group",color="Districts",
                                    width=500,height=400,
                                    title= "DISTRICTS OF SELECTED STATES AND ITS APPOPENS", 
                                    hover_data=["States","Districts","AppOpens"],
                                    color_discrete_sequence= px.colors.sequential.Burgyl)
        st.plotly_chart(fig_map_user_plot_1)

    return muy


def top_tran_plot_1(df,year):

    tty= df[df["Years"] == year]
    tty.reset_index(drop= True, inplace= True)

    ttyg=pd.DataFrame(tty.groupby(["States","Quarter","Pincodes"])[["Transaction_Count", "Transaction_Amount"]].sum())
    ttyg.reset_index(inplace= True)

    col1,col2= st.columns([2,2],gap="large")
    
    with col1:    

        fig_top_tran_1= px.bar(ttyg, x="States", y= "Transaction_Amount",barmode= "group",color="Quarter",
                                hover_data=["States","Pincodes","Transaction_Amount","Quarter"],
                                title="STATES TRANSACTION AMOUNT AND PINCODES",width=400, 
                                height= 400, color_discrete_sequence=px.colors.sequential.Burgyl)
        st.plotly_chart(fig_top_tran_1)
    
    with col2:
        fig_top_tran_2= px.bar(ttyg, x="States", y= "Transaction_Count",barmode= "group", color= "Quarter",
                               hover_data=["States","Pincodes","Transaction_Count","Quarter"],
                               title="STATES TRANSACTION COUNT AND PINCODES",width=400, 
                               height= 400, color_discrete_sequence=px.colors.sequential.Burgyl)
        st.plotly_chart(fig_top_tran_2)

    
    return tty
    

def top_user_plot_1(df,year,quarter,state):

    tuy= df[(df["Years"] == year) & (df["Quarter"]==quarter) & (df["States"]== state)]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter","Pincodes"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", barmode= "group", color= "Pincodes",
                            width=800, height=500,hover_data=["States","Quarter","RegisteredUsers","Pincodes"],
                            title="SELECTED STATE REGISTERED USERS AND PINCODES",
                            color_continuous_scale= px.colors.sequential.Emrld_r)
    st.plotly_chart(fig_top_plot_1)

    return tuy


def ques1():
    brand= Aggre_user[["Brands","Transaction_Count"]]
    brand1= brand.groupby("Brands")["Transaction_Count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_Count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "TOP MOBILE BRANDS USED")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_Amount"]]
    lt1= lt.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_Amount",title= "STATES WITH LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_Amount"]]
    htd1= htd.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_Amount"]]
    htd1= htd.groupby("Districts")["Transaction_Amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="TOP 10 STATES WITH APPOPENS",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="LOWEST 10 STATES WITH APPOPENS",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_Amount"]]
    ht1= ht.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_Amount",title= "STATES WITH HIGHEST TRNSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Top_user[["States", "RegisteredUsers"]]
    dt1= dt.groupby("States")["RegisteredUsers"].sum().sort_values(ascending=False)
    dt2= pd.DataFrame(dt1).head(20).reset_index()

    fig_dt= px.bar(dt2, x= "States", y= "RegisteredUsers", title= "STATES WITH HIGHEST REGISTERED USERS",
                color_discrete_sequence= px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_dt)

# Streamlit Part

# SETTING PAGE CONFIGURATIONS
icon=Image.open(r"C:\Users\Dell\JupyterPythoncodes\phonepeimg.jpg")
st.set_page_config(page_title= "Welcome To Streamlit Page",
                   page_icon=icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is created by *Apoorva Khare!*"""})

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

SELECT = option_menu(
    menu_title = None,
    options = ["Home", "Data Exploration", "Insights"],
    default_index=0,
    orientation="horizontal",
    styles={"container": {"padding": "0!important", "background-color": "white","size":"cover", "width": "100"},
        "icon": {"color": "black", "font-size": "20px"},

        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}})


with st.sidebar:
    st.title(":green[PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION]")
    st.header("Technologies Used")
    st.caption(":blue[Data extraction: Github Cloning]")
    st.caption(":blue[Data transformation: Python]")
    st.caption(":blue[Database insertion: mysql-connector-python]")
    st.caption(":blue[Data retrieval: Pandas]")
    st.caption(":blue[Dashboard creation: Streamlit and Plotly]")


if SELECT == "Home":
    st.header("PHONEPE")
    st.subheader("INDIA'S BEST TRANSACTION APP")
    st.markdown("PhonePe is a Digital Wallet & Online Payment App that allows you to make instant Money Transfers with UPI.")
    st.write("*************FEATURES*************")
    st.write("*Credit & Debit card linking")
    st.write("*Bank Balance check")
    st.write("*Money Storage")
    st.write("*PIN Authorization")

if SELECT == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["**AGGREGATED ANALYSIS**", "**MAP ANALYSIS**", "**TOP ANALYSIS**"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Transaction Analysis", "User Analysis"])

        if method == "Transaction Analysis":
                col1,col2=st.columns(2)
                with col1:
                    years_at= st.selectbox("**Select the Year**", Aggre_transaction["Years"].unique())
                with col2:
                    quarters_at= st.selectbox("**Select the Quarter**", Aggre_transaction["Quarter"].unique())
                if years_at == 2023 and quarters_at in [4]:
                    st.markdown("#### Sorry No Data to Display for 2023 Quarter 4")
                else:
                    df_agg_tran_Y= Aggre_Transaction_Year(Aggre_transaction,years_at,quarters_at)

                    #Select the State for Analyse the Transaction type
                    state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y["States"].unique())
                    Aggre_Transaction_type(df_agg_tran_Y,state_Y_Q)

        elif method == "User Analysis":
            col1,col2=st.columns(2)
            with col1:
                year_au= st.selectbox("Select the Year",Aggre_user["Years"].unique())
            with col2:
                quarter_au= st.selectbox("Select the Quarter",Aggre_user["Quarter"].unique())
            if year_au == 2022 and quarter_au in [2,3,4]:
                st.markdown("#### Sorry No Data to Display")
            else:
                agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au,quarter_au)
                agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

                state_au= st.selectbox("**Select the State**",agg_user_Y["States"].unique())
                Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Transaction Analysis", "Map User Analysis"])
        if method_map == "Map Transaction Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                years_m2= st.slider("**Select the Year**", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())
            with col2: 
                quarters_m2= st.slider("**Select the Quarter**", Map_transaction["Quarter"].min(),Map_transaction["Quarter"].max(),Map_transaction["Quarter"].min())

            with col3:
                state_m3= st.selectbox("Select the State", Map_transaction["States"].unique())
            if years_m2 == 2023 and quarters_m2 in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 Quarter 4")

            else:
                df_map_tran_Y= map_tran_plot_1(Map_transaction, years_m2,quarters_m2,state_m3)

        elif method_map == "Map User Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                year_mu1= st.slider("**Select the Year**",min_value=2018,max_value=2023)
            with col2:
                quarter_mu1= st.slider("**Select the Quarter**",min_value=1,max_value=4)
            with col3:
                    state_mu1= st.selectbox("Select State",
                             ('Andaman & Nicobar','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
                              'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli and Daman and Diu','Delhi','Goa','Gujarat','Haryana',
                              'Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep',
                              'Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram',
                              'Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim',
                              'Tamil Nadu','Telangana','Tripura','Utar Pradesh','Uttarakhand','West Bengal'),index=1)
            if year_mu1 == 2023 and quarter_mu1 in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 Quarter 4")
            else:
                df_map_user_Y= map_user_plot_1(Map_user, year_mu1,quarter_mu1,state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",[ "Top Transaction Analysis", "Top User Analysis"])
        
        if method_top == "Top Transaction Analysis":
            
            years_t2= st.select_slider("**Select the Year**", options=[2018, 2019, 2020, 2021, 2022, 2023])
 
            df_top_tran_Y= top_tran_plot_1(Top_transaction,years_t2)

        elif method_top == "Top User Analysis":
            col1,col2,col3=st.columns(3)
            with col1:
                years_tu= st.selectbox("Select the Year",Top_user["Years"].unique())
            with col2:
                quarter_tu=st.selectbox("**Select the Quarter**",(1, 2, 3, 4),index=1)
            with col3:
                state_tu= st.selectbox("Select State",Top_user["States"].unique())

            if years_tu == 2023 and quarter_tu in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 Quarter 4")
            else:
                df_top_user_Y= top_user_plot_1(Top_user,years_tu,quarter_tu,state_tu)

if SELECT == "Insights":

    ques= st.selectbox("**Select the Question**",('1. Top Brands Of Mobiles Used','2. States With Lowest Trasaction Amount',
                                  '3. Districts With Highest Transaction Amount','4. Top 10 Districts With Lowest Transaction Amount',
                                  '5. Top 10 States With AppOpens','6. Least 10 States With AppOpens','7. States With Lowest Trasaction Count',
                                 '8. States With Highest Trasaction Count','9. States With Highest Trasaction Amount',
                                 '10. States with Highest Registered Users'))
    
    if ques=="1. Top Brands Of Mobiles Used":
        ques1()

    elif ques=="2. States With Lowest Trasaction Amount":
        ques2()

    elif ques=="3. Districts With Highest Transaction Amount":
        ques3()

    elif ques=="4. Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="5. Top 10 States With AppOpens":
        ques5()

    elif ques=="6. Least 10 States With AppOpens":
        ques6()

    elif ques=="7. States With Lowest Trasaction Count":
        ques7()

    elif ques=="8. States With Highest Trasaction Count":
        ques8()

    elif ques=="9. States With Highest Trasaction Amount":
        ques9()

    elif ques=="10. States with Highest Registered Users":
        ques10()
       

    
