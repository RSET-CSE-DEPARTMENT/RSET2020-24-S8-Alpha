from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, JsonResponse
from django.db.models import *
from .models import *
import yfinance as yf
import time
import datetime
import pandas as pd
from functools import reduce
import warnings
warnings.filterwarnings('ignore')

from django.shortcuts import render
import plotly.graph_objs as go
import plotly.offline as opy
import pandas as pd
from tensorflow.keras.models import load_model

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from django.contrib.sessions.models import Session
import matplotlib.pyplot as plt
import numpy as np
import datetime
import re
import json
import joblib
import pickle
import plotly.graph_objs as go
import plotly.offline as offline
import mpld3

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import HRPOpt
from pypfopt.efficient_frontier import EfficientCVaR
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

adani = load_model('stock_chat/static/Train_Folder/ADANIENT.h5')
bajaj = load_model('stock_chat/static/Train_Folder/BAJFINANCE.h5')
bharti = load_model('stock_chat/static/Train_Folder/BHARTIARTL.h5')
hcl = load_model('stock_chat/static/Train_Folder/HCLTECH.h5')
hdfc = load_model('stock_chat/static/Train_Folder/HDFCBANK.h5')
icici = load_model('stock_chat/static/Train_Folder/ICICIBANK.h5')
infy = load_model('stock_chat/static/Train_Folder/INFY.h5')
itc = load_model('stock_chat/static/Train_Folder/ITC.h5')
kotak = load_model('stock_chat/static/Train_Folder/KOTAKBANK.h5')
lici = load_model('stock_chat/static/Train_Folder/LICI.h5')
lt = load_model('stock_chat/static/Train_Folder/Train2/LT_NS.h5')
maruti = load_model('stock_chat/static/Train_Folder/Train2/MARUTI_NS.h5')
ongc = load_model('stock_chat/static/Train_Folder/ONGC.h5')
reliance = load_model('stock_chat/static/Train_Folder/Train2/RELIANCE_NS.h5')
sbi = load_model('stock_chat/static/Train_Folder/Train2/SBIN_NS.h5')
sun = load_model('stock_chat/static/Train_Folder/Train2/SUNPHARMA.h5')
tata = load_model('stock_chat/static/Train_Folder/Train2/TATAMOTORS.h5')
tcs = load_model('stock_chat/static/Train_Folder/Train2/TCS.h5')
titan = load_model('stock_chat/static/Train_Folder/Train2/TITAN.h5')
wipro = load_model('stock_chat/static/Train_Folder/Train2/WIPRO.h5')


# adani_scale = joblib.load('stock_chat/static/Train_Folder/ADANIENT.pkl')
# bajaj_scale = joblib.load('stock_chat/static/Train_Folder/BAJFINANCE.pkl')
# bharti_scale = joblib.load('stock_chat/static/Train_Folder/BHARTIARTL.pkl')
# hcl_scale = joblib.load('stock_chat/static/Train_Folder/HCLTECH.pkl')
# hdfc_scale = joblib.load('stock_chat/static/Train_Folder/HDFCBANK.pkl')
# icici_scale = joblib.load('stock_chat/static/Train_Folder/ICICIBANK.pkl')
# infy_scale = joblib.load('stock_chat/static/Train_Folder/INFY.pkl')
# itc_scale = joblib.load('stock_chat/static/Train_Folder/ITC.pkl')
# kotak_scale = joblib.load('stock_chat/static/Train_Folder/KOTAKBANK.pkl')
# lici_scale = joblib.load('stock_chat/static/Train_Folder/LICI.pkl')
# lt_scale = joblib.load('stock_chat/static/Train_Folder/Train2/LT_NS.pkl')
# maruti_scale = joblib.load('stock_chat/static/Train_Folder/Train2/MARUTI_NS.pkl')
# reliance_scale = joblib.load('stock_chat/static/Train_Folder/Train2/RELIANCE_NS.pkl')
# sbi_scale = joblib.load('stock_chat/static/Train_Folder/Train2/SBIN_NS.pkl')
# sun_scale = joblib.load('stock_chat/static/Train_Folder/Train2/SUNPHARMA.pkl')
# tata_scale = joblib.load('stock_chat/static/Train_Folder/Train2/TATAMOTORS.pkl')
# tcs_scale = joblib.load('stock_chat/static/Train_Folder/Train2/TCS.pkl')
# titan_scale = joblib.load('stock_chat/static/Train_Folder/Train2/TITAN.pkl')
# wipro_scale = joblib.load('stock_chat/static/Train_Folder/Train2/WIPRO.pkl')

