from .models import *

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
    for possession in account_possessions:
        pos_risk = possession.total_amount * risk_map[possession.security_id.sector]
        risk += pos_risk
    risk = risk*10
    return risk

def aggressive():
    pass

def moderate():
    pass

def safe():
    pass
