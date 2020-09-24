import pandas as pd
import io
import os
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
# from xgboost import XGBClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models

df_train = None
df_test = None
df_reference = None
strong_feature = None
medium_feature = None
weak_feature = None
df_test_pred = None
metrics = None
threshold = None
num_default = None
good_standing = None
no_information = None

def initialize():
    global df_test
    global df_train
    global df_reference
    global df_test_pred
    global strong_feature
    global medium_feature
    global weak_feature
    global threshold
    global num_default
    global good_standing
    global no_information

    threshold = 0.41

    df_train = pd.read_csv('back-end/downloadables/data/LPC_Modified_Train.csv', index_col=0)
    df_test = pd.read_csv('back-end/downloadables/data/LPC_Modified_Test.csv')
    df_reference = pd.read_csv('back-end/downloadables/data/LPC_Reference.csv', index_col=0)
    # strong_feature,medium_feature,weak_feature = calculate_iv(df_train)
    strong_feature,medium_feature,weak_feature = calculate_iv(df_train,df_test)

    d_train,d_test = models.pre_process_woe(df_train,df_test)

    # df_test_pred = train_model(df_train,df_test,df_test,threshold)
    df_test_pred = train_model(d_train,d_test,df_test,threshold)

    num_default,good_standing,no_information = overall_stat(df_test,df_test_pred,threshold)


def train_model(d_train,d_test,df_test,threshold):
    global metrics

    print("\n\nTRAINING MODEL......")

    d_train = d_train.copy()
    d_test = d_test.copy()
    # d_train = models.pre_process(d_train)

    #Logistic Regression
    lregclassifier = LogisticRegression()
    model, tneg,fpos,fneg,tpos = models.model_train(d_train, lregclassifier, threshold)
    metrics = models.calculate_metrics(tneg,fpos,fneg,tpos)

    # x_id = df_test.loc[df_test['ScoreBucket'].str.contains("X"),'Id'].tolist()
    df = df_test.copy()
    df = df[~df.ScoreBucket.str.contains("X")]
    # df = models.pre_process(df)

    model_prob = models.model_predict(d_test,model)

    model_prob = model_prob.tolist()

    # for i in x_id:
    #     model_pred.insert(i+1,0)

    model_pred = []

    for prob in model_prob:
        if prob[1] >= threshold:
            model_pred.append(1)
        elif prob[1] < threshold:
            model_pred.append(0)

    df['Loan_Status_Prob'] = model_prob
    df['Loan_Status'] = model_pred
    # print(df[['First Name','Loan_Status_Prob','Loan_Status']])
    return df

def overall_stat(df_test,df_pred,threshold):

    num_default = {}
    good_standing = {}
    no_information = {}

    defaulter_list = df_pred.loc[df_pred['Loan_Status'] == 1][['Id','First Name','Last Name','Loan_Status_Prob', 'City','State','00Zip']]
    defaulter_list['name'] = defaulter_list['First Name'].str.strip() + " " + defaulter_list['Last Name'].str.strip()
    defaulter_list['00Zip'] = defaulter_list['00Zip'].astype(str)
    defaulter_list['address'] = defaulter_list['City'].str.strip() + ", " + defaulter_list['State'].str.strip() + "-" + defaulter_list['00Zip'].str.strip()
    num_default['count'] = defaulter_list.shape[0]
    num_default['info'] = []
    for index,row in defaulter_list.iterrows():
        num_default['info'].append({'id': row['Id'],
                                    'name':row['name'],
                                    'prob':int(round(row['Loan_Status_Prob'][1]*100,0)),
                                    'address':str(row['address'])})

    # print(num_default)

    good_standing_list = df_pred.loc[df_pred['Loan_Status'] == 0][['Id','First Name','Last Name','Loan_Status_Prob', 'City','State','00Zip']]
    good_standing_list['name'] = good_standing_list['First Name'].str.strip() + " " + good_standing_list['Last Name'].str.strip()
    good_standing_list['00Zip'] = good_standing_list['00Zip'].astype(str)
    good_standing_list['address'] = good_standing_list['City'].str.strip() + ", " + good_standing_list['State'].str.strip() + "-" + good_standing_list['00Zip'].str.strip()
    good_standing['count'] = good_standing_list.shape[0]
    good_standing['info'] = []
    for index,row in good_standing_list.iterrows():
        good_standing['info'].append({'id':row['Id'],
                                    'name':row['name'],
                                    'prob':int(round(row['Loan_Status_Prob'][1]*100,0)),
                                    'address':str(row['address'])})

    no_info_list = df_test.loc[df_test['ScoreBucket'] == 'X'][['Id','First Name','Last Name', 'City','State','00Zip']]
    no_info_list['name'] = no_info_list['First Name'].str.strip() + " " + no_info_list['Last Name'].str.strip()
    no_info_list['00Zip'] = no_info_list['00Zip'].astype(str)
    no_info_list['address'] = no_info_list['City'].str.strip() + ", " + no_info_list['State'].str.strip() + "-" + no_info_list['00Zip'].str.strip()
    no_information['count'] = no_info_list.shape[0]
    no_information['info'] = []
    for index,row in no_info_list.iterrows():
        no_information['info'].append({'id':row['Id'],
                                        'name':row['name'],
                                        'prob': 0,
                                        'address':str(row['address'])})

    return num_default,good_standing,no_information

