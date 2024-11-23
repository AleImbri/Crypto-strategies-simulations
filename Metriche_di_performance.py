import numpy as np

# Rendimento Totale (Total Return)
def total_return(portfolio_values):
    V_i = portfolio_values.iloc[0]  # valore iniziale del portafoglio
    V_f = portfolio_values.iloc[-1]  # valore finale del portafoglio
    return (V_f - V_i) / V_i * 100  # rendimento in percentuale

# Max Drawdown (MDD)
def max_drawdown(portfolio_values):
    peak = portfolio_values.iloc[0]
    max_dd = 0
    for value in portfolio_values:
        peak = max(peak, value)
        drawdown = (peak - value) / peak
        max_dd = max(max_dd, drawdown)
    return max_dd * 100  # drawdown massimo in percentuale

# Volatilità (Standard Deviation)
def volatility(portfolio_values):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]  # calcolo rendimenti giornalieri
    return np.std(returns) * np.sqrt(252)  # volatilità annualizzata

# Sharpe Ratio
def sharpe_ratio(portfolio_values, risk_free_rate=0.0):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]  # rendimenti giornalieri
    excess_returns = returns - risk_free_rate / 252  # tasso privo di rischio giornalizzato
    return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)  # annualizziamo

# Sortino Ratio
def sortino_ratio(portfolio_values, risk_free_rate=0.0):
    returns = np.diff(portfolio_values) / portfolio_values[:-1]  # rendimenti giornalieri
    downside_returns = np.where(returns < 0, returns, 0)  # rendimenti negativi
    excess_returns = returns - risk_free_rate / 252  # tasso privo di rischio giornalizzato
    downside_deviation = np.std(downside_returns)  # deviazione standard dei rendimenti negativi
    return np.mean(excess_returns) / downside_deviation * np.sqrt(252)  # annualizziamo

# Calmar Ratio
def calmar_ratio(portfolio_values):
    total_ret = total_return(portfolio_values) / 100  # rendimento annualizzato
    max_dd = max_drawdown(portfolio_values) / 100  # max drawdown
    return total_ret / max_dd if max_dd != 0 else np.inf  # gestiamo divisioni per zero

# Profit Factor
def profit_factor(prices, bitcoin_posseduti):
    total_gains = 0
    total_losses = 0
    
    bitcoin_posseduti_correnti = 0
    cost_basis = 0
    
    for i in range(len(prices)):
        prezzo_corrente = prices.iloc[i]
        bitcoin_correnti = bitcoin_posseduti.iloc[i]
        
        # Acquisto (aumento di bitcoin posseduti)
        if bitcoin_correnti > bitcoin_posseduti_correnti:
            bitcoin_acquistati = bitcoin_correnti - bitcoin_posseduti_correnti
            cost_basis = (cost_basis * bitcoin_posseduti_correnti + bitcoin_acquistati * prezzo_corrente) / bitcoin_correnti
            bitcoin_posseduti_correnti = bitcoin_correnti
        
        # Vendita (diminuzione di bitcoin posseduti)
        elif bitcoin_correnti < bitcoin_posseduti_correnti:
            bitcoin_venduti = bitcoin_posseduti_correnti - bitcoin_correnti
            pnl = bitcoin_venduti * (prezzo_corrente - cost_basis)
            if pnl > 0:
                total_gains += pnl
            else:
                total_losses += abs(pnl)
            bitcoin_posseduti_correnti = bitcoin_correnti
    
    if total_losses == 0:
        return float('inf')
    else:
        return total_gains / total_losses    

# PnL per singolo trade
def calcola_pnl(prices, bitcoin_posseduti):
    pnl_per_trade = []
    
    bitcoin_posseduti_correnti = 0
    cost_basis = 0
    
    for i in range(len(prices)):
        prezzo_corrente = prices.iloc[i]
        bitcoin_correnti = bitcoin_posseduti.iloc[i]
        
        # Acquisto
        if bitcoin_correnti > bitcoin_posseduti_correnti:
            bitcoin_acquistati = bitcoin_correnti - bitcoin_posseduti_correnti
            cost_basis = (cost_basis * bitcoin_posseduti_correnti + bitcoin_acquistati * prezzo_corrente) / bitcoin_correnti
            bitcoin_posseduti_correnti = bitcoin_correnti
        
        # Vendita
        elif bitcoin_correnti < bitcoin_posseduti_correnti:
            bitcoin_venduti = bitcoin_posseduti_correnti - bitcoin_correnti
            pnl = bitcoin_venduti * (prezzo_corrente - cost_basis)
            pnl_per_trade.append(pnl)
            bitcoin_posseduti_correnti = bitcoin_correnti
    
    return np.mean(pnl_per_trade)

