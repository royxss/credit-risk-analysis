import pandas as pd
import io
import os
import numpy as np

from operator import itemgetter

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
# from xgboost import XGBClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models, initialize

# reference: https://towardsdatascience.com/intro-to-credit-scorecard-9afeaaa3725f

# df = pd.read_csv('back-end/downloadables/data/LPS_Demo_Output.csv')

@api_view(['GET','POST'])
def get_all_default(request):
    if request.method == 'GET':
        response_object = initialize.num_default['info']
        response_object.sort(key=lambda x: (-x['prob'], x['name']))
        return Response(response_object)

@api_view(['GET','POST'])
def get_all_good_standing(request):
    if request.method == 'GET':
        response_object = initialize.good_standing['info']
        response_object.sort(key=lambda x: (-x['prob'], x['name']))
        return Response(response_object)

@api_view(['GET','POST'])
def get_all_no_info(request):
    if request.method == 'GET':
        response_object = initialize.no_information['info']
        response_object.sort(key=lambda x: (x['name']))
        return Response(response_object)

@api_view(['GET','POST'])
def get_overall_stat(request):
    if request.method == 'GET':
        stat = {}
        stat['num_default'] = initialize.num_default['count']
        stat['good_standing'] = initialize.good_standing['count']
        stat['no_information'] = initialize.no_information['count']

        return Response([stat])

@api_view(['GET','POST'])
def getinfo(request):
    if request.method == 'GET':

        cus_id = int(request.query_params['id'])
            # print(cus_id)
        response_object = generate_response_object(cus_id)
        response_object = [response_object]
        return Response(response_object)

def generate_response_object(cus_id):

    df_train = initialize.df_train
    df_test = initialize.df_test
    strong,medium,weak = initialize.strong_feature,initialize.medium_feature,initialize.weak_feature
    df_reference = initialize.df_reference
    df_test_pred = initialize.df_test_pred
    metrics = initialize.metrics
    threshold = initialize.threshold
    df_test_pred.to_csv()
    feature_importance = []

    num_features = 8

    credit_score = get_credit_score(cus_id,df_test,df_reference)

    response_object = get_account_info(cus_id,df_test)

    if credit_score != 0:
        # print(strong)
        # print("\n")
        # print(medium)
        # print("\n")
        # print(weak)
        # print("\n")
        feature_importance.append(find_personalized_recommendation(strong,'high',df_reference,df_test,cus_id))
        feature_importance.append(find_personalized_recommendation(medium,'medium',df_reference,df_test,cus_id))
        feature_importance.append(find_personalized_recommendation(weak,'low',df_reference,df_test,cus_id))
        feature_importance = [item for sublist in feature_importance for item in sublist]
        feature_importance = get_features_to_improve(feature_importance,num_features)
        # feature_importance = feature_importance[:6]

        user_predictions = get_user_predictions(df_test_pred,cus_id,metrics,threshold)
        response_object['user_predictions'] = user_predictions
    else:
        response_object['user_predictions'] = generate_empty_prediction()

    top_spendings = get_top_spendings(cus_id,df_test)

    other_indicators = get_other_indicators(cus_id,df_test)

    # response_object['credit_score'] = get_credit_score(cus_id,df_test,df_reference)
    response_object['credit_score'] = credit_score
    response_object['feature_importance'] = feature_importance
    response_object['top_spendings'] = top_spendings
    response_object['other_indicators'] = other_indicators
    return response_object

def generate_empty_prediction():
    user_predictions = {}
    user_predictions['DefaultScore'] = 0
    user_predictions['FalseNegativeRate'] = 0
    user_predictions['FalsePositiveRate'] = 0
    user_predictions['TruePositiveRate'] = 0
    user_predictions['ProbabilisticCutoff'] = 0

    return user_predictions

def get_credit_score(id,df,df_reference):
    credit_bucket = str(df.loc[df['Id'] == id, 'ScoreBucket'].iloc[0])
    if credit_bucket.lower() == 'x':
        # credit_score = 'Not Available'
        credit_score = 0
    else:
        credit_score = find_credit_score(credit_bucket,df_reference)
    return credit_score

def get_account_info(id,df):
    account_info = {}
    account_info['first_name'] = str(df.loc[df['Id'] == id, 'First Name'].iloc[0])
    account_info['last_name'] = str(df.loc[df['Id'] == id, 'Last Name'].iloc[0])
    account_info['address_1'] = str(df.loc[df['Id'] == id, 'Address 1'].iloc[0])
    city = str(df.loc[df['Id'] == id, 'City'].iloc[0])
    state = str(df.loc[df['Id'] == id, 'State'].iloc[0])
    zip_code = int(df.loc[df['Id'] == id, '00Zip'].iloc[0])
    account_info['address_2'] = city + ' ' + state + ' ' + str(zip_code)
    account_info['dob'] = str(df.loc[df['Id'] == id, 'DOB'].iloc[0])
    if account_info['dob'] == 'nan':
        account_info['dob'] = ""
    # print(account_info['dob'])
    # account_info['debt_ratio'] = round(float(df.loc[df['Id'] == id, 'Debt_Ratio'].iloc[0]) * 100,2)
    # account_info['credit_utilization'] = round(float(df.loc[df['Id'] == id, 'Credit_Utilization'].iloc[0]) * 100,2)

    return account_info