@never_cache
def login_page(request):
    return render(request, 'login.html')

@never_cache
def register_page(request):
    return render(request, 'register.html')

def register(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('conf')
    contact = request.POST.get('contact')

    if password == confirm_password:
        data = {}
        reg_obj = User.objects.filter(email = email)
        if reg_obj.count() > 0:
            data['result'] = 'no'
            return HttpResponse("<script>alert('Email already Exist);</script>")
        else:
            reg_obj2 = User(name=name, email=email,password=password,contact=contact)
            reg_obj2.save()
            data["result"] ="yes"
            saved_user = User.objects.get(pk=reg_obj2.pk)
            print(f'Name: {saved_user.name}, Mail: {saved_user.email}, Password: {saved_user.password}, Phone: {saved_user.contact}')
            return HttpResponse("<script>alert('Successfully Registered!'); window.location.href='/login_page/'</script>")
    else:
        return HttpResponse("<script>alert('Password does not match!..'); window.location.href='/register_page/'</script>")


@never_cache
def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    ob_mail = User.objects.get(email=email)
    
    if email == ob_mail.email and password == ob_mail.password:
        request.session['user'] = email
        obj = User.objects.get(email=email)
        name = obj.name.capitalize()
        return render(request,'home.html',{'user':name})
    else:
        return HttpResponse("<script>alert('Login Failed!!...');window.location.href='/login_page/'</script>")

@never_cache
def logout(request):
    if 'user' in request.session:
        del request.session['user']
        return render(request,'login.html')

@never_cache
def home_page(request):
    if 'user' in request.session:
        email = request.session['user']
        obj = User.objects.get(email=email)
        name = obj.name.capitalize()
        print('Name: ',name)
        return render(request,'home.html',{'user':name})
    
@never_cache
def chat_page(request):
    return render(request,"chat.html")

@never_cache
def analyze_page(request):
    return render(request,"analyze.html")

@never_cache
def predict_analysis(request):
    startdate = request.POST.get('start')
    enddate = request.POST.get('end')

    print(startdate, enddate)

amount_to_invest = None
num_days = None
risk = None

@csrf_exempt
def process_message(request):
    global amount_to_invest, num_days, risk
    if request.method == 'POST':
       
        data = json.loads(request.body.decode('utf-8'))

        # Extract relevant information
        content = data.get('content', '')
        message_type = data.get('type', '')
        Catg = data.get('category', '')
        category=Catg
        content = content.lower()
        
        if message_type == 'text':
            if Catg=="Home":
                try:
                    if content == 'hello' or content == 'hi'or content == 'good morning':
                        time.sleep(10)
                        string_without_quotes="Hey There Im Bot-X ! How are you?"
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content =='good bye':
                        string_without_quotes=" Good Bye !!"
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content =='perfect' or content =='great' or content =='amazing':
                        string_without_quotes=" Great carry on !!"
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content =='i am sad' or content =='sad':
                        string_without_quotes="  Oh no, that is sad to hear"
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content =='are you a bot?':
                        string_without_quotes="I am a bot, My name is Bot-X and I am here for your assistance"
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content =='thank you' or content =='appreciate it' or content =='gracias':
                        string_without_quotes="Thank you for using the chatbot."
                        response_data = {'botResponse': string_without_quotes}
                        return JsonResponse(response_data)
                    elif content == 'what are stocks' or content == 'details on stock market' or content == 'stock market' or content == 'details on stock market' or content == 'information on stocks' or content == 'information on stocks' or content == 'info on stock marketing':
                        bot_response = """The stock market is essentially a platform where people can buy and sell
                                        ownership shares of publicly traded companies. Imagine it like a big marketplace where these
                                        shares, called stocks or equities, are traded. When you buy a stock, you're essentially buying a
                                        small piece of ownership in that company. The value of these stocks can go up or down based
                                        on various factors like the company's performance, industry trends, economic conditions, and
                                        investor sentiment. Investors buy stocks hoping that their value will increase over time, allowing
                                        them to sell for a profit. The stock market serves as a crucial component of the economy,
                                        providing companies with a way to raise capital and investors with opportunities to grow their
                                        wealth."""

                        response_data = {'botResponse': bot_response}
                        return JsonResponse(response_data)
                    elif content == 'what is risk factor' or content == 'explain risk cactor' or content == 'whats risk rating' or content == 'details on stock market' or content == 'explain risk rating' or content == 'risk factor':
                        bot_response = """Risk Factor is a value between and including 1 and 10 such that a lower
                                            rating suggests that you are not willing to invest in companies that are not profitable
                                            currently but are predicted to be profitable in the near future (i.e. You required assured
                                            profit).
                                            A higher rating suggests that you are ready to invest in companies that are currently
                                            downhill but is predicted to go uphill in the future (i.e You have variable profit, profit can
                                            be too high or you could incur a loss"""

                        response_data = {'botResponse': bot_response}
                        return JsonResponse(response_data)
                    
                    
                    elif content == 'i want to invest' or content == 'suggest me companies to invest' or content == 'suggest me stocks to invest' or content == 'i am ready to invest' or content == 'lets invest' or content == 'lets do stocks':
                        bot_response = """Great ! I would like more information to perfectly suggest companies
                                        according to your needs.
                                        How much money are you willing to invest?
                                        """
                        response_data = {'botResponse': bot_response}
                        return JsonResponse(response_data)
                    elif 'the amount can be' in content:
                        amount_to_invest =  int(re.search(r'\d+', content).group())
              
                        bot_response = """For how many days are you willing to invest?"""
                        response_data = {'botResponse': bot_response}
                        return JsonResponse(response_data)
                    elif 'the no of days can be' in content:
                        num_days = int(re.search(r'\d+', content).group())
                       
                        bot_response = """What is the Risk Factor that you are willing to uphold? 
                                            in the scale of (1-10)"""
                        response_data = {'botResponse': bot_response}
                        return JsonResponse(response_data)
                    elif 'the risk level is' in content:
                        risk = int(re.search(r'\d+', content).group())
                
                        portfolio1 = pd.read_csv("stock_chat/static/Dataset/portfolio.csv")
                        portfolio1.drop(columns=['Date'], inplace=True)
                        print('111')
                        print(risk)

                        returns = portfolio1.pct_change().dropna()
                        print('222222')
                    # Perform Hierarchical Risk Parity (HRP) optimization
                        hrp = HRPOpt(returns)
                        weights_hrp = hrp.optimize()

                    # Get the latest prices
                        latest_prices = get_latest_prices(portfolio1)

                    # Calculate target risk based on risk factor
                        target_risk = 0.02 * risk
                        print('3333333')
                    # Scale the target risk based on the number of days planned to invest
                        print(amount_to_invest, num_days)

                        scaled_target_risk = target_risk * (int(num_days) / 30) ** 0.5
                        asset_amounts = []
                        expected_returns = []
                        asset_symbols = []
                    # Perform discrete allocation based on the optimized weights
                        da_hrp = DiscreteAllocation(weights_hrp, latest_prices, total_portfolio_value=float(amount_to_invest))
                        ret_hrp, vol_hrp, _ = hrp.portfolio_performance(verbose=True)
                        allocation_hrp, leftover_hrp = da_hrp.lp_portfolio(scaled_target_risk)
                        for asset, shares in allocation_hrp.items():
                            asset_price = latest_prices[asset]
                            asset_amount = shares * asset_price
                            asset_amounts.append(asset_amount)
                            asset_symbols.append(asset)
                            expected_return = returns.mean()[asset] * 100  # Multiply by 100 to represent in percentage
                            expected_returns.append(expected_return)
                        print(asset_symbols)
                        print(expected_returns)
                        print('4444444444444444')
                        # Create DataFrame to display allocation and expected returns
                        allocation_df = pd.DataFrame({'Asset Symbol': asset_symbols, 'Amount': asset_amounts, 'Expected Return (%)': expected_returns})

                    # Prepare response
                        bot_response = f"Here are your investment suggestions:\n\n{asset_symbols}\n\nAmount:{asset_amounts}\n\nExpected returns: {expected_returns}\n\nFunds remaining: ${leftover_hrp:.2f}"
                        print('55555555555555555555555555555555555')
                        # bot_response = f"Here are your investment suggestions:\n{allocation_df}"

                        response_data = {'botResponse': bot_response,'ndays':num_days}
                        return JsonResponse(response_data)
                
                except:
                    bot_response="Try again later!"
                    response_data = {'botResponse': bot_response}
                    return JsonResponse(response_data)
    else:
        amount_to_invest = None
        num_days = None
        risk = None
           
    return JsonResponse({'error': 'Invalid method'}, status=400)

scaler = MinMaxScaler(feature_range=(0, 1))

def predict_future_prices(model, data, look_back, num_days):
    last_sequence = data[-look_back:]  # Get the last sequence of known data
    predicted_prices = []
    for _ in range(num_days):
        prediction = model.predict(last_sequence.reshape(1, look_back, 1))  # Predict next day's price
        predicted_prices.append(prediction[0, 0])  # Append predicted price to list
        last_sequence = np.append(last_sequence[1:], prediction[0])  # Update last sequence with new prediction
    return scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))[:, 0]