def calculate_iv(d_train,d_test):

    print("\n\nCALCULATING WOE......")

    d_train = d_train.copy()
    d_test = d_test.copy()

    not_required_columns = ['DOB','First Name','Last Name', 'Address 1', 'City', 'State', '00Zip','Annual_Income']
    d_train = models.remove_columns(d_train,not_required_columns)
    d_test = models.remove_columns(d_test,not_required_columns)
    df_all = pd.concat([d_train, d_test], ignore_index=True)

    feature_bins = ['StudentLoanBal','CreditCardBal','AutoLoanBal','MortgageBal','OtherBal',
                    'Monthly_Debt', 'Years_of_Credit_History', 'Months_since_last_delinquent',
                    'Maximum_Open_Credit', 'Monthly_Income', 'Debt_Ratio','Credit_Utilization']
    df_all = models.create_bins(df_all,feature_bins)

    mask = df_all['Loan_Status'].isna()
    d_train = df_all[~mask]
    # d_test = df_all[mask]

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

    feature_list = ['ScoreBucket',
            'StudentLoanQty', 'StudentLoanDel', 'StudentLoanBal_Bins',
            'CreditCardQty', 'CreditCardDel', 'CreditCardBal_Bins',
            'AutoLoanQty', 'AutoLoanDel', 'AutoLoanBal_Bins',
            'MortgageQty','MortgageDel', 'MortgageBal_Bins',
            'OtherQty', 'OtherDel', 'OtherBal_Bins',
            'Monthly_Debt_Bins', 'Years_of_Credit_History_Bins', 'Months_since_last_delinquent_Bins',
            'Maximum_Open_Credit_Bins', 'Monthly_Income_Bins', 'Debt_Ratio_Bins','Credit_Utilization_Bins']

    # iv > 0.3 -> strong predictor; iv >0.1 and iv < 0.3 -> medium predictors
    strong_predictors={}
    medium_predictors={}
    weak_predictors={}

    for feature in feature_list:
        # print('WoE and IV for column: {}'.format(feature))
        woe_df, iv = calculate_woe_iv(d_train, feature, 'Loan_Status')
        # print(woe_df)
        # print('IV score: {:.2f}'.format(iv))
        # print('\n')

        if iv >= 0.3:
            strong_predictors[feature] = woe_df['Value'][0]
        elif iv < 0.3 and iv >= 0.1:
            medium_predictors[feature] = woe_df['Value'][0]
        elif iv < 0.1:
            weak_predictors[feature] = woe_df['Value'][0]

    # print("\nStrong Predictors: ")
    # print(strong_predictors)

    # print("\nMedium Predictors: ")
    # print(medium_predictors)

    # print("\nWeak Predictors: ")
    # print(weak_predictors)

    return [strong_predictors,medium_predictors,weak_predictors]