def calcola_principali_metriche(portfolio_values, prices=None, bitcoin_posseduti=None, risk_free_rate=0.0):
    """
    Calcola le principali metriche di performance per un portafoglio.
    
    Parametri:
        - portfolio_values: Serie temporale dei valori del portafoglio.
        - prices: (opzionale) Serie temporale dei prezzi, necessaria per Profit Factor.
        - bitcoin_posseduti: (opzionale) Serie temporale della quantità di bitcoin posseduti, necessaria per Profit Factor.
        - risk_free_rate: Tasso privo di rischio annuale, espresso in percentuale (default 0.0).
        
    Restituisce:
        - Un dizionario con i valori di tutte le metriche calcolate.
    """
    risultati = {}
    
    # Rendimento Totale
    try:
        risultati["Total Return"] = total_return(portfolio_values)
    except Exception as e:
        risultati["Total Return"] = f"Errore: {e}"
    
    # Max Drawdown
    try:
        risultati["Max Drawdown"] = max_drawdown(portfolio_values)
    except Exception as e:
        risultati["Max Drawdown"] = f"Errore: {e}"
    
    # Volatilità
    try:
        risultati["Volatility"] = volatility(portfolio_values)
    except Exception as e:
        risultati["Volatility"] = f"Errore: {e}"
    
    # Sharpe Ratio
    try:
        risultati["Sharpe Ratio"] = sharpe_ratio(portfolio_values, risk_free_rate)
    except Exception as e:
        risultati["Sharpe Ratio"] = f"Errore: {e}"
    
    # Sortino Ratio
    try:
        risultati["Sortino Ratio"] = sortino_ratio(portfolio_values, risk_free_rate)
    except Exception as e:
        risultati["Sortino Ratio"] = f"Errore: {e}"
    
    # Calmar Ratio
    try:
        risultati["Calmar Ratio"] = calmar_ratio(portfolio_values)
    except Exception as e:
        risultati["Calmar Ratio"] = f"Errore: {e}"
    
    # Profit Factor (richiede prices e bitcoin_posseduti)
    if prices is not None and bitcoin_posseduti is not None:
        try:
            risultati["Profit Factor"] = profit_factor(prices, bitcoin_posseduti)
        except Exception as e:
            risultati["Profit Factor"] = f"Errore: {e}"
    else:
        risultati["Profit Factor"] = "Non calcolabile: dati insufficienti, servono prezzi e quantità di bitcoin posseduti"

    # PnL (richiede prices e bitconi_posseduti)
    if prices is not None and bitcoin_posseduti is not None:
        try:
            risultati["PnL"] = calcola_pnl(prices, bitcoin_posseduti)
        except Exception as e:
            risultati["PnL"] = f"Errore: {e}"
    else:
        risultati["PnL"] = "Non calcolabile: dati insufficienti, servono prezzi e quantità di bitcoin posseduti"
    
    return risultati




# Alpha
def alpha(portfolio_values, prices, beta):
    portfolio_returns = np.diff(portfolio_values) / portfolio_values[:-1]  # rendimenti del portafoglio
    market_returns = np.diff(prices) / prices[:-1]  # rendimenti del mercato (prezzi di Bitcoin)
    return np.mean(portfolio_returns) - beta * np.mean(market_returns)

# Beta
def beta(portfolio_values, prices):
    portfolio_returns = np.diff(portfolio_values) / portfolio_values[:-1]  # rendimenti del portafoglio
    market_returns = np.diff(prices) / prices[:-1]  # rendimenti del mercato (prezzi di Bitcoin)
    covariance = np.cov(portfolio_returns, market_returns)[0][1]
    market_variance = np.var(market_returns)
    return covariance / market_variance if market_variance != 0 else np.inf