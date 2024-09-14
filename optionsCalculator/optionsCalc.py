from debug.configDebugLogs import DebugClient
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import logging as lg

# Set up debugging logs
lg.basicConfig(
    filename=DebugClient.ToDebugPath("optionsCalcLogs"),
    filemode='a', # Use 'a' to append to the current log file.
    format='%(asctime)s\t%(levelname)s\t%(message)s',
    level=lg.DEBUG
)

# Create calculations functions
class optionsCalcFuncs():
    def blackScholesCall(S0,X,T,r,sig):

        # Calculate d terms...
        d1 = (np.log(S0/X)+(r+0.5*sig**2)*T)/(sig*np.sqrt(T))
        d2 = d1-(sig*np.sqrt(T))

        # Utilize cumulative distribution function of standard normal distribution in final value calculation.
        callVal = S0*norm.cdf(d1) - X * np.exp(-r * T) * norm.cdf(d2)
        return callVal
    def blackScholesPut(S0,X,T,r,sig):
        
        # Calculate d terms...
        d1 = (np.log(S0/X)+(r+0.5*sig**2)*T)/(sig*np.sqrt(T))
        d2 = d1-(sig*np.sqrt(T))

        # Utilize cumulative distribution function of standard normal distribution in final value calculation.
        putVal = X*np.exp(-r*T)*norm.cdf(-d2)-S0*norm.cdf(-d1)
        return putVal
    def currencyFormatting(x, pos):
        return f'${x:,.2f}'

# Run calculations control flow
print("Welcome to the options calculator:\n")
calcType = str(input("Calculate 'Graph' or 'One Price'?\n"))
optType = str(input("Enter an option type (Call/Put):\n"))

if calcType == "One Price":
    if optType == "Call" or optType == "call":
        lg.info(f"Initializing call option one-value calculator.")

        S0 = float(input("Current stock price:\t\t"))
        X = float(input("Strike price:\t\t\t"))
        T = float(input("Time to expiration (days):\t\t"))/252 # Divide by 252 trading days per year.
        r = float(input("Risk free interest rate:\t\t"))
        sig = float(input("Volatility:\t\t\t"))

        callprice = optionsCalcFuncs.blackScholesCall(S0,X,T,r,sig)
        print(f"Call value at current price is ${callprice:.2f}")

    elif optType == "Put" or optType == "put":
        lg.info(f"Initializing put option one-value calculator.")

        S0 = float(input("Current stock price:\t\t"))
        X = float(input("Strike price:\t\t\t"))
        T = float(input("Time to expiration (days):\t\t"))/252 # Divide by 252 trading days per year.
        r = float(input("Risk free interest rate:\t\t"))
        sig = float(input("Volatility:\t\t\t"))
        
        putprice = optionsCalcFuncs.blackScholesPut(S0,X,T,r,sig)
        print(f"Put value at current price is ${putprice:.2f}")

    else:
        lg.warning("Invalid option type selection.\n\n")

elif calcType == "Graph":
    if optType == "Call" or optType == "call":
        lg.info(f"Initializing call option graph calculator.")

        Sb = float(input("Low stock price:\t\t"))
        Se = float(input("High stock price:\t\t"))
        S0_range = np.linspace(Sb, Se, 100) # Create array of stock prices at one hundred points.
        X = float(input("Strike price:\t\t\t"))
        T_range = [5/252, 10/252, 20/252, 62/252, 0.5, 1] # Plot expirations of one week, 2 weeks, one month, three months, six months, one year
        T_labels = ['1 WK', '2 WKs', '1 MO', '3 MOs', '6 MOs', '1 YR']
        r = float(input("Risk free interest rate:\t"))
        sig = float(input("Volatility:\t\t\t"))

        for T, label in zip(T_range, T_labels):
            callprices = [optionsCalcFuncs.blackScholesCall(S0, X, T, r, sig) for S0 in S0_range]
            plt.plot(S0_range, callprices, label=label)

        plt.title('Call Price vs. Stock Price')
        plt.xlabel('Stock Price ($)')
        plt.ylabel('Call Option Price ($)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(optionsCalcFuncs.currencyFormatting))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(optionsCalcFuncs.currencyFormatting))
        plt.legend()
        plt.grid(True)
        plt.show()

    elif optType == "Put" or optType == "put":
        lg.info(f"Initializing put option graph calculator.")

        Sb = float(input("Low stock price:\t\t"))
        Se = float(input("High stock price:\t\t"))
        S0_range = np.linspace(Sb, Se, 100) # Create array of stock prices at one hundred points.
        X = float(input("Strike price:\t\t\t"))
        T_range = [5/252, 10/252, 20/252, 62/252, 0.5, 1] # Plot expirations of one week, 2 weeks, one month, three months, six months, one year
        T_labels = ['1 WK', '2 WKs', '1 MO', '3 MOs', '6 MOs', '1 YR']
        r = float(input("Risk free interest rate:\t"))
        sig = float(input("Volatility:\t\t\t"))

        for T, label in zip(T_range, T_labels):
            putprices = [optionsCalcFuncs.blackScholesPut(S0, X, T, r, sig) for S0 in S0_range]
            plt.plot(S0_range, putprices, label=label)

        plt.title('Put Price vs. Stock Price')
        plt.xlabel('Stock Price ($)')
        plt.ylabel('Put Option Price ($)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(optionsCalcFuncs.currencyFormatting))
        plt.gca().yaxis.set_major_formatter(FuncFormatter(optionsCalcFuncs.currencyFormatting))
        plt.legend()
        plt.grid(True)
        plt.show()

    else:
        lg.warning("Invalid option type selection.\n\n")