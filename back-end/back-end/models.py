import pandas as pd
import io
import os
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
# from xgboost import XGBClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier


def remove_collinear_features(x, threshold):
    '''
    Objective:
        Remove collinear features in a dataframe with a correlation coefficient
        greater than the threshold. Removing collinear features can help a model
        to generalize and improves the interpretability of the model.

    Inputs:
        threshold: any features with correlations greater than this value are removed

    Output:
        dataframe that contains only the non-highly-collinear features
    '''

    # Dont want to remove correlations between Energy Star Score
    x = x.copy()
    y = x['Loan_Status']
    x = x.drop(columns = ['Loan_Status'])

    # Calculate the correlation matrix
    corr_matrix = x.corr()
    iters = range(len(corr_matrix.columns) - 1)
    drop_cols = []

    # Iterate through the correlation matrix and compare correlations
    for i in iters:
        for j in range(i):
            item = corr_matrix.iloc[j:(j+1), (i+1):(i+2)]
            col = item.columns
            row = item.index
            val = abs(item.values)

            # If correlation exceeds the threshold
            if val >= threshold:
                # Print the correlated features and the correlation value
                # print(col.values[0], "|", row.values[0], "|", round(val[0][0], 2))
                drop_cols.append(col.values[0])

    # Drop one of each pair of correlated columns
    drops = set(drop_cols)
    x = x.drop(columns = drops)

    # Add the score back in to the data
    x['Loan_Status'] = y

    return x

def remove_columns(df,col_list):
    df = df.copy()
    for col in col_list:
        if col in df.columns:
            df.drop(labels=[col],axis=1,inplace=True)
    return df

def create_bins(df,col_list):

    df = df.copy()
    for col in col_list:
        df[col + '_Bins'] = pd.qcut(df[col],5,duplicates = 'drop')

    df = remove_columns(df,col_list)

    return df

def one_hot_encode(df,col_list):
    df = df.copy()
    for col in col_list:
        # print(col)
        df = df.join(pd.get_dummies(df[col],prefix=col, drop_first = True))
        df = remove_columns(df,[col])
    return df

def pre_process_woe(d_train,d_test):
    d_train = d_train.copy()
    d_test = d_test.copy()
    not_required_columns = ['DOB','First Name','Last Name', 'Address 1', 'City', 'State', '00Zip','Annual_Income']

    d_train = remove_columns(d_train,not_required_columns)
    d_test = remove_columns(d_test,not_required_columns)

    all_columns = d_train.columns
    d_train = remove_collinear_features(d_train,0.6)
    d_test = d_test[~d_test.ScoreBucket.str.contains("X")]

    non_collinear_columns = d_train.columns
    collinear_columns = [d for d in all_columns if d not in non_collinear_columns]
    d_test=remove_columns(d_test,collinear_columns)

    df_all = pd.concat([d_train, d_test], ignore_index=True)

    feature_bins = ['StudentLoanBal','CreditCardBal','AutoLoanBal','MortgageBal','OtherBal',
                    'Monthly_Debt', 'Years_of_Credit_History', 'Months_since_last_delinquent',
                    'Credit_Utilization']
    df_all = create_bins(df_all,feature_bins)

    cols = df_all.columns.tolist()
    cols.remove('Loan_Status')
    df_all = one_hot_encode(df_all,cols)

    mask = df_all['Loan_Status'].isna()
    d_train = df_all[~mask]
    d_test = df_all[mask]

    return d_train,d_test

