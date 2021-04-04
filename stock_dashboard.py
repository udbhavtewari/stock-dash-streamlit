import streamlit as st
import pandas as pd
import html5lib
import yfinance as yf
import base64




st.title("Analysis of BSE SENSEX Companies")
st.header("A web application for financial analysis for investors")
st.sidebar.header('Filter by Company')





st.markdown("""
The following is a list of all companies that have been included in the BSE SENSEX since its 
establishment in 1986.
""")
st.info("""
* **Base Year :** 1978-79
* **Base Value :** 100
""")



# Web scraping of BSE Companies
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

df = load_data()



#Symbol selection
Symbols = df['Symbol'].tolist()
companies_selected = st.sidebar.selectbox('Select a company to display the graphs', Symbols)




st.header('Information on BSE listed companies at a glance')
st.dataframe(df)

#File Download
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="BSE.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df), unsafe_allow_html=True)


#Displaying data 
tickerData = yf.Ticker(companies_selected)
tickerDF = tickerData.history (period='max')
infoType = st.sidebar.radio(
        "Select from the following",
        ('Opening Price', 'Closing Price','Volume','Dividends')
    ) 

if st.button('Show Graphs'):
  if (infoType == 'Opening Price'):
    pass
  else:
    pass

  if(infoType == 'Opening Price'):
    st.write("""
    ## Opening Price
    """)
    st.line_chart(tickerDF.Open)

  if(infoType == 'Closing Price'):
    st.write("""
   ## Closing Price
    """)
    st.line_chart(tickerDF.Close)

  if(infoType == 'Volume'):
    st.write("""
    ## Volume
    """)
    st.line_chart(tickerDF.Volume)

  if(infoType == 'Dividends'):
    st.write("""
    ## Dividends
    """)
    st.line_chart(tickerDF.Dividends)

# Show button to display complete historical data
if st.button('Show Complete Historical Data'):
    #st.header('')
    data = tickerData.history(period="max")
    st.write(data)


# Display company profile
st.sidebar.header("Company Profile")
try :
  info = tickerData.info
  st.sidebar.write('Name : ' + info['longName'])
  st.sidebar.write('Exchange : ' + info['exchange'])
  st.sidebar.write('Market Capitalisation : ' + str(info['marketCap']))
  st.sidebar.write('Quote Type : ' + info['quoteType'])
except :
  st.sidebar.write("No data available at the moment")





#Name plate
st.sidebar.subheader(""" From InsightX by [Udbhav Tewari](https://www.linkedin.com/in/udbhavtewari)""")
st.write("**Disclaimer - This information is provided solely for educational purposes. The information is not intended to be investment or trading advice, and it is not a solicitation or recommendation to buy, sell, or keep any of the securities listed.**")





#Remove warning 
st.set_option('deprecation.showPyplotGlobalUse', False)





 