def get_other_indicators(id,df):
    other_indicators = {}
    other_indicators['debt_ratio'] = {}
    other_indicators['credit_utilization'] = {}

    other_indicators['debt_ratio']['value'] = int(round(df.loc[df['Id'] == id, 'Debt_Ratio'].iloc[0] * 100,0))
    other_indicators['credit_utilization']['value'] = int(round(df.loc[df['Id'] == id, 'Credit_Utilization'].iloc[0] * 100,0))

    other_indicators['debt_ratio']['recommendation'] = 43
    other_indicators['credit_utilization']['recommendation'] = 10

    return other_indicators

def find_credit_score(score_bucket,df_reference):
    # df_reference = pd.read_csv('back-end/downloadables/data/LPC_Reference.csv', index_col=0)
    credit_range = str(df_reference.loc[df_reference['Bucket'].str.contains(str(score_bucket)),'Score range'].iloc[0])
    # print("Credit Range: " + credit_range)
    credit_range = credit_range.split('-')
    credit_score = int(round((int(credit_range[1]) + int(credit_range[0]))/2,0))
    return credit_score

def find_credit_range(score_bucket,df_reference):
    credit_range = str(df_reference.loc[df_reference['Bucket'].str.contains(str(score_bucket)),'Score range'].iloc[0])
    # print("Credit Range: " + credit_range)
    return credit_range

def find_credit_bucket(credit_score,df_reference):
    # df_reference = pd.read_csv('back-end/downloadables/data/LPC_Reference.csv', index_col=0)
    cut_off_bucket = str(df_reference.loc[df_reference['Score range'].str.contains(str(credit_score+1)),'Bucket'].iloc[0])
    # print("Cutoff Bucket: " + cut_off_bucket)
    return cut_off_bucket

def get_top_spendings(id,df):
    # top_spendings_list = []
    top_spendings = {}
    top_labels = ['StudentLoanBal','CreditCardBal','AutoLoanBal','MortgageBal', 'OtherBal']
    for label in top_labels:
        top_spendings[label] = (float(df.loc[df['Id'] == id, label].iloc[0]))
    top_spendings = {k: v for k, v in sorted(top_spendings.items(), key=lambda item: item[1],reverse=True)}
    # top_spendings_list.append(top_spendings)
    return top_spendings

def get_user_predictions(df,id, metrics,threshold):
    user_predictions = {}

    prediction = df.loc[df['Id'] == id,'Loan_Status_Prob'].iloc[0]

    print(prediction)
    # user_predictions['DefaultScore'] = round(int(df_test.loc[df_test['Id'] == id,'loan_status'].iloc[0]),2)
    user_predictions['DefaultScore'] = int(round(prediction[1]*100,0))
    user_predictions['FalseNegativeRate'] = int(round(metrics['fnr']*100,0))
    user_predictions['FalsePositiveRate'] = int(round(metrics['fpr']*100,0))
    user_predictions['TruePositiveRate'] = int(round(metrics['tpr']*100,0))
    user_predictions['ProbabilisticCutoff'] = int(round(threshold * 100,0))

    # print(user_predictions)
    # print(metrics)

    return user_predictions

