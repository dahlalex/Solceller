from turtle import color
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import base64
import plotly.express as px
import plotly.graph_objects as go
import plotly
import pandas as pd
import json
from streamlit_lottie import st_lottie
import geopandas as gpd



# page config
st.set_page_config(
    page_title="",
    page_icon="",
    layout="wide"
)

# Load CSS
with open("styles/main.css") as f:
    st.markdown(
        "<style>{}</style>".format(f.read()), unsafe_allow_html=True
    )

# sidebar
with st.sidebar:
    selected = option_menu(
    menu_title=None, 
    options=["Hemsida", "Solkraft", "Karta"], 
    icons=['house', 'sun', "map"], 
    menu_icon="cast", 
    default_index=0, 
    )
    st.sidebar.title("Om")
    st.sidebar.info(
        """
        This web [app](https://share.streamlit.io/giswqs/streamlit-template) is maintained by [Alex Dahl](https://wetlands.io). You can follow me on social media:
            [GitHub](https://github.com/giswqs) | [Twitter](https://twitter.com/giswqs) | [YouTube](https://www.youtube.com/c/QiushengWu) | [LinkedIn](https://www.linkedin.com/in/qiushengwu).
        
        Source code: <https://github.com/giswqs/streamlit-template>
        More menu icons: <https://icons.getbootstrap.com>
    """
    )

