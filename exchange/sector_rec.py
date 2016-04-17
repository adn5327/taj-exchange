from .models import *


percent_modification = .25
risk_change = 1

risk_map = {
            'Technology': .85,
            'Financials': .77,
            'Energy':.73,
            'Healthcare':.57,
            'Telecom':.48,
            'Cyclical Goods':.40,
            'Industrials':.30,
            'NonCyclical Goods': .20,
            'Utilities':.18,
            'Basic Materials':.15,
            }


def calculate_current_risk(account):
    account_possessions = Possessions.objects.filter(account_id=account)
    risk = 0
    total_possessions = 0
    for possession in account_possessions:
        pos_risk = possession.total_amount * risk_map[possession.security_id.sector]
        total_possessions += possession.total_amount
        risk += pos_risk
    # risk = risk * 10
    risk = (float(risk) / float(total_possessions))*10
    return risk, total_possessions

def computeStrategy(depth, risk, total_possessions):
    raw_risk = risk / 10 

def aggressive():
    return computeStrategy()
    pass

def moderate():
    pass

def safe():
    pass