def stocks(ticker):
    stock_symbol = ticker
    stock_data = yf.download(stock_symbol,  period="max")
    stock_data.reset_index(inplace=True)

# Extract the 'Date' and 'Close' columns
    data = stock_data[['Date', 'Close']].copy()
    scale_data = scaler.fit_transform(data[['Close']])
    return scale_data



def fetch_stock(ticker):
    
    data = yf.download(ticker, period="max")
    data[f'{ticker}'] = data["Close"]
    data = data[[f'{ticker}']]
    return data
 

def merge_stocks(tickers):
    data_frames = []
    for i in tickers:
        data = fetch_stock(i)
        if data is not None:
            data_frames.append(data)

    df_merged = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), data_frames)
    return df_merged

stocks = ["ADANIENT.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "HCLTECH.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS", "ITC.NS", "KOTAKBANK.NS", "LICI.NS", "LT.NS","MARUTI.NS","ONGC.NS","RELIANCE.NS","SBIN.NS","SUNPHARMA.NS","TATAMOTORS.NS","TCS.NS","TITAN.NS","WIPRO.NS"]
portfolio = merge_stocks(stocks)

# Reset the index to include the "Date" column
portfolio.reset_index(inplace=True)

# Sort the DataFrame by "Date" column
portfolio.sort_values(by='Date', inplace=True)

# Save the portfolio DataFrame to a CSV file with both Date and Close prices
portfolio.to_csv("stock_chat/static/Dataset/portfolio.csv", index=False)

portfolio1 = pd.read_csv("stock_chat/static/Dataset/portfolio.csv")
portfolio1.drop(columns=['Date'], inplace=True)

returns = portfolio1.pct_change().dropna()
hrp = HRPOpt(returns)
weights_hrp = hrp.optimize()
latest_prices = get_latest_prices(portfolio1)

print("****************HRP**************")
da_hrp = DiscreteAllocation(weights_hrp, latest_prices, total_portfolio_value=100000)
ret_hrp, vol_hrp, _ = hrp.portfolio_performance(verbose=True)
allocation_hrp, leftover_hrp = da_hrp.greedy_portfolio()
print("Discrete allocation (HRP):", allocation_hrp)
print("Funds remaining (HRP): ${:.2f}".format(leftover_hrp))
print("*******************************")






def load_saved_model(model_path):
	model = load_model(model_path)
	return model



def generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,ht_path,ticker):
	plt.figure(figsize=(12, 6))
	plt.plot(data['Date'], scaler.inverse_transform(scaled_data), label='Actual Close Price', color='blue')
	plt.plot(data['Date'].iloc[-1:], scaler.inverse_transform(scaled_data)[-1:], marker='o', markersize=0.5, color='green', label='Current Close Price')
	plt.plot(pd.date_range(start=data['Date'].iloc[-1], periods=num_days+1, freq='D')[1:], predicted_prices, marker='o', markersize=0.5, color='red', label='Predicted Close Price')
	plt.xlabel('Date')
	plt.ylabel('Close Price')
	ti='Actual vs Predicted Close Price'+'('+ticker+')'
	plt.title(ti)
	plt.xticks(rotation=45)
	plt.legend()
	plt.grid(True)
	plt.tight_layout()
	
	# Convert plot to interactive HTML
	html = mpld3.fig_to_html(plt.gcf())
	
	# Save HTML to file
	with open("stock_chat/static/charts/"+ht_path+'.html', 'w') as f:
		f.write(html)