if selected == "Hemsida":
    # background for Hemsida
    def get_base64(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()

    def set_background(png_file):
        bin_str = get_base64(png_file)
        page_bg_img = '''
            <style>
            .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            z-index=3;
            }
            </style>
            ''' % bin_str
        st.markdown(page_bg_img, unsafe_allow_html=True)   
            
    set_background("assets/b.jpg")

    st.markdown(f"""
        <h1>Solceller i Sverige</h1><br>
        <p> Sverige ska ha <span style="color:#ff5050;"><b>100 %</b></span> förnybar elproduktion år 
        <span style="color:#ff5050;"><b>2040 </b></span>men ... <br>
        elproduktionen från solceller utgör <span style="color:#ff5050;"><b>en låg</b></span> andel</p><br>
        <h5> Hur ser Sveriges produktion av el ut i dagsläget ?</h5>
        <h5> Vad visar statistiken om nätanslutna solcellsanläggningar ?</h5>
        """, unsafe_allow_html=True)


    


if selected == "Solkraft":

    # Part 1

    col1, col2 = st.columns(2)
    with col1:
        st.header("Elproduktion i Sverige")

    with col2:
        # lottie animation
        def load_lottiefile(filepath: str):
            with open(filepath, "r") as f:
                return json.load(f)

        sun_lottie = load_lottiefile("assets/sun.json")
        st_lottie(
            sun_lottie,
            width=100,
            height=100
        )


    st.write(f"""Sveriges produktion av el består i dagsläget främst av vattenkraft, kärnkraft, vindkraft samt        
    kraftvärme. I 2021 utgjorde solkraften en liten andel, mindre än 1 % av Sveriges elproduktion.   
    Däremot producerade solkraften 1.1 TWh, en ökning på 40 procent jämfört med 2020. 
    """)

    # load csv
    with open ("data/tillförsel.csv", encoding="utf-8") as csv_file_a:
        CSV = csv_file_a.read()

    # dataframe from csv    
    df_till= pd.read_csv("data/tillförsel.csv")

    # store the columns in seperate variables
    values= df_till["2021"]
    names= df_till["Tillförsel"]

    # create pie chart
    fig= px.pie(
        data_frame= df_till, 
        values= values,
        names=names,
        title="Andel av elproduktionen 2021, TWh "
    )

    fig.update_traces(
        textfont_size= 20,
        textfont_color='#ffffff',
        marker=dict(line=dict(color='#ffffff', width=1))
    )

    fig.update_layout(
       legend=dict(font=dict(size=20)) 
    )
    st.write (fig)

    # source
    st.write("Källa: [SCB](https://www.scb.se/hitta-statistik/statistik-efter-amne/energi/tillforsel-och-anvandning-av-energi/arlig-energistatistik-el-gas-och-fjarrvarme/), [Energimyndigheten](http://www.energimyndigheten.se/statistik/solstatistik/)")

    # show and download the data
    col3, col4, col5 = st.columns(3)

    with col3:
       visa_data_1= st.checkbox("📋 Visa data", key="1")

    with col4:
        st.metric(
            label="Solkraften", 
            value="1.1 TWh", 
            delta="40 %"
        )

    with col5:
        st.download_button(
        label="⬇️ Ladda ner data",
        data= CSV,
        file_name="tillförsel.csv"
        )
    
    if visa_data_1:
        st.write(df_till)

    st.markdown("#")
    st.markdown("#")

    # Part 2

    col6, col7 = st.columns(2)
    with col6:
        st.header("Solceller i Sverige")

    with col7:
        solar_panel = load_lottiefile("assets/solar_panel.json")
        st_lottie(
            solar_panel,
            width=100,
            height=100
        )

    st.write(f"""
    I Sverige har ökningen av solcellsanläggningar gått snabbt de senaste åren.  
    Vid utgången av 2020 fanns ca 66 000 nätanslutna anläggningar i Sverige,   
    vilket är en ökning med 56 000 anläggningar sedan 2016. Följaktligen har också  
    den installerade effekten ökat lika mycket.  
    """
    )
    
    st.markdown("#")

    #Chart
    
    # read sol_total.csv
    dtype_dic_total= {"År": str,"IEPC": float, "SCA": float, "IE": float, "Länd": str}
    df_sol_total = pd.read_csv("data/sol_total.csv", dtype=dtype_dic_total, encoding="utf-8")

    # selectbox
    col8, col9 = st.columns(2)
    with col8:
        amne_c = st.selectbox(
            label="Charts ämne: ", 
            options= [
                "Installerad effekt (MW) Totalt",
                "Installerad effekt per capita (Watt per person)",
                "Solcellsanläggningar, antal Totalt",
            ]
        )
        chart_amne= {
            "Installerad effekt (MW) Totalt": df_sol_total[["År", "IE", "Länd"]],
            "Installerad effekt per capita (Watt per person)": df_sol_total[["År", "IEPC", "Länd"]],
            "Solcellsanläggningar, antal Totalt": df_sol_total[["År", "SCA", "Länd"]],
        }

        # Replace the strings returned by the multiselectbox by the dataframe in the dict
        df_amne_c = chart_amne[amne_c]
    
        # store each column in a seperate variable
        länd= df_amne_c["Länd"]
        värde = df_amne_c.iloc[:,1]
        date = df_amne_c["År"]

        #  create animated bar chart and store figure as fig_total
        fig_total = px.bar(
            df_amne_c,
            x= länd,
            y= värde,
            animation_frame=date,
            animation_group=länd,
            range_y= [0, värde.max()],
            labels= {"y" : "Värde", "Länd": " "},
        )

        st.plotly_chart(fig_total)

    # source
    st.write("Källa: [SCB](https://www.scb.se/hitta-statistik/statistik-efter-amne/energi/tillforsel-och-anvandning-av-energi/arlig-energistatistik-el-gas-och-fjarrvarme/), [Energimyndigheten](http://www.energimyndigheten.se/statistik/solstatistik/)")

    # show and download the data
    col10, col11, col12 = st.columns(3)

    with col10:
       visa_data_2 = st.checkbox("📋 Visa data", key="2")

    with col11:
        sol_house = load_lottiefile("assets/sol_house.json")
        st_lottie(
            sol_house,
            width=200,
            height=200
        )

    with col12:

         # load csv
        with open ("data/sol_total.csv", encoding="utf-8") as csv_file_b:
            CSV_2 = csv_file_b.read()

        st.download_button(
        label="⬇️ Ladda ner data",
        data= CSV_2,
        file_name="sol_total.csv"
        )
    
    if visa_data_2:
        st.write(df_sol_total)
    


if selected == "Karta":

    st.header("Solceller i Sveriges län")

    st.write("""
    Karta över installerad effekt och antalet nätanslutna solcellsanläggningar  
    mellan 2016 och 2020 i Sveriges län.
    """
    )

    st.markdown("#")

    # read geojson
    with open("data/län.geojson", encoding="utf-8")as f:
        geo = json.load(f)

    # read csv
    dtype_dic= {"År":str, "SCA": float}
    df_sol = pd.read_csv("data/sol.csv", dtype=dtype_dic)
    
    # selectbox
    col13, col14 = st.columns(2)
    with col13:
        amne = st.selectbox(
            label="Kartans ämne: ", 
            options= [
                "Installerad effekt (MW) Totalt",
                "Installerad effekt per capita (Watt per person)",
                "Solcellsanläggningar, antal Totalt",
            ]
        )
        kartan_amne= {
             "Installerad effekt (MW) Totalt": df_sol[["Län", "År", "IE"]],
            "Installerad effekt per capita (Watt per person)": df_sol[["Län", "År", "IEPC"]],
            "Solcellsanläggningar, antal Totalt": df_sol[["Län", "År", "SCA"]],
        }

        # Replace the strings returned by the multiselectbox by the dataframe in the dict
        df_amne = kartan_amne[amne]

    with col14:
        ar= st.selectbox(
            label="År: ", 
            options=df_amne["År"].unique(),
        )
    
    # select year
    df_selection = df_amne.query(
        "År == @ar"
    )

    # plotly map
    fig = go.Figure(
    go.Choroplethmapbox(
        geojson=geo,
        locations=df_selection.Län,
        featureidkey="properties.LANSNAMN",
        z=df_selection.iloc[:, 2],
        colorscale="sunsetdark",
        marker_opacity=0.5,
        marker_line_width=0,
        )
    )
    fig.update_layout(
    mapbox_style='carto-darkmatter',
    mapbox_zoom=3.6,
    mapbox_center={"lat": 62.8, "lon": 16.3},
    width=800,
    height=600,
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    st.plotly_chart(fig)

    # source
    st.write("Källa: [SCB](https://www.scb.se/hitta-statistik/statistik-efter-amne/energi/tillforsel-och-anvandning-av-energi/arlig-energistatistik-el-gas-och-fjarrvarme/), [Energimyndigheten](http://www.energimyndigheten.se/statistik/solstatistik/)")
    
    st.markdown("#")
    # show and download the data
    col15, col16, col17 = st.columns(3)

    with col15:
       visa_data_3 = st.checkbox("📋 Visa data", key="3")

    with col17:

         # load csv
        with open ("data/sol.csv", encoding="utf-8") as csv_file_c:
            CSV_3 = csv_file_c.read()

        st.download_button(
        label="⬇️ Ladda ner data",
        data= CSV_3,
        file_name="sol.csv"
        )
    
    if visa_data_3:
        st.write(df_sol)



    
    
    




    
    
    

   

     


    

       
        

        
   
    








