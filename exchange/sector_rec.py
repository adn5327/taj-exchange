from .models import *


percent_modification = .25
risk_change = 1
len2 = [.50,.50]
len3 = [.50,.25,.25]
sec_list = ['Technology', 'Financials', 'Energy',
            'Healthcare', 'Telecom', 'Cyclical Goods',
            'Industrials', 'NonCyclical Goods', 
            'Utilities', 'Basic Materials']
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
    if len(account_possessions) == 0:
        return 0, 0
    risk = 0
    total_possessions = 0
    for possession in account_possessions:
        pos_risk = possession.total_amount * risk_map[possession.security_id.sector]
        total_possessions += possession.total_amount
        risk += pos_risk
    # risk = risk * 10
    risk = (float(risk) / float(total_possessions))*10
    return risk, total_possessions

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

def recommend(risk, strategy):
    target_high = risk + risk_change
    target_low = risk - risk_change
    prev_sector_high = (None, 10)
    prev_sector_low = (None, 10)
    for i in range(len(sec_list)):
        cur_list = list()
        cur_list.append(sec_list[i])    
        if strategy != 'Aggressive':
            for j in range(i+1, len(sec_list)):
                cur_list.append(sec_list[j])
                if strategy != 'Moderate':
                    for k in range(j+1, len(sec_list)):
                        cur_list.append(sec_list[k])

        potential = update_risk(risk, cur_list)
        delta_high = abs(target_high - potential)
        delta_low = abs(target_low - potential)
        prev_sector_low = checkIfBetter(prev_sector_low, delta_low, cur_list)
        prev_sector_high = checkIfBetter(prev_sector_high, delta_high, cur_list)

    return prev_sector_low, prev_sector_high
                
def aggressive(risk):
    return recommend(risk, 'Aggressive')

def moderate(risk):
    return recommend(risk, 'Moderate')

def safe():
    return recommend(risk, 'Safe')

def checkIfBetter(curr_best, new_delta, new_list):
    if new_delta < curr_best[1]:
        return (new_list, new_delta)
    else:
        return curr_best