def predict_future_prices(model, scaler, data, look_back, num_days):
	last_sequence = data[-look_back:]  # Get the last sequence of known data
	predicted_prices = []
	for _ in range(num_days):
		prediction = model.predict(last_sequence.reshape(1, look_back, 1))  # Predict next day's price
		predicted_prices.append(prediction[0, 0])  # Append predicted price to list
		last_sequence = np.append(last_sequence[1:], prediction[0])  # Update last sequence with new prediction
	return scaler.inverse_transform(np.array(predicted_prices).reshape(-1, 1))[:, 0]

def down_fin(nm):
	stock_symbol = nm
	stock_data = yf.download(stock_symbol, period="max")  
	stock_data.reset_index(inplace=True)
	return stock_data


def scl(st_data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data = st_data[['Date', 'Close']].copy()
    scaled_data = scaler.fit_transform(data[['Close']])
    return scaled_data, scaler, data


def my_view_page(request):
	global num_days
	# Load the data
	ticker='ADANIENT.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data = scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(adani, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='BAJFINANCE.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(bajaj, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	######################################################################################################
	# Load the data
	ticker='BHARTIARTL.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(bharti, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='HCLTECH.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(hcl, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='HDFCBANK.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(hdfc, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='ICICIBANK.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(icici, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='INFY.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(infy, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='ITC.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(itc, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='KOTAKBANK.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(kotak, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	######################################################################################################
	# Load the data
	ticker='LICI.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(lici, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	######################################################################################################
	# Load the data
	ticker='LT.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(lt, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='MARUTI.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(maruti, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
 
 	# Load the data
	ticker='ONGC.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(maruti, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################

	# Load the data
	ticker='RELIANCE.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(reliance, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='SBIN.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(sbi, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#####################################################################################################
	# Load the data
	ticker='SUNPHARMA.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(sun, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	######################################################################################################
	# Load the data
	ticker='TATAMOTORS.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(tata, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#######################################################################################################
	# Load the data
	ticker='TCS.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(tcs, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	########################################################################################################
	# Load the data
	ticker='TITAN.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(titan, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	########################################################################################################
	# Load the data
	ticker='WIPRO.NS'
	st_data=down_fin(ticker)
	scaled_data, scaler, data=scl(st_data)

	# Use the loaded model and scaler for prediction
	# num_days = 5
	predicted_prices = predict_future_prices(wipro, scaler, scaled_data, 60, num_days)

	# Generate Plotly graph and save as HTML file
	s = ticker.replace('.NS', '')
	html_file_path = generate_interactive_plot(data, scaler, scaled_data, num_days, predicted_prices,s,s)
	#######################################################################################################

	return render(request, 'analyze.html')