def pre_process(credit):
    credit.drop(labels=['First Name','Last Name', 'Address 1', 'City', 'State', '00Zip','Annual_Income','Debt_Ratio', 'Credit_Utilization'],axis=1,inplace=True)

    credit = credit[~credit.ScoreBucket.str.contains("X")]

    credit['Credit Age'] = credit['Years_of_Credit_History'].apply(lambda x: "Short Credit Age" if x<5 else ("Good Credit Age" if x>5 and x<17 else "Exceptional Credit Age"))
    credit = credit.join(pd.get_dummies(credit['Credit Age'],drop_first = True))
    credit = credit.drop(['Credit Age','Years_of_Credit_History'], axis =1)

    credit['Years_in_current_job']=credit['Years_in_current_job'].str.extract(r"(\d+)")
    credit['Years_in_current_job'] = credit['Years_in_current_job'].astype(float)
    credit['Employment History'] = credit['Years_in_current_job'].apply(lambda x: "Emp Level Jr." if x<4 else ("Emp Level Mid" if x>4 and x<8 else "Emp Senior"))
    credit = credit.join(pd.get_dummies(credit['Employment History'],drop_first = True))
    credit = credit.drop(['Years_in_current_job','Employment History'], axis=1)

    credit['ScoreBucket'] = credit['ScoreBucket'].apply(lambda val: "Poor Credit" if val > "O" else val)
    credit['ScoreBucket'] = credit['ScoreBucket'].apply(lambda val: "Average Credit" if (val <= "O" and val > "G") else val)
    credit['ScoreBucket'] = credit['ScoreBucket'].apply(lambda val: "Good Credit" if (val <= "G" and val > "C") else val)
    credit['ScoreBucket'] = credit['ScoreBucket'].apply(lambda val: "Very Good Credit" if (val <= "C" and val > "B") else val)
    credit['ScoreBucket'] = credit['ScoreBucket'].apply(lambda val: "Exceptional Credit" if (val <= "B" and val >= "A") else val)
    credit = credit.join(pd.get_dummies(credit['ScoreBucket'], drop_first = True))
    credit = credit.drop(['ScoreBucket'], axis=1)

    def loan_to_categorical(credit,qty):
        credit[qty] = credit[qty].apply(lambda x: "No " + qty if x==0 else ("Some " + qty if x>0 and x<5 else "Major " + qty))
        credit = credit.join(pd.get_dummies(credit[qty],drop_first = True))
        credit = credit.drop([qty], axis=1)
        return credit

    # delinquent_subset = credit[['StudentLoanDel','CreditCardDel','AutoLoanDel','MortgageDel','OtherDel']]
    # delinquent_subset = pd.get_dummies(delinquent_subset)
    # credit.drop(labels=['StudentLoanDel','CreditCardDel','AutoLoanDel','MortgageDel','OtherDel'], axis=1, inplace=True)
    # credit = pd.concat([credit, delinquent_subset], axis = 1)

    loan_features = ['StudentLoanQty','CreditCardQty','AutoLoanQty','MortgageQty','OtherQty','StudentLoanDel','CreditCardDel','AutoLoanDel','MortgageDel','OtherDel']
    for qty in loan_features:
        credit = loan_to_categorical(credit,qty)

    # def continuous_to_categorical(credit,feature):
    #   meanxoutlier = credit[credit[feature] < 99999999.00 ][feature].mean()
    #   stddevxoutlier = credit[credit[feature] < 99999999.00 ][feature].std()
    #   poorline = meanxoutlier -  stddevxoutlier
    #   richline = meanxoutlier + stddevxoutlier
    #   credit[feature] = credit[feature].apply(lambda x: "Low " + feature if x<=poorline else ("Average " + feature if x>poorline and x<richline else "High " + feature))
    #   credit = credit.join(pd.get_dummies(credit[feature],drop_first = True))
    #   credit = credit.drop([feature], axis=1)
    #   return credit

    # continuous_columns = ['StudentLoanBal','StudentLoanQty',
    #                       'CreditCardBal','CreditCardQty',
    #                       'AutoLoanBal','AutoLoanQty',
    #                       'OtherBal','OtherQty',
    #                       'MortgageBal','MortgageQty',
    #                       'Monthly_Debt','Maximum_Open_Credit','Monthly_Income']
    # for feature in continuous_columns:
    #   credit = continuous_to_categorical(credit,feature)

    return credit

def model_train(credit,model,threshold):
    y = credit['Loan_Status']
    x = credit.drop(['Loan_Status'],axis=1)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify = y)

    model.fit(x_train,y_train)
    # model_pred = model.predict(x_test)
    model_pred = (model.predict_proba(x_test) >= threshold).astype(int)
    model_pred = [d[1] for d in model_pred]
    # print(model_pred)
    tneg, fpos, fneg, tpos = confusion_matrix(y_test, model_pred).ravel()

    return model, tneg,fpos,fneg,tpos



# train_cols = credit.columns
# test_cols = df.columns
# unmatched_train = [d for d in train_cols if d not in test_cols]
# unmatched_test = [d for d in test_cols if d not in train_cols]
# print(unmatched_train)
# print(unmatched_test)

def model_predict(df, model):
    df = df.copy()
    df = remove_columns(df,['Loan_Status','DOB','Id'])
    # df = df.drop(['Loan_Status','DOB','Id'], axis=1)
    # model_pred = model.predict(df)
    model_pred = model.predict_proba(df)

    # model_pred = (model.predict_proba(df) >= 0.4).astype(int)
    # model_pred = [d[1] for d in model_pred]

    # print(model_pred)
    return model_pred

def calculate_metrics(tneg,fpos,fneg,tpos):

    metrics={}

    # metrics['tp'] = tpos
    # metrics['fn'] = fneg
    # metrics['tn'] = tneg
    # metrics['fp'] = fpos

    # Sensitivity, hit rate, recall, or true positive rate
    metrics['tpr'] = tpos/(tpos+fneg)
    # Precision or positive predictive value
    metrics['ppv'] = tpos/(tpos+fpos)
    # Fall out or false positive rate
    metrics['fpr'] = fpos/(fpos+tneg)
    # False negative rate
    metrics['fnr'] = fneg/(tpos+fneg)
    # Specificity or true negative rate
    metrics['tnr'] = tneg/(tneg+fpos)
    # Negative predictive value
    metrics['npv'] = tneg/(tneg+fneg)
    # False discovery rate
    metrics['fdr'] = fpos/(tpos+fpos)
    # Accuracy
    metrics['acc'] = (tpos+tneg)/(tpos+tneg+fpos+fneg)

    # print(metrics)
    return metrics