import pandas as pd
import io
import os
import numpy as np

from rest_framework.decorators import api_view
from rest_framework.response import Response

# reference: https://towardsdatascience.com/intro-to-credit-scorecard-9afeaaa3725f

# df = pd.read_csv('back-end/downloadables/data/LPS_Demo_Output.csv')

@api_view(['GET','POST'])
def getinfo(request):
    if request.method == 'GET':

        cus_id = 6
        cut_off_score = 700

        cut_off_bucket = find_cut_off_bucket(cut_off_score)
        strong,medium,weak,df = calculate_iv(cut_off_bucket)

        response_object = []

        response_object.append(find_personalized_recommendation(strong,'high',df,cus_id))
        response_object.append(find_personalized_recommendation(medium,'medium',df,cus_id))
        response_object.append(find_personalized_recommendation(weak,'low',df,cus_id))

        response_object = [item for sublist in response_object for item in sublist]

        # content = {'message': 'Should return a meaningful info'}
        return Response(response_object)

def find_cut_off_bucket(cut_off_score = 700):
    df_reference = pd.read_csv('back-end/downloadables/data/LPC_Reference.csv', index_col=0)
    cut_off_bucket = str(df_reference.loc[df_reference['Score range'].str.contains(str(cut_off_score+1)),'Bucket'].iloc[0])
    print("Cutoff Bucket: " + cut_off_bucket)
    return cut_off_bucket


def calculate_iv(cut_off_bucket):

    df = pd.read_csv('back-end/downloadables/data/LPS_Demo_Output.csv')

    # removing rows with error
    df = df[df['IsError'] == False]
    df.drop(['IsError','ErrorDescription'], axis = 1, inplace = True)

    # finding age
    df['DOB'] = df['DOB'].fillna(value='01/01/1969') # most of the customers had dob 1969; so filling empty values with 1969
    df['DOB'] = pd.to_datetime(df['DOB'])
    now = pd.Timestamp('now')
    df['Age'] = (now - df['DOB']).astype('timedelta64[Y]')

    # separating into bins for woe calculation
    df['Age_Bins'] = pd.qcut(df['Age'],4, duplicates = 'drop')
    df['StudentLoanBal_Bins'] = pd.qcut(df['StudentLoanBal'],4, duplicates = 'drop')
    df['CreditCardBal_Bins'] = pd.qcut(df['CreditCardBal'],4, duplicates = 'drop')
    df['AutoLoanBal_Bins'] = pd.qcut(df['AutoLoanBal'],4, duplicates = 'drop')
    df['MortgageBal_Bins'] = pd.qcut(df['MortgageBal'],4, duplicates = 'drop')
    df['OtherBal_Bins'] = pd.qcut(df['OtherBal'],4, duplicates = 'drop')

    # setting target value based on the cut_off
    def targetValue(row):
        if row['ScoreBucket'] <= cut_off_bucket:
            return 1
        else:
            return 0

    df['Target'] = df.apply (lambda row: targetValue(row), axis=1)


    # calculating woe and iv from the formula in the reference
    def calculate_woe_iv(dataset, feature, target):
        lst = []
        for i in range(dataset[feature].nunique()):
            val = list(dataset[feature].unique())[i]
            lst.append({
                'Value': val,
                'All': dataset[dataset[feature] == val].count()[feature],
                'Good': dataset[(dataset[feature] == val) & (dataset[target] == 0)].count()[feature],
                'Bad': dataset[(dataset[feature] == val) & (dataset[target] == 1)].count()[feature]
            })

        dset = pd.DataFrame(lst)
        dset['Distr_Good'] = dset['Good'] / dset['Good'].sum()
        dset['Distr_Bad'] = dset['Bad'] / dset['Bad'].sum()
        dset['WoE'] = np.log(dset['Distr_Good'] / dset['Distr_Bad'])
        dset = dset.replace({'WoE': {np.inf: 0, -np.inf: 0}})
        dset['IV'] = (dset['Distr_Good'] - dset['Distr_Bad']) * dset['WoE']
        iv = dset['IV'].sum()

        dset = dset.sort_values(by='WoE')

        return dset, iv

    feature_list = ['Age_Bins',
            'StudentLoanQty', 'StudentLoanDel', 'StudentLoanBal_Bins',
            'CreditCardQty', 'CreditCardDel', 'CreditCardBal_Bins',
            'AutoLoanQty', 'AutoLoanDel', 'AutoLoanBal_Bins',
            'MortgageQty','MortgageDel', 'MortgageBal_Bins',
            'OtherQty', 'OtherDel', 'OtherBal_Bins']

    # iv > 0.3 -> strong predictor; iv >0.1 and iv < 0.3 -> medium predictors
    strong_predictors={}
    medium_predictors={}
    weak_predictors={}

    for feature in feature_list:
        print('WoE and IV for column: {}'.format(feature))
        woe_df, iv = calculate_woe_iv(df, feature, 'Target')
        # print(woe_df)
        print('IV score: {:.2f}'.format(iv))
        print('\n')

        if iv >= 0.3:
            strong_predictors[feature] = woe_df['Value'][0]
        elif iv < 0.3 and iv >= 0.1:
            medium_predictors[feature] = woe_df['Value'][0]
        elif iv < 0.1:
            weak_predictors[feature] = woe_df['Value'][0]

    print(strong_predictors)
    print(medium_predictors)
    print(weak_predictors)

    return [strong_predictors,medium_predictors,weak_predictors,df]

def find_personalized_recommendation(predictors,impact,df,cus_id):
    # strong,medium,weak = predictors
    l = []
    for k,v in predictors.items():
        d={}
        d['impact'] = impact
        print(k)
        if 'Bins' in k:
            feature = k.replace('_Bins','')
            value = int(df.loc[df['Id'] == cus_id, feature].iloc[0])
            lower_limit = float(predictors[k].left)
            upper_limit = float(predictors[k].right)
            if value < lower_limit and value >= upper_limit:
                d['performance'] = 'good'
            else:
                d['performance'] = 'bad'

        else:
            feature = k
            value = int(df.loc[df['Id'] == cus_id, feature].iloc[0])
            if value <= predictors[k]:
                d['performance'] = 'good'
            else:
                d['performance'] = 'bad'

        d['feature']=feature
        d['value'] = value

        l.append(d)

    return l