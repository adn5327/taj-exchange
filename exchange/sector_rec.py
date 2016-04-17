from .models import *


percent_modification = .25
risk_change = 1
len2 = [.50,.50]
len3 = [.50,.25,.25]
len_map = {
		1 : [1],
		2 : [.50,.50],
		3 : [.50,.25,.25],
		}

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

def computeStrategy(depth, sectors, risk, target, total_possessions):
    if depth == 0:
        return sectors

    for sector in risk_map:
        amount = total_possessions * percent_modification
        potential_risk = risk + (amount * risk_map[sector])
        potential_risk = (float(potential_risk) / float(total_possessions+amount)) * 10
        sectors.append()


    raw_risk = float(risk / 10)*total_possessions


def aggressive(risk, total_possessions):
    target_high = risk + risk_change
    target_low = risk - risk_change

def update_risk(current_risk, sectors):
	cur_risk_adjusted = (1-percent_modification)*current_risk
	lensec = len(sectors)
	'''
	if lensec == 1:
		cur_sec = sectors[0]
		return cur_risk_adjusted + percent_modification*10*risk_map[cur_sec]
	'''
	for i in range(lensec):
		cur_sec = sectors[i]
		cur_risk_adjusted += percent_modification*10*len_map[lensec][i]*risk_map[cur_sec]
	return cur_risk_adjusted

def aggressive():
    return computeStrategy()
    pass

def moderate():
    pass

def safe():
    pass
