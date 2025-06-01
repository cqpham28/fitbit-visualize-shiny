import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import utils
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

#===========================#
class Fetch_Visualize:
    def __init__(self, firecloudClient, user_name):
        self.firecloudClient = firecloudClient
        self.user_name = user_name
        self.data_A, self.day_A = self.get_Activity()
        self.data_ATS, self.day_ATS = self.get_ActivityTimeSeries()
        self.data_HRTS, self.day_HRTS = self.get_HeartRateTimeSeries()

    #--------------------------#
    def get_ref(self, scope:str):
        return utils.fetch(
            self.firecloudClient, 
            endpoints=[
                "fitbit", 
                "data-pilot", 
                 self.user_name, 
                scope
            ]
        )

    #--------------------------#
    def filter_time(self, df):

        df['time_new'] = pd.to_datetime(df['time'])
        start_time = pd.Timestamp(df['time_new'].dt.date.min()) + pd.Timedelta(hours=10)
        end_time = pd.Timestamp(df['time_new'].dt.date.min()) + pd.Timedelta(hours=16)
        df_filtered = df[(df['time_new'].dt.time >= start_time.time()) & (df['time_new'].dt.time <= end_time.time())]
        return df_filtered
        

    #--------------------------#
    def get_ActivityTimeSeries(self) -> None:
        print("<get_ActivityTimeSeries>")

        ref = self.get_ref(scope="_ActivityTimeSeries")
        tmp = {}
        for j, collection in enumerate(ref.collections()): # list of requests
            for doc in collection.stream():
                tmp[collection.id]  = doc.to_dict()

        data = {}
        for (_, value) in tmp.items(): 
            if "activities-steps-intraday" in value.keys():
                df = pd.DataFrame.from_dict(
                    value["activities-steps-intraday"].get("dataset")
                )
                date = value["activities-steps"][0].get("dateTime")
                total_steps = int(value["activities-steps"][0].get("value"))
                data[date] = (df, total_steps)

        return data, list(data.keys())

        

    #--------------------------#
    def plot_ActivityTimeSeries(self, df) -> None:   
        ## PLOT
        df_filtered = self.filter_time(df)
        df_filtered['time_shorten'] = df_filtered['time'].str.slice(stop=-3)


        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_filtered['time_shorten'],
                y=df_filtered['value'],
                mode='lines+markers',
                name='Value',
                line=dict(width=2), # Set dash style here
                marker=dict(size=6, symbol='circle'),
            )
        )
        # Update layout
        fig.update_layout(
            title=None,
            width=650,
            height=200,
            yaxis=dict(
                title=None,  # Remove y-axis title
            ),
            xaxis=dict(
                title=None,  # Remove x-axis title
                tickangle=-45,
            ),
        )
        return fig


    #--------------------------#
    def plot_gauge(self, suffix, title, value, max_value):
        """
        
        """
        valueformat = ',.0f' if isinstance(value, int) else ',.1f'

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            number={
                'valueformat': valueformat,
                'suffix': suffix,     # Add ' steps' suffix
                'font': {'size': 14}    # Optional: adjust font size
            },
            gauge={
                'axis': {'range': [0, max_value]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "lightblue"},
                    {'range': [max_value * 0.5, max_value], 'color': "lightblue"}
                ],
            }
        ))
        fig.update_layout(
            title=title,
            width=150, 
            height=150,
            margin=dict(l=1, r=1, t=40, b=5)  # Reduce padding
            )
        return fig


    #--------------------------#
    def get_HeartRateTimeSeries(self) -> None:
        """
        
        """
        print("<get_HeartRateTimeSeries>")
        ref = self.get_ref(scope="_HeartRateTimeSeries")
        tmp = {}
        for j, collection in enumerate(ref.collections()): # list of requests
            for doc in collection.stream():
                tmp[collection.id]  = doc.to_dict()

        data = {}
        for (_, value) in tmp.items(): 
            if "activities-heart-intraday" in value.keys():
                df = pd.DataFrame.from_dict(
                    value["activities-heart-intraday"].get("dataset")
                )
                date = value["activities-heart"][0].get("dateTime")
                data[date] = df

        return data, list(data.keys())



    #--------------------------#
    def plot_HeartRateTimeSeries(self, df) -> None:
        """
        
        """
        df_filtered = self.filter_time(df)            
        df_filtered['time_shorten'] = df_filtered['time'].str.slice(stop=-3)

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df_filtered['time_shorten'],
                y=df_filtered['value'],
                mode='lines+markers',
                name='Value',
                line=dict(width=2, color='green'), # Set dash style here
                marker=dict(size=6, symbol='circle'),
            )
        )
        # Update layout
        fig.update_layout(
            title=None,
            width=650,
            height=400,
            yaxis=dict(
                title=None,  # Remove y-axis title
            ),
            xaxis=dict(
                title=None,  # Remove x-axis title
                tickangle=-45,
            ),
        )

        return fig


    #--------------------------#
    def plot_HeartRateDistribution(self, df) -> None:
        """
        Plot the histogram of heart rate with a smooth  curve.
        """
        df_filtered = self.filter_time(df)
        hr_values = df_filtered['value']

        # Create histogram
        fig = go.Figure()

        # Add histogram
        fig.add_trace(
            go.Histogram(
                x=hr_values,
                nbinsx=30,
                name='HR Distribution',
                marker=dict(color='green', line=dict(width=1, color='black')),
                opacity=0.7,
                histnorm='probability density'  # Normalize to probability for comparison with KDE
            )
        )

        # Calculate KDE
        kde = gaussian_kde(hr_values)
        x_vals = np.linspace(hr_values.min(), hr_values.max(), 200)
        y_vals = kde(x_vals)

        # Add KDE line
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                name='KDE Curve',
                line=dict(color='red', width=2)
            )
        )

        # Update layout
        fig.update_layout(
            title=None,
            xaxis=dict(title=None),
            yaxis=dict(title=None),
            bargap=0.1,
            width=650,
            height=200,
            showlegend=True
        )

        return fig
    


    #--------------------------#
    def get_Activity(self) -> None:
        """
        
        """
        ref = self.get_ref(scope="_Activity")
        tmp = {}
        for j, collection in enumerate(ref.collections()): # list of requests
            for doc in collection.stream():
                tmp[collection.id]  = doc.to_dict()
        
        data = {}
        for (_, value) in tmp.items(): 
            if "summary" in value.keys():
                date = _.split(".json")[0].split("-date-")[1]
            
                df_activeDistance = pd.DataFrame.from_dict(value["summary"].get("distances"))
                activeMinutes = {
                    'Lightly Active': value["summary"].get("lightlyActiveMinutes", 0),
                    'Fairly Active': value["summary"].get("fairlyActiveMinutes", 0),
                    'Very Active': value["summary"].get("veryActiveMinutes", 0),
                }
                
                data[date] = (df_activeDistance, activeMinutes)

        return data, list(data.keys())



    #--------------------------#
    def plot_ActiveMinutes(self, activeMinutes) -> None:

        # Create the bar plot
        fig = go.Figure(
            go.Bar(
                x=list(activeMinutes.keys()),
                y=list(activeMinutes.values()),
                marker_color = px.colors.qualitative.Set3[:3]
            )
        )
        
        # Layout adjustments
        fig.update_layout(
            title=None,
            xaxis_title="Activity Level",
            yaxis_title="Minutes",
            width=400,
            height=200
        )

        return fig
    


    #--------------------------#
    def plot_ActiveDistances(self, df_activeDistances) -> None:

        activities = ['lightlyActive', 'moderatelyActive', 'veryActive']
        filtered_df = df_activeDistances[df_activeDistances['activity'].isin(activities)]

        # Prepare labels and values
        labels = filtered_df['activity']
        values = filtered_df['distance']

        # Create bar plot
        fig = go.Figure(
            go.Bar(
                x=labels,
                y=values,
                marker_color=px.colors.qualitative.Pastel[:3]
            )
        )
        
        # Update layout
        fig.update_layout(
            title=None,
            yaxis_title="Distance",
            xaxis_title="Activity Level",
            width=400,
            height=200
        )
        
        return fig