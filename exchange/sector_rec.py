from .models import *


percent_modification = .25
risk_change = 1
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
	for i in range(lensec):
		cur_sec = sectors[i]
		cur_risk_adjusted += percent_modification*10*len_map[lensec][i]*risk_map[cur_sec]
	return cur_risk_adjusted


def getDeltaUpdate(risk, cur_list, low, high):
    target_high = risk + risk_change
    target_low = risk - risk_change
    potential = update_risk(risk, cur_list)
    delta_high = abs(target_high - potential)
    delta_low = abs(target_low - potential)
    low = checkIfBetter(low, delta_low, cur_list)
    high = checkIfBetter(high, delta_high, cur_list)
    return low, high


def recommend(risk, strategy):
    target_high = risk + risk_change
    target_low = risk - risk_change
    prev_sector_high = (None, 10)
    prev_sector_low = (None, 10)
    for i in range(len(sec_list)):
        if strategy == 'Aggressive':
            cur_list = [sec_list[i]]
            prev_sector_low, prev_sector_high = getDeltaUpdate(risk, cur_list, prev_sector_low, prev_sector_high)
        else:
            for j in range(i+1, len(sec_list)):
                if strategy == 'Moderate':
                    cur_list = [sec_list[i], sec_list[j]]
                    prev_sector_low, prev_sector_high = getDeltaUpdate(risk, cur_list, prev_sector_low, prev_sector_high)
                else:
                    for k in range(j+1, len(sec_list)):
                        cur_list = [sec_list[i], sec_list[j], sec_list[k]]
                        prev_sector_low, prev_sector_high = getDeltaUpdate(risk, cur_list, prev_sector_low, prev_sector_high)

    return prev_sector_low, prev_sector_high
                
def aggressive(risk):
    return recommend(risk, 'Aggressive')

def moderate(risk):
    return recommend(risk, 'Moderate')

def safe(risk):
    return recommend(risk, 'Safe')

def checkIfBetter(curr_best, new_delta, new_list):
    if new_delta < curr_best[1]:
        return (new_list, new_delta)
    else:
        return curr_best