def find_personalized_recommendation(predictors,impact,df_reference,df,cus_id):
    # strong,medium,weak = predictors
    # print(df.columns)
    l = []
    for k,v in predictors.items():
        d={}
        d['impact'] = impact
        zero_value_features = ['StudentLoanQty', 'StudentLoanDel', 'StudentLoanBal',
                                    'CreditCardQty', 'CreditCardDel', 'CreditCardBal',
                                    'AutoLoanQty', 'AutoLoanDel', 'AutoLoanBal',
                                    'MortgageQty','MortgageDel', 'MortgageBal',
                                    'OtherQty', 'OtherDel', 'OtherBal',
                                    'Monthly_Debt']

        high_value_features = ['Years_of_Credit_History', 'Months_since_last_delinquent','Monthly_Income','Maximum_Open_Credit']
        low_value_features = ['Monthly_Debt',
                            'StudentLoanQty','StudentLoanDel',
                            'CreditCardDel',
                            'AutoLoanQty','AutoLoanDel',
                            'MortgageQty','MortgageDel',
                            'OtherQty','OtherDel',]
        exclude_features = ['Monthly_Income','Credit_Utilization','Debt_Ratio']
        # print(k)
        add_feature_flag = 1
        if 'Bins' in k:
            feature = k.replace('_Bins','')
            value = df.loc[df['Id'] == cus_id, feature].iloc[0]
            lower_limit = float(predictors[k].left)
            upper_limit = float(predictors[k].right)
            if lower_limit < 0:
                lower_limit = 0

            # print(feature)
            # print(value)

            if feature in exclude_features:
                add_feature_flag = 0

            # if 'Credit_Utilization' in k or 'Debt_Ratio' in k:
            #     value = value * 100
            #     lower_limit = lower_limit * 100
            #     upper_limit = upper_limit * 100

            if value > upper_limit and feature in high_value_features:
                d['performance'] = 'good'
                d['text'] = "The customer is performing better than the ideal range of " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))

            elif value < lower_limit and feature in low_value_features:
                d['performance'] = 'good'
                d['text'] = "The customer is performing better than the ideal range of " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))

            elif value > lower_limit and value <= upper_limit:
                d['performance'] = 'good'
                d['text'] = "The customer is in the ideal range of " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))
                # add_feature_flag = 0
            else:
                d['performance'] = 'bad'
                d['text'] = "The customer can perform better if in the ideal range of " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))

            # d['text'] = "The ideal value is between " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))


            # if 'Credit_Utilization' in k or 'Debt_Ratio' in k:
            #     d['text'] = "The ideal value is between " + str(round(lower_limit,2)) + " and " + str(round(upper_limit,2))
            #     value = round(value,2)
            # else:
            #     d['text'] = "The ideal value is between " + str(int(round(lower_limit,0))) + " and " + str(int(round(upper_limit,0)))

            # if add_feature_flag == 0:
            #     print("feature: " + feature)
            #     print("value: " + str(value))
            #     print("upper limit: " + str(upper_limit))
            #     print("lower limit: " + str(lower_limit))
        else:
            feature = k
            value = df.loc[df['Id'] == cus_id, feature].iloc[0]
            ideal_value = predictors[k]

            if feature == 'ScoreBucket':
                credit_range = find_credit_range(value,df_reference)
                ideal_credit_range = find_credit_range(ideal_value,df_reference)

                if value < ideal_value:
                    d['performance'] = 'good'
                    d['text'] = "The customer is performing better than the ideal value of " + str(ideal_value) + " (" + ideal_credit_range + ")"

                elif value == ideal_value:
                    d['performance'] = 'good'
                    d['text'] = "The customer has the ideal value of " + str(ideal_value) + " (" + ideal_credit_range + ")"

                else:
                    d['performance'] = 'bad'
                    d['text'] = "The customer can perform better if they have an ideal value of " + str(ideal_value) + " (" + ideal_credit_range + ")"

                value = value + " (" + credit_range + ")"

                # add_feature_flag = 0

            else:

                # value = int(value)

                if value < ideal_value and feature in low_value_features:
                    d['performance'] = 'good'
                    d['text'] = "The customer is performing better than the ideal value of " + str(ideal_value)

                elif value > ideal_value and feature in high_value_features:
                    d['performance'] = 'good'
                    d['text'] = "The customer is performing better than the ideal value of " + str(ideal_value)

                elif value == ideal_value:
                    d['performance'] = 'good'
                    d['text'] = "The customer has the ideal value of " + str(ideal_value)
                    # add_feature_flag = 0
                else:
                    d['performance'] = 'bad'
                    d['text'] = "The customer can perform better if they have an ideal value of " + str(ideal_value)



            # d['text'] = "The ideal value is " + str(predictors[k])


        if value == 0 and feature in zero_value_features:
            add_feature_flag = 0
            # print("feature: " + feature)
            # print("value: " + str(value))

        if isinstance(value,(int,float)):
            value = int(round(value,0))

        d['feature']=feature
        d['value'] = value

        # d['text'] = "Some Text"
        if add_feature_flag == 1:
            l.append(d)
        # elif add_feature_flag == 0:
        #     print(feature + "\n")

    return l

def get_features_to_improve(feature_importance,n):
    bad_features = []
    good_features = []
    for f in feature_importance:
        if f['performance'] == 'bad':
            bad_features.append(f)
        else:
            good_features.append(f)

    diff = len(bad_features) - n
    if diff < 0:
        bad_features = bad_features + good_features[:-diff]
    elif diff > 0:
        bad_features = bad_features[:n]

    # bad_features.sort(key=itemgetter('performance'), reverse=True)
    # bad_features.sort(key=itemgetter('impact'))

    performance_sortorder = {"good":0,"bad":1}
    impact_sortorder = {"high":0,"medium":1,"low":2}
    bad_features.sort(key=lambda x: performance_sortorder[x["performance"]])
    bad_features.sort(key=lambda x: impact_sortorder[x["impact"]])

    if len(bad_features) %2 != 0:
        bad_features = bad_features[:(len(bad_features)-1)]

    return bad_features