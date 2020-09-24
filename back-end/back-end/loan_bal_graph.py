import os
import json
import pandas as pd
import plotly.graph_objects as go

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# print(os.getcwd())

@api_view(['GET','POST'])
def get_loan_bal_graph(request):
    if request.method == 'GET':

        cus_name = 'Ford, Eli'
        last_name, first_name = cus_name.split(',')
        first_name = first_name.strip().lower()
        last_name = last_name.strip().lower()

        top_labels = ['StudentLoanBal','CreditCardBal','AutoLoanBal','MortgageBal', 'OtherBal']

        df = pd.read_csv(os.getcwd() + '/back-end/downloadables/data/LPS_Demo_Output.csv')

        df['Last Name'] = df['Last Name'].str.lower()

        data = {}

        for label in top_labels:
            data[label] = (float(df.loc[df['Last Name'].str.contains(last_name), label].iloc[0]))

        sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}

        x_data = []
        y_data = []

        for k,v in sorted_data.items():
            x_data.append(v)
            y_data.append(k)

        fig = go.Figure(go.Bar(
                    x=x_data,
                    y=y_data,
                    orientation='h'))

        figure = {'data' : fig._data,
                    'layout' : fig._layout}

        return Response(json.dumps(figure, default=str), status=status.HTTP_200_OK)
    # fig.show()