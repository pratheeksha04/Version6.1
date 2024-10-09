
import time
import dash
from dash import Dash, _dash_renderer, dcc, callback, Input, Output, State,html, exceptions

import dash_mantine_components as dmc
from dash_iconify import DashIconify
import os
import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc
import plotly.graph_objs as go
_dash_renderer._set_react_version("18.2.0")
import numpy as np
from ipmclass import ipmclass
from DigiTwin import DigiTwin
from PsiLdLq import PsiLdLq
from ipmclass import ipmclass
from evsimclass import evsimclass
from wltcclass import wltcclass
from OrdMatCalc import OrdMatCalc
from LossTypeCalc import LossTypeCalc
from dash import dash_table as dt
from dash import callback_context
from stdrpm import stdrpm
from stdnm_omega import stdnm_omega
from plotly.subplots import make_subplots
import dash_ag_grid as dag
from scipy.spatial import ConvexHull
from scipy.spatial import Delaunay
# from matplotlib.patches import Polygon
from scipy.interpolate import griddata
from matplotlib.path import Path

global IPMflag,evsimflag,dpflag,plTnflag,plImflag,inputflag,dataflag,curflag
global ip
ip={}
IPMflag = 0
evsimflag = 0
dpflag = 0
plTnflag = 0
plImflag = 0
inputflag = 0
dataflag = 0
curflag = 1
def resetab():
    global IPMflag,evsimflag,dpflag,plTnflag,plImflag,dataflag,curflag
    evsimflag = 0
    IPMflag = 0
    dpflag = 0
    plTnflag = 0
    plImflag = 0
    dataflag = 0
    # curflag = 1;  #Current tab pointer



light_theme = {
    'colorScheme': 'light'
}
# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
    "assets/gradient.css",
    "assets/custom_table_styles.css"
],assets_folder=os.getcwd()+'/assets/')
#crds
# Constants

DIRECTORIES = {
    "motor": "Simulator Files/Motor/",
    "inverter": "Simulator Files/Inverter/",
    "battery": "Simulator Files/Battery/",
    "gear": "Simulator Files/Gear/",
    "tire": "Simulator Files/Tire/",
    "vehicle": "Simulator Files/Vehicle/"
}

# Helper Functions
def get_files_in_directory(directory):
    try:
        return os.listdir(directory)
    except FileNotFoundError:
        return []

def create_table_rows(files,name):
    return [
        dmc.TableTr(
            [
                dmc.TableTd(
                    dmc.Button(
                        file,
                        id={'type': f'{name}-file-button', 'index': idx},
                        n_clicks=0,
                        variant="subtle",
                        size="xs",
                        fullWidth=True,
                        justify="flex-start"
                    )
                ),
            ]
        )
        for idx, file in enumerate(files)
    ]

# Load initial file data
 

def TorqueVsSpeed(condition_value='None'):
    # print("graph1",Temp['AEditField'])
    if condition_value == '2':
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        tickvals = list(range(0, 401, 50)) 
        fig.update_yaxes(range=[0,400], tickvals=tickvals)
    
        # Plot the data for the left y-axis
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MaTn']), mode='markers', name='G-MTPA', marker_color='green',marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['CTn']), mode='markers', name='G-CPSR', marker_color='red',marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MvTn']), mode='markers', name='G-MTPV', marker_color='blue',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(ct['Teflag'][0:200]), mode='markers', name='Te(Nm) in Constant Torque', marker_color='magenta',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mp['Teflag'][0:200]), mode='markers', name='Te(Nm) in Max Power', marker_color='black',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mv['Teflag'][0:200]), mode='markers', name='Te(Nm) in MTPV', marker_color='cyan',marker=dict(size=6)))

        # Create a second y-axis
        fig.update_layout(yaxis2=dict(title='Power Factor', overlaying='y', side='right', range=[-1.5, 1.5]))

        # Plot the data for the right y-axis
        # fig.add_trace(go.Scatter(x=ipm.rpm, y=ipm.PF, mode='markers', name='Power factor = cos(δ-β)', marker_color='yellow', yaxis='y2',marker=dict(size=6)))

        # Update layout
        fig.update_xaxes(title_text='rpm')
        fig.update_yaxes(title_text='Torque (Nm)')
        fig.update_layout(title_text="Torque vs speed",title_font=dict(color="rgb(28,18,112)"))
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_zeroline=False,
            yaxis2_zeroline=False,
            yaxis2_showline=False,
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),
            # xaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis2_title_font=dict(color="white"),
            yaxis2_tickfont=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
            showlegend=False
        )
        fig.update_yaxes(showgrid=False, secondary_y=True,title_text='Torque (Nm)')
        fig.update_layout(showlegend=True)
    else:
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        tickvals = list(range(0, 401, 50)) 
        fig.update_yaxes(range=[0,400], tickvals=tickvals)
    
        # Plot the data for the left y-axis
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MaTn']), mode='markers', name='G-MTPA', marker_color='green',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['CTn']), mode='markers', name='G-CPSR', marker_color='red',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MvTn']), mode='markers', name='G-MTPV', marker_color='blue',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(ct['Teflag'][0:200]), mode='markers', name='Te(Nm) in Constant Torque', marker_color='magenta',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mp['Teflag'][0:200]), mode='markers', name='Te(Nm) in Max Power', marker_color='black',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mv['Teflag'][0:200]), mode='markers', name='Te(Nm) in MTPV', marker_color='cyan',marker=dict(size=2)))

        # Create a second y-axis
        fig.update_layout(yaxis2=dict(title='Power Factor', overlaying='y', side='right', range=[-1.5, 1.5]))

        # Plot the data for the right y-axis
        # fig.add_trace(go.Scatter(x=ipm.rpm, y=ipm.PF, mode='markers', name='Power factor = cos(δ-β)', marker_color='yellow', yaxis='y2',marker=dict(size=2)))

        # Update layout
        fig.update_xaxes(title_text='rpm')
        fig.update_yaxes(title_text='Torque (Nm)')
        fig.update_layout(title_text="Torque vs speed",title_font=dict(color="rgb(28,18,112)"))
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_zeroline=False,
            yaxis2_zeroline=False,
            yaxis2_showline=False,
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis2_title_font=dict(color="white"),
            yaxis2_tickfont=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
            showlegend=False
        )
        fig.update_yaxes(showgrid=False, secondary_y=True,title_text='Torque (Nm)')
        fig.update_layout(showlegend=False)
    return fig

def TempOnTnGraph(condition_value='None'):
    if condition_value == '2':
        traces = []
        leg = arr[1:14]
        for i in range(13):
            trace = go.Scatter(x=ipm.rpm, y=tmpTn[i], mode='markers',marker=dict(size=5),name=leg[i])
            traces.append(trace)

        # trace_ct = go.Scatter(x=ev.rpm, y=np.real(ct['Teflag']), mode='markers', name='Te(Nm) in Constant Torque', marker=dict(color='magenta', size=5))
        # trace_mp = go.Scatter(x=ev.rpm, y=np.real(mp['Teflag']), mode='markers', name='Te(Nm) in Max Power', marker=dict(color='black', size=5))
        # trace_mv = go.Scatter(x=ev.rpm[:201], y=np.real(mv['Teflag'][:201]), mode='markers', name='Te(Nm) in MTPV', marker=dict(color='cyan', size=5))

        # Create layout
        layout = go.Layout(
            title='Temperature Map on TN graph',
            xaxis=dict(title='rpm', color='rgb(11, 7, 44)', range=[0, 20000]),
            yaxis=dict(title='Nm', color='rgb(11, 7, 44)',),
            plot_bgcolor='rgba(255, 255, 255, 0.7)',
            showlegend=True,
            legend=dict(x=0.8, y=0.9)
        )

        # Create figure
        fig = go.Figure(data=traces ,layout=layout)
        # fig = go.Figure(data=traces + [trace_ct, trace_mp, trace_mv], layout=layout)
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showline=False, showgrid=False,zeroline=False),
            yaxis=dict(showline=False, showgrid=False, zeroline=False,range=[0, 400], tick0=0, dtick=50),
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            showlegend=True,
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        )
        # fig.update_layout(showlegend=True)
    else:
        traces = []
        for i in range(13):
            trace = go.Scatter(x=ipm.rpm, y=tmpTn[i], mode='markers',marker=dict(size=3))
            traces.append(trace)

        # trace_ct = go.Scatter(x=ev.rpm, y=np.real(ct['Teflag']), mode='markers', name='Te(Nm) in Constant Torque', marker=dict(color='magenta', size=3))
        # trace_mp = go.Scatter(x=ev.rpm, y=np.real(mp['Teflag']), mode='markers', name='Te(Nm) in Max Power', marker=dict(color='black', size=3))
        # trace_mv = go.Scatter(x=ev.rpm[:201], y=np.real(mv['Teflag'][:201]), mode='markers', name='Te(Nm) in MTPV', marker=dict(color='cyan', size=3))

        # Create layout
        layout = go.Layout(
            title='Temperature Map on TN graph',
            xaxis=dict(title='rpm', color='rgb(11, 7, 44)', range=[0, 20000]),
            yaxis=dict(title='Nm', color='rgb(11, 7, 44)',),
            plot_bgcolor='rgba(255, 255, 255, 0.7)',
            showlegend=True,
            legend=dict(x=0.8, y=0.9)
        )

        # Create figure
        fig = go.Figure(data=traces ,layout=layout)
        # fig = go.Figure(data=traces + [trace_ct, trace_mp, trace_mv], layout=layout)
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showline=False, showgrid=False,zeroline=False),
            yaxis=dict(showline=False, showgrid=False, zeroline=False,range=[0, 400], tick0=0, dtick=50),
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            showlegend=False
            #legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        )
        fig.update_layout(showlegend=False)
    # Show the plot
    return fig    
def PLoss(condition_value='None'):

    if condition_value == '2':
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pcu), mode='markers', marker=dict(color="grey", size=6), name='Pcu'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pfe), mode='markers', marker=dict(color="red", size=6), name='Pfe'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pstr), mode='markers', marker=dict(color="#538aa3", size=6), name='Pstr'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pinv), mode='markers', marker=dict(color="green", size=6), name='Pinv'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pwind), mode='markers', marker=dict(color="cyan", size=6), name='Pwind'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pfric), mode='markers', marker=dict(color="yellow", size=6), name='Pfric'))


        fig.update_xaxes(range=[0, 19700])
        fig.update_xaxes(title='rpm', title_font=dict(color='#001c49'))
        fig.update_yaxes(title='kW', title_font=dict(color='#001c49'))
        fig.update_layout(title='Ploss', legend=dict(title='Categories',title_font=dict(color='white'),font=dict(color='white'),), showlegend=True)
        fig.update_layout(
            title_font={'size': 12, 'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis_showline=False,  # Make y-axis line invisible
            yaxis_zeroline=False,  # Make y-axis zero line invisible
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            showlegend=False

        )
        fig.update_layout(showlegend=True)
    else:
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pcu), mode='markers', marker=dict(color="grey", size=2), name='Pcu'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pfe), mode='markers', marker=dict(color="red", size=2), name='Pfe'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pstr), mode='markers', marker=dict(color="#538aa3", size=2), name='Pstr'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pinv), mode='markers', marker=dict(color="green", size=2), name='Pinv'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pwind), mode='markers', marker=dict(color="cyan", size=2), name='Pwind'))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(ipm.Pfric), mode='markers', marker=dict(color="yellow", size=2), name='Pfric'))


        fig.update_xaxes(range=[0, 19700])
        fig.update_xaxes(title='rpm', title_font=dict(color='#001c49'))
        fig.update_yaxes(title='kW', title_font=dict(color='#001c49'))
        fig.update_layout(title='Ploss', legend=dict(title='Categories',title_font=dict(color='white'),font=dict(color='white'),), showlegend=True)
        fig.update_layout(
            title_font={'size': 12, 'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis_showline=False,  # Make y-axis line invisible
            yaxis_zeroline=False,  # Make y-axis zero line invisible
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            showlegend=False

        )
        fig.update_layout(showlegend=False)

    return fig

def PowerVsSpeed(condition_value='None'):
    if condition_value == '2':
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Plot the data for the left y-axis
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MaPe']), mode='markers', name='G-MTPA', marker_color='red',marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['CPe']), mode='markers', name='G-CPSR', marker_color='green',marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MvPe']), mode='markers', name='G-MTPV', marker_color='blue',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(ct['Peflag'][0:200]), mode='markers', name='Pe(kW) in Constant Torque', marker_color='magenta',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mp['Peflag'][0:200]), mode='markers', name='Pe(kW) in Max Power', marker_color='cyan',marker=dict(size=6)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mv['Peflag'][0:200]), mode='markers', name='Pe(kW) in MTPV', marker_color='black',marker=dict(size=6)))

        # Create a second y-axis
        fig.update_layout(yaxis2=dict(title='Power Factor', overlaying='y', side='right', range=[-1.5, 1.5]))

        # Plot the data for the right y-axis
        # fig.add_trace(go.Scatter(x=ipm.rpm, y=ipm.PF , mode='markers', name='Power factor = cos(δ-β)', marker_color='yellow', yaxis='y2',marker=dict(size=6)))

        # Update layout
        fig.update_layout(
            title="Power v/s Speed",
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="rpm",
            yaxis_title="kW",
            xaxis=dict(range=[0, 20000]),
            yaxis=dict(range=[0, 160], tick0=0, dtick=20),
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_zeroline=False,
            yaxis2_zeroline=False,
            yaxis2_showline=False,
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis2_title_font=dict(color="white"),
            yaxis2_tickfont=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
            showlegend=False
        )
        fig.update_yaxes(
            title_text='kW',
            showgrid=False,  # Set showgrid to False to hide gridlines
            secondary_y=True  # Target the secondary y-axis
        )
        fig.update_layout(showlegend=True)
    else:
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Plot the data for the left y-axis
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MaPe']), mode='markers', name='G-MTPA', marker_color='red',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['CPe']), mode='markers', name='G-CPSR', marker_color='green',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=ipm.rpm, y=np.real(gt['MvPe']), mode='markers', name='G-MTPV', marker_color='blue',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(ct['Peflag'][0:200]), mode='markers', name='Pe(kW) in Constant Torque', marker_color='magenta',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mp['Peflag'][0:200]), mode='markers', name='Pe(kW) in Max Power', marker_color='cyan',marker=dict(size=2)))
        # fig.add_trace(go.Scatter(x=ev.rpm[0:200], y=np.real(mv['Peflag'][0:200]), mode='markers', name='Pe(kW) in MTPV', marker_color='black',marker=dict(size=2)))

        # Create a second y-axis
        fig.update_layout(yaxis2=dict(title='Power Factor', overlaying='y', side='right', range=[-1.5, 1.5]))

        # Plot the data for the right y-axis
        # fig.add_trace(go.Scatter(x=ipm.rpm, y=ipm.PF , mode='markers', name='Power factor = cos(δ-β)', marker_color='yellow', yaxis='y2',marker=dict(size=2)))

        # Update layout
        fig.update_layout(
            title="Power v/s Speed",
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="rpm",
            yaxis_title="kW",
            xaxis=dict(range=[0, 20000]),
            yaxis=dict(range=[0, 160], tick0=0, dtick=20),
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            yaxis_showline=False,
            yaxis_zeroline=False,
            yaxis2_zeroline=False,
            yaxis2_showline=False,
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis2_title_font=dict(color="white"),
            yaxis2_tickfont=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
            showlegend=False
        )
        fig.update_yaxes(
            title_text='kW',
            showgrid=False,  # Set showgrid to False to hide gridlines
            secondary_y=True  # Target the secondary y-axis
        )
        fig.update_layout(showlegend=False)

    return fig
#motor
  

def TempOnPower(condition_value='None'):


    if condition_value == '2':
        leg = arr[1:14]
        traces = []
        for i in range(13):
            trace = go.Scatter(x=ipm.rpm, y=tmpPwr[i], mode='markers', marker=dict(size=6),name=leg[i])
            traces.append(trace)

        # trace_ct = go.Scatter(x=ev.rpm, y=np.real(ct['Peflag']), mode='markers', name='Pe(kW) in Constant Torque', marker=dict(color='magenta', size=6))
        # trace_mp = go.Scatter(x=ev.rpm, y=np.real(mp['Peflag']), mode='markers', name='Pe(kW) in Max Power', marker=dict(color='black', size=5))
        # trace_mv = go.Scatter(x=ev.rpm, y=np.real(mv['Peflag']), mode='markers', name='Pe(kW) in MTPV', marker=dict(color='cyan', size=5))

        # Create layout
        layout = go.Layout(
            title='Temperature Map on Power graph',
            xaxis=dict(title='rpm', color='rgb(11, 7, 44)', range=[-1000, 20000]),
            yaxis=dict(title='Power (kWH)', color='rgb(11, 7, 44)'),
            plot_bgcolor='rgba(255, 255, 255, 0.7)',
            showlegend=True,
            legend=dict(x=0.8, y=0.9)
        )

        # Create figure
        fig=go.Figure(data=traces ,layout=layout)
        # fig = go.Figure(data=traces + [trace_ct, trace_mp, trace_mv], layout=layout)
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showline=False, showgrid=False,zeroline=False ),
            yaxis=dict(showline=False, showgrid=False, zeroline=False,range=[0, 160], tick0=0, dtick=20),
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        )
        fig.update_layout(showlegend=True)
    else:
        traces = []
        for i in range(13):
            trace = go.Scatter(x=ipm.rpm, y=tmpPwr[i], mode='markers', marker=dict(size=3))
            traces.append(trace)

        # trace_ct = go.Scatter(x=ev.rpm, y=np.real(ct['Peflag']), mode='markers', name='Pe(kW) in Constant Torque', marker=dict(color='magenta', size=5))
        # trace_mp = go.Scatter(x=ev.rpm, y=np.real(mp['Peflag']), mode='markers', name='Pe(kW) in Max Power', marker=dict(color='black', size=5))
        # trace_mv = go.Scatter(x=ev.rpm, y=np.real(mv['Peflag']), mode='markers', name='Pe(kW) in MTPV', marker=dict(color='cyan', size=5))

        # Create layout
        layout = go.Layout(
            title='Temperature Map on Power graph',
            xaxis=dict(title='rpm', color='rgb(11, 7, 44)', range=[-1000, 20000]),
            yaxis=dict(title='Power (kWH)', color='rgb(11, 7, 44)'),
            plot_bgcolor='rgba(255, 255, 255, 0.7)',
            showlegend=True,
            legend=dict(x=0.8, y=0.9)
        )

        # Create figure
        fig=go.Figure(data=traces ,layout=layout)
        # fig = go.Figure(data=traces + [trace_ct, trace_mp, trace_mv], layout=layout)
        fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showline=False, showgrid=False,zeroline=False ),
            yaxis=dict(showline=False, showgrid=False, zeroline=False,range=[0, 160], tick0=0, dtick=20),
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        )
        fig.update_layout(showlegend=False)
    # Show the plot
    return fig

def IdIqControl(condition_value='None'):
    trace1 = go.Scatter(x=gt['MaId'], y=gt['MaIq'], mode='markers', marker=dict(color='red', size=6), name='G-MTPA')
    trace2 = go.Scatter(x=gt['CId'], y=gt['CIq'], mode='markers', marker=dict(color='rgb(0.8500, 0.3250, 0.0980)', size=4), name='G-CPSR')
    trace3 = go.Scatter(x=gt['MvId'], y=gt['MvIq'], mode='markers', marker=dict(color='blue', size=4), name='G-MTPV')
    trace4 = go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', marker=dict(color='rgb(0.3010, 0.7450, 0.9330)', symbol='triangle-up', size=4), name='A12-Posi')
    trace5 = go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', marker=dict(color='red', symbol='triangle-up', size=4), name='A12-Nega')

    # Create layout
    layout = go.Layout(
        title='Id Iq Control Map',
        xaxis=dict(title='Id(A)', color='rgb(11, 7, 44)',  range=[-800, 0]),
        yaxis=dict(title='Iq(A)', color='rgb(11, 7, 44)',  range=[0, 700]),
        plot_bgcolor='rgba(255, 255, 255, 0.7)',
        showlegend=True,
        legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
    )

    # Create figure
    fig = go.Figure(data=[trace1, trace2, trace3, trace4, trace5], layout=layout)


    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Id(A)', showline=False, showgrid=False,zeroline=False,range=[-800, 0], tick0=0, dtick=200 ),
        yaxis=dict(title='Iq(A)', showline=False, showgrid=False, zeroline=False,range=[0, 600], tick0=0, dtick=100),
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        showlegend=False
    )

    if condition_value == '2':
        fig.update_layout(showlegend=True)
    else:
        fig.update_layout(showlegend=False)
    return fig

def lutpointsgraph(condition_value='None'):
    tcId = np.arange(10, 671, 10) * -1
    tcId_2d = np.array([tcId])
    # Create the 2D plot using Plotly
    fig = go.Figure()
    # fig.update_layout(height=500,width=650)
    # print(tcId)
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.vLim_iq[0]).reshape(67,), mode='lines+markers',  line=dict(color='purple'), name=np.real(ev.trqTem[0]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.vLim_iq[1]).reshape(67,), mode='lines+markers', line=dict(color='orange'), name=np.real(ev.trqTem[1]), marker=dict(symbol='circle', color='blue', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.vLim_iq[2]).reshape(67,), mode='lines+markers', line=dict(color='pink'), name=str(ev.trqTem[2]), marker=dict(symbol='circle', color='yellow', size=2)))
 
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.Maxpwr_iq[0]).reshape(67,), mode='lines+markers', line=dict(color='lime'), name=np.real(ev.trqTem[13]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.Maxpwr_iq[1]).reshape(67,), mode='lines+markers', line=dict(color='blue'), name=np.real(ev.trqTem[14]), marker=dict(symbol='circle', color='blue', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.Maxpwr_iq[2]).reshape(67,), mode='lines+markers', line=dict(color='red'), name=np.real(ev.trqTem[12]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.Maxpwr_iq[3]).reshape(67,), mode='lines+markers', line=dict(color='green'), name=np.real(ev.trqTem[16]), marker=dict(symbol='circle', color='yellow', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.Maxpwr_iq[4]).reshape(67,), mode='lines+markers', line=dict(color='yellow'), name=np.real(ev.trqTem[17]), marker=dict(symbol='circle', color='blue', size=2)))
 
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.MTPV_iq[0]).reshape(67,), mode='lines+markers', line=dict(color='cyan'), name=np.real(ev.trqTem[18]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.MTPV_iq[1]).reshape(67,), mode='lines+markers', line=dict(color='magenta'), name=np.real(ev.trqTem[19]), marker=dict(symbol='circle', color='blue', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.MTPV_iq[2]).reshape(67,), mode='lines+markers', line=dict(color='lightblue'), name=np.real(ev.trqTem[20]), marker=dict(symbol='circle', color='yellow', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.MTPV_iq[3]).reshape(67,), mode='lines+markers', line=dict(color='darkblue'), name=np.real(ev.trqTem[21]), marker=dict(symbol='circle', color='blue', size=2)))
    fig.add_trace(go.Scatter(x=tcId_2d.reshape(67,), y=np.array(ev.MTPV_iq[4]).reshape(67,), mode='lines+markers', line=dict(color='gray'), name=np.real(ev.trqTem[22]), marker=dict(symbol='circle', color='red', size=2)))
 
    # Adding data points in 2D space
    fig.add_trace(go.Scatter(x=np.real(ev.PfId), y=np.real(ev.PfIq), mode='lines', line=dict(width=3), name='Unity Power Factor (PF)'))
    fig.add_trace(go.Scatter(x=np.real(ct['Aid']), y=np.real(ct['Aiq']), mode='markers', marker=dict(color='red', size=4), name='MTPA (ωea)'))
    fig.add_trace(go.Scatter(x=np.real(mp['id']), y=np.real(mp['iq']), mode='markers',name="Max Power Control (ωea➡ωeb)", marker=dict(color='yellow', size=4, symbol='circle', line=dict(color='black', width=1))))
    fig.add_trace(go.Scatter(x=mv['id'], y=mv['iq'], mode='markers', marker=dict(color='rgb(1.00, 0.62, 0.46)', size=4), name='"MTPV (ωeb➡Max Speed)'))
 
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[0]).reshape(61,), y=np.array(ev.vLimIq[0]).reshape(61,), mode='lines', line=dict(color='lightblue', width=4), name='V Limit at ωea', marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[1]).reshape(61,), y=np.array(ev.vLimIq[1]).reshape(61,), mode='lines', line=dict(color='yellow', width=4), name='V Limit at ωeb', marker=dict(symbol='circle', color='blue', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[2]).reshape(61,), y=np.array(ev.vLimIq[2]).reshape(61,), mode='lines', line=dict(color='cyan', width=4), name='V Limit at Max Speed', marker=dict(symbol='circle', color='red', size=2)))
 
    # Plotting the voltage limit curves using scatter plot
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[0]).reshape(61,), y=np.array(ev.vLimIq[0]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[0])))
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[1]).reshape(61,), y=np.array(ev.vLimIq[1]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[1])))
    fig.add_trace(go.Scatter(x=np.array(ev.vLimId[2]).reshape(61,), y=np.array(ev.vLimIq[2]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[2])))
 
    # Plotting the max power curves using scatter plot
    fig.add_trace(go.Scatter(x=np.array(ev.MaxPwrId[0]).reshape(61,), y=np.array(ev.MaxPwrIq[0]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[3])))
    fig.add_trace(go.Scatter(x=np.array(ev.MaxPwrId[1]).reshape(61,), y=np.array(ev.MaxPwrIq[1]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[4])))
    fig.add_trace(go.Scatter(x=np.array(ev.MaxPwrId[2]).reshape(61,), y=np.array(ev.MaxPwrIq[2]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[5])))
    fig.add_trace(go.Scatter(x=np.array(ev.MaxPwrId[3]).reshape(61,), y=np.array(ev.MaxPwrIq[3]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[6])))
    fig.add_trace(go.Scatter(x=np.array(ev.MaxPwrId[4]).reshape(61,), y=np.array(ev.MaxPwrIq[4]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[7])))
    # Plotting the MTPV curves using scatter plot
    fig.add_trace(go.Scatter(x=np.array(ev.MTPVId[0]).reshape(61,), y=np.array(ev.MTPVIq[0]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[8]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.MTPVId[1]).reshape(61,), y=np.array(ev.MTPVIq[1]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[9]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.MTPVId[2]).reshape(61,), y=np.array(ev.MTPVIq[2]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[10]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.MTPVId[3]).reshape(61,), y=np.array(ev.MTPVIq[3]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[11]), marker=dict(symbol='circle', color='red', size=2)))
    fig.add_trace(go.Scatter(x=np.array(ev.MTPVId[4]).reshape(61,), y=np.array(ev.MTPVIq[4]).reshape(61,), mode='lines+markers', name=np.real(ev.mrpm[12]), marker=dict(symbol='circle', color='red', size=2)))
   
    #fig.add_trace(go.Scatter(x=ev['MTPVId'][649:654], y=ev['MTPVIq'][649:654], mode='lines', line=dict(color='blue'),showlegend=False , name='MTPV_curves'))
    fig.add_trace(go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', marker=dict(symbol='triangle-up', color='green', size=5,line=dict(color='black',width=0.5)),name='Positive LUT points'))
    fig.add_trace(go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', marker=dict(symbol='triangle-up', color='#c31013', size=5,line=dict(color='black',width=0.5)),name='Negative LUT points'))
 
    # Set the layout of the 2D plot
    fig.update_layout(
        xaxis_title='Id(A)',
        yaxis_title='Iq(A)',
        xaxis=dict(range=[-700, 100]),
        yaxis=dict(range=[-100, 700]),
        title='LUT points and Torque and Speed curve, PF',
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_zeroline=False,
        autosize=True,
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        legend=dict(x=1.06, y=0.1, orientation='v' , font=dict(color='white')),
        showlegend=True
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False)
    # Show the 2D plot
    return fig
def TnCurveButtonPushed( ):
 
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # print("ev.rpmgraph",ev.rpm)
    fig.add_trace(go.Scatter(x=ev.rpm[:107], y=np.real(ct['Teflag'][:107]), mode='markers', name='Te(Nm) in Constant torque', marker=dict(color='red', size=5)), secondary_y=False)
    fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(mp['Teflag']), mode='markers', name='Te(Nm) in Max PW', marker=dict(color='green', size=5)), secondary_y=False)
    fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(mv['Teflag']), mode='markers', name='Te(Nm) in MTPV', marker=dict(color='yellow', size=5)), secondary_y=False)
 
    fig.add_trace(go.Scatter(x=ev.rpm[:252], y=np.real(mp['Peflag'][:252]), mode='markers', name='Pe(kW) in Max PW', marker=dict(color='black', size=5)), secondary_y=False)
    fig.add_trace(go.Scatter(x=ev.rpm[:74], y=np.real(ct['Peflag'][:74]), mode='markers', name='Pe(kW) in Constant torque', marker=dict(color='yellow', size=5)), secondary_y=False)
    fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(mv['Peflag']), mode='markers', name='Pe(kW) in MTPV', marker=dict(color='#e14eca', size=5)), secondary_y=False)
 
    fig.update_yaxes(range=[0, 450], title_text='[Nm],[kW]', title_font=dict(color='rgb(28,18,112)', size=12), secondary_y=False)
 
    fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(ct['Vmflag']), mode='markers', name='Vm in Constant torque', marker=dict(color='#e14eca', size=5)), secondary_y=True)
    fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(mp['Vmflag'][:200]), mode='markers', name='Vm in Max PW', marker=dict(color='#1d8cf8', size=5)), secondary_y=True)
    fig.add_trace(go.Scatter(x=ev.rpm[:200], y=np.real(mv['Vmflag'][:200]), mode='markers', name='Vm in MTPV', marker=dict(color='#2bffc6', size=5)), secondary_y=True)
    # fig.add_trace(go.Scatter(x=ev.rpm, y=np.real(mv['Peflag']), mode='markers', name='Pe(kW) in MTPV', marker=dict(color='#e14eca',size=3)), secondary_y=True)
    fig.add_trace(go.Scatter(x=ev.rpm[:106], y=np.real(ct['Imflag'][:106]), mode='markers', name='Im in Constant torque', marker=dict(color='#1d8cf8', size=5)), secondary_y=True)
    fig.add_trace(go.Scatter(x=ev.rpm[35:200], y=np.real(mp['Imflag'][35:200]), mode='markers', name='Im in Max PW', marker=dict(color='#e14eca', size=5)), secondary_y=True)
    fig.add_trace(go.Scatter(x=ev.rpm[:200], y=np.real(mv['Imflag'][:200]), mode='markers', name='Im in Max PW', marker=dict(color='#2bffc6', size=5)), secondary_y=True)
 
    fig.update_yaxes(range=[0, 800], title_text="[kW], [V], [A]", title_font=dict(color="white", size=12), secondary_y=True, tickfont=dict(color="white"))
 
    fig.update_xaxes(range=[0, 20000], title_text="rpm", title_font=dict(color="rgb(28,18,112)", size=12))
 
    fig.update_layout(title_text="Tn Curve",title_font=dict(color="rgb(28,18,112)"))
    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_zeroline=False,
        yaxis2_zeroline=False,
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        legend=dict(x=1.06, y=0.3, orientation='v' , font=dict(color='white')),
        showlegend=True
    )
    fig.update_yaxes(
        showgrid=False,  # Set showgrid to False to hide gridlines
        secondary_y=True  # Target the secondary y-axis
    )
 
    #fig.show()
    return fig
 
def TotalTorqueButtonPushed(condition_value='None'):
 
    degree = np.arange(-180, 181, 10)
    num = len(degree)
    simCur = mot['cur']/np.sqrt(2)
    magTrq = 3/4 * mot['pole'] * mot['flux'] * simCur * np.cos(np.deg2rad(degree[:num]))
    relTrq = 3/4 * mot['pole'] * mot['d'] * simCur**2 * np.sin(np.deg2rad(2*degree[:num]))/2
    Torque = magTrq + relTrq
 
    fig = go.Figure()
 
    # Add traces for Magnet torque, Reluctance torque, and Total torque
    fig.add_trace(go.Scatter(x=degree, y=magTrq, mode='lines', name='M=3P/4(ψm*I*cosβ)',  line=dict(color='#e14eca', width=4), fill='tozeroy', fillcolor='rgba(225, 78, 202, 0.2)'))
    fig.add_trace(go.Scatter(x=degree, y=relTrq, mode='lines', name='R=3P/4((Ld-Lq)*I*I*sin(2*β)/2)', line=dict(color='#2bffc6', width=4), fill='tozeroy', fillcolor='rgba(43, 255, 198, 0.2)'))
    fig.add_trace(go.Scatter(x=degree, y=Torque, mode='lines', name='Te = M * R',  line=dict(color='#1d8cf8', width=4), fill='tozeroy', fillcolor='rgba(29, 140, 248, 0.2)'))
   
    # Update the layout
    fig.update_layout(
        xaxis_title='angle(degree)',
        yaxis_title='Torque (Nm)',
        xaxis=dict(range=[min(degree), max(degree)]),
        title='Total torque = Magnet torque + Reluctance torque',
        title_font={'size': 12,'color': 'white'},
        legend=dict(x=1.03, y=0.5, orientation='v' , font=dict(color='white')),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        xaxis_title_font=dict(color="white"),  # Set x-axis title color to white
        yaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_zeroline=False,
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        autosize=True,
        showlegend=True,
        #margin=dict(r=12)
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
 
    return fig
def MaxtorqueperCurrentButtonPushed(condition_value='None'):
    x_data = list(range(91))
    fig = go.Figure()
    ev.T=ev.T.T
    ind=np.round(ev.maxT)
 
    for i in range(len(ev.T)):
        fig.add_trace(go.Scatter(x=x_data, y=ev.T[i], mode='lines', name=np.real(ind[i])))# name=f'Torque {i+1}'
 
    fig.add_trace(go.Scatter(x=ev.b, y=ev.maxT, mode='markers+text', text=[str(round(txt)) for txt in ev.maxT],
                            textposition='bottom right', marker=dict(size=10,color='#1d8cf8'),textfont=dict(color='#e9ecef')))
    ev.T=ev.T.T
    # Customize the layout
    fig.update_yaxes(range=[0, 400],tickvals=list(range(0, 401, 50)))
    fig.update_xaxes(range=[0, 100],tickvals=list(range(0, 101, 20)))
    fig.update_layout(
        xaxis=dict(title='angle (degree)', title_font=dict(size=12)),
        yaxis=dict(title='Torque (Nm)', title_font=dict(size=12)),
        title_text='MTPA (Max Troque at Irms)',
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_zeroline=False,
        autosize=True,
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        legend=dict(x=1.02, y=0.5, orientation='v' , font=dict(color='white')),
        showlegend=True,
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    # Show the Plotly figure
    #fig.show()
   
    return fig
 
def IsVsPfButtonPushed(condition_value='None'):
 
    fig = make_subplots(specs=[[{"secondary_y": True}]])
 
    # Initialize empty lists to store x and y values for the scatter plots
    x_values = []
    y_values = []
    colors = []
    symbols = []
 
    # Process the data to add scatter plots with non-zero values
    for i in range(len(ev.rpm)):
        if ct['betaflag'][i] != 0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(ct['betaflag'][i]))
            colors.append('#2bffc6')
            symbols.append('x')
 
        # Repeat similar blocks for other traces (mp, mv, delflag, Pfflag)
 
    # Plot the real part of the data on the left y-axis
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='β in constant torque',  marker=dict(color=colors, symbol=symbols, size=6)))
 
    for i in range(len(ev.rpm)):
        if mp['betaflag'][i] != 0:
                x_values.append(ev.rpm[i])
                y_values.append(np.real(mp['betaflag'][i]))
                colors.append('#e14eca')
                symbols.append('x')
 
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='β in Max power', marker=dict(color=colors, symbol=symbols, size=6)))
 
    for i in range(len(ev.rpm)):
        if mv['betaflag'][i] != 0:
                x_values.append(ev.rpm[i])
                y_values.append(np.real(mv['betaflag'][i]))
                colors.append('#fcd44c')
                symbols.append('x')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='β in MTPV',  marker=dict(color=colors, symbol=symbols, size= 6)))
 
    for i in range(len(ev.rpm)):
        if ct['delflag'][i] != 0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(ct['delflag'][i]))
            colors.append('#2bffc6')
            symbols.append('triangle-up')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='δ in constant torque',  marker=dict(color=colors, symbol=symbols, size=6)))
 
    for i in range(len(ev.rpm)):
        if mp['delflag'][i] != 0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(mp['delflag'][i]))
            colors.append('#e14eca')
            symbols.append('triangle-up')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='δ in Max power', marker=dict(color=colors, symbol=symbols, size=4)))
 
    for i in range(len(ev.rpm)):
        if mv['delflag'][i] != 0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(mv['delflag'][i]))
            colors.append('#fcd44c')
            symbols.append('triangle-up')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='δ in MTPV',  marker=dict(color=colors, symbol=symbols, size=6)))
    # Continue to add other traces in the same way
 
    for i in range(len(ev.rpm)):
        if ct['Pfflag'][i]!=0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(ct['Pfflag'][i]))
            colors.append('#2bffc6')
            symbols.append('circle')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='PF = cos(δ-β) in constant torque', marker=dict(color=colors, symbol=symbols, size=6)),secondary_y=True)
 
    for i in range(len(ev.rpm)):
        if mp['Pfflag'][i]!=0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(mp['Pfflag'][i]))
            colors.append('#e14eca')
            symbols.append('circle')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='PF = cos(δ-β) in Max power',  marker=dict(color=colors, symbol=symbols, size=6)),secondary_y=True)
 
    for i in range(len(ev.rpm)):
        if mv['Pfflag'][i] != 0:
            x_values.append(ev.rpm[i])
            y_values.append(np.real(mv['Pfflag'][i]))
            colors.append('#fcd44c')
            symbols.append('circle')
    fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='markers', name='PF = cos(δ-β) in MTPV',  marker=dict(color=colors, symbol=symbols, size=6)),secondary_y=True)
 
    # Set the x-axis and y-axis labels
    fig.update_xaxes(title_text='rpm')
    fig.update_yaxes(title_text='angle(degree)', color='blue', title_font=dict(size=12), secondary_y=False)
    fig.update_yaxes(title_text='PF', color='blue', title_font=dict(color="white", size=12), secondary_y=True, tickfont=dict(color="white"))
 
    # Set the axis limits
    fig.update_xaxes(range=[0, 15000])
    fig.update_yaxes(range=[-100, 100], secondary_y=False)
    fig.update_yaxes(range=[-1.5, 1], secondary_y=True)
 
    # Set the title
    fig.update_layout(
        title='Is, Vs, PF',
        title_font={'size': 12, 'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        yaxis_showline=False,
        yaxis_zeroline=False,
        yaxis2_showline=False,
        yaxis2_zeroline=False,
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),  # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),  # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        legend=dict(x=1.06, y=0.3, orientation='v' , font=dict(color='white')),
        showlegend=True
    )
 
    fig.update_yaxes(
        showgrid=False,
        secondary_y=True,  # Target the secondary y-axis
        showline=False,  # Set showline to False for the secondary y-axis
        # tickfont=dict(color="rgba(0, 0, 0, 0)"),  
        # title_font=dict(color="rgba(0, 0, 0, 0)"),
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
  # Set the linecolor to transparent
 
    # Display the legend
    # fig.update_layout(legend=dict(x=0.5, y=-0.3, xanchor='center', yanchor='top', orientation='h'))
 
    # Show the plot
    return fig
 
def efficiency_map(condition_value='None'):
    global a12
 
    p4000 = np.where(np.array(a12['prpm']) == 4000)[0]
    n4000 = np.where(np.array(a12['nrpm']) == 4000)[0]
    p5000 = np.where(np.array(a12['prpm']) == 5000)[0]
    n5000 = np.where(np.array(a12['nrpm']) == 5000)[0]
    p6000 = np.where(np.array(a12['prpm']) == 6000)[0]
    n6000 = np.where(np.array(a12['nrpm']) == 6000)[0]
    p8000 = np.where(np.array(a12['prpm']) == 8000)[0]
    n8000 = np.where(np.array(a12['nrpm']) == 8000)[0]
    p10000 = np.where(np.array(a12['prpm']) == 10000)[0]
    n10000 = np.where(np.array(a12['nrpm']) == 10000)[0]
 
    fig = go.Figure()
 
    # Plot the data points with different markers and colors
    fig.add_trace(go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', marker=dict(size=3, color='blue', symbol='triangle-up', line=dict(width=3,color='red'))))
    fig.add_trace(go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', marker=dict(size=3, color='gold', symbol='circle', line=dict(width=3,color='red'))))
 
    fig.add_trace(go.Scatter(x=a12['negId'][n4000], y=a12['negIq'][n4000], mode='lines+markers', marker=dict(size=3, color='green', symbol='circle', line=dict(width=3, color='red'))))
    fig.add_trace(go.Scatter(x=a12['posId'][p4000], y=a12['posIq'][p4000], mode='lines+markers', marker=dict(size=3, color='black', symbol='circle', line=dict(width=3, color='green'))))
    fig.add_trace(go.Scatter(x=a12['negId'][n5000], y=a12['negIq'][n5000], mode='lines+markers', marker=dict(size=3, color='yellow', symbol='circle', line=dict(width=3,color='red'))))
    fig.add_trace(go.Scatter(x=a12['posId'][p5000], y=a12['posIq'][p5000], mode='lines+markers', marker=dict(size=3, color='lightblue', symbol='circle', line=dict(width=3,color='green'))))
    fig.add_trace(go.Scatter(x=a12['negId'][n6000], y=a12['negIq'][n6000], mode='lines+markers', marker=dict(size=3, color='purple', symbol='circle', line=dict(width=3,color='red'))))
    fig.add_trace(go.Scatter(x=a12['posId'][p6000], y=a12['posIq'][p6000], mode='lines+markers', marker=dict(size=3, color='magenta', symbol='circle', line=dict(width=3,color='green'))))
    fig.add_trace(go.Scatter(x=a12['negId'][n8000], y=a12['negIq'][n8000], mode='lines+markers', marker=dict(size=3, color='lime', symbol='circle', line=dict(width=3,color='red'))))
    fig.add_trace(go.Scatter(x=a12['posId'][p8000], y=a12['posIq'][p8000], mode='lines+markers', marker=dict(size=3, color='orange', symbol='circle', line=dict(width=3,color='green'))))
    fig.add_trace(go.Scatter(x=a12['negId'][n10000], y=a12['negIq'][n10000], mode='lines+markers', marker=dict(size=3, color='royalblue', symbol='circle', line=dict(width=3,color='red'))))
    fig.add_trace(go.Scatter(x=a12['posId'][p10000], y=a12['posIq'][p10000], mode='lines+markers', marker=dict(size=3, color='brown', symbol='circle', line=dict(width=3,color='green'))))
 
    # Customize the layout
    #  fig.update_layout(showlegend=False)
    fig.update_layout(
        xaxis_title='Id',
        yaxis_title='Iq',
        title='Efficiency MAP on Power graph',
        title_font={'size': 12,'color': 'white'},
        xaxis=dict( showline=False, showgrid=False,zeroline=False),
        yaxis=dict(showline=False, showgrid=False,zeroline=False,),
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=True
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800, legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    return fig
 
def IdIqControlMapByTemp(condition_value='None'):

    maxt = np.real(np.max(ipm.Temp))
    mint = np.real(np.min(ipm.Temp))
    tmptg = np.arange(1, 14) / 14
    arr = np.zeros(14)
    arr[0] = mint
    arr[13] = maxt
    arr[1:13] = (maxt - mint) * tmptg[1:13] + mint

    tmpId =  ipm.tmpId;
    tmpIq =  ipm.tmpIq;

    a12efftab = pd.read_excel("InputTableFile.xlsx", sheet_name="A12 Efficiency", skiprows=2)
    # Convert DataFrame to NumPy array
    a12efftab = a12efftab.to_numpy()
    # Find indices where the first column equals 5000 and 10000
    p5000 = np.where(a12['prpm'] == 5000)
    n5000 = np.where(a12['nrpm'] == 5000) 
    p10000 = np.where(a12['prpm'] == 10000) 
    n10000 = np.where(a12['nrpm'] == 10000) 
    print("n5000",n5000)
    print("n10000",n10000)
    print("n5000",a12['negId'][n5000])

    ipm.plaId = np.array( ipm.plaId)
    ipm.plaIq = np.array( ipm.plaIq)
    # Create traces
    traces = []
   
    # Plotting temperature data
    for ind in range(13):
        traces.append(go.Scatter(x=tmpId[ind, :],y=tmpIq[ind, :],mode='markers',marker=dict(size=6)))
    # Plotting other data
    traces.append(go.Scatter(x= ipm.plaId[0, :],y=ipm.plaIq[0, :],mode='lines+markers',name='S-1k',marker=dict(size=7),line=dict(dash='solid')))
    traces.append(go.Scatter(x= ipm.plaId[1, :],y=ipm.plaIq[1, :],mode='lines+markers',name='S-2k',marker=dict(size=7),line=dict(dash='solid')))
    traces.append(go.Scatter(x= ipm.plaId[2, :],y=ipm.plaIq[2, :],mode='lines+markers',name='S-3k',marker=dict(size=7),line=dict(dash='solid')))
    traces.append(go.Scatter(x= ipm.plaId[3, :],y=ipm.plaIq[3, :],mode='lines+markers',name='S-4k',marker=dict(size=7),line=dict(dash='solid')))
 
    # Plotting additional lines
 
    traces.append(go.Scatter(x=a12['negId'][n5000],y=a12['negIq'][n5000],mode='lines',name='N-5000rpm',line=dict(width=4,color='red')))
    traces.append(go.Scatter(x=a12['posId'][p5000],y=a12['posIq'][p5000],mode='lines',name='P-5000rpm',line=dict(width=4,color='blue')))
    traces.append(go.Scatter(x=a12['negId'][n10000],y=a12['negIq'][n10000],mode='lines',name='N-10000rpm',line=dict(width=4,color='green')))
    traces.append(go.Scatter(x=a12['posId'][p10000],y=a12['posIq'][p10000],mode='lines',name='P-10000rpm',line=dict(width=4,color='yellow')))
    # Create layout
    layout = go.Layout(
        xaxis=dict(title='Id(A)',color="white"),
        yaxis=dict(title='Iq(A)',color="white"),
        title='Id Iq Control Map by Temperature',
    )
 
    # Create figure
    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showline=False, showgrid=False,zeroline=False,range=[-800, 0], tick0=0,dtick=200),
        yaxis=dict(showline=False, showgrid=False,zeroline=False,range=[0, 600], tick0=0, dtick=100),
        yaxis2=dict(showline=False, showgrid=False,zeroline=False, range=[0, 1.2]),
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        yaxis2_title_font=dict(color="white"),
        yaxis2_tickfont=dict(color="white"),
        legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        showlegend=True,
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    return fig
 
def IdIqControlMapByTorque(condition_value='None'):
    # Create traces
    ptg = [0, 50, 100, 150, 200, 250, 300, 350, 400, 500]
    trqId, trqIq = ipmclass.torquemap(ptg, len(ipm.rpm), ipm.Tn, ipm.Id, ipm.Iq)
 
    p5000 = np.where(a12['prpm'] == 5000)[0]
    n5000 = np.where(a12['nrpm'] == 5000)[0]
    p10000 = np.where(a12['prpm'] == 10000)[0]
    n10000 = np.where(a12['nrpm'] == 10000)[0]
 
    ipm.plaId = np.array(ipm.plaId)
    ipm.plaIq = np.array(ipm.plaIq)
    traces = []
 
    for i in range(9):
        traces.append(go.Scatter(x=trqId[i, :],y=trqIq[i, :],mode='markers',name=f'{ptg[i+1]}',marker=dict(size=4)))
 
    traces.append(go.Scatter(x=gt['MaId'],y=gt['MaIq'],mode='markers',name='G-MTPA',marker=dict(size=7,color='#EDB120',symbol='square')))
    traces.append(go.Scatter(x=gt['MvId'],y=gt['MvIq'],mode='markers',name='G-MTPV',marker=dict(size=7,color='blue',symbol='square')))
    traces.append(go.Scatter(x=a12['posId'],y=a12['posIq'],mode='markers',name='A12-Posi',marker=dict(symbol='triangle-up',size=8,color='black')))
    traces.append(go.Scatter(x=a12['negId'],y=a12['negIq'],mode='markers',name='A12-Nega',marker=dict(symbol='triangle-up',size=8,color='red')))
 
    for i in range(4):
        traces.append(go.Scatter(x=ipm.plaId[i, :],y=ipm.plaIq[i, :],mode='markers+lines',name=f'S{i+1}K',line=dict(width=2),marker=dict(size=10,symbol='square')))
 
    traces.append(go.Scatter(x=a12['negId'][n5000],y=a12['negIq'][n5000],mode='lines',name="N-5000rpm",line=dict(width=4)))
    traces.append(go.Scatter(x=a12['posId'][p5000],y=a12['posIq'][p5000],mode='lines',name="P-5000rpm",line=dict(width=4)))
    traces.append(go.Scatter(x=a12['negId'][n10000],y=a12['negIq'][n10000],mode='lines',name="N-10000rpm",line=dict(width=4)))
    traces.append(go.Scatter(x=a12['posId'][p10000],y=a12['posIq'][p10000],mode='lines',name="P-10000rpm",line=dict(width=4)))
 
    # Create layout
    layout = go.Layout(
        xaxis=dict(
            title='Id(A)',
        ),
        yaxis=dict(
            title='Iq(A)',
        ),
        title='Id Iq Control Map by Torque',
    )
 
    # Create figure
    fig = go.Figure(data=traces, layout=layout)
    fig.update_layout(
        xaxis=dict(range=[-800, 0],dtick=200),
        yaxis=dict(range=[0, 600], tick0=0, dtick=100)
    )
    fig.update_layout(
            title_font={'size': 12,'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showline=False, showgrid=False,zeroline=False),
            yaxis=dict(showline=False, showgrid=False,zeroline=False,),
            autosize=True,   # Set plot background color to transparent
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
            showlegend=True,
        )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=500)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    # Show the plot
    return fig
 
def TempProfile(condition_value='None'):
    # Define the X and Y ranges
    X = np.arange(500, 20001, 500)
    Y = np.arange(10, 601, 10)
 
    # Initialize the matrix mat with zeros
    mat = np.zeros((len(X), len(Y)))
 
    # Calculate values for the matrix
    for ind, x in enumerate(X):
        for idx, y in enumerate(Y):
            mat[ind, idx] = Temp['A'] * x + (Temp['B'] * y ** 2 - Temp['C'] * y + Temp['iniTemp'])
 
    # Create surface plot
    fig = go.Figure(data=[go.Surface(z=mat, x=Y, y=X, colorscale='viridis')])
 
    # Update layout
    fig.update_layout(
        title='Temperature Profile',
        scene=dict(
            xaxis_title='Y',
            yaxis_title='X',
            zaxis_title='Temperature',
        ),
    )
 
 
    fig.update_layout(
        height=400,
        # legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        title_font={'color': 'white', 'size': 12},
        scene=dict(
            xaxis=dict(
                #title='X Axis Title',
                title_font=dict(color='white'),
                tickfont=dict(color='white')  # Set tick font color to white for x-axis
            ),
            yaxis=dict(
                #title='Y Axis Title',
                title_font=dict(color='white'),
                tickfont=dict(color='white')  # Set tick font color to white for y-axis
            ),
            zaxis=dict(
                #title='Z Axis Title',
                # range=[40000,0],
                title_font=dict(color='white'),
                tickfont=dict(color='white')  # Set tick font color to white for z-axis
            ),
        ),
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
    )
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=800)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    #fig.update_coloraxes(tickcolor="white")
 
    return fig
 
def Ploss_lmc(condition_value='None'):
    global plaId,plaPL,brr
    # Create a Plotly figure
    arr = np.arange(5, 75, 5)
    brr = ipm.initial + ipm.increment * arr
    num_brr = len(brr)
    num_rpm = len(ipm.rpm)
    plaId = np.full((num_brr, num_rpm), np.nan)
    plaIq = np.full((num_brr, num_rpm), np.nan)
    plaPL = np.full((num_brr, num_rpm), np.nan)
   
    for ind in range(num_brr):
        for idx in range(num_rpm):
            if ipm.rpm[idx] == brr[ind]:
                plaId[ind, idx] = ipm.Id[idx]
                plaIq[ind, idx] = ipm.Iq[idx]
                plaPL[ind, idx] = ipm.Ploss[idx]
    fig = go.Figure()
    for idx in range(len(brr)):
        fig.add_trace(go.Scatter(x=plaId[idx, :], y=plaPL[idx, :], mode='lines', name=f'Row {idx}'))
    # Update layout
    fig.update_layout(title='Ploss vs Id', xaxis_title='plaId', yaxis_title='plaPL', showlegend=False)
    fig.update_layout(
        title_font={'size': 12, 'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Iq',showline=False, showgrid=False,zeroline=False),
        yaxis=dict(title='Ld',showline=False,showgrid=False,zeroline=False,),
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        height=400,
        legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
        showlegend=True,
    )
 
    # if condition_value == '2':
    #     fig.update_layout(showlegend=True,height=500, legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    # else:
    #     fig.update_layout(showlegend=False)
    return fig

# def PlossTabButtonDown():
#     global IPMflag
#     if IPMflag == 0:
#         crr = np.array([S1K, S5K, S10K, S15K]) + ipm.initial
#         ipm.plaId,ipm.plaIq = ipmclass.filter(crr,ipm.rpm,ipm.Id,ipm.Iq)
#         num=len(ipm.rpm)
#         ipmclass.losscalc(ipm,mot,inv,igbt,Temp,Flag,num)
#         gt = ipmclass.graphtool(ipm.IPMstatus,ipm.Id,ipm.Iq,ipm.Tn,ipm.Pe)
#         IPMflag = 1

def IPMModelingTabButtonDown():
    global mtpv_web,maxPe,maxTn,maxeff,maxposeff,IPMflag,evsimflag,maxt
    global ipm,ev,ct,mv,mp,gt,tmpTn,tmpPwr,arr
    curflag = 2
    
    if IPMflag == 2:
        print("2 flag")
        return mtpv_web,maxPe,maxTn,maxeff,maxposeff,maxt
    
    
    a=5
    crr = np.array([S1K, S5K, S10K, S15K]) + ipm.initial
    ipm.plaId,ipm.plaIq = ipmclass.filter(crr,ipm.rpm,ipm.Id,ipm.Iq)
    print("ipm.plaId ipmmodellig",ipm.plaId)
    num=len(ipm.rpm)
    ipmclass.losscalc(ipm,mot,inv,igbt,Temp,Flag,num)
    gt = ipmclass.graphtool(ipm.IPMstatus,ipm.Id,ipm.Iq,ipm.Tn,ipm.Pe)

    maxt = np.real(np.max(ipm.Temp))
    mint = np.real(np.min(ipm.Temp))
    tmptg = np.arange(1, 14) / 14
    arr = np.zeros(14)
    arr[0] = mint
    arr[13] = maxt
    arr[1:13] = (maxt - mint) * tmptg[1:13] + mint
    # app.MaxTempEditField.Value = maxt;
    tmpTn,tmpPwr,ipm.tmpId,ipm.tmpIq =ipmclass.temperaturemap(arr,len(ipm.rpm),ipm.Temp,ipm.IPMstatus,ipm.Tn,ipm.Pe,ipm.Id,ipm.Iq)

    if evsimflag == 0:
        ev = evsimclass()
        # EffMaxSpeed=10000
        ct,mp,mv = ev.init(mot,EffMaxSpeed)
        evsimflag = 1
        mtpv_web=np.real(ipm.webwe)
        maxPe=np.real(max(ipm.Pe))
        maxTn=np.real(max(ipm.Tn))
        maxeff=np.real(max( ipm.n)*100)
        maxposeff=np.real(max(ipm.posin)*100)
        return mtpv_web,maxPe,maxTn,maxeff,maxposeff,maxt
    
    IPMflag = 2
    return mtpv_web,maxPe,maxTn,maxeff,maxposeff,maxt
 

def DrivepatternmodelingTabButtonDown():
    global tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
    global ip,dp,wlow,wmiddle,whigh,dpflag,IPMflag,evsimflag,ev,gt,mtpv_web,maxPe,maxTn,maxeff,maxposeff
    IPMflag = 0

    curflag = 3
    if dpflag == 1:
        return tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
    elif dpflag == 0:
        if IPMflag == 0:
            crr = np.array([S1K, S5K, S10K, S15K]) + ipm.initial
            ipm.plaId,ipm.plaIq = ipmclass.filter(crr,ipm.rpm,ipm.Id,ipm.Iq)
            num=len(ipm.rpm)
            ipmclass.losscalc(ipm,mot,inv,igbt,Temp,Flag,num)
            gt = ipmclass.graphtool(ipm.IPMstatus,ipm.Id,ipm.Iq,ipm.Tn,ipm.Pe)
            IPMflag = 1
    
        initJ = 0.5 * tire['Ma'] * tire['Tirerw'] ** 2
        ip['GrossWt'] = vhcl['crb'] + (vhcl['psgw'] * vhcl['psgnum']) + vhcl['lug'] + (vhcl['tireno'] * tire['Ma'])  
        ip['J'] = 2 * initJ + ip['GrossWt'] * tire['Tirerw'] ** 2 * (1 - sx)    
        tbl = pd.read_excel("InputTableFile.xlsx", sheet_name="Cruising Pattern",header=0)

        ip['zone'] = int(CrusPtnDropDown)
        if ip['zone'] == 1:
            ip['crsPtn'] = np.transpose(tbl['NEDC'])
        elif ip['zone'] == 2:
            ip['crsPtn']  = np.transpose(tbl['WLTC'])
        elif ip['zone'] == 3:
            ip['crsPtn']  = np.transpose(tbl['CLTC'])
        elif ip['zone'] == 4:
            ip['crsPtn']  = np.transpose(tbl['FTP75'])
        dp = wltcclass()

        wltctable = pd.read_excel("InputTableFile.xlsx", sheet_name="WLTC-Class3")

        wlow = 590
        wmiddle = 1023
        whigh = 1478

        dp.sec = wltctable['S'][:]
        kmh = wltctable['km_h'][:]

        dp.num = len(kmh)
        ip['Vx']=[0] *dp.num
        Vd = True
        if Vd == True:
            ip['VDswitch'] = 1
            ip['Vx'][:wlow] = ip['crsPtn'][:wlow] * lowf / (1 - sx)
            ip['Vx'][wlow:wmiddle] = ip['crsPtn'][wlow:wmiddle] * midf / (1 - sx)
            ip['Vx'][wmiddle:whigh] = ip['crsPtn'][wmiddle:whigh] * highf / (1 - sx)
            ip['Vx'][whigh:dp.num] = ip['crsPtn'][whigh:dp.num] * exhif / (1 - sx)

        else:
            ip['VDswitch'] = 0
            ip['Vx'][:wlow] = ip['crsPtn'][:wlow] * lowf
            ip['Vx'][wlow:wmiddle] = ip['crsPtn'][wlow:wmiddle] * midf
            ip['Vx'][wmiddle:whigh] = ip['crsPtn'][wmiddle:whigh] * highf
            ip['Vx'][whigh:dp.num] = ip['crsPtn'][whigh:dp.num] * exhif
        dp.init(mot['pole'],btt,gear,tire,ip,ipm)
        Ploss = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
        arr = [Tn50, Tn100, Tn200,Tn300]
        dp.constTrq(arr, ipm)

        tirerw=tire['Tirerw']
        moi=initJ
        dcp=dp.WLTCconpow
        Drive_distance=dp.WLTCdist
        bat_consumption=dp.bttcon
        cruis_distance=dp.crusdist
        Max_rpm=np.nansum(dp.werpm)
        socPe=-dp.AccPe[np.where(~np.isnan(dp.AccPe))[0][-1]]
        socPbtt=-dp.AccPbatt[np.where(~np.isnan( dp.AccPbatt))[0][-1]]
        ploss_td=sum(Ploss)/3600
        cop_loss=sum(dp.Pcu)/3600
        Iron_loss=sum(dp.Pfe)/3600
        Inverter_loss=sum(dp.Pinv)/3600
        stray_loss=sum(dp.Pstr)/3600
        friction_loss=sum(dp.Pf)/3600
        Windage_loss=sum(dp.Pw)/3600
        effc=sum(dp.n)/dp.count
        wnum = dp.num
        dpflag = 1
        if evsimflag == 0:
            global ct,mp,mv
            ev = evsimclass()
            # EffMaxSpeed=10000
            ct,mp,mv = ev.init(mot,EffMaxSpeed)
            mtpv_web=np.real(ipm.webwe)
            maxPe=np.real(max(ipm.Pe))
            maxTn=np.real(max(ipm.Tn))
            maxeff=np.real(max( ipm.n)*100)
            maxposeff=np.real(max(ipm.posin)*100)
            evsimflag = 1
        return tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
 


def SpeedAccelDecel(condition_value='None' ):
    global dp
    # Create figure
    fig = go.Figure()
    # Left y-axis
    fig.add_trace(go.Scatter(x=dp.sec[2:wlow], y=dp.wwrpm[2:wlow], mode='lines', line=dict(color='blue'), name='Low'))
    fig.add_trace(go.Scatter(x=dp.sec[wlow+1:wmiddle], y=dp.wwrpm[wlow+1:wmiddle], mode='lines', line=dict(color='red'), name='Middle'))
    fig.add_trace(go.Scatter(x=dp.sec[wmiddle+1:whigh], y=dp.wwrpm[wmiddle+1:whigh], mode='lines', line=dict(color='green'), name='High'))
    fig.add_trace(go.Scatter(x=dp.sec[whigh+1:dp.num], y=dp.wwrpm[whigh+1:dp.num], mode='lines', line=dict(color='yellow'), name='Extra High'))
 
    # Right y-axis
    fig.add_trace(go.Scatter(x=dp.sec[2:dp.num], y=dp.Fx[2:dp.num], mode='lines', line=dict(color='blue'), name='Fx', yaxis='y2'))
 
    fig.update_layout(
                title="Speed (rpm) and Acceleration/Deceleration vs Time",
                title_font={'size': 12,'color': 'white'},
                paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(title='Time (s)', showline=False, showgrid=False,zeroline=False,range=[0, 1800], dtick=200),
                yaxis=dict(title='Speed (rpm)', range=[-500, 3000],showline=False, showgrid=False,zeroline=False,dtick=500),
                yaxis2=dict(title='Acceleration (km/h/s)',showline=False,range=[-10000, 6000], showgrid=False,zeroline=False,side='right',dtick=2000),
                #showlegend=False,
                autosize=True,   # Set plot background color to transparent
                yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
                xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
                yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
                xaxis_title_font=dict(color="white"),
                yaxis2_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
                yaxis2_title_font=dict(color="white") ,
                showlegend=False,
                )
    if condition_value=="2":
        fig.update_layout(showlegend=True,legend=dict(x=1.03, y=0.6, orientation='v', font=dict(color='white')))
    # Show the figure
    return fig
 
def effMapTn(condition_value='None') :
    global wlow, wmiddle, whigh
    global ev, ct, mp, mv
    wnum = dp.num
 
    ptg = np.array([0, 30, 50, 60, 70, 75, 80, 85, 87.5, 90, 92.5, 95, 97.5, 100]) / 100
    effposiTn, effposiPwr, effnegaTn, effnegaPwr = ipmclass.efficiency(len(ipm.rpm), ptg, ipm.IPMstatus, ipm.posin, ipm.negan, ipm.Tn, ipm.Pe)
 
    # Create a new figure
    fig = go.Figure()
 
    # Plot efficiency map
    fig.update_layout(title='Efficiency Map on TN graph')
    if condition_value=="1":
        for i in range(13):
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effposiTn[i]), mode='markers', name=f'{ptg[i+1]*100:.1f}%', marker=dict(size=2)))
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effnegaTn[i]), mode='markers', marker=dict(size=2),showlegend=False))  # Empty string for unnamed legend
 
        # Plot other data points
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[1:wlow]), y=np.real(dp.Tn[1:wlow]), mode='markers', name='Low', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wlow + 1: wmiddle]), y=np.real(dp.Tn[wlow + 1: wmiddle]), mode='markers', name='Medium', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wmiddle + 1:whigh]), y=np.real(dp.Tn[wmiddle + 1:whigh]), mode='markers', name='High', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[whigh + 1:wnum]), y=np.real(dp.Tn[whigh + 1:wnum]), mode='markers', name='Extra-high', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:90]), y=np.real(ct['Teflag'][:90]), mode='markers', name='Te(Nm) in Constant Torque', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mp['Teflag'][:200]), mode='markers', name='Te(Nm) in Max Power', marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mv['Teflag'][:200]), mode='markers', name='Te(Nm) in MTPV', marker=dict(size=2)))
 
    if condition_value=="2":
        for i in range(13):
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effposiTn[i]), mode='markers', name=f'{ptg[i+1]*100:.1f}%', marker=dict(size=4)))
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effnegaTn[i]), mode='markers', marker=dict(size=4),showlegend=False))  # Empty string for unnamed legend
 
    # Plot other data points
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[1:wlow]), y=np.real(dp.Tn[1:wlow]), mode='markers', name='Low', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wlow + 1: wmiddle]), y=np.real(dp.Tn[wlow + 1: wmiddle]), mode='markers', name='Medium', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wmiddle + 1:whigh]), y=np.real(dp.Tn[wmiddle + 1:whigh]), mode='markers', name='High', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[whigh + 1:wnum]), y=np.real(dp.Tn[whigh + 1:wnum]), mode='markers', name='Extra-high', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:90]), y=np.real(ct['Teflag'][:90]), mode='markers', name='Te(Nm) in Constant Torque', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mp['Teflag'][:200]), mode='markers', name='Te(Nm) in Max Power', marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mv['Teflag'][:200]), mode='markers', name='Te(Nm) in MTPV', marker=dict(size=4)))
 
 
 
    fig.update_layout(
        title_font={'size': 12, 'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='rpm', showline=False, showgrid=False, zeroline=False, range=[-1000, 20000]),
        yaxis=dict(title='Nm', showline=False, showgrid=False, zeroline=False),
        autosize=True,  # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),  # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),  # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False,
    )
 
    # # Show the plot
    if condition_value == '2':
        fig.update_layout(showlegend=True,legend=dict(x=1.03, y=0.6, orientation='v', font=dict(color='white')))
    # else:
    #     fig.update_layout(showlegend=False, height=400)
 
    return fig
 
def piegraph(condition_value='None'):
    val = [sum(dp.Pcu), sum(dp.Pfe), sum(dp.Pstr), sum(dp.Pf), sum(dp.Pw), sum(dp.Pinv)]
    fig = go.Figure(data=[go.Pie(labels=['Pcu', 'Pfe', 'Pstr', 'Pfric', 'Pwind', 'Pinv'], values=val),])
 
    # Customize the layout
    fig.update_layout(title='P-LOSS/WLTC total')
    fig.update_traces(rotation=180)
    fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 12, 'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        showlegend=False,
    )
   
    if condition_value == '2':
        fig.update_layout(showlegend=True, legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    return fig
 
def wltc_btt( condition_value='None'):
    wnum = dp.num
    # Create figure with secondary y-axis
    fig = go.Figure()
    # print("dp.AccPe",dp.AccPe)
    # Add traces
    fig.add_trace(go.Scatter(x=np.real(dp.sec[:wnum]), y=np.real(dp.AccPe), mode='lines', name='Acc(Pe) w/o Ploss', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=np.real(dp.sec[:wnum]), y=np.real(dp.AccPbatt[:wnum]), mode='lines', name='Acc(Pbtt) consumption w/Ploss', line=dict(color='blue')))
 
    # Add secondary y-axis
    fig.add_trace(go.Scatter(x=np.real(dp.sec[:wnum]), y=np.real(dp.Pekws), mode='lines', name='Pe(kW/s)', line=dict(color='#00cc96', width=1) ,yaxis='y2'))
    fig.add_trace(go.Scatter(x=np.real(dp.sec[:wnum]), y=np.real(dp.Ploss), mode='lines', name='Ploss/s', line=dict(color='yellow'), yaxis='y2'))
 
    # Update layout
    fig.update_layout(
        xaxis=dict(title='Seconds'),
        yaxis=dict(title='kW', range=[-7, 0], titlefont=dict(color='rgb(11, 7, 44)', size=12)),
        yaxis2=dict(title='kW/s', range=[-0.015, 0.02], titlefont=dict(color='rgb(11, 7, 44)', size=12), overlaying='y', side='right'),
        xaxis_range=[0, 1800]
    )
 
    fig.update_layout(
        title='WLTC(1800 sec): BTT Power Consumption (SOC)',
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showline=False, showgrid=False,zeroline=False),
        yaxis=dict(title='kW',showline=False, showgrid=False,zeroline=False,range=[-7, 0], dtick=1),
        yaxis2=dict(title='Nm',showline=False, showgrid=False,zeroline=False,range=[-0.015, 0.02]),
        # showlegend=False,
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis2_title_font=dict(color="white"),
        yaxis2_tickfont=dict(color="white"),
        showlegend=False
    )
    if condition_value == '2':
        fig.update_layout(showlegend=True, legend=dict(x=1.01, y=0.3, orientation='v' , font=dict(color='white')),)
    # else:
    #     fig.update_layout(showlegend=False,height=400)
    return fig
 
def effPower(condition_value='None'):
    global wlow,wmiddle,whigh
    wnum = dp.num
    ptg = np.array([0, 30, 50, 60, 70, 75, 80, 85, 87.5, 90, 92.5, 95, 97.5, 100]) / 100
    effposiTn,effposiPwr,effnegaTn,effnegaPwr = ipmclass.efficiency(len(ipm.rpm),ptg,ipm.IPMstatus,ipm.posin,ipm.negan,ipm.Tn,ipm.Pe)
 
    fig = go.Figure()
    if condition_value=="1":
        for i in range(13):
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effposiPwr[i]), mode='markers', name=f'{ptg[i+1]*100:.1f}%',marker=dict(size=2)))
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effnegaPwr[i]), mode='markers', name='EffnegaTn',marker=dict(size=2),showlegend=False))
 
        # # Plot other data points
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[1:wlow]), y=np.real(dp.Pekwh[1:wlow]), mode='markers', name='Low',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wlow + 1:wmiddle]), y=np.real(dp.Pekwh[wlow + 1:wmiddle]), mode='markers', name='Medium',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wmiddle + 1: whigh]), y=np.real(dp.Pekwh[wmiddle + 1: whigh]), mode='markers', name='High',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[whigh + 1:wnum]), y=np.real(dp.Pekwh[whigh + 1:wnum]), mode='markers', name='Extra-high',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[: 90]), y=np.real(ct['Peflag'][:90]), mode='markers', name='Pe(kW) in Constant Torque',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mp['Peflag'][:200]), mode='markers', name='Pe(kW) in Max Power',marker=dict(size=2)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mv['Peflag'][:200]), mode='markers', name='Pe(kW) in MTPV',marker=dict(size=2)))
 
    if condition_value=="2":
        for i in range(13):
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effposiPwr[i]), mode='markers', name=f'{ptg[i+1]*100:.1f}%',marker=dict(size=4)))
            fig.add_trace(go.Scatter(x=np.real(ipm.rpm), y=np.real(effnegaPwr[i]), mode='markers', name='EffnegaTn',marker=dict(size=4),showlegend=False))
 
        # # Plot other data points
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[1:wlow]), y=np.real(dp.Pekwh[1:wlow]), mode='markers', name='Low',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wlow + 1:wmiddle]), y=np.real(dp.Pekwh[wlow + 1:wmiddle]), mode='markers', name='Medium',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[wmiddle + 1: whigh]), y=np.real(dp.Pekwh[wmiddle + 1: whigh]), mode='markers', name='High',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(dp.werpm[whigh + 1:wnum]), y=np.real(dp.Pekwh[whigh + 1:wnum]), mode='markers', name='Extra-high',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[: 90]), y=np.real(ct['Peflag'][:90]), mode='markers', name='Pe(kW) in Constant Torque',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mp['Peflag'][:200]), mode='markers', name='Pe(kW) in Max Power',marker=dict(size=4)))
        fig.add_trace(go.Scatter(x=np.real(ev.rpm[:200]), y=np.real(mv['Peflag'][:200]), mode='markers', name='Pe(kW) in MTPV',marker=dict(size=4)))
 
    fig.update_layout(title='Efficiency Map on Power graph')
    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='rpm', showline=False, showgrid=False,zeroline=False,range=[-1000, 20000]),
        yaxis=dict(title='Nm',showline=False, showgrid=False,zeroline=False ),
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False,
    )
    if condition_value == '2':
        fig.update_layout(showlegend=True, legend=dict(x=1.01, y=0.3, orientation='v' , font=dict(color='white')),)
 
    return fig
    # Show the plot
 
 
def IdIqAvatarA12( condition_value='None'):
    global a12,gt
 
    p5000 = np.where(np.array(a12['prpm']) == 5000)[0]
    n5000 = np.where(np.array(a12['nrpm']) == 5000)[0]
    p10000 = np.where(np.array(a12['prpm']) == 10000)[0]
    n10000 = np.where(np.array(a12['nrpm']) == 10000)[0]
 
    fig = go.Figure()
 
    # # Add the data traces
    if condition_value=="1":
        fig.add_trace(go.Scatter(x=gt['MaId'], y=gt['MaIq'], mode='markers', marker=dict(color='rgb(162,20,47)', size=2), name='G-MTPA'))
        fig.add_trace(go.Scatter(x=gt['CId'], y=gt['CIq'], mode='markers', marker=dict(color='rgb(119,172,48)', size=2), name='G-CPSR'))
        fig.add_trace(go.Scatter(x=gt['MvId'], y=gt['MvIq'], mode='markers', marker=dict(color='blue', size=2), name='G-MTPV'))
 
 
        fig.add_trace(go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', name='A12-Posi', marker=dict(color='black', symbol='triangle-up', size=2)))
        fig.add_trace(go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', name='A12-Nega', marker=dict(color='red', symbol='triangle-up', size=2)))
        fig.add_trace(go.Scatter(x=a12['negId'][n5000], y=a12['negIq'][n5000], mode='lines+markers', name='N-5000rpm', line=dict(width=2)))
        fig.add_trace(go.Scatter(x=a12['posId'][p5000], y=a12['posIq'][p5000], mode='lines+markers', name='P-5000rpm', line=dict(width=2)))
        fig.add_trace(go.Scatter(x=a12['negId'][n10000], y=a12['negIq'][n10000], mode='lines+markers', name='N-10000rpm', line=dict(width=2)))
        fig.add_trace(go.Scatter(x=a12['posId'][p10000], y=a12['posIq'][p10000], mode='lines+markers', name='P-10000rpm', line=dict(width=2)))
 
        for i in range(4):
            fig.add_trace(go.Scatter(x=ipm.plaId[i, :], y=ipm.plaIq[i, :], mode='lines+markers', marker=dict(size=4), name=f'S-{i+1}k'))
 
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[:19]), y=np.real(dp.ctIq[:19]), mode='lines+markers', name='Tn-50', marker=dict(size=2, line=dict(width=2))))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[19:38]), y=np.real(dp.ctIq[19:38]), mode='lines+markers', name='Tn-100', line=dict(width=2), marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[38:57]), y=np.real(dp.ctIq[38:57]), mode='lines+markers', name='Tn-200', line=dict(width=2), marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[57:76]), y=np.real(dp.ctIq[57:76]), mode='lines+markers', name='Tn-300',line=dict(width=2), marker=dict(size=6)))
 
    if condition_value=="2":
        fig.add_trace(go.Scatter(x=gt['MaId'], y=gt['MaIq'], mode='markers', marker=dict(color='rgb(162,20,47)', size=4), name='G-MTPA'))
        fig.add_trace(go.Scatter(x=gt['CId'], y=gt['CIq'], mode='markers', marker=dict(color='rgb(119,172,48)', size=4), name='G-CPSR'))
        fig.add_trace(go.Scatter(x=gt['MvId'], y=gt['MvIq'], mode='markers', marker=dict(color='blue', size=4), name='G-MTPV'))
 
 
        fig.add_trace(go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', name='A12-Posi', marker=dict(color='black', symbol='triangle-up', size=4)))
        fig.add_trace(go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', name='A12-Nega', marker=dict(color='red', symbol='triangle-up', size=4)))
        fig.add_trace(go.Scatter(x=a12['negId'][n5000], y=a12['negIq'][n5000], mode='lines+markers', name='N-5000rpm', line=dict(width=4)))
        fig.add_trace(go.Scatter(x=a12['posId'][p5000], y=a12['posIq'][p5000], mode='lines+markers', name='P-5000rpm', line=dict(width=4)))
        fig.add_trace(go.Scatter(x=a12['negId'][n10000], y=a12['negIq'][n10000], mode='lines+markers', name='N-10000rpm', line=dict(width=4)))
        fig.add_trace(go.Scatter(x=a12['posId'][p10000], y=a12['posIq'][p10000], mode='lines+markers', name='P-10000rpm', line=dict(width=4)))
 
        for i in range(4):
            fig.add_trace(go.Scatter(x=ipm.plaId[i, :], y=ipm.plaIq[i, :], mode='lines+markers', marker=dict(size=4), name=f'S-{i+1}k'))
 
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[:19]), y=np.real(dp.ctIq[:19]), mode='lines+markers', name='Tn-50', marker=dict(size=4, line=dict(width=2))))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[19:38]), y=np.real(dp.ctIq[19:38]), mode='lines+markers', name='Tn-100', line=dict(width=4), marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[38:57]), y=np.real(dp.ctIq[38:57]), mode='lines+markers', name='Tn-200', line=dict(width=4), marker=dict(size=6)))
        fig.add_trace(go.Scatter(x=np.real(dp.ctId[57:76]), y=np.real(dp.ctIq[57:76]), mode='lines+markers', name='Tn-300',line=dict(width=4), marker=dict(size=6)))
    # Set labels for axes
    fig.update_layout(xaxis_title='Id (A)', yaxis_title='Iq (A)')
    fig.update_xaxes(title_font=dict(color='purple', size=12))
    fig.update_yaxes(title_font=dict(color='purple', size=12))
 
    # Set axis limits
    fig.update_xaxes(range=[-700, 0], dtick=100)
    fig.update_yaxes(range=[0, 700], dtick=100)
 
    # Set the title
    fig.update_layout(title='Id Iq control Map of Avatar IPM and A12 ')
 
    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Id(A)', showline=False, showgrid=False,zeroline=False),
        yaxis=dict(title='Iq(A)',showline=False, showgrid=False,zeroline=False,),
        # showlegend=False,
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False,
    )
     
    if condition_value == '2':
        fig.update_layout(showlegend=True, legend=dict(x=1.01, y=0.3, orientation='v' , font=dict(color='white')),)
    # Show the plot
    return fig

#cruising



def CruisingdistanceandbatterybysimulationandpoleButtonPushed():
    # global mot,ipm,dp,btt, gear, tire, ip ,inv, igbt, Temp, Flag
    # global type,hdcalf,hqcalf,const,peflag,tnflag,Mode,DTtab,DTnum
    # global ldopt,lqopt,pmdopt
 
    poleArr = [4, 6, 8]
    bttcon = [0] * (len(poleArr) * 6)
    crusdist = [0] * (len(poleArr) * 6)
    counter = 0
 
    crussim  = mot.copy()
 
    Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=1)
    Psid = Psid.iloc[0:, 2:].values
    Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=1)
    Psiq = Psiq.iloc[0:, 2:].values
    Omega = (Psid ** 2) + (Psiq ** 2)
 
    tuntable = pd.read_excel("InputTableFile.xlsx", sheet_name="tuning")
 
    for pole in poleArr:
        crussim['pole'] = pole
        for idx in range(6):
            # Placeholder function for PsiLdLq - Needs actual implementation
            PLmat = PLmat = PsiLdLq(mot['pole'],DTtab,hdcalf,hqcalf,type,idx,pmdopt[idx],ldopt[idx],lqopt[idx],Psid,Psiq,Omega)
            PLmat['copy'] = tuntable['copy']
           
            tun = 1 # value fetched psipm  switch Psi_PMSwitchValueChanged
            if tun == 1:  # Psi_PM button is ON
                PLmat['tuning'] = list(tuntable['Tuning'])
            else:  # Psi_PM button is OFF
                PLmat['tuning'] = [1] * len(tuntable['Tuning'])
           
            # Placeholder class and methods - Needs actual implementation
            start_time = time.time()
            ipmobj = ipmclass()
            ipmobj.initial = ipm.initial
            ipmobj.increment = ipm.increment
            ipmobj.init(crussim,DTtab,idx,PLmat,tnflag,peflag,const)
            ipmobj.losscalc(crussim, inv, igbt, Temp, Flag, len(ipmobj.rpm))
            end_time = time.time()
 
            execution_time = end_time - start_time
            print(f"Execution time ipm {idx} : {execution_time} seconds")
 
 
            start_time = time.time()
            dpobj = wltcclass()
            dpobj.sec = dp.sec
            dpobj.num = dp.num
            dpobj.init(crussim['pole'], btt, gear, tire, ip, ipmobj)
            end_time = time.time()
 
            execution_time = end_time - start_time
            print(f"Execution time WLTC {idx} : {execution_time} seconds")
 
 
            bttcon[counter] = dpobj.bttcon
            crusdist[counter] = dpobj.crusdist
            counter += 1
            
   
    # fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=list(range(len(bttcon))), y=np.abs(bttcon), name='BTT (kWh/10km)', marker_color='blue'))
   
    fig.update_layout(
        title='Cruising Distance (km) and BTT (kWh/10km) by Pole Pair No.',
        xaxis_title='Index',
        yaxis_title='BTT (kWh/10km)',
        xaxis=dict(title='BTT (kWh/10km)', range=[-1, 16], dtick=5),
        yaxis=dict(range=[1.55, 1.85]),
        legend=dict(x=0.01, y=0.99, traceorder='normal')
    )
   
    fig.add_trace(go.Scatter(x=list(range(len(crusdist))), y=np.abs(crusdist), name='Cruising Distance', mode='lines+markers', marker=dict(color='yellow', size=10), line=dict(color='red'),yaxis='y2'))
    fig.update_yaxes(range=[420, 490],dtick=10, secondary_y=True)
    fig.update_layout(showlegend=False)
    # fig.show()
    return fig


def CruisingdistanceandbatterybysimulationmodelButtonPushed():
    # global mot,ipm,dp,btt, gear, tire, ip ,inv, igbt, Temp, Flag
    # global type,hdcalf,hqcalf,const,peflag,tnflag,Mode,DTtab,DTnum
    # global ldopt,lqopt,pmdopt

    bttcon = [0] * 6
    crusdist = [0] * 6
    
    crussim = mot.copy()

    Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=1)
    Psid = Psid.iloc[0:, 2:].values
    Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=1)
    Psiq = Psiq.iloc[0:, 2:].values
    Omega = (Psid ** 2) + (Psiq ** 2)

    tuntable = pd.read_excel("InputTableFile.xlsx", sheet_name="tuning")

    for idx in range(6):
        # Placeholder function for PsiLdLq - Needs actual implementation
        
        PLmat = PsiLdLq(mot['pole'],DTtab,hdcalf,hqcalf,type,idx,pmdopt[idx],ldopt[idx],lqopt[idx],Psid,Psiq,Omega)
        PLmat['copy'] = tuntable['copy']  # Column G
        
        tun = 1 # value fetched psipm  switch Psi_PMSwitchValueChanged
        if tun == 1:  # Psi_PM button is ON
            PLmat['tuning'] = list(tuntable['Tuning'])
        else:  # Psi_PM button is OFF
            PLmat['tuning'] = [1] * len(tuntable['Tuning'])
        
        # Placeholder class and methods - Needs actual implementation
        ipmobj = ipmclass()
        ipmobj.initial = ipm.initial
        ipmobj.increment = ipm.increment
        # print("crussim",crussim)
        # print("DTtab",DTtab)
        # print("idx",idx)
        # # print("PLmat",PLmat)
        # print("tnflag",tnflag)
        # print("peflag",peflag)
        # print("const",const)
        
        ipmobj.init(crussim,DTtab,idx,PLmat,tnflag,peflag,const)
        ipmobj.losscalc(crussim, inv, igbt, Temp, Flag, len(ipmobj.rpm))
        
        dpobj = wltcclass()
        dpobj.sec = dp.sec
        dpobj.num = dp.num
        # print("idx",idx)
        # print("crussim['pole']",crussim['pole'])
        # print("btt",btt)
        # print("gear",gear)
        # print("tire",tire)
        # print("ip",ip)
        dpobj.init(crussim['pole'], btt, gear, tire, ip, ipmobj)
        
        bttcon[idx] = dpobj.bttcon
        crusdist[idx] = dpobj.crusdist
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    print("len(bttcon)",len(bttcon))
    print("bttcon",bttcon)
    fig.add_trace(go.Bar(x=list(range(len(bttcon))), y=bttcon, name='BTT (kWh/10km)', marker_color='blue'))
    
    fig.update_layout(
        title='Cruising Distance (km) and BTT (kWh/10km) by Simulation Model',
        xaxis=dict(title='Index', range=[-1, 7], dtick=1),
        yaxis_title='BTT (kWh/10km)',
        yaxis=dict(range=[1.84, 2],dtick=0.02),
        yaxis2=dict(
            title='Cruising Distance (km)',
            overlaying='y',
            side='right',
            range=[395, 425]
        ),
        legend=dict(x=0.01, y=0.99, traceorder='normal')
    )
    print("len(crusdist)",len(crusdist))
    print("crusdist",crusdist)    
    fig.add_trace(go.Scatter(x=list(range(len(crusdist))), y=crusdist, name='Cruising Distance', mode='lines+markers', marker=dict(color='yellow', size=10), line=dict(color='red'),yaxis='y2'))
    fig.update_yaxes(range=[395, 425],dtick=5, secondary_y=True)
    fig.update_layout(showlegend=False)
    # fig.show()
    return fig
def CruisingdistanceandbatterybygearratioButtonPushed():
    # global dp,ip
    gdrArr = np.arange(5, 15.5, 0.5)

    bttcon= np.zeros(len(gdrArr))
    crusdist = np.zeros(len(gdrArr))
    print("gear",gear)
    crusgear = gear.copy()
    print("gear1",gear)
    obj = wltcclass()
    obj.sec = dp.sec
    obj.num = dp.num
    print("gear2",gear)

    for idx in range(len(gdrArr)):
        print("gear4",gear)
        crusgear['gdr'] = gdrArr[idx]
        # Call the init function to calculate parameters
        print("gear5",gear)
        obj.init(mot['pole'], btt, crusgear, tire, ip, ipm)
        print("gear6",gear)
        # Store the results
        bttcon[idx] = obj.bttcon
        crusdist[idx] = obj.crusdist
    # for idx, gdr in enumerate(gdrArr):
    #     print("gear4",gear)
    #     crusgear['gdr'] = gdr
    #     obj.init(mot['pole'], btt, crusgear, tire, ip, ipm)
    #     bttcon1[idx] = obj.bttcon
    #     crusdist1[idx] = obj.crusdist

    # Plotting with Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=gdrArr, y=bttcon, name='BTT (kWh/10km)', marker_color='blue'))

    fig.update_layout(
        title='Cruising Distance (km) and BTT (kWh/10km) by Gear Ratio',
        xaxis = dict(title='Gear Ratio',range=[4,16],dtick=5),
        yaxis=dict(
            title='BTT (kWh/10km)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            # range=[0, 2.5],
            dtick=0.5
        ),
        yaxis2=dict(
            title='Cruising Distance (km)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right',
            # range=[389, 480],
            dtick=10
        ),
        # legend=dict(x=0.01, y=0.99, traceorder='normal')
    )
    # print("len(crusdist)",len(crusdist))
    print("gdrArr",gdrArr)
    print("bttcon1",bttcon)
    print("crusdist1",crusdist)    
    fig.add_trace(go.Scatter(x=gdrArr, y=crusdist, name='Cruising Distance', mode='lines+markers', marker=dict(color='yellow', size=10), line=dict(color='red'), yaxis='y2'))
    fig.update_layout(showlegend=False)
    # fig.show()
    return fig





def CruisingdistanceandbatterybyIdcButtonPushed():
    # global mot,ipm,dp,btt, gear, tire, ip ,inv, igbt, Temp, Flag
    # global type,hdcalf,hqcalf,const,peflag,tnflag,Mode,DTtab,DTnum
    # global ldopt,lqopt,pmdopt

    ImArr = np.arange(598, 679, 4)

    bttcon = np.zeros(len(ImArr))
    crusdist = np.zeros(len(ImArr))

    crusIm = mot.copy()

    Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=1)
    Psid = Psid.iloc[0:, 2:].values
    Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=1)
    Psiq = Psiq.iloc[0:, 2:].values
    Omega = (Psid ** 2) + (Psiq ** 2)

    tuntable = pd.read_excel("InputTableFile.xlsx", sheet_name="tuning")

    PLmat = PsiLdLq(mot['pole'],DTtab,hdcalf,hqcalf,type,DTnum,pmdopt[DTnum],ldopt[DTnum],lqopt[DTnum],Psid,Psiq,Omega)
    PLmat['copy'] = tuntable['copy']  # Column G
    
    tun = 1 # value fetched psipm  switch Psi_PMSwitchValueChanged
    if tun == 1:  # Psi_PM button is ON
        PLmat['tuning'] = list(tuntable['Tuning'])
    else:  # Psi_PM button is OFF
        PLmat['tuning'] = [1] * len(tuntable['Tuning'])

    for idx, Im in enumerate(ImArr):
        crusIm['cur'] = Im

        # Create ipm class object
        ipmobj = ipmclass()
        ipmobj.initial = ipm.initial
        ipmobj.increment = ipm.increment

        # Calculate IPM modeling parameters
        ipmobj.init(crusIm, DTtab, DTnum, PLmat, tnflag, peflag, const)
        ipmobj.losscalc(crusIm, inv, igbt, Temp, Flag, len(ipmobj.rpm))

        dpobj = wltcclass()
        dpobj.sec = dp.sec
        dpobj.num = dp.num

        # Calculate the wltc parameters
        dpobj.init(crusIm['pole'], btt, gear, tire, ip, ipmobj)
        bttcon[idx] = dpobj.bttcon
        crusdist[idx] = dpobj.crusdist

    # Plotting with Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ImArr, y=bttcon, name='BTT (kWh/10km)', marker_color='blue'))

    fig.update_layout(
        title='Cruising Distance (km) and BTT (kWh/10km) by Idc',
        xaxis = dict(title='Current (Idc)',range=[600,680],dtick=20),
        # xaxis_title='Current (Idc)',
        yaxis=dict(
            title='BTT (kWh/10km)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            range=[1.8, 1.9],
            dtick=0.01
        ),
        yaxis2=dict(
            title='Cruising Distance (km)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right',
            range=[414, 437],
            dtick=2
        ),
        legend=dict(x=0.01, y=0.99, traceorder='normal')
    )

    fig.add_trace(go.Scatter(x=ImArr, y=crusdist, name='Cruising Distance', mode='lines+markers', marker=dict(color='yellow', size=10), line=dict(color='red'), yaxis='y2'))
    fig.update_layout(showlegend=False)
    # fig.show()
    return fig

def CruisingdistanceandbatterybyTireinchButtonPushed():
    # global btt, gear, ip, ipm, tire

    inchArr = np.arange(18, 39)

    bttcon = np.zeros(len(inchArr))
    crusdist = np.zeros(len(inchArr))

    crustire = tire.copy()

    obj = wltcclass()
    obj.sec = dp.sec
    obj.num = dp.num

    for idx, inch in enumerate(inchArr):
        crustire['TireOutD'] = inch
        crustire['Tirerw'] = crustire['TireOutD'] * 25.4 / 2 / 1000
        # Calculate the wltc parameters
        obj.init(mot['pole'], btt, gear, crustire, ip, ipm)
        bttcon[idx] = obj.bttcon
        crusdist[idx] = obj.crusdist

    # Plotting with Plotly
    fig = go.Figure()
    fig.add_trace(go.Bar(x=inchArr, y=bttcon, name='BTT (kWh/10km)', marker_color='blue'))

    fig.update_layout(
        title='Cruising Distance (km) and BTT (kWh/10km) by Tire inch',
        xaxis = dict(title='Tire Diameter (inch)'),
        yaxis=dict(
            title='BTT (kWh/10km)',
            titlefont=dict(color='blue'),
            tickfont=dict(color='blue'),
            # range=[0, 3.5],
            dtick=0.5
        ),
        yaxis2=dict(
            title='Cruising Distance (km)',
            titlefont=dict(color='red'),
            tickfont=dict(color='red'),
            overlaying='y',
            side='right',
            # range=[250, 650],
            dtick=50
        ),
        legend=dict(x=0.01, y=0.99, traceorder='normal')
    )

    fig.add_trace(go.Scatter(x=inchArr, y=crusdist, name='Cruising Distance', mode='lines+markers', marker=dict(color='yellow', size=10), line=dict(color='red'), yaxis='y2'))
    fig.update_layout(showlegend=False)

    return fig


def IdvsIqPlot():
 
    fig=go.Figure()
   
    fig.add_trace(go.Scatter(x=np.real(dp.Id),y=np.real(dp.Iq), mode='markers', marker=dict(size=3, color='rgb(52, 196, 235)')))
    fig.update_layout(title='Id vs Iq')
    fig.update_layout(
        title_font={'size': 15,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Id(A)', showline=False, showgrid=False,zeroline=False,range=[min(np.real(dp.Id)),max(np.real(dp.Id))], dtick=50),
        yaxis=dict(title='Iq(A)',showline=False, showgrid=False,zeroline=False,range=[min(dp.Iq), max(dp.Iq)], dtick=50),
        # showlegend=False,
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white")
    )
 
    return fig

def PlossbyWLTCzonesButtonPushed():
    # Define the zones
    wlow = 590
    wmiddle = 1023
    whigh = 1478
    wnum = dp.num

    # Calculate the power losses for each zone
    Pcu = [
        np.sum(dp.Pcu[1:wlow]) / 3600,
        np.sum(dp.Pcu[wlow:wmiddle]) / 3600,
        np.sum(dp.Pcu[wmiddle:whigh]) / 3600,
        np.sum(dp.Pcu[whigh:wnum]) / 3600
    ]
    Pfe = [
        np.sum(dp.Pfe[1:wlow]) / 3600,
        np.sum(dp.Pfe[wlow:wmiddle]) / 3600,
        np.sum(dp.Pfe[wmiddle:whigh]) / 3600,
        np.sum(dp.Pfe[whigh:wnum]) / 3600
    ]
    Pstr = [
        np.sum(dp.Pstr[1:wlow]) / 3600,
        np.sum(dp.Pstr[wlow:wmiddle]) / 3600,
        np.sum(dp.Pstr[wmiddle:whigh]) / 3600,
        np.sum(dp.Pstr[whigh:wnum]) / 3600
    ]
    Pfr = [
        np.sum(dp.Pf[1:wlow]) / 3600,
        np.sum(dp.Pf[wlow:wmiddle]) / 3600,
        np.sum(dp.Pf[wmiddle:whigh]) / 3600,
        np.sum(dp.Pf[whigh:wnum]) / 3600
    ]
    Pw = [
        np.sum(dp.Pw[1:wlow]) / 3600,
        np.sum(dp.Pw[wlow:wmiddle]) / 3600,
        np.sum(dp.Pw[wmiddle:whigh]) / 3600,
        np.sum(dp.Pw[whigh:wnum]) / 3600
    ]
    Pinv = [
        np.sum(dp.Pinv[1:wlow]) / 3600,
        np.sum(dp.Pinv[wlow:wmiddle]) / 3600,
        np.sum(dp.Pinv[wmiddle:whigh]) / 3600,
        np.sum(dp.Pinv[whigh:wnum]) / 3600
    ]

    # Combine the data
    y = np.array([Pcu, Pfe, Pstr, Pfr, Pw, Pinv]).T

    # Create the bar plot
    fig = go.Figure()

    categories = ['Low', 'Middle', 'High', 'Extra-High']
    labels = ['Pcu', 'Pfe', 'Pstr', 'Pfric', 'Pwind', 'Pinv']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    for i, label in enumerate(labels):
        fig.add_trace(go.Bar(
            x=categories,
            y=y[:, i],
            name=label,
            marker_color=colors[i]
        ))

    # Update layout
    fig.update_layout(
        title='Ploss by WLTC zone',
        xaxis=dict(title='Zone' ,showline=False, showgrid=False,zeroline=False,),
        yaxis=dict(title='kW', title_font=dict(size=12), showline=False, showgrid=False,zeroline=False,),
        legend=dict(title='Loss Type', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        barmode='group',
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color='white')
    )

    return fig

def IdIqcontrolMapButtonPushed( ):
    global a12,gt

    p5000 = np.where(np.array(a12['prpm']) == 5000)[0]
    n5000 = np.where(np.array(a12['nrpm']) == 5000)[0]
    p10000 = np.where(np.array(a12['prpm']) == 10000)[0]
    n10000 = np.where(np.array(a12['nrpm']) == 10000)[0]

    fig = go.Figure()

    # # Add the data traces

    fig.add_trace(go.Scatter(x=gt['MaId'], y=gt['MaIq'], mode='markers', marker=dict(color='rgb(162,20,47)', size=2), name='G-MTPA'))
    fig.add_trace(go.Scatter(x=gt['CId'], y=gt['CIq'], mode='markers', marker=dict(color='rgb(119,172,48)', size=2), name='G-CPSR'))
    fig.add_trace(go.Scatter(x=gt['MvId'], y=gt['MvIq'], mode='markers', marker=dict(color='blue', size=2), name='G-MTPV'))


    fig.add_trace(go.Scatter(x=a12['posId'], y=a12['posIq'], mode='markers', name='A12-Posi', marker=dict(color='black', symbol='triangle-up', size=2)))
    fig.add_trace(go.Scatter(x=a12['negId'], y=a12['negIq'], mode='markers', name='A12-Nega', marker=dict(color='red', symbol='triangle-up', size=2)))
    fig.add_trace(go.Scatter(x=a12['negId'][n5000], y=a12['negIq'][n5000], mode='lines+markers', name='N-5000rpm', line=dict(width=2)))
    fig.add_trace(go.Scatter(x=a12['posId'][p5000], y=a12['posIq'][p5000], mode='lines+markers', name='P-5000rpm', line=dict(width=2)))
    fig.add_trace(go.Scatter(x=a12['negId'][n10000], y=a12['negIq'][n10000], mode='lines+markers', name='N-10000rpm', line=dict(width=2)))
    fig.add_trace(go.Scatter(x=a12['posId'][p10000], y=a12['posIq'][p10000], mode='lines+markers', name='P-10000rpm', line=dict(width=2)))

    for i in range(4):
        fig.add_trace(go.Scatter(x=ipm.plaId[i, :], y=ipm.plaIq[i, :], mode='lines+markers', marker=dict(size=4), name=f'S-{i+1}k'))

    fig.add_trace(go.Scatter(x=np.real(dp.ctId[:19]), y=np.real(dp.ctIq[:19]), mode='lines+markers', name='Tn-50', marker=dict(size=2, line=dict(width=2))))
    fig.add_trace(go.Scatter(x=np.real(dp.ctId[19:38]), y=np.real(dp.ctIq[19:38]), mode='lines+markers', name='Tn-100', line=dict(width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=np.real(dp.ctId[38:57]), y=np.real(dp.ctIq[38:57]), mode='lines+markers', name='Tn-200', line=dict(width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=np.real(dp.ctId[57:76]), y=np.real(dp.ctIq[57:76]), mode='lines+markers', name='Tn-300',line=dict(width=2), marker=dict(size=6)))

    # Set labels for axes
    fig.update_layout(xaxis_title='Id (A)', yaxis_title='Iq (A)')
    fig.update_xaxes(title_font=dict(color='purple', size=12))
    fig.update_yaxes(title_font=dict(color='purple', size=12))

    # Set axis limits
    fig.update_xaxes(range=[-700, 0], dtick=100)
    fig.update_yaxes(range=[0, 700], dtick=100)

    # Set the title
    fig.update_layout(title='Id Iq control Map of Avatar IPM and A12 ')

    fig.update_layout(
        title_font={'size': 12,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Id(A)', showline=False, showgrid=False,zeroline=False),
        yaxis=dict(title='Iq(A)',showline=False, showgrid=False,zeroline=False,),
        # showlegend=False,
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False, 
    )
     

    # Show the plot
    return fig

def data_tabg1(condition_value='None'):
    # Read data from Excel file
    datatable = pd.read_excel('C:/SimulatorFiles/InputTableFile.xlsx', sheet_name='Data')

    # Extract the necessary data
    ectxt = datatable.iloc[1:13, 0].values  # Adjusted index
    ecdata = datatable.iloc[1:13, 1:3].values  # Adjusted index
    encom = (ecdata[:, 0] / ecdata[:, 1]) * 10  # Compute encom values

    # Calculate trendline coefficients
    coefficients = np.polyfit(ecdata[:, 0], encom, 1)
    xFit = np.linspace(min(ecdata[:, 0]), max(ecdata[:, 0]), 100)
    yFit = np.polyval(coefficients, xFit)

    # Create a figure object
    fig = go.Figure()

    # Scatter plot for encom data
    fig.add_trace(go.Scatter(
        x=ecdata[:, 0], 
        y=encom, 
        mode='markers', 
        name='Energy Consumption',
        marker=dict(size=4, symbol='circle', color='rgb(0, 0, 255)')
    ))

    # Add text labels to each point
    for i, txt in enumerate(ectxt):
        fig.add_annotation(x=ecdata[i, 0], y=encom[i], text=txt, font=dict(size=10,color='white'),showarrow=False)

    # Plot the simulated model point
    # btt_charge = app.btt['charge']  # Assuming 'app.btt.charge' is stored here
    # dp_bttcon = app.dp['bttcon']  # Assuming 'app.dp.bttcon' is stored here

    fig.add_trace(go.Scatter(
        x=[btt['charge']], 
        y=[dp.bttcon], 
        mode='markers', 
        name='Simulated model', 
        marker=dict(color='red', symbol='triangle-up', size=12)
    ))

    fig.add_annotation(x=btt['charge'], y=dp.bttcon, text='Simulated model', font=dict(size=10,color='white'),showarrow=False)

    # Add the trendline
    fig.add_trace(go.Scatter(
        x=xFit, 
        y=yFit, 
        mode='lines', 
        name='Trendline', 
        line=dict(color='green', dash='dash', width=2)
    ))

    # Update layout to match the styling
    fig.update_layout(
        title='Energy Consumption (kwh/10km) Vs Battery Capacity',
        title_font=dict(size=15, color='white'),
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title='Battery Capacity', color='white', showgrid=False, showline=False),
        yaxis=dict(title='Energy Consumption (kwh/10km)', color='white', showgrid=False, showline=False),
        xaxis_tickfont=dict(color="white"),
        yaxis_tickfont=dict(color="white"),
        showlegend=False,
        # height=400
    )
    if condition_value == '2':
        fig.update_layout(showlegend=True, height=800,legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)  

    # Return the figure
    return fig
def CLTCButtonPushed(condition_value='None'):
 
    # BTTchargeEditField = 80  # Placeholder value
    # CruisingDistance = 365.4  # Placeholder value
 
    # Read data from an Excel file
    cltctable = pd.read_excel("InputTableFile.xlsx", sheet_name="CLTC")
   
 
    cwtxt = cltctable.iloc[:, 2].values
    cltcdata = cltctable.iloc[3:, 5:8].values
    cltcdata = cltcdata.astype(float)
    cltccom = cltcdata[:, 2] / 10
 
    # Create a figure object
    fig = go.Figure()
 
    # Plot cltccom data
    fig.add_trace(go.Scatter(x=cltcdata[:, 0], y=cltccom, mode='markers', name='CLTCCOM', marker=dict(color='rgb(52, 196, 235)', symbol='circle', size=10)))
 
    # Add text labels for each point
    for i, txt in enumerate(cltctable.iloc[3:, 2]):
        fig.add_annotation(x=cltcdata[i, 0], y=cltccom[i], text=txt, showarrow=False, font=dict(size=10,color='white'))
 
    # Calculate charge
    # CruisingDistanceEditField =481.16062584
    charge = (btt['charge']/ (dp.crusdist / 81)) / 10
    print('bttchragae',btt['charge'])
    print('dp.crusdist',dp.crusdist)
    print("charge",charge);
    # Plot charge
    fig.add_trace(go.Scatter(x=[btt['charge']], y=[charge], mode='markers', name='Charge', marker=dict(color='red', symbol='triangle-up', size=12)))
    fig.add_annotation(x=btt['charge'], y=charge, text='Simulated model', showarrow=False,font=dict(size=10,color='white'))
 
    # Add a trendline
    z = np.polyfit(cltcdata[:, 0], cltccom, 1)
    trendline_x = np.linspace(min(cltcdata[:, 0]), max(cltcdata[:, 0]), 100)
    trendline_y = np.polyval(z, trendline_x)
    fig.add_trace(go.Scatter(x=trendline_x, y=trendline_y, mode='lines', name='Trendline', line=dict(color='green', dash='dash', width=2)))
 
    # Set axis labels and title
    fig.update_layout(
        xaxis_title='Battery Capacity',
        yaxis_title='CLTC Energy Consumption (kwh/10km)',
        title='CLTC Energy Consumption (kwh/10km) Vs Battery Capacity',
    )
 
 
    fig.update_layout(
                    # title="Crusing Distance (km) and BTT (kwh/10km) by Ld/Lq",
                    title_font={'size': 15,'color': 'white'},
                    paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title_font=dict(size=9), showline=False, showgrid=False,zeroline=False),
                    yaxis=dict(title_font=dict(size=9),title='Tn/Pw',showline=False, showgrid=False,zeroline=False,),
                    # yaxis2=dict(showline=False, showgrid=False,zeroline=False,side='right'),
                    showlegend=False,
                    autosize=True,   # Set plot background color to transparent
                    yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
                    xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
                    yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
                    xaxis_title_font=dict(color="white"),
    height=400
 
    )
    if condition_value == '2':
        fig.update_layout(showlegend=True, height=800,legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)  
    # Show the plot
    return fig
#cruising
 
 
def data_tabg3(condition_value='None'):
    # Read data from an Excel file
    cltctable = pd.read_excel("InputTableFile.xlsx", sheet_name="CLTC")
    crustable = pd.read_excel("InputTableFile.xlsx", sheet_name="CruisingGraphs")
 
    # Extract and process cltcdata
    cltcdata = cltctable.iloc[3:, 5:8].values
    cltcdata = cltcdata.astype(float)  # Convert the data to numeric types
 
    # Calculate wltccom
    wltccom = (cltcdata[:, 0] / (cltcdata[:, 1] * 0.81)) * 10
 
    # Fit a polynomial
    coefficients = np.polyfit(cltcdata[:, 0], wltccom, 1)
    xFit = np.linspace(min(cltcdata[:, 0]), max(cltcdata[:, 0]), 100)
    yFit = np.polyval(coefficients, xFit)
 
    # Extract cruising data
    crusdata = crustable.iloc[3:9, 8].values
    crusdata = crusdata.astype(float)  # Convert the data to numeric types
    crustxt = ["Sim-#1", "Sim-#2", "Sim-#3", "Sim-#4", "Sim-#5", "Sim-#6"]
 
    # Repeat the battery charge value for plotting
    xax = np.repeat(80, 6)
 
    # Create a figure object
    fig = go.Figure()
 
    # Plot wltccom data
    fig.add_trace(go.Scatter(x=cltcdata[:, 0], y=wltccom, mode='markers', name='WLTC Energy Consumption (kwh/10km)', marker=dict(color='rgb(52, 196, 235)', symbol='circle', size=10)))
 
    # Add text labels for each point
    cwtxt = cltctable.iloc[3:, 2].values
    for i, txt in enumerate(cwtxt):
        fig.add_annotation(x=cltcdata[i, 0], y=wltccom[i], text=txt, showarrow=False, font=dict(size=10,color='white'))
 
    # Plot simulated model data
    fig.add_trace(go.Scatter(x=xax, y=crusdata, mode='markers', name='Simulated Model', marker=dict(color='red', symbol='triangle-up', size=12)))
 
    # Add text labels for simulated model points
    for i, txt in enumerate(crustxt):
        fig.add_annotation(x=xax[i], y=crusdata[i], text=txt, showarrow=False, font=dict(size=10,color='white'))
 
    # Plot the trendline
    fig.add_trace(go.Scatter(x=xFit, y=yFit, mode='lines', name='Trendline', line=dict(color='green', dash='dash', width=2)))
 
    # Set axis labels and title
    fig.update_layout(
        xaxis_title='Battery Capacity',
        yaxis_title='WLTC Energy Consumption (kwh/10km)',
        title='WLTC Energy Consumption (kwh/10km) Vs Battery Capacity',
    )
   
    fig.update_layout(
                    # title="Crusing Distance (km) and BTT (kwh/10km) by Ld/Lq",
                    title_font={'size': 15,'color': 'white'},
                    paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(title_font=dict(size=9), showline=False, showgrid=False,zeroline=False),
                    yaxis=dict(title_font=dict(size=9), showline=False, showgrid=False,zeroline=False,),
                    #yaxis2=dict(showline=False, showgrid=False,zeroline=False,side='right'),
                    showlegend=False,
                    autosize=True,   # Set plot background color to transparent
                    yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
                    xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
                    yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
                    xaxis_title_font=dict(color="white"),
 
    height=400
    )
    if condition_value == '2':
        fig.update_layout(showlegend=True, height=800,legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)
    # Show the plot
    return fig
 
def BatteryderatingseriesButtonPushed(condition_value='None'):
    datatable = pd.read_excel("InputTableFile.xlsx", sheet_name="Data")
    ecdata = datatable.iloc[1:14, 1:3].values
    encom = (ecdata[:, 0] / ecdata[:, 1]) * 10
    cpdata = datatable.iloc[1:5, 4:9].values
    x = ['Data1', 'Data2', 'Data3', 'Data4']  # x values for the bars
    gap_width = 0.225
    cpdata = cpdata.T
 
    fig = go.Figure()
 
    for i in range(4):
        offset = i * gap_width
        fig.add_trace(go.Bar(x=[j + offset for j in range(1, 5)], y=cpdata[i], name=f'Data{i+1}'))
 
    fig.add_trace(go.Scatter(x=[j + (2.5 * gap_width) for j in range(1, 5)], y=cpdata[4], mode='lines+markers', yaxis='y2'))
 
    fig.update_layout(barmode='group', title='Batt Derating Senarios', xaxis_title='Data', yaxis_title='kW',
                      xaxis=dict(tickfont=dict(color='rgb(11, 7, 44)', size=6), tickvals=[j + (1.5 * gap_width) for j in range(4)], ticktext=x),
                      yaxis=dict(tickfont=dict(color='rgb(11, 7, 44)', size=6)),
                      yaxis2=dict(overlaying='y', side='right', tickfont=dict(color='rgb(11, 7, 44)', size=6), range=[1, 25]))
    fig.update_layout(
        title_font={'size': 15,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showline=False, showgrid=False,zeroline=False ),
        yaxis=dict(showline=False, showgrid=False, zeroline=False),
        yaxis2=dict(showline=False, showgrid=False, zeroline=False),
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False,
        height=400
    )
 
    if condition_value == '2':
        fig.update_layout(showlegend=True,height=800, legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)
 
    return fig
 
def MotorSpecificationsButtonPushed(condition_value='None'):
    datatable = pd.read_excel("InputTableFile.xlsx", sheet_name="Data")
    msdata = datatable.iloc[6:10, 4:8].values
    x = [5, 10, 20, 40]  # x values for the bars
    fig = go.Figure()
    gap_width = 0.8
    for i in range(2):
        for j in range(4):
            offset = i * gap_width
            fig.add_trace(go.Bar(x=[x[j]+offset], y=[msdata[i][j]], width=0.6, name=f'Tn/Pw {x[j]}'))
 
    fig.update_layout(yaxis2=dict(title='Right Y-Axis Label', range=[0, 1], overlaying='y', side='right'))
    fig.add_trace(go.Scatter(x=x, y=msdata[2], mode='lines+markers', name='Line 1', yaxis='y2', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=x, y=msdata[3], mode='lines+markers', name='Line 2', yaxis='y2', line=dict(color='yellow')))
 
    fig.update_layout(
        title='Motor Specifications',
        xaxis=dict(tickmode='array', tickvals=[5, 10, 20, 40]),
        yaxis=dict(title='Tn/Pw', range=[0, 500]),  
    )
   
    fig.update_layout(
        title_font={'size': 15,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showline=False, showgrid=False,zeroline=False ),
        yaxis=dict(showline=False, showgrid=False, zeroline=False),
        yaxis2=dict(showline=False, showgrid=False, zeroline=False),
        autosize=True,
        yaxis_title_font=dict(color="white"),  
        xaxis_tickfont=dict(color="white"),    
        yaxis_tickfont=dict(color="white"),    
        xaxis_title_font=dict(color="white"),
        showlegend=False,
        height = 400
    )
       
 
    if condition_value == '2':
        fig.update_layout(showlegend=True,height=800,legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)
 
    return fig
 
 
 
 
def kWLeafButtonPushed(condition_value='None'):
    datatable = pd.read_excel("InputTableFile.xlsx", sheet_name="Data", header=None)
    # Extract and process data
    mldata = datatable.iloc[2:13, 10:12].values
    mlrpm = mldata[:, 0]
 
    # cPfric = 3  # Define cPfric
    mloss = 0.000001 * mot['cPfric'] * (mlrpm**2) - 0.0003 * mlrpm + 1.4471
    nis = mldata[:, 1]
 
    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mlrpm, y=mloss, mode='lines+markers', name='Mloss', marker=dict(size=2), line=dict(color='red')))
    fig.add_trace(go.Scatter(x=mlrpm, y=nis, mode='lines+markers', name='NIS', marker=dict(size=2), line=dict(color='blue')))
 
    # Update layout
    fig.update_layout(xaxis_title='ML RPM', yaxis_title='Loss and NIS', title='80 kW Leef',
                      xaxis=dict(tickfont=dict(color='rgb(11, 7, 44)', size=6)),
                      yaxis=dict(tickfont=dict(color='rgb(11, 7, 44)', size=6)))
   
    fig.update_layout(
        title_font={'size': 15,'color': 'white'},
        paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showline=False, showgrid=False,zeroline=False ),
        yaxis=dict(showline=False, showgrid=False, zeroline=False),
        autosize=True,   # Set plot background color to transparent
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        showlegend=False,
        height=400
        #legend=dict(x=1.03, y=0.3, orientation='v' , font=dict(color='white')),
    )
   
    if condition_value == '2':
        fig.update_layout(showlegend=True,height=800, legend=dict(x=1.00, y=0.3, orientation='v' , font=dict(color='white')),)
    else:
        fig.update_layout(showlegend=False)
 
    return fig




files_motor = get_files_in_directory(DIRECTORIES['motor'])
rows = create_table_rows(files_motor,'motor')
body_motor = dmc.TableTbody(rows)

#inverter
files_inverter = get_files_in_directory(DIRECTORIES['inverter'])
rows = create_table_rows(files_inverter,'inverter')
body_inverter = dmc.TableTbody(rows)

#battery
files_battery = get_files_in_directory(DIRECTORIES['battery'])
rows = create_table_rows(files_battery,'battery')
body_battery = dmc.TableTbody(rows)

#gear
files_gear = get_files_in_directory(DIRECTORIES['gear'])
rows = create_table_rows(files_gear,'gear')
body_gear = dmc.TableTbody(rows)

#tire
files_tire = get_files_in_directory(DIRECTORIES['tire'])
rows = create_table_rows(files_tire,'tire')
body_tire = dmc.TableTbody(rows)

#body
files_vehicle = get_files_in_directory(DIRECTORIES['vehicle'])
rows = create_table_rows(files_vehicle,'vehicle')
body_vehicle = dmc.TableTbody(rows)

# Define Motor Parameters
motor_parameters = [
    {"parameter": "Pole", "value": 8},
    {"parameter": "Resistance(Ω)", "value": 0.0125},
    {"parameter": "Voltage(V)", "value": 350},
    {"parameter": "Current (A)", "value": 680},
    {"parameter": "Coefficient of Iron Loss", "value": 0.2400},
    {"parameter": "Coefficient of Stray Loss ( x 1.E-09 )", "value": 0.6000},
    {"parameter": "Coefficient of Friction Loss", "value": 3},
    {"parameter": "Coefficient of Windage loss", "value": 2},
    {"parameter": "Switching frequency (Hz)", "value": 6500},
    {"parameter": "DC-link Voltage (V)", "value": 350},
    {"parameter": "Dc-link Current (A)", "value": 480},
]

motor_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'motor-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(motor_parameters)
]

motor_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
motor_body = dmc.TableTbody(motor_rows)

motor_table = dmc.Table(
    [motor_head, motor_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_motor_contents = dmc.Flex([
    motor_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-motor-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")



#inverter
# Define Motor Parameters

inverter_parameters = [
    {"parameter": "tr (us)", "value": 0.09},
    {"parameter": "tf (us)", "value": 0.15},
    {"parameter": "ton (us)", "value": 125},
    {"parameter": "von", "value": 0.7},
    {"parameter": "trr (us)", "value": 0.06},
]

inverter_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'inverter-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(inverter_parameters)
]

inverter_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
inverter_body = dmc.TableTbody(inverter_rows)

inverter_table = dmc.Table(
    [inverter_head, inverter_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_inverter_contents = dmc.Flex([
    inverter_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="inv-file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-inverter-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")

#inverter

#battery

battery_parameters = [
    {"parameter": "Battery charge (kWH)", "value": 80},
    {"parameter": "Regeneration ratio (for ωr*T)", "value": 1},
    {"parameter": "Regeneration limit (km/h)", "value": 16},
]

battery_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'battery-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(battery_parameters)
]

battery_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
battery_body = dmc.TableTbody(battery_rows)

battery_table = dmc.Table(
    [battery_head, battery_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_battery_contents = dmc.Flex([
    battery_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="btt-file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-battery-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")

#battery
#gear
gear_parameters = [
    {"parameter": "Gear ratio", "value": 10},
    {"parameter": "Shaft diameter (m)", "value": 0.05},
]

gear_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'gear-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(gear_parameters)
]

gear_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
gear_body = dmc.TableTbody(gear_rows)

gear_table = dmc.Table(
    [gear_head, gear_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_gear_contents = dmc.Flex([
    gear_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="gear-file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-gear-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")

#gear


#tire
tire_parameters = [
    {"parameter": "Tire Outer diameter (inch)", "value": 30},
    {"parameter": "Weight of a tire (kg)", "value": 10},
]

tire_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'tire-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(tire_parameters)
]

tire_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
tire_body = dmc.TableTbody(tire_rows)

tire_table = dmc.Table(
    [tire_head, tire_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_tire_contents = dmc.Flex([
    tire_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="tire-file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-tire-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")

#tire

'Curb Weight (kg)', 'Luggage weight (kg)', 'Passenger weight (kg)', 'Passenger number', 'Tire number'
#vehicle
vehicle_parameters = [
    {"parameter": "Curb Weight (kg)", "value": 1000},
    {"parameter": "Luggage weight (kg)", "value": 100},
    {"parameter": "Passenger weight (kg)", "value": 70},
    {"parameter": "Passenger number", "value": 4},
    {"parameter": "Tire number", "value": 4},
]

vehicle_rows = [
    dmc.TableTr(
        [
            dmc.TableTd(parameter["parameter"]),
            dmc.TableTd(
                dmc.NumberInput(
                    value=parameter["value"],
                    type="number",
                    id={'type': 'vehicle-save-value', 'index': idx},
                    size="xs"
                )
            ),
        ]
    )
    for idx, parameter in enumerate(vehicle_parameters)
]

vehicle_head = dmc.TableThead(
    dmc.TableTr(
        [
            dmc.TableTh("Parameter"),
            dmc.TableTh("Value"),
        ]
    )
)
vehicle_body = dmc.TableTbody(vehicle_rows)

vehicle_table = dmc.Table(
    [vehicle_head, vehicle_body],
    striped=True,
    highlightOnHover=True,
    withTableBorder=True,
    withColumnBorders=True,
)

add_vehicle_contents = dmc.Flex([
    vehicle_table,
    dmc.Divider(variant="solid", mt=10),
    dmc.Paper(
        children=[
            dmc.Flex([
                dmc.TextInput(label="Enter the File Name", id="vehicle-file-name-input", style={"flex": 1}, me=5),
                dmc.Button("Save File", id="save-vehicle-file", style={"flex": 1}, mt=25)
            ], direction="row"),
        ],
        shadow="xs",
        mt=10, p=10
    )
], direction="column")
#vehicle


#cards
# Theme toggle button
theme_toggle = dmc.ActionIcon(
    [
        # dmc.Paper(DashIconify(icon="radix-icons:sun", width=25), darkHidden=True),
        dmc.Paper(DashIconify(icon="openmoji:home-button", width=25), lightHidden=True),
    ],
    variant="transparent",
    color="yellow",
    id="home-btn",
    size="lg",
)

# Function to load IPM Modelling content
def load_ipm_modelling():
    return ipm_tab

#help modal

Introduction_contents = [
    dmc.Flex([
        html.Iframe(
            src='/assets/GUI.pdf',
            style={'width': '100%', 'height': 'calc(100vh - 100px)','border': 'none'}
        )
    ],style={"flex": 1, "height": "100%"},direction="column",mt=10)
 
]
User_Manual = [
    dmc.Flex([
        html.Iframe(
            src='/assets/web_v6.0_manual.pdf',
            style={'width': '100%', 'height': 'calc(100vh - 100px)','border': 'none'}
        )
    ],style={"flex": 1, "height": "100%"},direction="column",mt=10)
 
]
data = ["xEV Document", "User Manual"]
help_modal = dmc.Modal(children=[
            dmc.Center(dmc.SegmentedControl(data=data, radius=20, id="segment-control", value="xEV Document")),
            html.Div(id="modal-content")  # Placeholder for content
],id="help-modal", fullScreen=True,)

#help button

help_button = dmc.Button(
    children = ["Help"], 
    variant="outline", 
    id="help-button", 
    style={
        "position": "fixed", 
        "right": "15px", 
        "top": "10px"
    }
)


# Headers


header = dmc.Flex(
    [
        dmc.Group(
            [
                dmc.Burger(id="burger-button", opened=False, hiddenFrom="md"),
                dmc.Text("Home Page", size="xl", fw=700),
                theme_toggle,
            ],
            align="center",
            style={"flex": 1, "justify-content": "center"}
        ),
        # help_button,
        # help_modal
    ],
    justify="space-between",
    align="center",
    style={"width": "100%"}
)
# Simulator_Button=dmc.Button(
#             "xEV Simulator",id="simulator_page", variant="outline", n_clicks=0,
#             color="black",
#             # fullWidth=True,
#             mt="md",
#             radius="md",
            
#         )

header_evm = dmc.Flex(
    [
        dmc.Group(
            [
                dmc.Burger(id="burger-button-evm", opened=False, hiddenFrom="md"),
                dmc.Text("xEV Simulator", size="xl", fw=700),
                theme_toggle,
                dmc.Button(
            "xEV Simulator",id="simulator_page", variant="subtle", n_clicks=0,
            # color="black",
            # fullWidth=True,
            mt="md",
            radius="md",
            darkHidden=True,
            
        ),
            ],
            align="center",
            style={"flex": 1, "justify-content": "center"}
        ),
        
        help_button,
        help_modal
    ],
    justify="space-between",
    align="center",
    style={"width": "100%"}
)


header_genDes = dmc.Flex(
    [
        dmc.Group(
            [
                dmc.Burger(id="burger-button-evm", opened=False, hiddenFrom="md"),
                dmc.Text("Generative Design", size="xl", fw=700),
                theme_toggle,
            ],
            align="center",
            style={"flex": 1, "justify-content": "center"}
        ),
        help_button,
        help_modal
    ],
    justify="space-between",
    align="center",
    style={"width": "100%"}
)

 

Introduction_contents = [
    dmc.Flex([
        html.Iframe(
            src='/assets/GUI.pdf',
            style={'width': '100%', 'height': 'calc(100vh - 100px)','border': 'none'}
        )
    ],style={"flex": 1, "height": "100%"},direction="column",mt=10)
 
]
# Create options for the dropdown
dropdown_options = [{'label': str(i), 'value': str(i)} for i in range(1, 7)]

# Create labels 

dig_Twin0=  html.Tr([
            html.Td("",colSpan=3),
            html.Td("Adjust",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8439a3"}),
            html.Td("0",id="AdjLdEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8439a3"}),
            html.Td("0",id="AdjLqEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8439a3"}),
            html.Td("0",id="AdjPMEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8439a3"}),
            html.Td("",colSpan=7),
           ])
 
dig_Twin1=html.Tr([html.Td("Select Digital Twin No(1-6)",colSpan=9, style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"green"}),  
                  #dcc.Input( type="number", value=0.004,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"}
                html.Td("D-T", style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"blue"}),
                html.Td("D-T",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"blue"}),
                html.Td("Speed Macro",rowSpan=2, style={"color":"black","textAlign": "center", "borderRadius": "5px","backgroundColor":"white"}),
                html.Td("Digital Twin range by A12 speed",colSpan=2, style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"green"}),
               
 
                ],style={"marginTop":"5px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")
 
dig_Twin2= html.Tr([
     html.Td(dcc.Dropdown( id='DTnumDropDown',options=[{'label': '1', 'value': '0'},{'label': '2', 'value': '1'},{'label': '3', 'value': '2'},{'label': '4', 'value': '3'}, {'label': '5', 'value': '4'},  {'label': '6', 'value': '5'} ],value='2', style={'backgroundColor': 'green',"borderRadius": "5px",}),style={"color":"black",'backgroundColor': 'grren',"borderRadius": "5px"}),
        html.Td("D.T",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#308c84"}),
        html.Td("A:Ψdmax",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("B:Ψdmax",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("Ld",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("Lq",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("Ψmd",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("Ψmq",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("a",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#184c6c"}),
        html.Td("STD(Nm)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#0874bc"}),
        # html.Td("if=-Ψm/Ld",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"#0874bc"}),
        # html.Td("ξ=Lq/Ld",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"green"}),
        # html.Td("A＝if/2",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"green"}),
        # html.Td("B=if/2sqrt(ξ",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"green"}),
        html.Td("STD(rpm)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"green"}),
        # html.Td("Speed Macro",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"green"}),
        html.Td("Min",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#d1d100"}),
        html.Td("Max",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#d1d100"}),
    ])
 
dig_Twin3=html.Tr([
    html.Td("1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("ax/√(1+(ax)^2)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c", "fontSize": "13px"}),
    html.Td("0.137",id="dtA1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"},contentEditable="true"),
    html.Td("0.211",id="dtB1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("222",id="dtLd1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("323",id="dtLq1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.085",id="pmd1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="pmq1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("1.28",id="dta1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"},contentEditable="true"),
    html.Td("0",id="stdNm1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="dtif1",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="dtE1",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="Aif1",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="Bif1",style={"color":"white","textAlign": "center", "borderRadius": "2px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="stdrpm1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("806.2",id="speed1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="Min1EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max1EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
 
dig_Twin4 = html.Tr([
    html.Td("2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c",}),
    html.Td("tanh(ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c", "fontSize": "13px"}),
    html.Td("0.117",id="dtA2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.182",id="dtB2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("230",id="dtLd2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("333",id="dtLq2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.092",id="pmd2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="pmq2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("1.18",id="dta2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="stdNm2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="dtif2",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="dtE2",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Aif2",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Bif2",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    html.Td("0",id="stdrpm2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("804.7",id="speed2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="Min2EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max2EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
 
 
dig_Twin5 = html.Tr([
    html.Td("3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("A12-Vm/ω  ax/sqrt(1+(ax)^2)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689", "fontSize": "12px"}),
    html.Td("0",id="dtA3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="dtB3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="dtLd3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="dtLq3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="pmd3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="pmq3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("1",id="dta3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="stdNm3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    # html.Td("0",id="dtif3",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="dtE3",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Aif3",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Bif3",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    html.Td("0",id="stdrpm3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("796.9",id="speed3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b1a689"}),
    html.Td("0",id="Min3EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max3EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
 
 
dig_Twin6= html.Tr([
    html.Td("4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("arctan(ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c", "fontSize": "13px"}),
    html.Td("0.106",id="dtA4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.161",id="dtB4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("276",id="dtLd4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("403",id="dtLq4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.1034",id="pmd4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="pmq4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("1.06",id="dta4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="stdNm4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="dtif4",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="dtE4",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Aif4",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Bif4",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    html.Td("0",id="stdrpm4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("816",id="speed4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="Min4EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max4EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
dig_Twin7 = html.Tr([
    html.Td("5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("1-exp(-ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c", "fontSize": "13px"}),
    html.Td("0.151",id="dtA5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.225",id="dtB5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("250",id="dtLd5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("366",id="dtLq5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0.0907",id="pmd5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="pmq5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("1.39",id="dta5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="stdNm5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="dtif5",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="dtE5",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Aif5",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Bif5",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    html.Td("0",id="stdrpm5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("836.3",id="speed5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("0",id="Min5EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max5EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
 
 
dig_Twin8 = html.Tr([
    html.Td("6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("A12-Vm/ω  ax/sqrt(1+(ax)^2)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092", "fontSize": "12px"}),
    html.Td("0.141",id="dtA6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("0.229",id="dtB6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("213",id="dtLd6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("311.2",id="dtLq6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("0.07296",id="pmd6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("0",id="pmq6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("1.41",id="dta6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("0",id="stdNm6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    # html.Td("0",id="dtif6",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="dtE6",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Aif6",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("0",id="Bif6",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    html.Td("0",id="stdrpm6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("807.3",id="speed6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a3b092"}),
    html.Td("0",id="Min6EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("0",id="Max6EditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"})
])
dig_Twin9=html.Tr([
    html.Td("",colSpan=14),
])
dig_Twin10= html.Tr([
    html.Td(""),
    html.Td("1:LINEAR 2:POLYNOMIAL",style={"color":"white","textAlign": "center", "borderRadius": "5px", "fontSize": "14px"}),
    html.Td(dcc.Dropdown( id='Hdcalfunc',options=[{'label': '1', 'value': '1'},{'label': '2', 'value': '2'},],value='1', style={'backgroundColor': 'white',"borderRadius": "5px",}),style={"color":"black", "borderRadius": "5px"}),
    html.Td(dcc.Dropdown( id='Hqcalfunc',options=[{'label': '1', 'value': '1'},{'label': '2', 'value': '2'},],value='1', style={'backgroundColor': 'white',"borderRadius": "5px",}  ),style={"color":"black", "borderRadius": "5px"}),
    html.Td("",colSpan=10 ),
    # html.Td(""),html.Td("")
])
dig_Twin11 = html.Tr([
    html.Td("1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("ax/√(1+(ax)^2)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1", "fontSize": "13px"}),
    html.Td(""),
    html.Td(""),
    html.Td("0",id="ldopt1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("87",id="lqopt1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("18",id="pmdopt1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td(" ",colSpan=5),
    # html.Td("0",id="Eopt1",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td(" ",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    html.Td("Mode: 0=Off, 1=On, 2=idiq",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319", "fontSize": "12px"}),
    html.Td(dcc.Dropdown( id='ModeDropDown',options=[{'label': '0', 'value': '0'},{'label': '1', 'value': '1'},{'label': '2', 'value': '2'}],value='0',style={"backgroundColor":"#b3b319"}),style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    #html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
 
dig_Twin12= html.Tr([
    html.Td("2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("tanh(ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1", "fontSize": "13px"}),
    html.Td(""),
    html.Td(""),
    html.Td("0",id="ldopt2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("88",id="lqopt2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("13",id="pmdopt2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td(" "),
    html.Td("Constant Ψ,Ld,Lq",colSpan=2,style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#0874bc"}),
    html.Td(dcc.Dropdown( id='ConstantLdLqDropDown',
            options=[{'label': '0', 'value': '0'},
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                    {'label': '3', 'value': '3'}],value='0' ,style={'backgroundColor': '#a6b493',"borderRadius": "5px", 'color': 'black'}),style={'backgroundColor': '#a6b493', "borderRadius": "5px",'color': 'black'}),
    # html.Td("0",id="Eopt2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a6b493"}),
    html.Td(""),
    html.Td("Low",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("6800",id="DTlowEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    # html.Td("Mode:0=off, 1=On, 2=idiq ",colSpan=2,style={"textAlign": "center",'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("13",id="Eopt2",style={'backgroundColor': '#b1a58a', 'color': 'black'}),html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
 
dig_Twin13 = html.Tr([
    html.Td("3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("ax√(1+ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1", "fontSize": "13px"}),
    html.Td("" ),
    html.Td("" ),
    html.Td("0",id="ldopt3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("102",id="lqopt3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("0",id="pmdopt3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td(" " ),
    html.Td("Type 0:Id=0,1:AVR,2:MAX",colSpan=2,style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#0874bc"}),
    html.Td(dcc.Dropdown( id='TypeDropDown',options=[{'label': '0', 'value': '0'},
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},],value='2',style={'backgroundColor': '#a6b493', "borderRadius": "5px",'color': 'black'}  # Default value
                ),style={"color":"white","borderRadius": "5px","backgroundColor":"#a6b493"}),
    # html.Td("0",id="Eopt3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a6b493"}),
    html.Td(" " ),
    html.Td("High",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("15000",id="DThighEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    # html.Td("3D ",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("0",id="Eopt3",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
dig_Twin14 = html.Tr([
    html.Td("4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("arctan(ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1", "fontSize": "13px"}),
    html.Td(""),
    html.Td("" ),
    html.Td("0",id="ldopt4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("100",id="lqopt4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td("20",id="pmdopt4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#8233a1"}),
    html.Td(" " ),
    html.Td("Tn:1=DQ,2=xEV",colSpan=2,style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#0874bc"}),
    html.Td(dcc.Dropdown( id='TnflagDropDown',options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                ],
                value='1',style={'backgroundColor': '#a6b493',"borderRadius": "5px", 'color': 'black'}  # Default value
            ),style={"color":"white","borderRadius": "5px","backgroundColor":"#a6b493"}),
    # html.Td("0",id="Eopt4",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a6b493"}),
    html.Td(" " ),
    html.Td("Vm",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("350",id="VmEditField",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    # html.Td("10 ",id="achoice",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td("20",id="Eopt4",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
dig_Twin15= html.Tr([
    html.Td("5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("1-exp(-ax)",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1", "fontSize": "13px"}),
    html.Td(""),
    html.Td(""),
    html.Td("0",id="ldopt5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("90",id="lqopt5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td("11",id="pmdopt5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#3382a1"}),
    html.Td(" "),
    html.Td("Pe",colSpan=2,style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#0874bc"}),
    html.Td(dcc.Dropdown( id='PeflagDropDown',options=[
                    {'label': '1', 'value': '1'},
                    {'label': '2', 'value': '2'},
                ],value='1',style={'backgroundColor': '#a6b493', 'color': 'black',"borderRadius": "5px",}  # Default value
            ),style={'backgroundColor': '#a6b493', 'color': 'black',"borderRadius": "5px",}),
    # html.Td("0",id="Eopt5",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a6b493"}),
    html.Td(" "),
    html.Td("3D",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    html.Td("10",id="achoice",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    # html.Td(" 1",id="DEditField_2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b87c7c"}),
    # html.Td("11",id="Eopt5",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
 
dig_Twin16= html.Tr([
    html.Td("6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#5e9c64"}),
    html.Td("A12",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#5e9c64", "fontSize": "13px"}),
    html.Td("" ),
    html.Td("" ),
    html.Td("0",id="ldopt6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#5e9c64"}),
    html.Td("76",id="lqopt6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#5e9c64"}),
    html.Td("0",id="pmdopt6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#5e9c64"}),
    html.Td(" " ),
    html.Td("PsiPm",colSpan=2,style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#ccc6c6"}),
    html.Td(dmc.Switch(size="lg",radius="lg",checked=True,    onLabel="ON",offLabel="OFF",id="psi_pmswitch")),
    # html.Td("0",id="Eopt6",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#a6b493"}),#psipsm toggle
    html.Td(""),
    html.Td(" "),
    html.Td("1",id="DEditField_2",style={"color":"white","textAlign": "center", "borderRadius": "5px","backgroundColor":"#b3b319"}),
    # html.Td(" ",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # #html.Td("0",id="Eopt6",style={'backgroundColor': '#b1a58a', 'color': 'black'}),
    # html.Td(" "),html.Td(""),html.Td(" "),html.Td(" ")
])
 
 
 
digTwin_body=[html.Tbody([dig_Twin0,dig_Twin1,dig_Twin2,dig_Twin3,dig_Twin4,dig_Twin5,dig_Twin6,dig_Twin7,dig_Twin8,dig_Twin9,dig_Twin10,dig_Twin11,dig_Twin12,dig_Twin13,dig_Twin14,dig_Twin15,dig_Twin16],
            style={"marginTop":"5px"}
            )]
 
digitalTwin_fields = [
    dbc.Table(digTwin_body , bordered=True,
    hover=True,
    responsive=True,
    # striped=True,
  style={"width": "100%","tableLayout": "fixed"}#"height":"calc(100vh - 100px)",
),
]
#digital twin ui end
# Additional Tabs
# additional_tabs = [
#     dmc.TabsTab("IPM Modelling", value="IPM Modelling"),
#     dmc.TabsTab("Drive Pattern", value="Drive Pattern"),
#     dmc.TabsTab("Ploss Analysis1", value="Ploss Analysis1"),
#     dmc.TabsTab("Ploss Analysis2", value="Ploss Analysis2"),
#     dmc.TabsTab("Data", value="Data"),
# ]

input_contents = [
    dmc.Flex([
        dmc.Flex([
            # dmc.MantineProvider(
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Motor", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/evmotor.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="motor-table",
                                    children=[body_motor],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                            dmc.Table(
                                [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='file-content')],
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                verticalSpacing=2
                            ),h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-motor-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-motor-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='motor-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%", "margin": "10px"}
            ),
            # 2nd card
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Inverter", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/inverter.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="inverter-table",
                                    children=[body_inverter],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='inverter-file-content')],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing=2
                                ),
                            h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-inverter-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-inverter-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='inverter-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%", "margin": "10px"}
            ),
            # 3rd card
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Battery", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/battery.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="battery-table",
                                    children=[body_battery],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                            dmc.Table(
                                [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='battery-file-content')],
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                verticalSpacing=2
                            ),h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-battery-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-battery-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='battery-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%",  "margin": "10px"}
            ),
            # 4th
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Gear", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/gear.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="gear-table",
                                    children=[body_gear],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                            dmc.Table(
                                [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='gear-file-content')],
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                verticalSpacing=2
                            ),h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-gear-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-gear-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='gear-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%", "margin": "10px"}
            ),
            # 5th
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Tire", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/tire.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="tire-table",
                                    children=[body_tire],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                            dmc.Table(
                                [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='tire-file-content')],
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                verticalSpacing=2
                            ),h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-tire-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-tire-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='tire-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%", "margin": "10px"}
            ),
            # 6th card
            dmc.Card(
                children=[
                    dmc.CardSection(
                        dmc.Group(
                            children=[dmc.Text("Vehicle", fw=500)],
                            justify="center",
                        ),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        dmc.Flex([
                            dmc.Image(src="assets/images/body.png", h=150, w=200),
                        ], justify="center", align="center",style={"height": "150px"}),
                        withBorder=True,
                        inheritPadding=True,
                        py="xs",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                                dmc.Table(
                                    id="vehicle-table",
                                    children=[body_vehicle],
                                    striped=True,
                                    highlightOnHover=True,
                                    withTableBorder=True,
                                    withColumnBorders=True,
                                    verticalSpacing="2"
                                ),
                            h=145)
                        
                        ],
                        inheritPadding=True,
                        mt="sm",
                        pb="md",
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.ScrollArea(
                            dmc.Table(
                                [dmc.TableThead(dmc.TableTr([dmc.TableTh("Parameter"), dmc.TableTh("Value")])), html.Tbody(id='vehicle-file-content')],
                                striped=True,
                                highlightOnHover=True,
                                withTableBorder=True,
                                withColumnBorders=True,
                                verticalSpacing=2
                            ),h=200)
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                        # style={"height": "200px"}
                    ),
                    dmc.CardSection(
                        children=[
                            dmc.SimpleGrid(
                                cols=2,
                                spacing="xs",
                                verticalSpacing="md",
                                children=[
                                    dmc.Button("Add", variant="outline", id="add-vehicle-btn"),
                                    dmc.Button("Edit", variant="outline", id="edit-vehicle-btn"),
                                    dmc.Text("Selected Item"),
                                    dmc.TextInput(disabled=True, id='vehicle-selected-file')
                                ]
                            )
                        ],
                        inheritPadding=True,
                        withBorder=True,
                        mt="sm",
                        pb="md",
                    ),
                ],
                withBorder=True,
                shadow="sm",
                radius="md",
                # w=300,
                style={"width": "100%",  "margin": "10px"}
            ),
            # ,defaultColorScheme="light")
            
        ], justify="center", align="center", p=10),
        dmc.Flex([
            dmc.Button("Next",variant="subtle",id="next-button"),
            dmc.Flex([
                dmc.Button("<<<<",variant="subtle",id="dt-button"),
            ],direction="row",align="center",justify="flex-end",ms=100),
            html.Div(id="next-link")
        ],direction="row",mt=10,align="center",justify="center"),
        html.Div([
            dmc.Drawer(
            title="Digital Twin",
            id="dt-drawer",
            padding="xs",
            size="100%",
            children = digitalTwin_fields,
            # style={"flex": "1","position":"relative"}
            ),
            dmc.Modal(title="Add", id="add-motor-modal", size="lg", children=add_motor_contents),
            dmc.Modal(title="Add", id="add-inverter-modal", size="lg", children=add_inverter_contents),
            dmc.Modal(title="Add", id="add-battery-modal", size="lg", children=add_battery_contents),
            dmc.Modal(title="Add", id="add-gear-modal", size="lg", children=add_gear_contents),
            dmc.Modal(title="Add", id="add-tire-modal", size="lg", children=add_tire_contents),
            dmc.Modal(title="Add", id="add-vehicle-modal", size="lg", children=add_vehicle_contents),
            dmc.Modal(title="Edit", id="edit-motor-modal", size="lg"),
            dmc.Modal(title="Edit", id="edit-inverter-modal", size="lg"),
            dmc.Modal(title="Edit", id="edit-battery-modal", size="lg"),
            dmc.Modal(title="Edit", id="edit-gear-modal", size="lg"),
            dmc.Modal(title="Edit", id="edit-tire-modal", size="lg"),
            dmc.Modal(title="Edit", id="edit-vehicle-modal", size="lg"),
            dmc.Modal(
                title="WARNING",
                id="module-error",
                children=[
                    dmc.Flex([
                        dmc.Flex([
                            DashIconify(icon="emojione:warning", style={"height": "50%", "width": "auto"}),
                            dmc.Blockquote(
                                "Select all the modules",
                                color="red",
                                style={"flex": 1, "height": "100%"}
                            ),
                        ], direction="row", align="center", gap="xl", style={"flex": 1, "alignItems": "center", "height": "auto"})
                    ], style={"flex": 1})
                ],
                centered = True,
            ),
        ]),
    ],direction="column")
]



table_head=dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("IPM characteristics"),
                    dmc.TableTh("Value"),
                    dmc.TableTh("Unit"),
                ]))

table_body= dmc.TableTbody(children=[
        dmc.TableTr([
            dmc.Tooltip(
                    label="Specific motor speed at which the control strategy shifts to Maximum Torque Per Volt (MTPV) operation. This value of motor speed is greater than that of Rated speed.",
                    children= dmc.TableTd("MTPV(ωeb)"),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
         
            dmc.TableTd(0,id="tab-mtpvweb"),
            dmc.TableTd(0,id="mtpvweb-unit"),
        ]),
    dmc.TableTr([
        dmc.Tooltip(
                    label="Highest electrical power that the motor can convert into mechanical power.",
                    children=dmc.TableTd("Max Power"),
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
            # dmc.TableTd("Max Power"),
            dmc.TableTd(0,id="tab-maxpower"),
            dmc.TableTd("kW"),
        ]),
    dmc.TableTr([
            dmc.Tooltip(
                label="Highest amount of rotational force that the motor can generate",
                children=dmc.TableTd("Max Torque"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(0,id="tab-maxtorque"),
            dmc.TableTd("Nm"),
        ]),
    dmc.TableTr([
        dmc.Tooltip(
                label="The highest efficiency achievable by the system under optimal operating conditions.",
                children=dmc.TableTd("Max Efficiency %"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(0,id="tab-maxeff"),
            dmc.TableTd("%"),
        ]),  
    dmc.TableTr([          
            dmc.Tooltip(
                label="The maximum efficiency recorded during regenerative braking or energy recovery phase",
                children=dmc.TableTd("Max Positive Efficiency %"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            dmc.TableTd(0,id="tab-maxposeff"),
            dmc.TableTd("%"),
        ])  
])

table_header = [
    html.Thead(html.Tr([html.Th("IGBT/FRD Modeling",colSpan=4,style={"textAlign": "center","backgroundColor":"#0073bd"}),html.Th("日立 800A (150°C)",style={"backgroundColor":"white","color":""})]))
]
row1 = html.Tr([html.Td("Inverter", style={"verticalAlign": "middle","backgroundColor":"#ffbfa3","color":"black","textAlign": "center",}, rowSpan="5"),  html.Td("DC Link",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="dc-link-input", type="number", value=350, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"}), html.Td("V",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="v-input", type="number", value=350,className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")
row2 = html.Tr([html.Td("Irms(A)",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="input-irms", type="number", value=480, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"}), html.Td("P-P(A)",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="input-pp", type="number", value=679,className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row3 = html.Tr([html.Td("SW Frequency",style={"backgroundColor":"white","color":"black"}), html.Td("",style={"backgroundColor":"white"}),  html.Td("Hz",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="input-irms", type="number", value=6500, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row4 = html.Tr([html.Td("Modulation",style={"backgroundColor":"white","textAlign": "center","color":"black"}, colSpan="3"),  html.Td(dcc.Input(id="igbtModEditField", type="number", value=0.8,className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])#"0.8",id = "igbtModEditField"
row5 = html.Tr([html.Td("Power  Factor(PF)",style={"backgroundColor":"white","textAlign": "center","color":"black"}, colSpan="3"),
                html.Td(dcc.Input(id="input-pp", type="number", value=0.9,className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])

row6 = html.Tr([html.Td("IGBT/FWD", style={"verticalAlign": "middle","backgroundColor":"#f0d086","color":"black","textAlign": "center","color":"black"}, rowSpan="3", contentEditable="true"),  html.Td("Therma R",style={"backgroundColor":"white","verticalAlign": "middle"}, rowSpan="3", contentEditable="true"), html.Td("Rth(IGBT)",style={"backgroundColor":"white"}), html.Td("k/W",style={"backgroundColor":"white"}), html.Td(dcc.Input(id="input-irms", type="number", value=0.136, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row7 = html.Tr([  html.Td("Rth(Diode)",style={"backgroundColor":"white","color":"black"}), html.Td("k/W",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="input-irms", type="number", value=0.208, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row8 = html.Tr([ html.Td("Rth(IGBT-Diode)",style={"backgroundColor":"white","color":"black"}), html.Td("k/W",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id="input-irms", type="number", value=0.041, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])

row9 = html.Tr([html.Td("IGBT", style={"verticalAlign": "middle","backgroundColor":"#d9f5bd","color":"black","textAlign": "center"}, rowSpan="12"),  html.Td("Vce(sat)",style={"verticalAlign": "middle","backgroundColor":"white","color":"black"}, rowSpan="2"), html.Td("A1(rc)",style={"backgroundColor":"white","color":"black"}), html.Td("V/A",style={"backgroundColor":"white","color":"black"}), 
                html.Td(dcc.Input(id="A1EditField", type="number", value=0.0012, className="rounded-input",style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])#"0.0012",id='A1EditField'
row10 = html.Tr([ html.Td("A0(Vce0)",style={"backgroundColor":"white","color":"black"}), html.Td("V",style={"backgroundColor":"white","color":"black"}),html.Td(dcc.Input(id='A0EditField', type='number', value=0.8965, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])

row11 = html.Tr([ html.Td("Eon=C3*I^3+C2*I^2+C1*I+C0",style={"verticalAlign": "middle","backgroundColor":"white","color":"black"}, rowSpan="5",colSpan="2"), html.Td("C3",style={"backgroundColor":"white","color":"black"}),html.Td(dcc.Input(id='C3EditField', type='number', value=3e-8, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row12 = html.Tr([ html.Td("C2",style={"backgroundColor":"white","color":"black"}),html.Td(dcc.Input(id='C2EditField', type='number', value=-0.000028, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row13 = html.Tr([ html.Td("C1",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='C1EditField', type='number', value=0.058, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row14 = html.Tr([ html.Td("C0",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='C0EditField', type='number', value=1.365, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row15= html.Tr([ html.Td("On-Loss at IpmJ",style={"backgroundColor":"#f5f5bd","color":"black"}), html.Td(dcc.Input(id='val', type='number', value=32.568054, className='rounded-input',style={"backgroundColor":"#f5f5bd","color":"black"}),style={"backgroundColor":"#f5f5bd","color":"black"} )])
                                                                                                                                                                                                                             # html.Td(dcc.Input(id='val', type='number', value=32.568054, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"}
row16 = html.Tr([ html.Td("Eoff=D3*I^3+D2*I^2+D1*I+D0",style={"verticalAlign": "middle","backgroundColor":"white","color":"black"}, rowSpan="5",colSpan="2"), html.Td("D3",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='D3EditField', type='number', value=7.4e-8, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row17 = html.Tr([ html.Td("D2",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='D2EditField', type='number', value=-0.000084, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row18 = html.Tr([ html.Td("D1",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='D1EditField', type='number', value="0.09", className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row19 = html.Tr([ html.Td("D0",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='D0EditField', type='number', value="4.021", className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row20= html.Tr([ html.Td("Off-Loss at IpmJ",style={"backgroundColor":"#f5f5bd","color":"black"}), html.Td(dcc.Input(id='D0', type='number', value=43.360739, className='rounded-input',style={"backgroundColor":"#f5f5bd","color":"black"}),style={"backgroundColor":"#f5f5bd","color":"black"})])

row21 = html.Tr([html.Td("FWD", style={"verticalAlign": "middle","backgroundColor":"#9ed8ff","color":"black","textAlign": "center",}, rowSpan="8"),  html.Td("Vf=B1*I+B0",style={"verticalAlign": "middle","backgroundColor":"white","color":"black"}, rowSpan="2"), html.Td("B1(rf)",style={"backgroundColor":"white","color":"black"}), html.Td("V/A",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='B1EditField', type='number', value=0.0015, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row22 = html.Tr([ html.Td("B0(Vfo)",style={"backgroundColor":"white","color":"black"}), html.Td("V",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='B0EditField', type='number', value=0.84, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])

row23 = html.Tr([ html.Td("Err=E3*I^3+E2*I^2+E1*I+E0",style={"verticalAlign": "middle","backgroundColor":"white","color":"black"}, rowSpan="5",colSpan="2"), html.Td("E3",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='E3EditField', type='number', value=-2.9e-8, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row24 = html.Tr([ html.Td("E2",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='E2EditField', type='number', value=0.000025, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row25= html.Tr([ html.Td("E1",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='E1EditField', type='number', value=0.034, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row26 = html.Tr([ html.Td("E0",style={"backgroundColor":"white","color":"black"}),html.Td(dcc.Input(id='E0EditField', type='number', value=7.016, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])
row27= html.Tr([html.Td("On-Loss at IpmJ",style={"backgroundColor":"#f5f5bd","color":"black"}),html.Td(dcc.Input(id='exa', type='number', value=28.476634, className='rounded-input',style={"backgroundColor":"#f5f5bd","color":"black"}),style={"backgroundColor":"#f5f5bd","color":"black"})])

row28 = html.Tr([ html.Td("Parasitic R",style={"backgroundColor":"white","color":"black"}),html.Td("Bus-Bar Wiring-R",style={"backgroundColor":"white","color":"black"}), html.Td("ohm",style={"backgroundColor":"white","color":"black"}), html.Td(dcc.Input(id='exam', type='number', value=0.41, className='rounded-input',style={"backgroundColor":"white","color":"black"}),style={"backgroundColor":"white","color":"black"})])


table_body_igbt = [html.Tbody([row1, row2, row3,row4,row5,row6,row7,row8,row9,row10,row11,row12,row13,row14,row15,row16,row17,row18,row19,row20,row21,row22,row23,row24,row25,row26,row27,row28],style={"backgroundColor": "#1e1e2f"})]


tabipm_fields = [
    dbc.Table(table_header+table_body_igbt , bordered=True, 
    hover=True,
    responsive=True,
    # striped=True,
    # className='table-hover',
  style={"width": "100%", "tableLayout": "fixed"}
),
]

ipm_tab = dmc.Flex(
    [
        dmc.Flex(
        dmc.SimpleGrid(
        cols={  "sm": 2, "lg":2,"md":2,"xl":3},
        # spacing={"base": "sm", "sm": "sm","lg":"sm","md":"sm"},
        # verticalSpacing={"base": "md", "sm": "xl","lg":"xl"},
        children=[
            html.Div(
                children=[
                    html.Div(id="ipmedit"),
                    dcc.Loading(id="ipmloader1",children=dcc.Graph(id='graph1')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open1",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            html.Div(
                children=[
                    dcc.Loading(id="ipmloader2",children=dcc.Graph(id='graph2')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open2",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            html.Div(
                children=[
                    dcc.Loading(id="ipmloader3",children=dcc.Graph(id='graph3')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open3",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            html.Div(
                children=[
                    dcc.Loading(id="ipmloader4",children=dcc.Graph(id='graph4')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open4",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            html.Div(
                children=[
                    dcc.Loading(id="ipmloader5",children=dcc.Graph(id='graph5')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open5",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            html.Div(
                children=[
                    dcc.Loading(id="ipmloader6",children=dcc.Graph(id='graph6')),
                    html.Div(
                        id="full-screen-icon",
                        children=[
                            html.Button(
                            id="open6",
                            children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                            style={
                                "cursor": "pointer",
                                "position": "absolute",  # Position absolutely within the parent col
                                "bottom": "5px",  # Align to the bottom
                                "right": "10px",  # Align to the right
                                "background-color": "transparent",
                                "border": "1px solid transparent",
                                "border-radius": "50%",
                                "padding": "4px",
                            },
                        )],)              
                    ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
            ),
            dmc.Modal(id="modal1",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf1',style={'height': '800px'}),],),
            dmc.Modal(id="modal2",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf2',style={'height': '800px'}),],),
            dmc.Modal(id="modal3",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf3',style={'height': '800px'}),],),
            dmc.Modal(id="modal4",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf4',style={'height': '800px'}),],),
            dmc.Modal(id="modal5",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf5',style={'height': '800px'}),],),
            dmc.Modal(id="modal6",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf6',style={'height': '800px'}),],),
            ],
        ),
            style={
                'width': '70%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
 
        ),
 
        dmc.Flex(
            [
             dmc.Flex(
                dmc.SimpleGrid(
                    spacing={"base": "sm",  "sm": "sm","lg":"sm","md":"sm"},
                    cols={  "sm":2, "lg": 2},
                    children=[
                    dmc.Button("<<<<IGBT settings", id="drawer-igbt",variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60},),
                    # dmc.Button("<<<<IGBT settings", id="drawer-igbt",style={"backgroundColor": "#88a9b8","color": "black" }),
                    dmc.ActionIcon(id="ipm-edit-confirm",children=DashIconify(icon="fluent-emoji-flat:pencil"), color="blue", variant="subtle",style={"alignItems": "center", "justifyContent": "center" }),
                    dmc.Drawer(title="IGBT", id="open-igbt", children=tabipm_fields,padding="md",zIndex=10000, size="75%",style={"backgroundColor":"white"}),#children=tabipm_fields,
                    ]
                ),
        ),
    #     dmc.Divider(variant="solid"),
   
        dmc.Flex([
            dmc.Tooltip(
                    label="Represents urban driving conditions with frequent stops and low speeds",
                    children= dmc.Text("MaxSpeed", c="white",size="sm",style={"width": "100px"}),
                    position="left",
                    # offset=3,multiline=True,w=250,withArrow=True,
                    # transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
           
            dmc.NumberInput(value=10000,w=100,hideControls="True",id="EffMaxSpeed",disabled=True,),
            dmc.Tooltip(
                label="Represents urban driving conditions with frequent stops and low speeds",
                children= dmc.Text("MaxSpeed (Max LUT)rpm",size="sm", c="white",style={"width": "100px"}),
                position="left",offset=3,multiline=True,w=250,withArrow=True,
                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
            
            dmc.NumberInput(value=20000,w=100,hideControls="True",style={"width": "100px"},id="MaxSpeedRpmEditField",disabled=True)
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},),
        dmc.Flex([

            dmc.Text("Initial", c="white",size="sm",style={"width": "100px"}),
            dmc.NumberInput(value=0.0001,w=100,id="InitialEditField",hideControls="True",disabled=True,),
            dmc.Tooltip(
                label="Temperature of the motor at the moment it begins operation.",
                children=  dmc.Text("Ini. temp", c="white",size="sm",style={"width": "100px"}),
                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ),            
          
            dmc.NumberInput(value=75,id="InitempEditField",w=100,hideControls="True",style={"width": "100px"},disabled=True,)
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},),
        dmc.Flex([
            dmc.Text("Increment", c="white",size="sm",style={"width": "100px"}),
            dmc.NumberInput(value=200,w=100,id="IncrementEditField",hideControls="True",disabled=True,),
            dmc.Tooltip(
                label=" Temperature range considered comfortable for human living environments.",
                children=dmc.Text("Room Temp", c="white",size="sm",style={"width": "100px"}),
                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
            
            dmc.NumberInput(value=23,w=100,id="RoomTempEditField",hideControls="True",style={"width": "100px"},disabled=True,)
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},),
        dmc.Table([table_head,table_body],striped=True,highlightOnHover=True, withColumnBorders=True, withTableBorder=True,style={"marginTop":"20px"}),
        dmc.Flex([
            dmc.Button("Torque and Speed Curve",id="trqspd", variant="light",style={ "width": "190px" }),
            # dmc.Button("Torque and Speed Curve",id="trqspd",style={"backgroundColor": "#88a9b8", "color": "black", "width": "190px","whiteSpace": "normal", "overflow": "visible" }),
            dmc.Button("TN curve(Nm) & Power(Kw), Im(A), Vm(V)", id="tnpowerim", variant="light",style={ "width": "250px"}),
            dmc.Modal(id="modal-tncurve",fullScreen=True,zIndex=10000, children=[ dcc.Graph(id='graph7',style={'height': '800px'}),],),
            dmc.Modal(id="modal-tnpowerim",fullScreen=True,zIndex=10000, children=[ dcc.Graph(id='graph8',style={'height': '800px'}),],),
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},style={"marginTop":"20px"}),
        dmc.Flex([
            dmc.Button("Total Curve", id="totalcurve", variant="light",style={"width": "190px"}),
            dmc.Button("MTPA-Max torque at Irms", id="mtpa", variant="light", style={ "width": "250px"}),  
            dmc.Modal(id="modal-totalcurve",fullScreen=True,zIndex=10000,children=[dcc.Graph(id='graph9',style={'height': '800px'}),],),
            dmc.Modal(id="modal-mtpa",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph10',style={'height': '800px'}),],),
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"}),
        dmc.Flex([
            dmc.Button("Is(),Vs(),PF Curve", id="isvspf", variant="light",style={"width": "190px"}),
            dmc.Button("A12 Id Iq",id="a12id" , variant="light", style={ "width": "250px"}),
            dmc.Modal(id="modal-isvspf",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph11',style={'height': '800px'}),],),
            dmc.Modal(id="modal-a12id",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph12',style={'height': '800px'}),],),
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"}),
        dmc.Flex([
            dmc.Button("Id Iq Map By Temperature", id="idiqtemp", variant="light",style={"width": "190px"}),
            dmc.Button("Id Iq map by Torque",id="idiqtor",  variant="light", style={ "width": "250px"}),
            dmc.Modal(id="modal-idiqtemp",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph13',style={'height': '800px'}),],),
            dmc.Modal(id="modal-idiqtor",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph14',style={'height': '800px'}),],),
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"v"}),
        dmc.Flex([
            dmc.Button("Temperature Profile",  id="tempprof", variant="light",style={"width": "190px"}),
            dmc.Button("Ploss-LMC",  id="plosslmc", variant="light", style={ "width": "250px"}),
            dmc.Modal(id="modal-tempprof",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph15',style={'height': '800px'}),],),
            dmc.Modal(id="modal-plosslmc",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graph16',style={'height': '800px'}),],),
        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"}),
 
 
            ],
            style={
                'width': '30%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="md",
        )
    ],
    direction="row",
    justify="flex-start",
    gap="xs",
    style={
        'width': '100%',
        'height': 'calc(100vh - 100px)',
        'border': 'none',
        # 'marginTop': "15px",
        # "background-color": "white"
    },
)
 


driving_thead=dmc.TableThead(
            dmc.TableTr(
                [
                    dmc.TableTh("Paramter"),
                    dmc.TableTh("Value"),
                    dmc.TableTh("Unit"),
                ]))

driving_tbody=dmc.TableTbody(
    children=[
        dmc.TableTr([
            dmc.Tooltip(
                label="Distance from center of the tire to its outer edge.",
                children=dmc.TableTd("Tire rω"),
                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
            ), 
            
            dmc.TableTd(0.381,id="td-tirerw"),
            dmc.TableTd("(m)"),
            ]),
        dmc.TableTr([
                dmc.Tooltip(
                label="A measure of tire’s resistance to rotational acceleration around its axis, based on its mass distribution. It measures how much torque is needed to rotate the tire at a certain angular speed.",
                children=dmc.TableTd("Moment of Inertia of a tire"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
              dmc.TableTd(0.870966,id="td-moi"),
                dmc.TableTd("(kg*m^2)"),
            ]),
        dmc.TableTr([
                dmc.Tooltip(
                label="The amount of energy consumed by the vehicle’s drivetrain.",
                children=dmc.TableTd("Drive Consumption Power"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
                
                dmc.TableTd(4.0521888883,id="td-dcp"),
                dmc.TableTd("kW/1800s"),
            ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The total distance that can be covered while cruising.",
                children=dmc.TableTd("Drive distance"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(24.371921769,id="td-dd"),
            dmc.TableTd("km/1800s"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The total energy consumed by the battery to travel some distance, reflects how much energy is drawn from the battery during consumption.",
                children=dmc.TableTd("Battery Consumption"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(1.6626464366,id="td-bc"),
            dmc.TableTd("kWh/10km"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The distance vehicle can travel at a constant speed (cruising speed) in single charge to understand range efficiency under steady state condition.",
                children=dmc.TableTd("Cruising distance"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(481.16062584,id="td-cd"),
            dmc.TableTd("km"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="Represents urban driving conditions with frequent stops and low speeds",
                children=  dmc.TableTd("Max rpm"),
                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
           
            dmc.TableTd(6108522.5545,id="td-maxrpm"),
            dmc.TableTd("rpm"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="Corresponds electrical output power by the motor without any losses throughout the drive cycle.",
                children=dmc.TableTd("SOC Total: Acc(Pe) w/o Ploss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(-2372.8219444,id="td-socPe"),
            dmc.TableTd("kW/1800sec"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="Corresponds to battery power that is given as input to the motor throughout the drive cycle.",
                children=dmc.TableTd("SOC Total: Acc(Pbtt) w/Ploss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(-2885.7556586,id="td-socPbtt"),
            dmc.TableTd("kW/1800sec"),
        ]),
        dmc.TableTr([
            
            dmc.Tooltip(
                label="The total power loss in the system (electrical and mechanical), including all forms of inefficiency.",
                children=dmc.TableTd("PLoss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            dmc.TableTd(0.20530155376,id="td-ploss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The power loss in form of heat due to the electrical resistance in copper windings of the motor (I2R losses).",
                children=dmc.TableTd("Copper loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(262.60881132,id="td-coploss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The power loss due to magnetic hysteresis and eddy currents in the motor’s iron core.",
                children=dmc.TableTd("Iron loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(663.26034752,id="td-ironloss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The power loss occurring in the inverter during the conversion of DC to AC power.",
                children=dmc.TableTd("Inverter loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(229.66154512,id="td-invloss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="Miscellaneous power loss due to factors like leakage flux and small eddy currents not including in copper or iron losses.",
                children= dmc.TableTd("Stray loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
           
            dmc.TableTd(17.902185547,id="td-strayloss"),
            dmc.TableTd("kW"),
           
        ]),  
        dmc.TableTr([
            dmc.Tooltip(
                label="The power loss caused by mechanical friction between moving parts like bearings or gears.",
                children= dmc.TableTd("Friction loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
           
            dmc.TableTd(95.970688,id="td-fricloss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The power loss due to air resistance or drag inside the motor as parts move through air.",
                children=dmc.TableTd("Windage loss"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(95.970688,id="td-winloss"),
            dmc.TableTd("kW"),
        ]),
        dmc.TableTr([
            dmc.Tooltip(
                label="The ratio of the output power to the total input power.",
                children=dmc.TableTd("Efficiency"),
                position="right",
                offset=3,
                radius="sm",
                multiline=True,
                w=250,
                withArrow=True,
                transitionProps={
                "transition": "fade", 
                "duration": 200,
                "timingFunction": "ease"
                },
            ),
            
            dmc.TableTd(95.970688,id="td-effic"),
            dmc.TableTd("kW"),])            
    ]
)
paramter_header = [
    html.Thead(html.Tr([ 
                        html.Th("Zones",colSpan=2,style={"textAlign": "center","backgroundColor":"#7d2e8f", "borderRadius": "5px","color":"black","height":"50px","fontWeight": "normal" }),
                        html.Th(" ",style={"color":""}),
                        html.Th("Temperature",colSpan=2,style={"backgroundColor":"#4cd2ed","color":"white","borderRadius": "5px", "color":"black","height":"50px","fontWeight": "normal" }),
                        html.Th(" ",style={"color":""}),
                        html.Th("PLoss",colSpan=2,style={"textAlign": "center","backgroundColor":"#0564a3", "borderRadius": "5px", "color":"black","height":"50px","fontWeight": "normal" }),
                        html.Th("Temp",colSpan=2,style={"textAlign": "center","backgroundColor":"#0564a3", "borderRadius": "5px", "color":"black","height":"50px","fontWeight": "normal" }),


                        ]))
]

#style={"border": "1px solid #ccc", "padding": "10px"}
#<Icon icon="icon-park:edit-two" />
dr_row1 = html.Tr([ dmc.Tooltip(
                    label="Represents urban driving conditions with frequent stops and low speeds",
                    children=html.Td("Low", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
    
                  #dcc.Input( type="number", value=0.004,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"}
                html.Td(dcc.Input( type="number", value=1,className="rounded-inputval",id="LowEditField",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("A",style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number",id="AEditField", value=0.004,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), html.Td(""),
                dmc.Tooltip(
                    label="The power loss in form of heat due to the electrical resistance in copper windings of the motor (I2R losses).",
                    children=html.Td("Pcu", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number", value=1,id="Pcuflag",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td("Temp",style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=1,id="Tempflag",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"}))

                ],style={"padding": "5px","marginTop":"5px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row2 = html.Tr([dmc.Tooltip(
                    label="Simulates suburban or residential driving with moderate speeds and less frequent stops.",
                    children=html.Td("Medium", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ),  
                html.Td(dcc.Input( type="number", value=1,id="MediumEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("B",style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number",id="BEditField", value=0.0005,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), html.Td(""),
                dmc.Tooltip(
                    label="The power loss due to magnetic hysteresis and eddy currents in the motor’s iron core.",
                    children=html.Td("Pfe", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number",id="Pfeflag", value=2,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("")
                ],style={"padding": "5px","marginTop":"5px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row3 = html.Tr([dmc.Tooltip(
                    label="Emulates rural or main road driving with higher speeds and steady cruising periods.",
                    children=html.Td("High", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number", id="HighEditField", value=1,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("C",style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number",id="CEditField", value=0.0566,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), html.Td(""),
                dmc.Tooltip(
                    label="Miscellaneous power loss due to factors like leakage flux and small eddy currents not including in copper or iron losses.",
                    children=html.Td("Pstr", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number",id="Pstrflag", value=1,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("")
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row4= html.Tr([dmc.Tooltip(
                    label="Represents highway driving conditions with high speeds and minimal stops, testing the vehicle at its peak operational performance.",
                    children=html.Td("Ex-High", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ),  
                html.Td(dcc.Input( type="number", id="ExHighEditField", value=1,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("MaxTemp",style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=0,id="MaxTempEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), html.Td(""),
                dmc.Tooltip(
                    label="The power loss caused by mechanical friction between moving parts like bearings or gears.",
                    children=html.Td("Pf", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number",id="Pfflag", value=1,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("")
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row5= html.Tr([html.Td("Vehicle Dynamics", colSpan=2,style={"color":"white", "textAlign": "center", "borderRadius": "5px"}),  
                  html.Td(dmc.Switch(size="lg",radius="lg",checked=True,    onLabel="ON",offLabel="OFF")), 
                 html.Td(""), 
                html.Td(""), html.Td(""),
                dmc.Tooltip(
                    label="The power loss due to air resistance or drag inside the motor as parts move through air.",
                    children=html.Td("Pw", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ),  
                html.Td(dcc.Input( type="number",id="Pwflag", value=1,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("")
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row6= html.Tr([html.Td( colSpan=2 ),
                html.Td(""), html.Td(""), 
                html.Td(""), html.Td(""),
                dmc.Tooltip(
                    label="The power loss occurring in the inverter during the conversion of DC to AC power",
                    children=html.Td("Pinv", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),  
                    position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                    transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                ), 
                html.Td(dcc.Input( type="number",id="Pinvflag", value=2,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(""), html.Td("")
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")


dr_row7= html.Tr([
                html.Td("Filter-1",colSpan=3, style={"textAlign": "center","backgroundColor":"#b8b869", "borderRadius": "5px","color":"black","height":"50px"}), 
                html.Td("Filter-2",colSpan=2, style={"textAlign": "center","backgroundColor":"#b8b869", "borderRadius": "5px","color":"black","height":"50px"}), 
                html.Td(""),html.Td("",colSpan=3),
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row8= html.Tr([  html.Td("Tn-50", style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=50,id="Tn50",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})), 
                html.Td(dcc.Input( type="number", value=15000,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td("S1-K", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),
                html.Td(dcc.Input( type="number", value=1000,id="S1KEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td(""),html.Td(dmc.Button("CLTC energy consumption(kwh/10km)Vs Batt cap.",id="clctenergy", variant="light", style={"width": "100%"}),colSpan=4,style={"textAlign": "center",}),
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row9= html.Tr([   html.Td("Tn-100", style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=100,id="Tn100",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                  html.Td(dcc.Input( type="number", value=10000,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td("S5-K", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),
                html.Td(dcc.Input( type="number", value=5000,id="S5KEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td(""),html.Td(dmc.Button("Battery Derating series", variant="light",id="batderser", style={"width": "100%"}),colSpan=4,style={"textAlign": "center",}),
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row10= html.Tr([  html.Td("Tn-200", style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=200,id="Tn200",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                  html.Td(dcc.Input( type="number", value=5000,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td("S10-K", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),
                html.Td(dcc.Input( type="number", value=10000,id="S10KEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td(""),html.Td(dmc.Button("Motor Specifications", variant="light" ,id="motorspecs",style={"width": "100%"}),colSpan=4,style={"textAlign": "center",}),
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")

dr_row11= html.Tr([ html.Td("Tn-300", style={"color":"white","textAlign": "center", "borderRadius": "5px"}), 
                html.Td(dcc.Input( type="number", value=300,id="Tn300",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                  html.Td(dcc.Input( type="number", value=5000,className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td("S15-K", style={"color":"white","textAlign": "center", "borderRadius": "5px"}),
                html.Td(dcc.Input( type="number", value=15000,id="S15KEditField",className="rounded-inputval",style={"backgroundColor":"#a6a6a6"})),
                html.Td(""),html.Td(dmc.Button("80 kW Leaf", variant="light",id="kwleaf",style={"width": "100%"}),colSpan=4,style={"textAlign": "center",}),
                ],style={"padding": "5px", "marginBottom": "10px"})#dcc.Input(id="v-input", type="number", value=350, className="rounded-input")





drivepattern_body=[html.Tbody([dr_row1,dr_row2,dr_row3,dr_row4,dr_row5,dr_row6 ,dr_row7,dr_row8,dr_row9,dr_row10,dr_row11],
            style={"padding": "5px","marginTop":"5px"}
            )]

driveparameter_fields = [
    dbc.Table(paramter_header+drivepattern_body , bordered=True, 
    hover=True,
    responsive=True,
    # striped=True,
  style={"width": "100%","tableLayout": "fixed"}#"height":"calc(100vh - 100px)",
),
    dmc.Modal(id="modal-clctenergy",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='datag1',style={'height': '800px'}),],),
    dmc.Modal(id="modal-batderser",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='datag2',style={'height': '800px'}),],),
    dmc.Modal(id="modal-motorspecs",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='datag3',style={'height': '800px'}),],),
    dmc.Modal(id="modal-kwleaf",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='datag4',style={'height': '800px'}),],),
    

]




drive_pattern=dmc.Flex([
    dmc.Flex([
        #     dmc.Flex(
        #         [
        #             # dmc.Button("Cruising Pattern",variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60}),
        # #             dmc.Text("Cruising Pattern", c="white", style={
        # #     "width": "150px",
        # #     "border": "1px ",  # Adjust the border color and thickness as needed
        # #     "backgroundColor": "#7d2e8f",  # Set the background color to red
        # #     "padding": "5px",  # Optional: add padding for better appearance
        # #     "borderRadius": "3px" , # Optional: make the corners rounded
        # #     "marginBottom":"5px",
        # #     "marginRight":"6px","marginLeft":"2px"
        # # }),
        #         dmc.Space(w=10),
        #         dmc.Select(
        #             value="2",
        #             data=[
        #                 {"value": "1", "label": "NEDC"},
        #                 {"value": "2", "label": "WLTC"},
        #                 {"value": "3", "label": "CLTC"},
        #                 {"value": "4", "label": "FTP75"},
        #             ],
        #             w=200,
        #             mb=10,
        #             id='CrusPtnDropDown',
        #         ),
        #         dmc.Space(w=100),
        #         # dmc.Button("Parameter Settings>>>", id="drawer-parameter",variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60},),
        #         # dmc.Button("Parameter Settings>>>", id="drawer-parameter", style={"backgroundColor": "#88a9b8", "color": "black"}),
        #         # dmc.Drawer(title="Driving Pattern", id="open-parameter", children=driveparameter_fields,padding="md",size="73%",style={"backgroundColor":"white"}),#children=tabipm_fields,
        #         dmc.Flex(
        #             [
        #                 # dmc.ActionIcon(id="dp-edit-confirm",children=DashIconify(icon="fluent-emoji-flat:pencil",width=20),size="lg", variant="light",),
        #                 dmc.Space(w=10),
        #                 dmc.Button("Traction Force", variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60},style={"width": "37%"}),
        #                 # dmc.Text("Traction Force", c="black", style={'width': '35%', "marginRight": "0px", "border": "1px ", "backgroundColor": "#9eacc7","padding": "5px", "borderRadius": "3px","marginBottom":"5px","textAlign":"center"}),
        #                 html.Div(id="dpedit")
        #             ],
        #             justify="flex-end",
        #             style={"flex": "1"}
        #         )
        #     ],
        #     style={"width": "100%","marginRight": "2px"}
        # ),
            dmc.Flex([
                dmc.Flex([
                    dmc.SimpleGrid(
                    cols={ "sm": 2, "lg":2,"md":2,"xl":3},
                    # spacing={"base": "sm", "sm": "sm","lg":"sm","md":"sm"},
                    # verticalSpacing={"base": "md", "sm": "xl","lg":"xl"},
                    children=[
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader1",children=dcc.Graph(id='graphd1')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open7",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader2",children=dcc.Graph(id='graphd2')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open8",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader3",children=dcc.Graph(id='graphd3')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open9",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader4",children=dcc.Graph(id='graphd4')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open10",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader5",children=dcc.Graph(id='graphd5')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open11",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                        html.Div(
                            children=[
                                dcc.Loading(id="dploader6",children=dcc.Graph(id='graphd6')),
                                html.Div(
                                    id="full-screen-icon",
                                    children=[
                                        html.Button(
                                        id="open12",
                                        children=[DashIconify(id="openicon",icon="iconamoon:screen-full-thin",width=30,style={"color": "white"})],
                                        style={
                                            "cursor": "pointer",
                                            "position": "absolute",  # Position absolutely within the parent col
                                            "bottom": "5px",  # Align to the bottom
                                            "right": "10px",  # Align to the right
                                            "background-color": "transparent",
                                            "border": "1px solid transparent",
                                            "border-radius": "50%",
                                            "padding": "4px",
                                        },
                                    )],)              
                                ],style={'border-color': '#2e2e2e','border-style': 'solid','position': 'relative'}
                        ),
                    ],
                    # style={"width":"100%","height":"100%"}
                    ),
                ], style={
                'width': '70%',
                # 'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",),
                dmc.Flex([
                    dmc.Flex(
                        dmc.SimpleGrid(
                            # spacing={"base": "sm",  "sm": "sm","lg":"sm","md":"sm"},
                            cols={  "sm":2, "lg": 2},
                            children=[
                            
                            dmc.Button("Parameter Settings>>>", id="drawer-parameter",variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60},),
                            # dmc.Button("<<<<IGBT settings", id="drawer-igbt",style={"backgroundColor": "#88a9b8","color": "black" }),
                            dmc.ActionIcon(id="dp-edit-confirm",children=DashIconify(icon="fluent-emoji-flat:pencil",width=20),size="lg", variant="light",),
                            dmc.Drawer(title="Driving Pattern", id="open-parameter", children=driveparameter_fields,padding="md",size="73%",style={"backgroundColor":"white"}),#children=tabipm_fields,
                            html.Div(id="dpedit")
                            ]
                        ),
                    ),
                    dmc.Flex(
                        dmc.SimpleGrid(
                            # spacing={"base": "sm",  "sm": "sm","lg":"sm","md":"sm"},
                            cols={  "sm":2, "lg": 2},
                            children=[
                            
                            dmc.Button("Cruising Pattern",variant="gradient",gradient={"from": "teal", "to": "blue", "deg": 60}),
                            # dmc.Button("<<<<IGBT settings", id="drawer-igbt",style={"backgroundColor": "#88a9b8","color": "black" }),
                            dmc.Select(
                                value="2",
                                data=[
                                    {"value": "1", "label": "NEDC"},
                                    {"value": "2", "label": "WLTC"},
                                    {"value": "3", "label": "CLTC"},
                                    {"value": "4", "label": "FTP75"},
                                ],
                                w=200,
                                mb=10,
                                id='CrusPtnDropDown',
                            ),
                            ]
                        ),
                    ),                    

                    dmc.Flex(
                        [
                            dmc.Tooltip(
                                label="The acceleration due to gravity is the force that pulls objects towards the earth",
                                children=dmc.Text("Gravity", c="white",size="sm",style={"width": "80px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),   
                            dmc.NumberInput(value=9.81,w=60,id="GravityEditField",hideControls="True",disabled=True),
                            dmc.Text("m..", c="white",style={"width": "20px"}),
                            dmc.Tooltip(
                                label="Rolling resistance is the force that opposes the motion of the vehicle as the tire roll over a surface.",
                                children=dmc.Text("Rolling Resistance", c="white" ,size="sm",style={"width": "120px","marginLeft":"15px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),        
                            dmc.NumberInput(value=0.008,w=60,id="frEditField",hideControls="True",disabled=True),
                        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},ms=10
                    ),
                    dmc.Flex(
                        [
                            dmc.Tooltip(
                                label="Head wind is the speed of the wind blowing directly against the direction of the vehicle’s motion.",
                                children=dmc.Text("Head Wind", c="white",size="sm" ,style={"width": "80px"}),#,"marginLeft":"10px"
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),                             
                            
                            dmc.NumberInput(value=0,w=60,id="VWindEditField",hideControls="True",disabled=True),
                            dmc.Text("k..", c="white",style={"width": "20px"}),
                            dmc.Tooltip(
                                label=" The drag coefficient is a dimensionless number representing the vehicle’s aerodynamic efficiency",
                                children=dmc.Text("Drag Coeff", c="white",size="sm" ,style={"width": "120px","marginLeft":"15px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),    
                            
                            dmc.NumberInput(value=0.25,w=60,id="CdEditField",hideControls="True",disabled=True),
                        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},ms=10
                    ),
                    dmc.Flex(
                        [
                            dmc.Tooltip(
                                label="The frontal area is the cross-sectional area of the vehicle facing the airflow.",
                                children=dmc.Text("Frontial Area", c="white",size="sm" ,style={"width": "80px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),                             
                            
                            dmc.NumberInput(value=1.5,w=60,id="AfEditField",hideControls="True",disabled=True),
                            dmc.Text("m^2", c="white",style={"width": "20px"}),
                            dmc.Tooltip(
                                label="Slip ratio is the difference between the rotational speed of the tire and the actual speed of the vehicle.",
                                children=dmc.Text("Slip Ratio", c="white",size="sm",style={"width": "120px","marginLeft":"15px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),    
                            
                            dmc.NumberInput(value=0.02,w=60,id="sxEditField",hideControls="True",disabled=True),
                        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},ms=10
                    ),
                    dmc.Flex(
                        [
                            dmc.Tooltip(
                                label="Air density is mass per unit volume of air.",
                                children=dmc.Text("Air Density", c="white",size="sm" ,style={"width": "80px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),                             
                            
                            dmc.NumberInput(value=1.225,w=60,id="pEditField",hideControls="True",disabled=True),
                            dmc.Text("k...", c="white",style={"width": "20px"}),
                            dmc.Tooltip(
                                label="Transmission efficiency is the ratio of the output power to the input power of the transmission system.",
                                children=dmc.Text("Trans Eff", c="white",size="sm",style={"width": "120px","marginLeft":"15px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ), 
                            
                            dmc.NumberInput(value=0.98,w=60,id="ndrEditField",hideControls="True",disabled=True),
                        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},ms=10
                           
                    ),
                    dmc.Flex(
                        [
                            dmc.Tooltip(
                                label="Road grade refers to the slope or incline of the road",
                                children=dmc.Text("Road Grade", c="white",size="sm",style={"width": "80px"}),
                                position="right",offset=3,radius="sm",multiline=True,w=250,withArrow=True,
                                transitionProps={"transition": "fade", "duration": 200,"timingFunction": "ease"},
                            ),                             
                            dmc.NumberInput(value=0,w=60,id="RoadGradeEditField",hideControls="True",disabled=True),
                        ], direction={"base": "row", "sm": "row","lg":"row"},gap={"base": "sm", "sm": "sm","lg":"sm"},ms=10
                    ),
                    dmc.ScrollArea(h=250,children=dmc.Table([driving_thead,driving_tbody],striped=True,highlightOnHover=True, withColumnBorders=True, withTableBorder=True,style={"marginTop":"10px","marginLeft":"5px"}),
                                   ),
                    dmc.Space(h=10),
                    dmc.Flex([
                        dmc.Button("Cruising Distance and battery by simulation and pole", id="btn-cursd1", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Cruising Distance and battery by simulation model", id="btn-cursd2", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Cruising Distance and battery by gear ratio", id="btn-cursd3", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Cruising Distance and battery byIdc", id="btn-cursd4", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Cruising Distance and battery by Tire inch", id="btn-cursd5", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Ploss by WLTC zones", id="btn-cursd6", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Id, Iq Control Map", id="btn-cursd7", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Button("Id vs Iq", id="btn-cursd8", variant="light",style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Cruising Distance and battery by simulation and pole",id="btn-cursd1",variant="outline", style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Cruising Distance and battery by simulation model",id="btn-cursd2",variant="outline", style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Cruising Distance and battery by gear ratio",id="btn-cursd3", variant="outline", style={"marginLeft":"5px", "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Cruising Distance and battery byIdc",id="btn-cursd4", variant="outline",style={"marginLeft":"5px",  "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Cruising Distance and battery by Tire inch",id="btn-cursd5", variant="outline",style={"marginLeft":"5px","whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        # dmc.Button("Id vs Iq",id="btn-cursd6", variant="outline",style={"marginLeft":"5px",  "whiteSpace": "normal", "wordBreak": "break-word", "textAlign": "center", "height": "auto", "lineHeight": "normal"}),
                        dmc.Modal(id="modal-cursd1",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd1',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd2",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd2',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd3",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd3',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd4",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd4',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd5",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd5',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd6",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd6',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd7",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd7',style={'height': '800px'}),],),
                        dmc.Modal(id="modal-cursd8",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='cursd8',style={'height': '800px'}),],),
                        dmc.Modal(id="modal7",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf7',style={'height': '800px'}),],),
                        dmc.Modal(id="modal8",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf8',style={'height': '800px'}),],),
                        dmc.Modal(id="modal9",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf9',style={'height': '800px'}),],),
                        dmc.Modal(id="modal10",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf10',style={'height': '800px'}),],),
                        dmc.Modal(id="modal11",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf11',style={'height': '800px'}),],),
                        dmc.Modal(id="modal12",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf12',style={'height': '800px'}),],),
                        dmc.Modal(id="modal13",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf13',style={'height': '800px'}),],),
                        dmc.Modal(id="modal14",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf14',style={'height': '800px'}),],),
                    ], direction={"base": "column", "sm": "column","lg":"column"},gap={"base": "sm", "sm": "sm","lg":"sm"},),
                   
 
 
                ],
                style={
                'width': '30%',
                # 'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="md",
                # direction={"base": "column", "sm": "column","lg":"column"},
                # gap={"base": "sm", "sm": "sm","lg":"sm"},
                # style={"display":"flex"}
                ),
 
 
 
            ], direction={"base": "row", "sm": "row"},),
         ],
         direction={"base": "column", "sm": "column"},
        #  gap={"base": "sm", "sm": "sm","lg":"sm"},
        # justify={"sm": "flex-start","md":"flex-start","base":"flex-start"},
        style={'width': '100%', 'height': 'calc(100vh - 100px)','border': 'none','marginTop':"15px"}
        ),  
       
 
],
    direction="row",
    justify="flex-start",
    gap="xs",
 
# direction={"base": "row", "sm": "row",},
# gap={"base": "sm", "sm": "sm","lg":"sm"},
# justify={"sm": "flex-start","md":"flex-start","base":"flex-start"},
style={'width': '100%', 'height': 'calc(100vh - 100px)','border': 'none'})




# columnDefs=[{'field': col} for col in df.columns],
# rowData=df.to_dict('records'),
columns = [{"headerName": f"Column {i+1}", "field": f"Column {i+1}"} for i in range(10)]

# Create 10 empty rows
empty_data = [
    {f"Column {i+1}": f"Value {row+1}-{i+1}" for i in range(10)} for row in range(10)
]
df = pd.DataFrame('', index=range(20), columns=[f'Col {i}' for i in range(20)])
df.insert(0, 'Row Headers', [f'Row {i+1}' for i in range(20)])


Next_Tn = dmc.Flex(
    [
        dmc.Flex(
            [
                dmc.Text("Pe",size="sm", id="tnlosstype1Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='LossPointTableTn1',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="tnlosstype2Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='LossPointTableTn2',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="tnlosstype3Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='LossPointTableTn3',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
             
            ],
            style={
                'width': '35%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                'overflowY': 'auto'
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                # dmc.Space(h="xl"),
                dmc.Text("Pe",size="sm", id="tnlosstype1textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTableTn1',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="tnlosstype2textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTableTn2',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="tnlosstype3textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTableTn3',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
             
            ],
            style={
                'width': '35%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                'overflowY': 'auto'
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphTn1", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open25",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphTn2", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    id="open26",
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphTn3", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    id="open27",
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                dmc.Modal(id="modal25",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf25",style={'height': '800px'}),],),
                dmc.Modal(id="modal26",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf26",style={'height': '800px'}),],),
                dmc.Modal(id="modal27",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf27",style={'height': '800px'}),],),
                # dcc.Graph(id="graphTn1",style={"height":"32%"}),
                # dcc.Graph(id="graphTn2",style={"height":"32%"}),
                # dcc.Graph(id="graphTn3",style={"height":"32%"}),
            ],
            style={
                'width': '30%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        )
    ],
    direction="row",
    justify="flex-start",
    gap="xs",
    style={
        'width': '100%',
        'height': 'calc(100vh - 10px)',
        'border': 'none',
        # 'marginTop': "15px",
        # "background-color": "white"
    },
)
 
ploss_torque = dmc.Flex(
    [
        dmc.Flex(
            [
                # dmc.Space(h="xl"),
                 dmc.Paper(
                    children=[dmc.Text("Frequency table-Efiiciency by Tn",size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"})],
                    # radius="xl", # or p=10 for border-radius of 10px
                    # withBorder=True,
                    # shadow="sm",
                    style={"backgroundColor": "rgba(34, 139, 230, 0.15)", "display": "flex", "justifyContent": "center", "alignItems": "center"}
                ),
                # dmc.Flex(dmc.Text("frequency Loss", size="xs")),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='TnFrequencyTab',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,
                            className="custom-table" 
                        ),
                    ]    
                ),
                dmc.Text("Select 20 points",size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.Flex([
                    dmc.Paper(children=[dmc.Text("Mode", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                    # dmc.Text("Mode", fw=500),
                    dmc.Select(id="TnLossModeDD",value="2",data=[ {"value": "1", "label": "Top10;Bottom10;"},{"value": "2", "label": "Free Points"},],style={"color": "#0be40a",} ),
                    dmc.Button("Clear",id="clear_tn",style={"color": "#5db1ec","backgroundColor": "rgba(34, 139, 230, 0.15)",}),
                    dmc.Button("Next",id="Next_TnLossButton",style={"color": "#5db1ec","backgroundColor": "rgba(34, 139, 230, 0.15)","justifyContent": "flex-end"}),
                ],
                direction="row",
                # gap="sm",
                align="center",
                justify="space-between",
                mt=5
                ),
                dmc.ScrollArea(
                    h="68%",
                    w="100%",
                    children=[
                        dt.DataTable(
                            id='TnFreePtsTab',
                            # editable=False,  # Disable editing
                            row_selectable=False,  # Disable row selection
                            # cell_selectable=False,
                        ),
                        dcc.Store(id='click-counts-Tn', data={})
                    ],
                ),
                dmc.Drawer(title=dmc.Text("From Selected points",size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),id="Tn-drawer",padding="xs",size="100%",children=Next_Tn),
                dmc.Modal(
                    title="WARNING",
                    id="ploss-torque-modal",
                    children=[
                        dmc.Flex([
                            dmc.Flex([
                                DashIconify(icon="emojione:warning", style={"height": "50%", "width": "auto"}),
                                dmc.Blockquote(
                                    "Select all the dropdowns",
                                    color="red",
                                    style={"flex": 1, "height": "100%"}
                                ),
                            ], direction="row", align="center", gap="xl", style={"flex": 1, "alignItems": "center", "height": "auto"})
                        ], style={"flex": 1})
                    ],
                    centered = True,
                ),
            ],
            style={
                'width': '40%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                dmc.Flex(
                    [
                        dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="TnLoss1",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                       dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        # dmc.Text("Dropdown2", fw=500),
                        dmc.Select(id="TnAvg1",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    # mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dcc.Loading(
                            children=[dmc.Table(
                                id='TnLossTab1',
                                striped=False,
                                withTableBorder=True,
                                withColumnBorders=True,
                                px=50,
                                className="custom-table"
                            ),],
                        )
                    ]    
                ),
                dmc.Flex(
                    [
                       dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="TnLoss2",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                        dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(id="TnAvg2",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    # mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dcc.Loading(
                            children=[dmc.Table(
                                id='TnLossTab2',
                                striped=False,
                                withTableBorder=True,
                                withColumnBorders=True,
                                px=50,
                                className="custom-table"
                            ),],
                        )
                    ]    
                ),
                dmc.Flex(
                    [
                        dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="TnLoss3",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                        dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(id="TnAvg3",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    # mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dcc.Loading(
                            children=[dmc.Table(
                                id='TnLossTab3',
                                striped=False,
                                withTableBorder=True,
                                withColumnBorders=True,
                                px=50,
                                className="custom-table"
                            ),],
                        )
                    ]    
                ),
            ],
            style={
                'width': '40%',
                # 'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="tn-graph1",style={"height": "270px" ,"width": "100%"}),
                                # dcc.Graph(id="tn-graph1", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open13",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="tn-graph2", style={"height": "270px", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open14",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "270px", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="tn-graph3", style={"height": "270px", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open15",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                dmc.Modal(id="modal13",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf13',style={'height': '800px'}),],),
                dmc.Modal(id="modal14",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf14',style={'height': '800px'}),],),
                dmc.Modal(id="modal15",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf15',style={'height': '800px'}),],),
                # dcc.Graph(id="tn-graph1",style={"height":"32%"}),
                # dcc.Graph(id="tn-graph2",style={"height":"32%"}),
                # dcc.Graph(id="tn-graph3",style={"height":"32%"}),
            ],
            style={
                'width': '20%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="md",
        )
    ],
    direction="row",
    justify="flex-start",
    gap="xs",
    style={
        'width': '100%',
        'height': 'calc(100vh - 100px)',
        'border': 'none',
        # 'marginTop': "15px",
        # "background-color": "white"
    },
)


Next_ImLoss = dmc.Flex(
    [
        dmc.Flex(
            [
                dmc.Text("Pe",size="sm", id="Imlosstype1Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTab1',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="Imlosstype2Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTab2',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="Imlosstype3Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrderTab3',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
             
            ],
            style={
                'width': '35%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                'overflowY': 'auto'
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                # dmc.Space(h="xl"),
                dmc.Text("Pe",size="sm", id="Imlosstype1textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrdMatCalc1',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="Imlosstype2textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrdMatCalc2',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Pe",size="sm", id="Imlosstype3textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='OrdMatCalc3',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
             
            ],
            style={
                'width': '35%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                'overflowY': 'auto'
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphImL1", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open28",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphImL2", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    id="open29",
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphImL3", style={"height": "100%", "width": "100%"}),
                                dmc.ActionIcon(
                                    DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
                                    id="open29",
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "2px",
                                        "left": "5px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                dmc.Modal(id="modal28",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf28",style={'height': '800px'}),],),
                dmc.Modal(id="modal29",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf29",style={'height': '800px'}),],),
                dmc.Modal(id="modal30",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf30",style={'height': '800px'}),],),
                # dcc.Graph(id="graphTn1",style={"height":"32%"}),
                # dcc.Graph(id="graphTn2",style={"height":"32%"}),
                # dcc.Graph(id="graphTn3",style={"height":"32%"}),
            ],
            style={
                'width': '30%',
                'height': 'calc(100vh - 10px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        )
    ],
    direction="row",
    justify="flex-start",
    gap="xs",
    style={
        'width': '100%',
        'height': 'calc(100vh - 10px)',
        'border': 'none',
        # 'marginTop': "15px",
        # "background-color": "white"
    },
)
 



#ploss current

# Next_ImLoss=dmc.Flex(
#     [
#         dmc.Flex(
#             [
#                 # dmc.Space(h="xl"),
#                 dmc.Text("Pe",size="sm", id="Imlosstype1Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrderTab1',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
#                 dmc.Text("Pe",size="sm", id="Imlosstype2Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrderTab2',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
#                 dmc.Text("Pe",size="sm", id="Imlosstype3Text",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrderTab3',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
             
#             ],
#             style={
#                 'width': '35%',
#                 'height': 'calc(100vh - 10px)',
#                 'border': 'none',
#                 'marginTop': "15px",
#                 'overflowY': 'auto'
#             },
#             direction="column",
#             gap="xs",
#         ),
#         dmc.Flex(
#             [
#                 # dmc.Space(h="xl"),
#                 dmc.Text("Pe",size="sm", id="Imlosstype1textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrdMatCalc1',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
#                 dmc.Text("Pe",size="sm", id="Imlosstype2textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrdMatCalc2',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
#                 dmc.Text("Pe",size="sm", id="Imlosstype3textsetpoints",style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
#                 dmc.ScrollArea(
#                     h="32%",
#                     w="100%",
#                     children=[
#                         dmc.Table(
#                             id='OrdMatCalc3',
#                             striped=False,
#                             withTableBorder=True,
#                             withColumnBorders=True,
#                             px=50,className="custom-table",
#                             style={"backgroundColor":"white","color":"black"}
#                         ),
#                     ]    
#                 ),
             
#             ],
#             style={
#                 'width': '35%',
#                 'height': 'calc(100vh - 10px)',
#                 'border': 'none',
#                 'marginTop': "15px",
#                 'overflowY': 'auto'
#             },
#             direction="column",
#             gap="xs",
#         ),
#         dmc.Flex(
#             [
#                 html.Div(
#                     [
#                         html.Div(
#                             [
#                                 dcc.Graph(id="graphImL1", style={"height": "100%", "width": "100%"}),
#                                 dmc.ActionIcon(
#                                     id="open28",
#                                     children=DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
#                                     size="lg",
#                                     color="#2e2e2e",
#                                     variant="subtle",
#                                     n_clicks=0,
#                                     mb=10,
#                                     style={
#                                         "position": "absolute",
#                                         "top": "2px",
#                                         "left": "5px",
#                                         "fontSize": "24px",
#                                         "cursor": "pointer",
#                                         "zIndex": 10  # Ensure the icon appears above the graph
#                                     }
#                                 ),
#                             ],
#                             style={"position": "relative", "height": "100%", "width": "100%"}
#                         )
#                     ],
#                     style={"height": "32%", "position": "relative"}  # Adjust the height as needed
#                 ),
#                 html.Div(
#                     [
#                         html.Div(
#                             [
#                                 dcc.Graph(id="graphImL2", style={"height": "100%", "width": "100%"}),
#                                 dmc.ActionIcon(
#                                     DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
#                                     id="open29",
#                                     size="lg",
#                                     color="#2e2e2e",
#                                     variant="subtle",
#                                     n_clicks=0,
#                                     mb=10,
#                                     style={
#                                         "position": "absolute",
#                                         "top": "2px",
#                                         "left": "5px",
#                                         "fontSize": "24px",
#                                         "cursor": "pointer",
#                                         "zIndex": 10  # Ensure the icon appears above the graph
#                                     }
#                                 ),
#                             ],
#                             style={"position": "relative", "height": "100%", "width": "100%"}
#                         )
#                     ],
#                     style={"height": "32%", "position": "relative"}  # Adjust the height as needed
#                 ),
#                 html.Div(
#                     [
#                         html.Div(
#                             [
#                                 dcc.Graph(id="graphImL3", style={"height": "100%", "width": "100%"}),
#                                 dmc.ActionIcon(
#                                     DashIconify(icon="iconamoon:screen-full-thin", width=30,color="white"),
#                                     id="open30",
#                                     size="lg",
#                                     color="#2e2e2e",
#                                     variant="subtle",
#                                     n_clicks=0,
#                                     mb=10,
#                                     style={
#                                         "position": "absolute",
#                                         "top": "2px",
#                                         "left": "5px",
#                                         "fontSize": "24px",
#                                         "cursor": "pointer",
#                                         "zIndex": 10  # Ensure the icon appears above the graph
#                                     }
#                                 ),
#                             ],
#                             style={"position": "relative", "height": "100%", "width": "100%"}
#                         )
#                     ],
#                     style={"height": "32%", "position": "relative"}  # Adjust the height as needed
#                 ),
#                 dmc.Modal(id="modal28",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf28",style={'height': '800px'}),],),
#                 dmc.Modal(id="modal29",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf29",style={'height': '800px'}),],),
#                 dmc.Modal(id="modal30",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id="graphf30",style={'height': '800px'}),],),
#                 # dcc.Graph(id="graphTn1",style={"height":"32%"}),
#                 # dcc.Graph(id="graphTn2",style={"height":"32%"}),
#                 # dcc.Graph(id="graphTn3",style={"height":"32%"}),
#             ],
#             style={
#                 'width': '30%',
#                 'height': 'calc(100vh - 10px)',
#                 'border': 'none',
#                 'marginTop': "15px",
#                 # "background-color": "black"
#             },
#             direction="column",
#             gap="xs",
#         ),


#         # dmc.Flex(
#         #     [
#         #         dcc.Graph(id="graphImL1",style={"height":"32%"}),
#         #         dcc.Graph(id="graphImL2",style={"height":"32%"}),
#         #         dcc.Graph(id="graphImL3",style={"height":"32%"}),
#         #     ],
#         #     style={
#         #         'width': '20%',
#         #         'height': 'calc(100vh - 10px)',
#         #         'border': 'none',
#         #         'marginTop': "15px",
#         #         # "background-color": "black"
#         #     },
#         #     direction="column",
#         #     gap="xs",
#         # )
#     ],
#     direction="row",
#     justify="flex-start",
#     gap="xs",
#     style={
#         'width': '100%',
#         'height': 'calc(100vh - 10px)',
#         'border': 'none',
#         'marginTop': "15px",
#         # "background-color": "white"
#     },
# )


ploss_current = dmc.Flex(
    [
        dmc.Flex(
            [
                # dmc.Space(h="xl"),
                dmc.Paper(
                    children=[dmc.Text("Frequency table-Efiiciency by Tn",size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"})],
                    # radius="xl", # or p=10 for border-radius of 10px
                    # withBorder=True,
                    # shadow="sm",
                    style={"backgroundColor": "rgba(34, 139, 230, 0.15)", "display": "flex", "justifyContent": "center", "alignItems": "center"}
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='TncurrentTab',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            px=50,className="custom-table",
                            style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Text("Select 20 points",size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center", "padding": "8px"}),
                dmc.Flex([
                    dmc.Paper(children=[dmc.Text("Mode", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                    # dmc.Text("Mode", fw=500),
                    dmc.Select(id="CurrentLossModeDD",value="2",data=[ {"value": "1", "label": "Top10;Bottom10;"},{"value": "2", "label": "Free Points"},],),
                    dmc.Button("Clear",id="clear_im",style={"color": "#5db1ec","fontWeight": "bold","backgroundColor":  "rgba(34, 139, 230, 0.15)",}),
                    dmc.Button("Next",id="Next_CurrentLossButton",style={"color": "#5db1ec","fontWeight": "bold","backgroundColor":  "rgba(34, 139, 230, 0.15)","justifyContent": "flex-end"}),
                    dmc.Drawer(id="imcurrent-drawer",padding="xs",size="100%",children=Next_ImLoss),
                    dmc.Modal(
                        title="WARNING",
                        id="ploss-current-modal",
                        children=[
                            dmc.Flex([
                                dmc.Flex([
                                    DashIconify(icon="emojione:warning", style={"height": "50%", "width": "auto"}),
                                    dmc.Blockquote(
                                        "Select all the dropdowns",
                                        color="red",
                                        style={"flex": 1, "height": "100%"}
                                    ),
                                ], direction="row", align="center", gap="xl", style={"flex": 1, "alignItems": "center", "height": "auto"})
                            ], style={"flex": 1})
                        ],
                        centered = True,
                    ),
                ],
                direction="row",
                gap="sm",
                align="center",
                justify="space-between",
                mt=5
                ),                
                dmc.ScrollArea(
                    h="68%",
                    w="100%",
                    children=[
                        dt.DataTable(
                            id='CurrentFreePtsTab',
                        ),
                    ]
                ),
                dcc.Store(id='click-counts', data={})
            ],
            style={
                'width': '40%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                'overflowY': 'auto'
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                dmc.Flex(
                    [
                       dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="ImLoss1",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                        dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(id="ImAvg1",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    # mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='CurrentLossTab1',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            className="custom-table",
                            px=50,style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Flex(
                    [
                        dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="ImLoss2",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                        dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(id="ImAvg2",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='CurrentLossTab2',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            className="custom-table",
                            px=50,style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
                dmc.Flex(
                    [
                        dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor": "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(
                            value=None,
                            id="ImLoss3",
                            data=[
                                {"value": "1", "label": "Pe with regeneration"},{"value": "2", "label": "Pe(kWh)"},{"value": "3", "label": "Pe(kW/s)"},
                                {"value": "4", "label": "Pcu(kW)"},{"value": "5", "label": "Pfe(kW)"},{"value": "6", "label": "Pstr(kW)"},
                                {"value": "7", "label": "Pf(kW)"},{"value": "8", "label": "Pw(kW)"},{"value": "9", "label": "Pinv(kW)"},
                                {"value": "10", "label": "sum Ploss(kW)"},{"value": "11", "label": "Temp"},{"value": "12", "label": "η = Pe/Pbatt"}
                            ],
                        ),
                        dmc.Paper(children=[dmc.Text("Style", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                              withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
                        dmc.Select(id="ImAvg3",value="2",data=[ {"value": "1", "label": "Average"},{"value": "2", "label": "Exact"},],),
                    ],
                    direction="row",
                    gap="sm",
                    align="center",
                    justify="space-between",
                    mt=5
                ),
                dmc.ScrollArea(
                    h="32%",
                    w="100%",
                    children=[
                        dmc.Table(
                            id='CurrentLossTab3',
                            striped=False,
                            withTableBorder=True,
                            withColumnBorders=True,
                            className="custom-table",
                            px=50,style={"backgroundColor":"white","color":"black"}
                        ),
                    ]    
                ),
            ],
            style={
                'width': '40%',
                # 'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        ),
        dmc.Flex(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphIm1", style={"height": "270px", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open16",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphIm2", style={"height": "270px", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open17",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id="graphIm3", style={"height": "270px", "width": "100%"}),
                                dmc.ActionIcon(
                                    id="open18",
                                    children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                                    size="lg",
                                    color="#2e2e2e",
                                    variant="subtle",
                                    n_clicks=0,
                                    mb=10,
                                    style={
                                        "position": "absolute",
                                        "top": "10px",
                                        "left": "10px",
                                        "fontSize": "24px",
                                        "cursor": "pointer",
                                        "zIndex": 10  # Ensure the icon appears above the graph
                                    }
                                ),
                            ],
                            style={"position": "relative", "height": "100%", "width": "100%"}
                        )
                    ],
                    style={"height": "32%", "position": "relative"}  # Adjust the height as needed
                ),
                dmc.Modal(id="modal16",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf16',style={'height': '800px'}),],),
                dmc.Modal(id="modal17",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf17',style={'height': '800px'}),],),
                dmc.Modal(id="modal18",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf18',style={'height': '800px'}),],),
            ],
            style={
                'width': '20%',
                'height': 'calc(100vh - 120px)',
                'border': 'none',
                'marginTop': "15px",
                # "background-color": "black"
            },
            direction="column",
            gap="xs",
        )
    ],
    direction="row",
    justify="flex-start",
    gap="xs",
    style={
        'width': '100%',
        'height': 'calc(100vh - 100px)',
        'border': 'none',
        'marginTop': "15px",
        # "background-color": "white"
    },
)


ploss_tab=dmc.Flex([
    dmc.Flex([
            dmc.Paper(children=[dmc.Text("Loss Type", size="sm", style={"color": "#5db1ec","fontWeight": "bold", "textAlign": "center","padding": "8px"})], 
                withBorder=True,shadow="sm", style={"backgroundColor":  "rgba(34, 139, 230, 0.15)",'width': '30%',"justifyContent": "center", "alignItems": "center"}),
            # dmc.Text("Mode", fw=500),
            dmc.Select(id="ploss_types",value="2",data=[ 
                {"value": "1", "label": "Pbattery"},{"value": "2", "label": "Ploss",},{"value": "3", "label": "Pcopper"},{"value": "4", "label": "Piron",},
                {"value": "5", "label": "Pstray"},{"value": "6", "label": "Pfriction",},{"value": "7", "label": "Pwindage"},{"value": "8", "label": "Pinverter",},
                {"value": "9", "label": "Positive efficicency"},{"value": "10", "label": "Negative efficicency",},{"value": "11", "label": "efficicency"},
                ],
                       style={"color": "#0be40a",} ), 
    ],
    direction="row",
    # gap="sm",
    align="center",
    justify="center",
    mt=5
    ),
    dmc.Flex([
        dcc.Graph(id='graphpl1',style={'height': '750px','width': '100%',}),
    ], mt=5)

],direction="column",
    style={
        'width': '100%',
        'height': 'calc(100vh - 10px)',
        'border': 'none',
        'marginTop': "15px",
        # "background-color": "white"
    },
)

#ploss current

# Page Content for EVM Simulator
data_tab=dmc.Flex([
    dmc.SimpleGrid(
    cols={  "sm": 2, "lg":2,"md":2,"xl":3},
    # spacing={"base": "sm", "sm": "sm","lg":"sm","md":"sm"},
    # verticalSpacing={"base": "md", "sm": "xl","lg":"xl"},
    children=[
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt1", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open19",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={ "position": "relative"}  # Adjust the height as needed
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt2", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open20",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative"}  # Adjust the height as needed
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt3", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open21",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative"}  # Adjust the height as needed
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt4", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open22",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative"}  # Adjust the height as needed
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt5", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open23",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative"}  # Adjust the height as needed
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Loading(dcc.Graph(id="graphdt6", style={"height": "100%", "width": "100%"})),
                        dmc.ActionIcon(
                            id="open24",
                            children=DashIconify(icon="iconamoon:screen-full-thin", width=30),
                            size="lg",
                            color="white",
                            variant="subtle",
                            n_clicks=0,
                            mb=10,
                            style={
                                "position": "absolute",
                                "bottom": "10px",
                                "right": "10px",
                                "fontSize": "24px",
                                "cursor": "pointer",
                                "zIndex": 10  # Ensure the icon appears above the graph
                            }
                        ),
                    ],
                    style={"position": "relative", "height": "100%", "width": "100%"}
                )
            ],
            style={"position": "relative"}  # Adjust the height as needed
        ),
        dmc.Modal(id="modal19",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf19',style={'height': '800px'}),],),
        dmc.Modal(id="modal20",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf20',style={'height': '800px'}),],),
        dmc.Modal(id="modal21",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf21',style={'height': '800px'}),],),
        dmc.Modal(id="modal22",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf22',style={'height': '800px'}),],),
        dmc.Modal(id="modal23",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf23',style={'height': '800px'}),],),
        dmc.Modal(id="modal24",fullScreen=True,zIndex=10000,children=[ dcc.Graph(id='graphf24',style={'height': '800px'}),],),
          ],
    # style={"width":"100%","height":"100%"}
    ),])
page_content_evm = dmc.Tabs(
        id="tabs",
        children=[
            dmc.TabsList(
                [
                    # dmc.TabsTab("Introduction", value="Introduction"),
                    dmc.TabsTab("Input", value="Input"),
                    dmc.TabsTab("IPM Modelling", value="ipm",darkHidden=True,id="ipm"),
                    dmc.TabsTab("Drive pattern modeling", value="drive-pattern",id="drive-pattern",darkHidden=True),
                    dmc.TabsTab("P-Loss analysis by Torque", value="ploss-torque",darkHidden=True,id="pt"),
                    dmc.TabsTab("P-Loss analysis by Current", value="ploss-current",darkHidden=True,id="pc"),
                    # dmc.TabsTab("Data", value="data",darkHidden=True,id="data"),
                    dmc.TabsTab("Ploss", value="ploss-tab",darkHidden=True,id="ploss-tab"),
                ],
            style={"justifyContent": "center", "display": "flex"}
            ),
            # dmc.TabsPanel(children=Introduction_contents, value="Introduction"),
            dmc.TabsPanel(children=input_contents, value="Input"),
            dmc.TabsPanel(children=ipm_tab, value="ipm"),
            dmc.TabsPanel(children=drive_pattern, value="drive-pattern"),
            dmc.TabsPanel(children=ploss_torque, value="ploss-torque"),
            dmc.TabsPanel(children=ploss_current, value="ploss-current"),
            dmc.TabsPanel(children=ploss_tab, value="ploss-tab"),
            # dmc.TabsPanel(children=data_tab, value="data"),
            # dmc.TabsPanel("Settings tab content", value="settings"),
        ],
        value="Input",
        color="#2596be",
        variant="pills",
)

page_content_genDes = dmc.Flex()


paragraph = """
xEV is an electric vehicle simulation tool that generates a digital twin of the electric vehicle. It provides multiple recommendations for efficient combinations of motors, inverters, batteries, bodies, and other components, enabling users to analyze the full characteristics of an electric vehicle.\n

xEV Simulator is a tool designed to support the design and analysis of different modules of electric vehicles. By providing specific inputs such as motor types, battery configurations, and other vehicle components, users can simulate the performance of an electric vehicle. It generates detailed outputs, including visualized graphs, which help in analyzing the vehicle's overall characteristics.\n

Generative Design, on the other hand, uses AI algorithms and mathematical models to automatically generate the optimal parameters for specific vehicle components, such as motors, inverters, and other parts. It tailors these parameters based on user-defined requirements, allowing engineers to explore various design possibilities.\n

Hence, the xEV simulator focuses on simulating and analyzing the performance of the entire vehicle, while Generative Design focuses on creating the most efficient design by generating optimal parameters using AI-driven optimization.
"""

# Main Page Content

page_content = dmc.Flex(
    [
                dmc.Card(
                    children=[
                        dmc.CardSection(
                                dmc.Image(src="assets/Images/xSimImg.JPG")
                        ),
                       dmc.Button(
            "xEV Simulator",id="simulator_page", variant="subtle", n_clicks=0,
            # color="black",
            # fullWidth=True,
            mt="md",
            radius="md",
            # darkHidden=True
            
        )

                    ],
                withBorder=True,
                shadow="sm",
                radius="md",
                w=350,
               
                ),
                dmc.Card(
                    children=[
                        dmc.CardSection(
                            dmc.Image(src="assets/Images/GdImg.JPG"),
                        # h=160,
                        ),
                        dmc.Button(
                            "Generative Design",id="genDes_page",variant="subtle", n_clicks=0,
                        #    color="black",
                            fullWidth=True,
                            mt="md",
                            radius="md",
                        ),
                    ],
                withBorder=True,
                shadow="sm",
                radius="md",
                w=350,
                # style={"backgroundColor": "white"},
                )
    ],  
     id="page-content",
    justify="center",
      direction="row",  # Horizontally center the Paper
    align="center",    # Vertically center the Paper
    gap=200,
    style={"height": 'calc(100vh - 45px)',}
)

# page_content = dmc.Flex(
#     [
#         # dmc.Flex([
#         #     dmc.Paper(
#         #         children=[
#         #             dmc.Blockquote(
#         #                 children=[dmc.Title(f"Introduction", order=5),paragraph,dmc.Space(h="xl"),dmc.Title(f"Note", order=6),dmc.Text("Generative Design feature has not yet been integrated into the xEV Simulator application but will be added soon", size="md"),]
#         #             )
#         #         ],
#         #         shadow="md",
#         #         p="md",
#         #         style={"display": "flex", "flex": 1, "alignItems": "center", "justifyContent": "center"},
#         #     )
#         # ],mt=5, style={"height": "35%"}),

#         dmc.Flex([
#             dmc.Paper(
#                 children=[
#                     dmc.Button("", id="simulator_page", variant="subtle", n_clicks=0, color="black", style={"fontSize": "20px", "width": "100%", "height": "100%"}),
#                 ],
#                 shadow="md",
#                 p="md",
#                 ms=10,
#                 radius="xl",
#                 style={"display": "flex", "flex": 1, "alignItems": "center", "justifyContent": "center", "background": "#d2f5d5",
#                         "backgroundImage": "url('assets/images/xSimImg.JPG')",
#                         "backgroundSize": "cover", 
#                         "backgroundPosition": "center",
#                 },
#             ),
#             dmc.Paper(
#                 children=[
#                     dmc.Button("", id="genDes_page", variant="subtle", n_clicks=0, color="black",style={"fontSize": "20px", "width": "100%", "height": "100%"}),
#                 ],
#                 shadow="md",
#                 p="md",
#                 me=10,
#                 radius="xl",
#                 style={"display": "flex", "flex": 1, "alignItems": "center", "justifyContent": "center", "background": "#f4dbf1",
#                         "backgroundImage": "url('assets/images/GdImg.JPG')",
#                         "backgroundSize": "cover", 
#                         "backgroundPosition": "center",
#                        },
#             )  
#         ],
#         direction="row",
#         justify="flex-start",
#         mt=25,
#         # align = "center",
#         gap="xl",
#         # style={"height": "65%"}
#         ),
#     ],
#     id="page-content",
#     direction="column",
#     justify="flex-start",
#     # align="center",
#     gap="xs",
#     style={
#         "flex": 1,
#         'width': '100%',
#         'height': 'calc(100vh - 45px)',
#         'border': 'none',
#     },
# )



 
# App Shells
app_shell_home = dmc.AppShell(
    [
        dmc.AppShellHeader(header, id="app-shell-header",style={"display":"flex","justify-content":"center","position":"fixed","height":"50px"}),
        dmc.AppShellMain(page_content,mt=35),
    ],
    # header={"height": 50},
    # pt=5,
    id="app-shell",
)
 
app_shell_evm = dmc.AppShell(
    [
        dmc.AppShellHeader(header_evm, id="app-shell-header-evm", style={"display": "flex", "justify-content": "center","height":"50px"}),
        dmc.AppShellMain(page_content_evm,mt=54),
    ],
    # header={"height": 50},
    # pt=5,
    id="app-shell-evm",
)

app_shell_genDes = dmc.AppShell(
    [
        dmc.AppShellHeader(header_genDes, id="app-shell-header-evm", style={"display": "flex", "justify-content": "center","height":"50px"}),
        dmc.AppShellMain(page_content_genDes,mt=20),
    ],
    # header={"height": 50},
    # pt=5,
    id="app-shell-genDes",
)
 
# Define the layout
app.layout = dmc.MantineProvider(
    [dcc.Location(id="url", refresh=False), app_shell_home],
    id="mantine-provider",
    forceColorScheme="dark",
    # theme={
    #     "components": {
    #         "Card" : {"styles": {"root": {"border-color": "var(--mantine-color-gray-3)","background-color":"white"},"section" : {"border-color": "var(--mantine-color-gray-3)"}},},
    #         # "table" : {"styles" : {"root":{"--table-hover-color": "var(--mantine-color-gray-1)","--table-striped-color": "var(--mantine-color-gray-0)","table-border-color": "var(--mantine-color-gray-3)"}}}
    #     }
    # }
)
 
# Callbacks

# @callback(
#     Output("url", "pathname"),
#     Input("simulator_page", "n_clicks"),
#     Input("genDes_page", "n_clicks"),
#     Input("home-btn","n_clicks"),
#     prevent_initial_call=True,
# )
# def switch_path(sim_clicks,genDes_clicks,home):

#     ctx = callback_context
#     if not ctx.triggered:
#         return "/home"
#     button_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     print("button_id",button_id)

#     if button_id == "simulator_page":
#         return "/xev-simulator"
#     elif button_id == "genDes_page":
#         return "/genDes"
#     elif button_id == "home-btn":
#         return "/home"


 
# @callback(
#     Output("mantine-provider", "children"),
#     Input("url", "pathname"),
#     prevent_initial_call=True,
# )
# def display_page(pathname):
#     print("pathname",pathname)
#     if pathname == '/xev-simulator':
#         return [dcc.Location(id="url", refresh=False), app_shell_evm]
#     elif pathname == '/genDes':
#         return [dcc.Location(id="url", refresh=False), app_shell_genDes]
#     elif pathname == '/home':
#         return [dcc.Location(id="url", refresh=False), app_shell_home]
#     else:
#         return [dcc.Location(id="url", refresh=False), app_shell_home]



@callback(
    Output("mantine-provider", "children"),
    Output("url", "pathname"),
    [Input("simulator_page", "n_clicks"),
     Input("home-btn", "n_clicks")]
)
def display_page(simulator_clicks, home_clicks):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    
    if triggered_input == "simulator_page" and simulator_clicks:
        # Navigate to xEV simulator page
        return [dcc.Location(id="url", refresh=False), app_shell_evm], "/xev-simulator"
    
    elif triggered_input == "home-btn" and home_clicks:
        # Navigate back to home page
        return [dcc.Location(id="url", refresh=False), app_shell_home], "/"
    
    # Default: Stay on the current page
    return dash.no_update, dash.no_update
# @callback(
#     Output("mantine-provider", "children"),
#     Input("url", "pathname")
# )
# def display_page(pathname):
#     if pathname == '/xev-simulator':
#         return app_shell_evm
#     else:
#         return app_shell_home


# @callback(
#     [Output("mantine-provider", "children"), Output("url", "pathname")],
#     [Input("simulator_page", "n_clicks"), Input("url", "pathname")]
# )
# def display_page(n_clicks, pathname):
#     print(pathname)
#     # Check which input triggered the callback
#     triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]

#     # # Case when the button is clicked
#     if triggered_input == "simulator_page":
#         return[dcc.Location(id="url", refresh=False), app_shell_evm], "/xev-simulator"


#     # Case when the URL is directly accessed or the home page is requested
#     if pathname == "/xev-simulator":
#         return [dcc.Location(id="url", refresh=False), app_shell_evm], pathname
#     else:
#         return [dcc.Location(id="url", refresh=False), app_shell_home], "/"


 #card callbacks
# Callbacks
@app.callback(
    Output("motor-table", "children"),
    Input("save-motor-file", "n_clicks"),
    State("file-name-input", "value"),
    [State({'type': 'motor-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**motor_parameters[idx], "value": values[idx]}
        for idx in range(len(motor_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['motor'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['motor'])
    rows = create_table_rows(files,'motor')
    body = dmc.TableTbody(rows)
    return [body]

def get_tooltip_motor(parameter_name):
    if "Pole" in parameter_name:
        return "The number of permanent magnet poles in the rotor."
    elif "Resistance" in parameter_name:
        return "The resistance of a stator winding of an electrical machine"
    elif "Voltage" in parameter_name:
        return "Peak value of stator phase voltage"
    elif "Current" in parameter_name:
        return "Peak value of stator phase current"
    elif "Coefficient of Iron Loss" in parameter_name:
        return "This coefficient quantifies the energy loss due to hysteresis and eddy currents in the iron core of the motor"
    elif "Coefficient of Friction Loss" in parameter_name:
        return "This coefficient represents the energy loss due to friction between moving parts in mechanical systems, such as gears, bearings, and other mechanical components"
    elif "Coefficient of Stray Loss" in parameter_name:
        return "This coefficient refers to the fraction of energy that is lost in the system due to factors other than primary energy conversion processes."
    elif "Coefficient of Windage loss" in parameter_name:
        return "This coefficient measures the energy loss due to air resistance experienced by rotating components, such as motors and fans."
    elif "DC-link Voltage" in parameter_name:
        return "DC voltage present across the input terminals of an inverter."
    elif "Dc-link Current" in parameter_name:
        return "DC current that flows through the input terminals of an inverter"
    elif "Switching frequency":
        return "The switching frequency is the frequency at which the switch (i.e. IGBT) may be turned ON and OFF"
    else:
        return ""  # No tooltip for other parameters
    
@app.callback(
    [Output('file-content', 'children'),
     Output('motor-selected-file', 'value')],
    Input({'type': 'motor-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'motor-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_motor = get_files_in_directory(DIRECTORIES['motor'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_motor[file_index]
    
    file_path = os.path.join(DIRECTORIES['motor'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_motor(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    radius="sm",
                    w=410,
                    multiline=True,
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]
    
    return table_rows, file_name


def get_tooltip_inverter(parameter_name):
    if "tr" in parameter_name:
        return "The time taken by IGBT’s collector current to rise from 10% to 90% of its rated value at turn-on"
    elif "tf" in parameter_name:
        return "The time taken by the IGBT’s collector current to fall from 90% to 10% of its rated value at turn-off"
    elif "ton" in parameter_name:
        return "The duration for which the inverter remains in the “on” state during a switching cycle."
    elif "von" in parameter_name:
        return "Voltage level across the inverter when it is in “on” state."
    elif "trr" in parameter_name:
        return "The time taken by the freewheeling diode (connected in parallel to the IGBT) to switch from conducting in the forward direction to blocking in the reverse direction"
    else:
        return ""  # No tooltip for other parameters
    
#inverter 
@app.callback(
    [Output('inverter-file-content', 'children'),
     Output('inverter-selected-file', 'value')],
    Input({'type': 'inverter-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'inverter-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_inverter = get_files_in_directory(DIRECTORIES['inverter'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_inverter[file_index]
    
    file_path = os.path.join(DIRECTORIES['inverter'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_inverter(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    radius="sm",
                    w=400,
                    multiline=True,
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]

    # table_rows = [
    #     dmc.TableTr([dmc.TableTd(cell) for cell in row])
    #     for row in file_content
    # ]
    
    return table_rows, file_name

 
@app.callback(
    Output("inverter-table", "children"),
    Input("save-inverter-file", "n_clicks"),
    State("inv-file-name-input", "value"),
    [State({'type': 'inverter-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**inverter_parameters[idx], "value": values[idx]}
        for idx in range(len(inverter_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['inverter'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['inverter'])
    rows = create_table_rows(files,'inverter')
    body = dmc.TableTbody(rows)
    return [body]


def get_tooltip_battery(parameter_name):
    if "Battery charge" in parameter_name:
        return "The amount of electrical energy stored in the battery"
    elif "Regeneration ratio" in parameter_name:
        return "Ratio of kinetic energy that can be converted back into electrical energy during regenerative braking to the energy consumed during acceleration"
    elif "Regeneration limit" in parameter_name:
        return "The maximum speed at which regenerative braking can be effectively applied, beyond which the regenerative system cannot capture energy from braking."
    else:
        return ""  # No tooltip for other parameters
#battery
@app.callback(
    [Output('battery-file-content', 'children'),
     Output('battery-selected-file', 'value')],
    Input({'type': 'battery-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'battery-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_battery = get_files_in_directory(DIRECTORIES['battery'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_battery[file_index]
    
    file_path = os.path.join(DIRECTORIES['battery'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_battery(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    radius="sm",
                     w=350,
                     multiline=True,
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]

    
    return table_rows, file_name



@app.callback(
    Output("battery-table", "children"),
    Input("save-battery-file", "n_clicks"),
    State("btt-file-name-input", "value"),
    [State({'type': 'battery-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**battery_parameters[idx], "value": values[idx]}
        for idx in range(len(battery_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['battery'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['battery'])
    rows = create_table_rows(files,'battery')
    body = dmc.TableTbody(rows)
    return [body]


def get_tooltip_gear(parameter_name):
    if "Gear ratio" in parameter_name:
        return "The ratio of the number of teeth in the driving wheel to the number of teeth in the driven wheel."
    elif "Shaft diameter" in parameter_name:
        return "The diameter of the shaft."
    else:
        return ""  # No tooltip for other parameters

#gear
@app.callback(
    [Output('gear-file-content', 'children'),
     Output('gear-selected-file', 'value')],
    Input({'type': 'gear-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'gear-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_gear = get_files_in_directory(DIRECTORIES['gear'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_gear[file_index]
    
    file_path = os.path.join(DIRECTORIES['gear'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_gear(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    multiline=True,
                     w=290,
                    radius="sm",
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]

    return table_rows, file_name



@app.callback(
    Output("gear-table", "children"),
    Input("save-gear-file", "n_clicks"),
    State("gear-file-name-input", "value"),
    [State({'type': 'gear-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**gear_parameters[idx], "value": values[idx]}
        for idx in range(len(gear_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['gear'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['gear'])
    rows = create_table_rows(files,'gear')
    body = dmc.TableTbody(rows)
    return [body]


def get_tooltip_tire(parameter_name):
    if "Tire Outer diameter" in parameter_name:
        return "The total height of the tire when mounted on a wheel and inflated,"" measured from ground to the top of the tire." "It includes both the tire’s tread and sidewall."
    elif "Weight of a tire" in parameter_name:
        return "The mass of each tire used in the vehicle."
    else:
        return ""  # No tooltip for other parameters
#tire
@app.callback(
    [Output('tire-file-content', 'children'),
     Output('tire-selected-file', 'value')],
    Input({'type': 'tire-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'tire-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_tire = get_files_in_directory(DIRECTORIES['tire'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_tire[file_index]
    
    file_path = os.path.join(DIRECTORIES['tire'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_tire(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    radius="sm",
                    multiline=True,
                     w=250,
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]

    
    return table_rows, file_name



@app.callback(
    Output("tire-table", "children"),
    Input("save-tire-file", "n_clicks"),
    State("tire-file-name-input", "value"),
    [State({'type': 'tire-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**tire_parameters[idx], "value": values[idx]}
        for idx in range(len(tire_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['tire'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['tire'])
    rows = create_table_rows(files,'tire')
    body = dmc.TableTbody(rows)
    return [body]

def get_tooltip_vehicle(parameter_name):
    if "Curb weight" in parameter_name:
        return "The total weight of the vehicle with all its standard equipment, including the battery pack, fluids (like coolant and brake fluid), and necessary components for operation, but without any passengers, cargo, or driver."
    elif "Luggage weight" in parameter_name:
        return "The total weight of any cargo, luggage or additional items carried in the vehicle, excluding passengers."
    elif "Passenger weight" in parameter_name:
        return "Weight of each person sitting inside the vehicle."
    elif "Passenger number":
        return "Number of passengers inside the vehicle"
    elif "Tire number":
        return "Total number of tires used by the vehicle to move, excluding the spare tire."
    else:
        return ""  # No tooltip for other parameters

#vehicle
@app.callback(
    [Output('vehicle-file-content', 'children'),
     Output('vehicle-selected-file', 'value')],
    Input({'type': 'vehicle-file-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    State({'type': 'vehicle-file-button', 'index': dash.dependencies.ALL}, 'id'),
    prevent_initial_call=True
)
def display_file_content(n_clicks, file_ids):
    files_vehicle = get_files_in_directory(DIRECTORIES['vehicle'])
    ctx = dash.callback_context
    if not ctx.triggered:
        return [], ""

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    file_index = eval(triggered_id)['index']
    file_name = files_vehicle[file_index]
    
    file_path = os.path.join(DIRECTORIES['vehicle'], file_name)
    if not (file_name.endswith('.xlsx') or file_name.endswith('.xls')):
        return [dmc.TableTr(dmc.TableTd(f"Selected file '{file_name}' is not an Excel file."))], file_name

    df = pd.read_excel(file_path, header=None, skiprows=1)
    file_content = df.values.tolist()

    table_rows = [
        dmc.TableTr([
            dmc.TableTd(
                dmc.Tooltip(
                    label=get_tooltip_vehicle(row[0]),  # Conditionally add tooltips for the parameter
                    children=row[0],
                    position="right",
                    offset=3,
                    radius="sm",
                    multiline=True,
                     w=250,
                    withArrow=True,
                    transitionProps={
                        "transition": "fade", 
                        "duration": 200,
                        "timingFunction": "ease"
                    },
                      # This is the parameter name
                )
            ),
            dmc.TableTd(row[1])  # This is the value
        ])
        for row in file_content
    ]

    
    return table_rows, file_name


@app.callback(
    Output("vehicle-table", "children"),
    Input("save-vehicle-file", "n_clicks"),
    State("vehicle-file-name-input", "value"),
    [State({'type': 'vehicle-save-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if not file_name.endswith(".xlsx"):
        file_name += ".xlsx"

    if n_clicks is None:
        return ""

    updated_parameters = [
        {**vehicle_parameters[idx], "value": values[idx]}
        for idx in range(len(vehicle_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['vehicle'], file_name)
    df.to_excel(file_path, index=False)

    global files, rows
    files = get_files_in_directory(DIRECTORIES['vehicle'])
    rows = create_table_rows(files,'vehicle')
    body = dmc.TableTbody(rows)
    return [body]

# Edit motor modal toggle


@app.callback(
    Output("edit-motor-modal", "children"),
    Output("edit-motor-modal", "opened"),
    Input("edit-motor-btn", "n_clicks"),
    Input("motor-selected-file", "value"),
    State("edit-motor-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_edit_motor(n_clicks,motor_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-motor-btn":
        if motor_file:
            mot_data = pd.read_excel("Simulator Files/Motor/"+motor_file)
            parameters = mot_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'motor-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-motor-save", style={"flex": 1}, mt=25),
                            html.Div(id="motor-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened

@app.callback(
    Output("motor-save", "children"),
    Input("edit-motor-save", "n_clicks"),
    Input("motor-selected-file", "value"),
    [State({'type': 'motor-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**motor_parameters[idx], "value": values[idx]}
        for idx in range(len(motor_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['motor'], file_name)
    df.to_excel(file_path, index=False)

    return ""



# Edit inverter modal toggle
@app.callback(
    Output("edit-inverter-modal", "children"),
    Output("edit-inverter-modal", "opened"),
    Input("edit-inverter-btn", "n_clicks"),
    Input("inverter-selected-file", "value"),
    State("edit-inverter-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_inverter_motor(n_clicks,inverter_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-inverter-btn":
        if inverter_file:
            inv_data = pd.read_excel("Simulator Files/Inverter/"+inverter_file)
            parameters = inv_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'inverter-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-inverter-save", style={"flex": 1}, mt=25),
                            html.Div(id="inverter-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened

@app.callback(
    Output("inverter-save", "children"),
    Input("edit-inverter-save", "n_clicks"),
    Input("inverter-selected-file", "value"),
    [State({'type': 'inverter-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**inverter_parameters[idx], "value": values[idx]}
        for idx in range(len(inverter_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['inverter'], file_name)
    df.to_excel(file_path, index=False)

    return ""



# Edit battery modal toggle
@app.callback(
    Output("edit-battery-modal", "children"),
    Output("edit-battery-modal", "opened"),
    Input("edit-battery-btn", "n_clicks"),
    Input("battery-selected-file", "value"),
    State("edit-battery-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_edit_motor(n_clicks,battery_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-battery-btn":
        if battery_file:
            btt_data = pd.read_excel("Simulator Files/Battery/"+battery_file)
            parameters = btt_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'battery-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-battery-save", style={"flex": 1}, mt=25),
                            html.Div(id="battery-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened


@app.callback(
    Output("battery-save", "children"),
    Input("edit-battery-save", "n_clicks"),
    Input("battery-selected-file", "value"),
    [State({'type': 'battery-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**battery_parameters[idx], "value": values[idx]}
        for idx in range(len(battery_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['battery'], file_name)
    df.to_excel(file_path, index=False)

    return ""





# Edit gear modal toggle
@app.callback(
    Output("edit-gear-modal", "children"),
    Output("edit-gear-modal", "opened"),
    Input("edit-gear-btn", "n_clicks"),
    Input("gear-selected-file", "value"),
    State("edit-gear-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_edit_motor(n_clicks,gear_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-gear-btn":
        if gear_file:
            btt_data = pd.read_excel("Simulator Files/Gear/"+gear_file)
            parameters = btt_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'gear-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-gear-save", style={"flex": 1}, mt=25),
                            html.Div(id="gear-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened

@app.callback(
    Output("gear-save", "children"),
    Input("edit-gear-save", "n_clicks"),
    Input("gear-selected-file", "value"),
    [State({'type': 'gear-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**gear_parameters[idx], "value": values[idx]}
        for idx in range(len(gear_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['gear'], file_name)
    df.to_excel(file_path, index=False)

    return ""






# Edit tire modal toggle
@app.callback(
    Output("edit-tire-modal", "children"),
    Output("edit-tire-modal", "opened"),
    Input("edit-tire-btn", "n_clicks"),
    Input("tire-selected-file", "value"),
    State("edit-tire-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_edit_motor(n_clicks,tire_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-tire-btn":
        if tire_file:
            btt_data = pd.read_excel("Simulator Files/Tire/"+tire_file)
            parameters = btt_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'tire-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-tire-save", style={"flex": 1}, mt=25),
                            html.Div(id="tire-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened

@app.callback(
    Output("tire-save", "children"),
    Input("edit-tire-save", "n_clicks"),
    Input("tire-selected-file", "value"),
    [State({'type': 'tire-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**tire_parameters[idx], "value": values[idx]}
        for idx in range(len(tire_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['tire'], file_name)
    df.to_excel(file_path, index=False)

    return ""




# Edit vehicle modal toggle
@app.callback(
    Output("edit-vehicle-modal", "children"),
    Output("edit-vehicle-modal", "opened"),
    Input("edit-vehicle-btn", "n_clicks"),
    Input("vehicle-selected-file", "value"),
    State("edit-vehicle-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_edit_motor(n_clicks,vehicle_file, opened):
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "edit-vehicle-btn":
        if vehicle_file:
            btt_data = pd.read_excel("Simulator Files/Vehicle/"+vehicle_file)
            parameters = btt_data.to_dict(orient='records')          
            rows = [
                dmc.TableTr(
                    [
                        dmc.TableTd(parameter["parameter"]),
                        dmc.TableTd(
                            dmc.NumberInput(
                                value=parameter["value"],
                                type="number",
                                id={'type': 'vehicle-edit-value', 'index': idx},
                                size="xs"
                            )
                        ),
                    ]
                )
                for idx, parameter in enumerate(parameters)
            ]

            head = dmc.TableThead(
                dmc.TableTr(
                    [
                        dmc.TableTh("Parameter"),
                        dmc.TableTh("Value"),
                    ]
                )
            )
            body = dmc.TableTbody(rows)

            table = dmc.Table(
                [head, body],
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
            )

            content = dmc.Flex([
                table,
                dmc.Divider(variant="solid", mt=10),
                dmc.Paper(
                    children=[
                        dmc.Flex([
                            dmc.Button("Save File", id="edit-vehicle-save", style={"flex": 1}, mt=25),
                            html.Div(id="vehicle-save")
                        ], direction="row"),
                    ],
                    shadow="xs",
                    mt=10, p=10
                )
            ], direction="column")


            return content,not opened
        return [],opened
    return [],opened

@app.callback(
    Output("vehicle-save", "children"),
    Input("edit-vehicle-save", "n_clicks"),
    Input("vehicle-selected-file", "value"),
    [State({'type': 'vehicle-edit-value', 'index': dash.dependencies.ALL}, 'value')],
    prevent_initial_call=True
)
def save_to_excel(n_clicks, file_name, values):
    if n_clicks is None:
        return ""

    updated_parameters = [
        {**vehicle_parameters[idx], "value": values[idx]}
        for idx in range(len(vehicle_parameters))
    ]
    df = pd.DataFrame(updated_parameters)

    file_path = os.path.join(DIRECTORIES['vehicle'], file_name)
    df.to_excel(file_path, index=False)

    return ""


# Add motor modal toggle
@app.callback(
    Output("add-motor-modal", "opened"),
    Input("add-motor-btn", "n_clicks"),
    State("add-motor-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened

@app.callback(
    Output("add-inverter-modal", "opened"),
    Input("add-inverter-btn", "n_clicks"),
    State("add-inverter-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened


@app.callback(
    Output("add-battery-modal", "opened"),
    Input("add-battery-btn", "n_clicks"),
    State("add-battery-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened


@app.callback(
    Output("add-gear-modal", "opened"),
    Input("add-gear-btn", "n_clicks"),
    State("add-gear-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened


@app.callback(
    Output("add-tire-modal", "opened"),
    Input("add-tire-btn", "n_clicks"),
    State("add-tire-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened

@app.callback(
    Output("add-vehicle-modal", "opened"),
    Input("add-vehicle-btn", "n_clicks"),
    State("add-vehicle-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_add_motor(n_clicks, opened):
    return not opened

 #card callbacks

#next button 

#next button 

@app.callback(
    Output("ipm", "darkHidden"),
    Output("drive-pattern", "darkHidden"),
    Output("pt", "darkHidden"),
    Output("pc", "darkHidden"),
    Output("ploss-tab", "darkHidden"),
    Output("next-link","children"),
    Output("module-error", "opened"),
    [Input("next-button", "n_clicks"),
     Input("motor-selected-file", "value"),
     Input("inverter-selected-file", "value"),
     Input("battery-selected-file", "value"),
     Input("gear-selected-file", "value"),
     Input("tire-selected-file", "value"),
     Input("vehicle-selected-file", "value"),
     State("module-error", "opened"),
     ],
     allow_duplicate=True
)
def NextButtonPushed(n_clicks, motor_file, inverter_file, battery_file, gear_file, tire_file, vehicle_file,opened):
    global mot,inv,gear,tire,vhcl,btt,IPMflag
    mot = {}
    inv = {}
    gear = {}
    tire = {}
    vhcl = {}

    if IPMflag != 0:
        resetab()

    if n_clicks is None:
        return True,True,True,True,True,True, opened
   
    all_files_non_empty = all(
        isinstance(file, str) and file.strip() for file in
        [motor_file, inverter_file, battery_file, gear_file, tire_file, vehicle_file]
    )

    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "next-button":
        if all_files_non_empty:

            # fetch motor
            mot_data = pd.read_excel("Simulator Files/Motor/"+motor_file)
            values = mot_data['value'].tolist()
            keys = ['pole', 'res', 'vol', 'cur', 'cfe', 'cstr', 'cPfric', 'cPwind', 'freq', 'DCV', 'DCC']
            mot = dict(zip(keys, values))
            mot['Cstrunit'] = 0.000000001
            mot['unit'] = 0.000001
            print('mot',mot)

            #fetch Inverter
            inv_data = pd.read_excel("Simulator Files/Inverter/"+inverter_file)
            values = inv_data['value'].tolist()
            keys = ['tr', 'tf', 'ton', 'von', 'trr']
            inv = dict(zip(keys, values))
            print('inv',inv)

            #fetch Battery
            btt_data = pd.read_excel("Simulator Files/Battery/"+battery_file)
            values = btt_data['value'].tolist()
            keys = ['charge', 'regen_ratio', 'regen_limit']
            btt = dict(zip(keys, values))
            print('btt',btt)

            #fetch Gear
            gear_data = pd.read_excel("Simulator Files/Gear/"+gear_file)
            values = gear_data['value'].tolist()
            keys = ['gdr', 'shaftD']
            gear = dict(zip(keys, values))
            print('gear',gear)

            #fetch Tire
            tire_data = pd.read_excel("Simulator Files/Tire/"+tire_file)
            values = tire_data['value'].tolist()
            keys = ['TireOutD', 'Ma']
            tire = dict(zip(keys, values))
            tire['Tirerw'] = ((tire['TireOutD']*25.4)/2)/1000
            print('tire',tire)

            #fetch Vehicle
            vehicle_data = pd.read_excel("Simulator Files/Vehicle/"+vehicle_file)
            values = vehicle_data['value'].tolist()
            keys = ['crb', 'lug', 'psgw', 'psgnum', 'tireno']
            vhcl = dict(zip(keys, values))
            print('vhcl',vhcl)

            #function call
            # basic_calc()


            return False,False,False,False,False,False,opened
        else:
            return True,True,True,True,True,True,not opened
    else:
        return True,True,True,True,True,True,opened
    
#basic calc
 
@callback(
    Output("open-igbt", "opened"),
    Input("drawer-igbt", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_demo(n_clicks):
    return True
@callback(
    Output("open-parameter", "opened"),
    Input("drawer-parameter", "n_clicks"),
    prevent_initial_call=True,
)
def drawer_parameter(n_clicks):
    return True

# @app.callback(
#     Output("ipm-content", "children"),
#     Input("tabs", "value")
# )
# def render_content(tab):
#     if tab == "ipm":
#         return load_ipm_modelling()
#     return dash.no_update


@app.callback(
    [
      Output('dtA3','children'),Output('dtB3','children'),Output('dtLd3','children'),Output('dtLq3','children'),Output('pmd3','children'),
      Output('pmq3','children'),Output('dta3','children'),Output('dtA6','children'),Output('dtB6','children'),Output('dtLd6','children'),
      Output('dtLq6','children'),Output('pmd6','children'),Output('dta6','children'),Output('AdjLdEditField','children'),Output('AdjLqEditField','children'),Output('AdjPMEditField','children'),Output('stdrpm1','children'),
      Output('stdrpm2','children'),Output('stdrpm3','children'),Output('stdrpm4','children'),Output('stdrpm5','children'),Output('stdrpm6','children'),
      Output('stdNm1','children'),Output('stdNm2','children'),Output('stdNm3','children'),Output('stdNm4','children'),Output('stdNm5','children'),Output('stdNm6','children'),
      Output('Min1EditField','children'),Output('Min2EditField','children'),Output('Min3EditField','children'),Output('Min4EditField','children'),Output('Min5EditField','children'),
      Output('Min6EditField','children'),Output('Max1EditField','children'),Output('Max2EditField','children'),Output('Max3EditField','children'),Output('Max4EditField','children'),
      Output('Max5EditField','children'),Output('Max6EditField','children'),
      ],
    [Input("next-link","children"),Input("next-link","disable_n_clicks"),Input('dtA1', 'children'), Input('dtB1', 'children'),Input('dtLd1', 'children'), Input('dtLq1', 'children'), Input('pmd1', 'children'), Input('pmq1', 'children'), Input('dta1', 'children'),
     Input('dtA2', 'children'), Input('dtB2', 'children'),Input('dtLd2', 'children'), Input('dtLq2', 'children'), Input('pmd2', 'children'), Input('pmq2', 'children'), Input('dta2', 'children'),
     Input('dtA3', 'children'), Input('dtB3', 'children'),Input('dtLd3', 'children'), Input('dtLq3', 'children'), Input('pmd3', 'children'), Input('pmq3', 'children'), Input('dta3', 'children'),
     Input('dtA4', 'children'), Input('dtB4', 'children'), Input('dtLd4', 'children'), Input('dtLq4', 'children'), Input('pmd4', 'children'), Input('pmq4', 'children'), Input('dta4', 'children'),
     Input('dtA5', 'children'), Input('dtB5', 'children'), Input('dtLd5', 'children'), Input('dtLq5', 'children'), Input('pmd5', 'children'), Input('pmq5', 'children'), Input('dta5', 'children'),
     Input('dtA6', 'children'), Input('dtB6', 'children'), Input('dtLd6', 'children'), Input('dtLq6', 'children'), Input('pmd6', 'children'), Input('pmq6', 'children'), Input('dta6', 'children'),
     Input('DTnumDropDown','value')],Input('ldopt1', 'children'),Input('ldopt2', 'children'),Input('ldopt3', 'children'),Input('ldopt4', 'children'),Input('ldopt5', 'children'),Input('ldopt6', 'children')
     ,Input('lqopt1', 'children'),Input('lqopt2', 'children'),Input('lqopt3', 'children'),Input('lqopt4', 'children'),Input('lqopt5', 'children'),Input('lqopt6', 'children'),
     Input('pmdopt1', 'children'),Input('pmdopt2', 'children'),Input('pmdopt3', 'children'),Input('pmdopt4', 'children'),Input('pmdopt5', 'children'),Input('pmdopt6', 'children'),
     Input('VmEditField','children'),Input('DTlowEditField','children'),Input('DThighEditField','children'),Input('ModeDropDown','value'),Input('TypeDropDown','value'),
     Input('Hdcalfunc','value'),Input('Hqcalfunc','value'),Input('ConstantLdLqDropDown','value'),Input('TnflagDropDown','value'),Input('PeflagDropDown','value'),
     Input('speed1','children'),Input('speed2','children'),Input('speed3','children'),Input('speed4','children'),Input('speed5','children'),Input('speed6','children'),Input('InitialEditField','value'),Input('IncrementEditField','value'),Input('EffMaxSpeed','value'),
     prevent_initial_call=True,
     allow_duplicate=True

)

def update_output(nextlink,disable_n_clicks,dtA1, dtB1, dtLd1, dtLq1, pmd1, pmq1, dta1, 
                  dtA2, dtB2, dtLd2, dtLq2, pmd2, pmq2, dta2, 
                  dtA3, dtB3, dtLd3, dtLq3, pmd3, pmq3, dta3, 
                  dtA4, dtB4, dtLd4, dtLq4, pmd4, pmq4, dta4, 
                  dtA5, dtB5, dtLd5, dtLq5, pmd5, pmq5, dta5, 
                  dtA6, dtB6, dtLd6, dtLq6, pmd6, pmq6, dta6,
                  DTnumDropDown,ldopt1,ldopt2,ldopt3,ldopt4,ldopt5,ldopt6,
                  lqopt1,lqopt2,lqopt3,lqopt4,lqopt5,lqopt6,
                  pmdopt1,pmdopt2,pmdopt3,pmdopt4,pmdopt5,pmdopt6,VmEditField,
                  DTlowEditField,DThighEditField,ModeDropDown,
                  TypeDropDown,Hdcalfunc,Hqcalfunc,ConstantLdLqDropDown,TnflagDropDown,PeflagDropDown,
                  speed1,speed2,speed3,speed4,speed5,speed6,InitialEditField,IncrementEditField,EffMaxSpeed1
                  ):
    # resetab()
    global mot,inv,gear,tire,vhcl
    global DTtab,DTnum,ipm,a12
    global type,hdcalf,hqcalf,const,peflag,tnflag,Mode,EffMaxSpeed
    global ldopt,lqopt,pmdopt
    a12={}
    a12efftab = pd.read_excel("InputTableFile.xlsx", sheet_name="A12 Efficiency", header=1)
    a12efftab = a12efftab.fillna(0)
    a12['prpm']= a12efftab.iloc[:, 0].values
    a12['posId'] = a12efftab.iloc[:, 1].values
    a12['posIq'] = a12efftab.iloc[:, 2].values
    a12['nrpm'] = a12efftab.iloc[:, 10].values
    a12['negId'] = a12efftab.iloc[:, 11].values
    a12['negIq'] = a12efftab.iloc[:, 12].values
    a12['Te'] = a12efftab.iloc[:, 15].values
    a12['I'] = a12efftab.iloc[:, 13].values
    # global InitialEditField,IncrementEditField
    # print("nextlink",nextlink)
    EffMaxSpeed=EffMaxSpeed1
    if nextlink == False and disable_n_clicks == None:
        tab_values = [[float(dtA1), float(dtB1), float(dtLd1), float(dtLq1), float(pmd1), float(pmq1), float(dta1)],
                    [float(dtA2), float(dtB2), float(dtLd2), float(dtLq2), float(pmd2), float(pmq2), float(dta2)],
                    [float(dtA3), float(dtB3), float(dtLd3), float(dtLq3), float(pmd3), float(pmq3), float(dta3)],
                    [float(dtA4), float(dtB4), float(dtLd4), float(dtLq4), float(pmd4), float(pmq4), float(dta4)], 
                    [float(dtA5), float(dtB5), float(dtLd5), float(dtLq5), float(pmd5), float(pmq5), float(dta5)],
                    [float(dtA6), float(dtB6), float(dtLd6), float(dtLq6), float(pmd6), float(pmq6), float(dta6)]]
        
        ldopt = [float(value) for value in [ldopt1, ldopt2, ldopt3, ldopt4, ldopt5, ldopt6]]
        lqopt = [float(value) for value in [lqopt1, lqopt2, lqopt3, lqopt4, lqopt5, lqopt6]]
        pmdopt = [float(value) for value in [pmdopt1, pmdopt2, pmdopt3, pmdopt4, pmdopt5, pmdopt6]]


        Vm = float(VmEditField)
        
        DTtab = DigiTwin(mot['pole'],Vm,tab_values)
    
        dtA3 = DTtab[2, 0]
        dtB3 = DTtab[2, 1]
        dtLd3 = DTtab[2, 2]
        dtLq3 = DTtab[2, 3]
        pmd3 = DTtab[2, 4]
        pmq3 = DTtab[2, 5]
        dta3 = DTtab[2, 6]
        dtA6 = DTtab[5, 0]
        dtB6 = DTtab[5, 1]
        dtLd6 = DTtab[5, 2]
        dtLq6 = DTtab[5, 3]
        pmd6 = DTtab[5, 4]
        pmq6 = DTtab[5, 5]
        dta6 = DTtab[5, 6]

        DTnum = int(DTnumDropDown)

        mot['ld'] = DTtab[DTnum, 2]
        EditFieldDaxis = mot['ld']
        
        mot['lq'] = DTtab[DTnum, 3]
        EditFieldQaxis =mot['lq']
        
        mot['flux'] = DTtab[DTnum, 4]
        # print("mot['flux']",mot['flux'])
        EditFieldFlux = mot['flux']
        
        # Additional calculations
        mot['d'] = ( mot['lq'] - mot['ld']) *  mot['unit'] 
        mot['e'] = mot['lq'] / mot['ld']
        mot['If'] =  mot['flux']/ ( mot['ld'] *  mot['unit'] )

        AdjLdEditField = ldopt[DTnum]
        AdjLqEditField = lqopt[DTnum]
        AdjPMEditField = pmdopt[DTnum]

        type = float(TypeDropDown)
        hdcalf = float(Hdcalfunc)
        hqcalf = float(Hqcalfunc)
        const = float(ConstantLdLqDropDown)  
        peflag = float(TnflagDropDown)  
        tnflag = float(PeflagDropDown)
        Mode = int(ModeDropDown)

        Psid = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_d", header=1)
        Psid = Psid.iloc[0:, 2:].values
        Psiq = pd.read_excel("InputTableFile.xlsx", sheet_name="Psi_q", header=1)
        Psiq = Psiq.iloc[0:, 2:].values
        Omega = (Psid ** 2) + (Psiq ** 2)


        PLmat = PsiLdLq(mot['pole'],DTtab,hdcalf,hqcalf,type,DTnum,pmdopt[DTnum],ldopt[DTnum],lqopt[DTnum],Psid,Psiq,Omega)



        tuntable = pd.read_excel("InputTableFile.xlsx", sheet_name="tuning")
        PLmat['copy'] = tuntable['copy']

        tun = 1 # value fetched psipm  switch Psi_PMSwitchValueChanged
        if tun == 1:  # Psi_PM button is ON
            PLmat['tuning'] = list(tuntable['Tuning'])
        else:  # Psi_PM button is OFF
            PLmat['tuning'] = [1] * len(tuntable['Tuning'])

        ipm = ipmclass()
        ipm.initial = float(InitialEditField)
        ipm.increment = float(IncrementEditField)
        ipm.init(mot,DTtab,DTnum,PLmat,tnflag,peflag,const)
        
        stdspd,simtab=stdrpm(ipm.Id, ipm.Iq, ipm.Tn, ipm.rpm, ipm.Irms, a12)
        stdval,maxval,minval = stdnm_omega(Vm,mot['pole'],Mode,DTlowEditField,DThighEditField,Omega,simtab,PLmat['DTKk0'],PLmat['k0mat'])


        if DTnum == 0:
            stdrpm1 = stdspd
        else:
            stdrpm1 = float(speed1)

        if DTnum == 1:
            stdrpm2 = stdspd
        else:
            stdrpm2 = float(speed2)
        
        if DTnum == 2:
            stdrpm3 = stdspd
        else:
            stdrpm3 = float(speed3)

        if DTnum == 3:
            stdrpm4 = stdspd
        else:
            stdrpm4 = float(speed4)

        if DTnum == 4:
            stdrpm5 = stdspd
        else:
            stdrpm5 = float(speed5)

        if DTnum == 5:
            stdrpm6 = stdspd
        else:
            stdrpm6 = float(speed6)
        
        Min1EditField = minval[0]
        Max1EditField =maxval[0]
        Min2EditField = minval[1]
        Max2EditField =maxval[1]
        Min3EditField =minval[2]
        Max3EditField = maxval[2]
        Min4EditField =minval[3]
        Max4EditField = maxval[3]
        Min5EditField = minval[4]
        Max5EditField =maxval[4]
        Min6EditField = minval[5]
        Max6EditField = maxval[5]

        stdNm1 = stdval[0]
        stdNm2 =  stdval[1]
        stdNm3 = stdval[2]
        stdNm4 =  stdval[3]
        stdNm5 = stdval[4]
        stdNm6 = stdval[5]
        
        # return [dtA3]
        return (
        str(round(dtA3, 4)), str(round(dtB3, 4)), str(round(dtLd3, 4)), str(round(dtLq3, 4)),str(round(pmd3, 4)), str(round(pmq3, 4)), str(round(dta3, 4)),
        str(round(dtA6, 4)), str(round(dtB6, 4)), str(round(dtLd6, 4)), str(round(dtLq6, 4)), str(round(pmd6, 4)), str(round(dta6, 4)),
        str(round(AdjLdEditField, 4)),str(round(AdjLqEditField, 4)),str(round(AdjPMEditField, 4)),
        str(round(stdrpm1, 4)),str(round(stdrpm2, 4)),str(round(stdrpm3, 4)),str(round(stdrpm4, 4)),str(round(stdrpm5, 4)),str(round(stdrpm6, 4)),
        str(round(stdNm1, 4)),str(round(stdNm2, 4)),str(round(stdNm3, 4)),str(round(stdNm4, 4)),str(round(stdNm5, 4)),str(round(stdNm6, 4)),
        str(round(Min1EditField, 4)),str(round(Min2EditField, 4)),str(round(Min3EditField, 4)),str(round(Min4EditField, 4)),str(round(Min5EditField, 4)),str(round(Min6EditField, 4)),
        str(round(Max1EditField, 4)),str(round(Max2EditField, 4)),str(round(Max3EditField, 4)),str(round(Max4EditField, 4)),str(round(Max5EditField, 4)),str(round(Max6EditField, 4))
    )
    return [dash.no_update] * 40

#     return (
#     str(round(dtA3, 4)), str(round(dtB3, 4)), str(round(dtLd3, 4)), str(round(dtLq3, 4)),str(round(pmd3, 4)), str(round(pmq3, 4)), str(round(dta3, 4)),
#     str(round(dtA6, 4)), str(round(dtB6, 4)), str(round(dtLd6, 4)), str(round(dtLq6, 4)), str(round(pmd6, 4)), str(round(dta6, 4)),
#     str(round(dtif1, 4)), str(round(dtE1, 4)), str(round(Aif1, 4)), str(round(Bif1, 4)), str(round(dtif2, 4)), str(round(dtE2, 4)),
#     str(round(Aif2, 4)), str(round(Bif2, 4)), str(round(dtif3, 4)), str(round(dtE3, 4)), str(round(Aif3, 4)) ,str(round(Bif3, 4)), str(round(dtif4, 4)),
#     str(round(dtE4, 4)), str(round(Aif4, 4)), str(round(Bif4, 4)), str(round(dtif5, 4)), str(round(dtE5, 4)), str(round(Aif5, 4)),
#     str(round(Bif5, 4)), str(round(dtif6, 4)), str(round(dtE6, 4)), str(round(Aif6, 4)), str(round(Bif6, 4)), EditFieldDaxis, EditFieldQaxis, EditFieldFlux,
#     str(round(AdjLdEditField, 4)),str(round(AdjLqEditField, 4)),str(round(AdjPMEditField, 4)),str(round(Eopt1, 4)),str(round(Eopt2, 4)),str(round(Eopt3, 4)),
#     str(round(Eopt4, 4)),str(round(Eopt5, 4)),str(round(Eopt6, 4)),
#     str(round(stdrpm1, 4)),str(round(stdrpm2, 4)),str(round(stdrpm3, 4)),str(round(stdrpm4, 4)),str(round(stdrpm5, 4)),str(round(stdrpm6, 4)),
#     str(round(stdNm1, 4)),str(round(stdNm2, 4)),str(round(stdNm3, 4)),str(round(stdNm4, 4)),str(round(stdNm5, 4)),str(round(stdNm6, 4)),
#     str(round(Min1EditField, 4)),str(round(Min2EditField, 4)),str(round(Min3EditField, 4)),str(round(Min4EditField, 4)),str(round(Min5EditField, 4)),str(round(Min6EditField, 4)),
#     str(round(Max1EditField, 4)),str(round(Max2EditField, 4)),str(round(Max3EditField, 4)),str(round(Max4EditField, 4)),str(round(Max5EditField, 4)),str(round(Max6EditField, 4))
# )
@app.callback(
    [Output("td-tirerw","children"),
     Output("td-moi","children"),
     Output("td-dcp","children"),
     Output("td-dd","children"),
     Output("td-bc","children"),
     Output("td-cd","children"),
     Output("td-maxrpm","children"),
     Output("td-socPe","children"),
     Output("td-socPbtt","children"),
     Output("td-ploss","children"),
     Output("td-coploss","children"),
     Output("td-ironloss","children"),
     Output("td-invloss","children"),
     Output("td-strayloss","children"),
     Output("td-fricloss","children"),
     Output("td-winloss","children"),
     Output("td-effic","children"),
    Output("graphd1", "figure"),
     Output("graphd2", "figure"),
     Output("graphd3", "figure"),
     Output("graphd4", "figure"),
     Output("graphd5", "figure"),
     Output("graphd6", "figure"),
 
     ],
    [Input("dpedit","children"),
    Input('GravityEditField', 'value'),
    Input('frEditField', 'value'),
    Input('VWindEditField', 'value'),
    Input('CdEditField', 'value'),
    Input('AfEditField', 'value'),
    Input('pEditField', 'value'),
    Input('ndrEditField', 'value'),
    Input('sxEditField', 'value'),
    Input('RoadGradeEditField', 'value'),
    Input('LowEditField', 'value'),
    Input('MediumEditField', 'value'),
    Input('HighEditField', 'value'),
    Input('ExHighEditField', 'value'),
    Input('CrusPtnDropDown','value'),
    Input('Tn50','value'),
    Input('Tn100','value'),
    Input('Tn200','value'),
    Input('Tn300','value'),
     Input("tabs", "value")]
 
)
def reload_wltcdata(disable_n_clicks,GravityEditField, frEditField, VWindEditField,
    CdEditField, AfEditField, pEditField, ndrEditField, sxEditField,
    RoadGradeEditField, LowEditField, MediumEditField, HighEditField,
    ExHighEditField,CrusPtnDropDown1,Tn_50,Tn_100,Tn_200,Tn_300,tab):
    global ip,sx,lowf,midf,highf,exhif,CrusPtnDropDown,Tn50,Tn100,Tn200,Tn300,ev,gt,dpflag,ipm

    if disable_n_clicks == True:
        return [dash.no_update] * 23
            # return (dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
            # dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,
            # dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, 
            # go.Figure(), go.Figure(),go.Figure(), go.Figure(), go.Figure(), go.Figure())
        # return [dash.no_update] * 23
    
    ip['gravity'] = float(GravityEditField)
    ip['fr'] = float(frEditField)          
    ip['Vwind'] = float(VWindEditField)    
    ip['Cd'] = float(CdEditField)          
    ip['Af'] = float(AfEditField)          
    ip['p'] = float(pEditField)  
    sx = float(sxEditField)              
    ip['rdgrd'] = float(RoadGradeEditField)  
    CrusPtnDropDown = CrusPtnDropDown1
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "CrusPtnDropDown":
        dpflag = 0
        tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc = DrivepatternmodelingTabButtonDown()

    CrusPtnDropDown = CrusPtnDropDown1
 
    lowf = float(LowEditField )
    midf = float(MediumEditField )
    highf = float(HighEditField )
    exhif = float(ExHighEditField )
    Tn50=float(Tn_50)
    Tn100=float(Tn_100)
    Tn200=float(Tn_200)
    Tn300=float(Tn_300)

    if tab == "drive-pattern" and disable_n_clicks == None :
        print("fssjh")
        tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc=DrivepatternmodelingTabButtonDown()
        figured1 = SpeedAccelDecel(condition_value='1')
        figured2 = effMapTn(condition_value='1')
        figured3 = piegraph(condition_value='1')
        figured4= wltc_btt(condition_value='1')
        figured5 = effPower(condition_value='1')
        figured6= data_tabg1(condition_value='1')
        # PLossanalysisbyCurrentTabButtonDown()
        return tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc,figured1 ,figured2,figured3,figured4,figured5,figured6
    return [dash.no_update] * 23


@app.callback(
    [Output("MaxTempEditField","value"),
    Output("tab-mtpvweb","children"),
     Output("tab-maxpower","children"),
     Output("tab-maxtorque","children"),
     Output("tab-maxeff","children"),
     Output("tab-maxposeff","children"),
 
 
    Output("graph1", "figure"),
     Output("graph2", "figure"),
     Output("graph3", "figure"),
     Output("graph4", "figure"),
     Output("graph5", "figure"),
     Output("graph6", "figure"),
     ],
    [Input("AEditField","value"),
     Input("BEditField","value"),
     Input("CEditField","value"),
     Input("InitempEditField","value"),
     Input("RoomTempEditField","value"),
 
    Input('igbtModEditField','value'),
    Input('A1EditField', 'value'),
    Input('A0EditField', 'value'),
    Input('C3EditField', 'value'),
    Input('C2EditField', 'value'),
    Input('C1EditField', 'value'),
    Input('C0EditField', 'value'),
    Input('D3EditField', 'value'),
    Input('D2EditField', 'value'),
    Input('D1EditField', 'value'),
    Input('D0EditField', 'value'),
    Input('B1EditField', 'value'),
    Input('B0EditField', 'value'),
    Input('E3EditField', 'value'),
    Input('E2EditField', 'value'),
    Input('E1EditField', 'value'),
    Input('E0EditField', 'value'),
 
    Input('Pcuflag', 'value'),
    Input('Pfeflag', 'value'),
    Input('Pstrflag', 'value'),
    Input('Pfflag', 'value'),
    Input('Pwflag', 'value'),
    Input('Pinvflag', 'value'),
    Input('Tempflag', 'value'),
 
    Input('S1KEditField', 'value'),
    Input('S5KEditField', 'value'),
    Input('S10KEditField', 'value'),
    Input('S15KEditField', 'value'),
    Input("tabs", "value"),

    Input("ipmedit","children"),
     ],
)
def reload_data(aedit,bedit,cedit,inittemp,roomtem,modulation,A1_value, A0_value, C3_value, C2_value, C1_value, C0_value, D3_value, D2_value, D1_value, D0_value, B1_value, B0_value,
                 E3_value, E2_value, E1_value, E0_value,Pcuflag, Pfeflag, Pstrflag, Pfflag, Pwflag, Pinvflag, Tempflag,S1K_value,S5K_value,S10K_value,S15K_value,tab,ipmedit):
    
    if ipmedit == True:
        return [dash.no_update] * 12
    global Temp,igbt,S1K,S5K,S10K,S15K,Flag
    Temp={}
    Temp['A']=aedit
    Temp['B']=bedit
    Temp['C']=cedit
    Temp['iniTemp']=inittemp
    Temp['RoomT']=roomtem
 
    igbt={}
    igbt['modulation'] = float(modulation)
    igbt['A1'] = float(A1_value)
    igbt['A0'] = float(A0_value)
    igbt['C3'] = float(C3_value)
    igbt['C2'] = float(C2_value)
    igbt['C1'] = float(C1_value)
    igbt['C0'] = float(C0_value)
    igbt['D3'] = float(D3_value)
    igbt['D2'] = float(D2_value)
    igbt['D1'] = float(D1_value)
    igbt['D0'] = float(D0_value)
    igbt['B1'] = float(B1_value)
    igbt['B0'] = float(B0_value)
    igbt['E3'] = float(E3_value)
    igbt['E2'] = float(E2_value)
    igbt['E1'] = float(E1_value)
    igbt['E0'] = float(E0_value)
 
    Flag={}
 
    Flag['Pcu']=Pcuflag
    Flag['Pfe']=Pfeflag
    Flag['Pstr']=Pstrflag
    Flag['Pf']=Pfflag
    Flag['Pw']=Pwflag
    Flag['Pinv']=Pinvflag
    Flag['temp']=Tempflag
 
    S1K=S1K_value
    S5K=S5K_value
    S10K=S10K_value
    S15K=S15K_value
 
    if tab == "ipm" and ipmedit == None:
        tab_mtpvweb,tab_maxpower,tab_maxtorque,tab_maxeff,tab_maxposeff,maxt=IPMModelingTabButtonDown()
        figure1 = TorqueVsSpeed(condition_value='1')  
        figure2 = TempOnTnGraph(condition_value='1') 
        figure3 = PLoss(condition_value='1')  
        figure4 = PowerVsSpeed(condition_value='1') 
        figure5 = TempOnPower(condition_value='1') 
        figure6 = IdIqControl(condition_value='1')
        return maxt ,tab_mtpvweb,tab_maxpower,tab_maxtorque,tab_maxeff,tab_maxposeff,figure1, figure2, figure3, figure4, figure5, figure6
    return [dash.no_update] * 12

# @app.callback(
#     [Output("graphdt1", "figure"),
#      Output("graphdt2", "figure"),
#      Output("graphdt3", "figure"),
#      Output("graphdt4", "figure"),
#      Output("graphdt5", "figure"),
#      Output("graphdt6", "figure"),
#      ],
#       Input("tabs", "value"))
# def reload_datatab(tab):
#     global tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
#     if tab == "data":
#         if dpflag == 0:
#             tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc = DrivepatternmodelingTabButtonDown()
#         figuredt1 = data_tabg1()  
#         figuredt2 = data_tabg2() 
#         figuredt3 = data_tabg3() 
#         figuredt4 = data_tabg4()  
#         figuredt5 = data_tabg5() 
#         figuredt6 = data_tabg6()
#         return figuredt1, figuredt2, figuredt3, figuredt4, figuredt5, figuredt6
#     return [dash.no_update] * 6
    








@callback(
    Output("dt-drawer", "opened"),
    Input("dt-button", "n_clicks"),
    # State(f"drawer-size-{size}", "opened"),
    prevent_initial_call=True,
)
def open_dt_drawer(n_clicks):
    return True

@callback(
   
    Output("modal-tncurve", "opened"),
     Output("graph7", "figure"),
    Input("trqspd", "n_clicks"),
    State("modal-tncurve", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure7 =  lutpointsgraph()
    return not opened,figure7

@callback(
    Output("modal-tnpowerim", "opened"),
     Output("graph8", "figure"),
    Input("tnpowerim", "n_clicks"),
    State("modal-tncurve", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure8 = TnCurveButtonPushed()
    return not opened,figure8

@callback(
    Output("modal-totalcurve", "opened"),
     Output("graph9", "figure"),
    Input("totalcurve", "n_clicks"),
    State("modal-totalcurve", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure9 = TotalTorqueButtonPushed()
    return not opened,figure9

@callback(
    Output("modal-mtpa", "opened"),
     Output("graph10", "figure"),
    Input("mtpa", "n_clicks"),
    State("modal-mtpa", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure10 = MaxtorqueperCurrentButtonPushed()
    return not opened,figure10

@callback(
    Output("modal-isvspf", "opened"),
     Output("graph11", "figure"),
    Input("isvspf", "n_clicks"),
    State("modal-isvspf", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure11 = IsVsPfButtonPushed()
    return not opened,figure11

@callback(
    Output("modal-a12id", "opened"),
     Output("graph12", "figure"),
    Input("a12id", "n_clicks"),
    State("modal-a12id", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure12 = efficiency_map()
    return not opened,figure12

@callback(
    Output("modal-idiqtemp", "opened"),
     Output("graph13", "figure"),
    Input("idiqtemp", "n_clicks"),
    State("modal-idiqtemp", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure13 = IdIqControlMapByTemp()
    return not opened,figure13

@callback(
    Output("modal-idiqtor", "opened"),
     Output("graph14", "figure"),
    Input("idiqtor", "n_clicks"),
    State("modal-idiqtor", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure14 = IdIqControlMapByTorque()
    return not opened,figure14


@callback(
    Output("modal-tempprof", "opened"),
     Output("graph15", "figure"),
    Input("tempprof", "n_clicks"),
    State("modal-tempprof", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure15 = TempProfile()
    return not opened,figure15

@callback(
    Output("modal-plosslmc", "opened"),
     Output("graph16", "figure"),
    Input("plosslmc", "n_clicks"),
    State("modal-plosslmc", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure16 = Ploss_lmc()
    return not opened,figure16

@callback(
    Output("modal-cursd1", "opened"),
     Output("cursd1", "figure"),
    Input("btn-cursd1", "n_clicks"),
    State("modal-cursd1", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CruisingdistanceandbatterybysimulationandpoleButtonPushed()
    return not opened,figure


@callback(
    Output("modal-cursd2", "opened"),
     Output("cursd2", "figure"),
    Input("btn-cursd2", "n_clicks"),
    State("modal-cursd2", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CruisingdistanceandbatterybysimulationmodelButtonPushed()
    return not opened,figure

@callback(
    Output("modal-cursd3", "opened"),
     Output("cursd3", "figure"),
    Input("btn-cursd3", "n_clicks"),
    State("modal-cursd3", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CruisingdistanceandbatterybygearratioButtonPushed()
    return not opened,figure

@callback(
    Output("modal-cursd4", "opened"),
     Output("cursd4", "figure"),
    Input("btn-cursd4", "n_clicks"),
    State("modal-cursd4", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CruisingdistanceandbatterybyIdcButtonPushed()
    return not opened,figure


@callback(
    Output("modal-cursd5", "opened"),
     Output("cursd5", "figure"),
    Input("btn-cursd5", "n_clicks"),
    State("modal-cursd5", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CruisingdistanceandbatterybyTireinchButtonPushed()
    return not opened,figure


@callback(
    Output("modal-cursd6", "opened"),
     Output("cursd6", "figure"),
    Input("btn-cursd6", "n_clicks"),
    State("modal-cursd6", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = PlossbyWLTCzonesButtonPushed()
    return not opened,figure

@callback(
    Output("modal-cursd7", "opened"),
     Output("cursd7", "figure"),
    Input("btn-cursd7", "n_clicks"),
    State("modal-cursd7", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = IdIqcontrolMapButtonPushed()
    return not opened,figure

@callback(
    Output("modal-cursd8", "opened"),
     Output("cursd8", "figure"),
    Input("btn-cursd8", "n_clicks"),
    State("modal-cursd8", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = IdvsIqPlot()
    return not opened,figure

@callback(
    Output("modal-clctenergy", "opened"),
     Output("datag1", "figure"),
    Input("clctenergy", "n_clicks"),
    State("modal-clctenergy", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = CLTCButtonPushed()
    return not opened,figure

@callback(
    Output("modal-batderser", "opened"),
     Output("datag2", "figure"),
    Input("batderser", "n_clicks"),
    State("modal-batderser", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = BatteryderatingseriesButtonPushed()
    return not opened,figure

@callback(
    Output("modal-motorspecs", "opened"),
     Output("datag3", "figure"),
    Input("motorspecs", "n_clicks"),
    State("modal-motorspecs", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = MotorSpecificationsButtonPushed()
    return not opened,figure

@callback(
    Output("modal-kwleaf", "opened"),
     Output("datag4", "figure"),
    Input("kwleaf", "n_clicks"),
    State("modal-kwleaf", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure = kWLeafButtonPushed()
    return not opened,figure
# Callback to update cell click count and determine color

#ploss torque


@app.callback(
    Output('TnFrequencyTab', 'data'),
    Output('TnFreePtsTab', 'columns'),
    Output('TnFreePtsTab', 'data'),
    Output('TnFreePtsTab', 'style_data_conditional'),
    Output('click-counts-Tn', 'data'),
    Input("tabs", "value"),
    Input('TnFreePtsTab', 'active_cell'),
    Input("clear_tn","n_clicks"),
    State('click-counts-Tn', 'data')
)
def PLossanalysisbyTorqueTabButtonDown(tab, active_cell, clicks, click_counts):

    global tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
    global dp, curflag, plTnflag, dpflag, TnScale, TnN, Tntab
    global TnScale_init,TnScale_inc,Tnfreqmap
 
    curflag = 5
 
    if tab != "ploss-torque":
        return [], [], [], [], {}
    
    if plTnflag == 1:
        dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
    
    if dpflag == 0:
        tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc=DrivepatternmodelingTabButtonDown()
    dp.Tn = np.array(dp.Tn)
    dp.n = np.array(dp.n)
    dp.werpm = np.array(dp.werpm)
   
    TnScale_init = np.ceil(np.max(dp.Tn) / 10) * 10
    TnScale_inc = (TnScale_init - np.floor(min(dp.Tn)/10) * 10) / 20
 
    TnN = np.zeros(dp.num)
    TnN[dp.n > 0] = 1
 
    xax = TnScale_init - np.arange(21) * TnScale_inc
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
 
    Tnfreqmap = np.zeros((len(xax) - 1, len(yax) - 1))
 
    for ind in range(len(xax) - 1):
        for idx in range(len(yax) - 1):
            Tnfreqmap[ind, idx] = np.sum(
                (dp.werpm >= yax[idx]) &
                (dp.werpm < yax[idx + 1]) &
                (dp.Tn > xax[ind + 1]) &
                (dp.Tn <= xax[ind])
            )
    TnFrequencyTab_data = Tnfreqmap.tolist()
 
    TnFrequencyTab_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, TnFrequencyTab_data)]
    TnFrequencyTab_data.insert(0, ColNames)
 
    # Combine data
    res = {
        "body": TnFrequencyTab_data
    }
 
 
    Tntab = np.zeros_like(Tnfreqmap)
 
    stlind = Tnfreqmap == 0
    Tntab[stlind] = 1
 
    # Prepare DataFrame for the DataTable
    fillertab = np.full((len(RowNames), len(ColNames) - 1), "", dtype=str)  # Reduced by 1 as we'll add RowNames
    df = pd.DataFrame(fillertab, columns=ColNames[1:], index=RowNames)  # Skip first column name for df
 
    # Insert RowNames as the first column
    df.insert(0, ColNames[0], RowNames)
 
    # Define style for cells where Tnfreqmap == 0
    style_data_conditional = [
        {
            'if': {
                'row_index': row,
                'column_id': ColNames[col + 1]  # +1 to adjust for the new first column
            },
            'backgroundColor': 'black',
            'color': 'white'
        }
        for row, col in zip(*np.where(stlind))
    ]
 
    cols = [{"name": col, "id": col} for col in df.columns]
 
    # return res, cols, df.to_dict('records'), style_data_conditional
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "clear_tn":
        return res, cols, df.to_dict('records'), style_data_conditional, {}
    # Handle cell clicks to toggle between pink and white
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']

        if col != ColNames[0]:  # Ignore clicks on the first column (row headers)
            cell_id = f"{row}-{col}"

            # Check if the cell is black
            is_black_cell = any(
                style['if']['row_index'] == row and style['if']['column_id'] == col and style['backgroundColor'] == 'black'
                for style in style_data_conditional
            )

            if not is_black_cell:  # Only proceed if the cell is not black
                pink_cells_count = sum(1 for count in click_counts.values() if count % 2 == 1)

                if cell_id in click_counts:
                    if click_counts[cell_id] % 2 == 1:  # If pink, allow it to turn white
                        click_counts[cell_id] += 1
                    elif pink_cells_count < 20:  # If white, allow it to turn pink if less than 20 pink cells
                        click_counts[cell_id] += 1
                else:
                    if pink_cells_count < 20:
                        click_counts[cell_id] = 1

    # Style pink and white cells based on click counts
    for cell_id, count in click_counts.items():
        row, col = cell_id.split('-', 1)
        row = int(row)
        if col != ColNames[0]:  # Skip styling for the first column
            if count % 2 == 1:  # Odd clicks - pink
                style_data_conditional.append({
                    'if': {'row_index': row, 'column_id': col},
                    'backgroundColor': 'pink'
                })
            else:  # Even clicks - white
                style_data_conditional.append({
                    'if': {'row_index': row, 'column_id': col},
                    'backgroundColor': 'white'
                })

    plTnflag = 1
    return res, cols, df.to_dict('records'), style_data_conditional, click_counts
 


 
@app.callback(
    Output('Next_TnLossButton', 'disabled'),
    [Input('click-counts-Tn', 'data'),
     Input('TnLossModeDD', 'value')]
)
def toggle_button(click_counts,TnLossModeDD):
    global Tnpoints
    Tnpoints = []
    mode = int(TnLossModeDD)
    if mode == 1:
        return False
 
    # Define the mapping of column ranges to their indices
    column_map = {
        "0 - 1000": 0,
        "1000 - 2000": 1,
        "2000 - 3000": 2,
        "3000 - 4000": 3,
        "4000 - 5000": 4,
        "5000 - 6000": 5,
        "6000 - 7000": 6,
        "7000 - 8000": 7,
        "8000 - 9000": 8,
        "9000 - 10000": 9,
        "10000 - 11000": 10,
        "11000 - 12000": 11,
        "12000 - 13000": 12,
        "13000 - 14000": 13,
        "14000 - 15000": 14,
        "15000 - 16000": 15,
        "16000 - 17000": 16,
        "17000 - 18000": 17,
        "18000 - 19000": 18,
        "19000 - 20000": 19
    }
 
 
    # Count the number of cells currently colored pink
    pink_cells_count = sum(1 for count in click_counts.values() if count % 2 == 1)
 
    # Check if there are exactly 20 pink cells
    if pink_cells_count == 20:
        for key, value in click_counts.items():
            if value % 2 == 1:  # Only consider cells that are currently pink
                split_key = key.split('-')
               
                # Extract row and column range
                if len(split_key) == 3:
                    row = int(split_key[0])
                    col_range = f"{split_key[1].strip()} - {split_key[2].strip()}"
                   
                    # Translate the column range to its corresponding index
                    col = column_map.get(col_range, None)
                   
                    if col is not None:
                        Tnpoints.append((row, col))  # Store as tuple (row, col)
 
    # Enable the button only if there are exactly 20 pink cells
    return pink_cells_count < 20
 
 
 
@app.callback(
    Output('TnFreePtsTab', 'cell_selectable'),
    [Input('TnLossModeDD', 'value')]
)
def update_table(selected_value):
    if selected_value is None:
        return False
   
    if selected_value == "1":
        return False
    else:
        return True
   
def ploss_torque1(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  
        xaxis_tickfont=dict(color="white"),    
        yaxis_tickfont=dict(color="white"),    
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,
        yaxis_zeroline=False,  
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig
 
@app.callback(
    Output("tnlosstype1textsetpoints","children"),
    Output("tnlosstype1Text", "children"),
    Output('TnLossTab1', 'data'),
    Output('tn-graph1','figure'),
    [Input('TnLoss1', 'value'),
     Input('TnAvg1', 'value')]
)
def update_table(selected_value,TnAvg1):
    global TnLosstype1,TnLoss1,TnLoss1_data1,matf1,avg1
    avg1 = int(TnAvg1)

    TnLoss1={}
    global TnScale_init,TnScale_inc,Tnfreqmap,dp
 
    if selected_value is None:
        return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Tn at set points",
        "2": "Pe(kWh) by Tn at set points",
        "3": "Pe(kW/s) by Tn at set points",
        "4": "Pcu(kW) by Tn at set points",
        "5": "Pfe(kW) by Tn at set points",
        "6": "Pstr(kW) by Tn at set points",
        "7": "Pf(kW) by Tn at set points",
        "8": "Pw(kW) by Tn at set points",
        "9": "Pinv(kW) by Tn at set points",
        "10": "sum Ploss(kW) by Tn at set points",
        "11": "Temp by Tn at set points",
        "12": "η = Pe/Pbatt by Tn at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
    dp.Pf = np.array(dp.Pf)
    if selected_value == "1":
        TnLosstype1 = dp.condPe
    elif selected_value == "2":
        TnLosstype1 = dp.Pekwh
    elif selected_value == "3":
        TnLosstype1 = dp.Pekws
    elif selected_value == "4":
        TnLosstype1 = dp.Pcu
    elif selected_value == "5":
        TnLosstype1 = dp.Pfe
    elif selected_value == "6":
        TnLosstype1 = dp.Pstr
    elif selected_value == "7":
        TnLosstype1 = dp.Pf
    elif selected_value == "8":
        TnLosstype1 = dp.Pw
    elif selected_value == "9":
        TnLosstype1 = dp.Pinv
    elif selected_value == "10":
        TnLosstype1 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        TnLosstype1 = dp.Temp
    elif selected_value == "12":
        TnLosstype1 = dp.n
 
    xax = TnScale_init - np.arange(0, 21) * TnScale_inc
    mat = LossTypeCalc(Tnfreqmap, avg1, TnLosstype1, dp.Tn,dp.werpm, xax)
    matf1 = mat
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
 
    # TnLoss1['data'] = mat.tolist()
    TnLoss1_data = mat.tolist()
    TnLoss1_data1 = mat.tolist()
 
    TnLoss1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, TnLoss1_data)]
    TnLoss1_data.insert(0, ColNames)
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
    # Combine data
    res = {
        "body": TnLoss1_data
    }
 
    
    fig = ploss_torque1(matf1)
 
    return selected_label1,selected_label,res,fig
 
def ploss_torque2(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig
 
@app.callback(
    Output("tnlosstype2textsetpoints","children"),
    Output("tnlosstype2Text", "children"),
    Output('TnLossTab2', 'data'),
    Output('tn-graph2','figure'),
    [Input('TnLoss2', 'value'),
     Input('TnAvg2', 'value')]
)
def update_table(selected_value,TnAvg2):
    global TnLosstype2,TnLoss2,matf2,avg2
    avg2 = int(TnAvg2)    
    TnLoss2 = {}
    global TnScale_init,TnScale_inc,Tnfreqmap,dp
 
    if selected_value is None:
        return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Tn at set points",
        "2": "Pe(kWh) by Tn at set points",
        "3": "Pe(kW/s) by Tn at set points",
        "4": "Pcu(kW) by Tn at set points",
        "5": "Pfe(kW) by Tn at set points",
        "6": "Pstr(kW) by Tn at set points",
        "7": "Pf(kW) by Tn at set points",
        "8": "Pw(kW) by Tn at set points",
        "9": "Pinv(kW) by Tn at set points",
        "10": "sum Ploss(kW) by Tn at set points",
        "11": "Temp by Tn at set points",
        "12": "η = Pe/Pbatt by Tn at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
    dp.Pf = np.array(dp.Pf)
    if selected_value == "1":
        TnLosstype2 = dp.condPe
    elif selected_value == "2":
        TnLosstype2 = dp.Pekwh
    elif selected_value == "3":
        TnLosstype2 = dp.Pekws
    elif selected_value == "4":
        TnLosstype2 = dp.Pcu
    elif selected_value == "5":
        TnLosstype2 = dp.Pfe
    elif selected_value == "6":
        TnLosstype2 = dp.Pstr
    elif selected_value == "7":
        TnLosstype2 = dp.Pf
    elif selected_value == "8":
        TnLosstype2 = dp.Pw
    elif selected_value == "9":
        TnLosstype2 = dp.Pinv
    elif selected_value == "10":
        TnLosstype2 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        TnLosstype2 = dp.Temp
    elif selected_value == "12":
        TnLosstype2 = dp.n
 
    xax = TnScale_init - np.arange(0, 21) * TnScale_inc
    mat = LossTypeCalc(Tnfreqmap, avg2, TnLosstype2, dp.Tn,dp.werpm, xax)
    matf2 = mat
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
 
 
    TnLoss1_data = mat.tolist()
    TnLoss2['data'] = mat.tolist()
 
    TnLoss1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, TnLoss1_data)]
    TnLoss1_data.insert(0, ColNames)
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
    # Combine data
    res = {
        "body": TnLoss1_data
    }
 
    fig =  ploss_torque2(matf2)

    return selected_label1,selected_label,res,fig
 

def ploss_torque3(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig


@app.callback(
    Output("tnlosstype3textsetpoints","children"),
    Output("tnlosstype3Text", "children"),
    Output('TnLossTab3', 'data'),
    Output('tn-graph3','figure'),
    [Input('TnLoss3', 'value'),
     Input('TnAvg3', 'value')]
)
def update_table(selected_value,TnAvg3):
    global TnLosstype3,TnLoss3,matf3,avg3
    avg3 = int(TnAvg3)
    TnLoss3 = {}
    global TnScale_init,TnScale_inc,Tnfreqmap,dp
 
    if selected_value is None:
        return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Tn at set points",
        "2": "Pe(kWh) by Tn at set points",
        "3": "Pe(kW/s) by Tn at set points",
        "4": "Pcu(kW) by Tn at set points",
        "5": "Pfe(kW) by Tn at set points",
        "6": "Pstr(kW) by Tn at set points",
        "7": "Pf(kW) by Tn at set points",
        "8": "Pw(kW) by Tn at set points",
        "9": "Pinv(kW) by Tn at set points",
        "10": "sum Ploss(kW) by Tn at set points",
        "11": "Temp by Tn at set points",
        "12": "η = Pe/Pbatt by Tn at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Pf= np.array(dp.Pf)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
 
    if selected_value == "1":
        TnLosstype3 = dp.condPe
    elif selected_value == "2":
        TnLosstype3 = dp.Pekwh
    elif selected_value == "3":
        TnLosstype3 = dp.Pekws
    elif selected_value == "4":
        TnLosstype3 = dp.Pcu
    elif selected_value == "5":
        TnLosstype3 = dp.Pfe
    elif selected_value == "6":
        TnLosstype3 = dp.Pstr
    elif selected_value == "7":
        TnLosstype3 = dp.Pf
    elif selected_value == "8":
        TnLosstype3 = dp.Pw
    elif selected_value == "9":
        TnLosstype3 = dp.Pinv
    elif selected_value == "10":
        TnLosstype3 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        TnLosstype3 = dp.Temp
    elif selected_value == "12":
        TnLosstype3 = dp.n
 
    xax = TnScale_init - np.arange(0, 21) * TnScale_inc
    mat = LossTypeCalc(Tnfreqmap, avg3, TnLosstype3, dp.Tn,dp.werpm, xax)
    matf3 = mat
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
 
 
    TnLoss1_data = mat.tolist()
    TnLoss3['data']  = mat.tolist()
 
    TnLoss1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, TnLoss1_data)]
    TnLoss1_data.insert(0, ColNames)
 
    # Combine data
    res = {
        "body": TnLoss1_data
    }
 
    fig = ploss_torque3(matf3)
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
    return selected_label1,selected_label,res,fig
 
def TnLoss(y1,ord1):
    # y1 = y1 / y1.sum(axis=1, keepdims=True)
    y1_percentage  = y1 / y1.sum(axis=1)[:, None]
    ord1 = np.array(ord1)
    reversed_ord1 = ord1[::-1]
 
 
    # Use boolean indexing to select rows where ord1 is True
    result = y1_percentage[reversed_ord1 != 0, :]
 
    # Create a list of categories for the bars
    categories = ['Pcu(kW)', 'Pfe(kW)', 'Pstr(kW)', 'Pf(kW)', 'Pw(kW)', 'Pinv(kW)']
 
    # Create a list of colors for the bars
    colors = ['#a4a4a4', '#febc05','#51a3c6' ,'#70ae3f', '#254478', '#a1460b']
 
    # Initialize the figure
    fig = go.Figure()
 
    # Create stacked bar traces for each category
    for i in range(len(categories)):
        fig.add_trace(go.Bar(
            y=np.arange(result.shape[0]),
            x=result[:, i],
            orientation='h',
            name=categories[i],
            marker=dict(color=colors[i]),
            text=result[:, i],
            hoverinfo='x+name'  # Show the values and category name in hover text
        ))
 
    print("ord1",ord1)
    custom_y_ticks = list(range(20))
    # Customize the layout
    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title='Y-Axis Title',
            # range=[0.5,len(y1) + 0.5],
            tickvals=custom_y_ticks,  # Set the custom tick positions
            ticktext=[f' {round(ord1[i],3)}' for i in custom_y_ticks],  # Set custom tick labels
        ),  # Set y-axis range
        xaxis=dict(title='Values', range=[0, 1]),  # Set the x-axis range to [0, 1]
        # title='Stacked Horizontal Bar Chart',
        legend=dict(
            title='Categories',
            title_font=dict(color='white'),  # Set legend title color to white
            font=dict(color='white'),  # Set legend text color to white
        ),
        showlegend=True
    )
    # fig.update_layout(title='WLTC-Ploss by Tn at set points',height=400)
    fig.update_layout(
            title_font={'size': 15, 'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis_showline=False,  # Make y-axis line invisible
            yaxis_zeroline=False,  # Make y-axis zero line invisible
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
 
        )
    # fig.update_xaxes(range=[0, np.max(np.sum(y1, axis=1))], showline=True, linecolor='white')
    # fig.update_yaxes(range=[0.5, len(y1) + 0.5], tickvals=ord1, showline=True, linecolor='#4DBEEE')
    # Show the plot
    fig.update_layout(showlegend=True)
    return fig
 
def ImLoss_Current(y1,ord1):
    # y1 = y1 / y1.sum(axis=1, keepdims=True)
    y1_percentage  = y1 / y1.sum(axis=1)[:, None]
    ord1 = np.array(ord1)
    reversed_ord1 = ord1[::-1]
 
 
    # Use boolean indexing to select rows where ord1 is True
    result = y1_percentage[reversed_ord1 != 0, :]
 
    # Create a list of categories for the bars
    categories = ['Pcu(kW)', 'Pfe(kW)', 'Pstr(kW)', 'Pf(kW)', 'Pw(kW)', 'Pinv(kW)']
 
    # Create a list of colors for the bars
    colors = ['#a4a4a4', '#febc05','#51a3c6' ,'#70ae3f', '#254478', '#a1460b']
 
    # Initialize the figure
    fig = go.Figure()
 
    # Create stacked bar traces for each category
    for i in range(len(categories)):
        fig.add_trace(go.Bar(
            y=np.arange(result.shape[0]),
            x=result[:, i],
            orientation='h',
            name=categories[i],
            marker=dict(color=colors[i]),
            text=result[:, i],
            hoverinfo='x+name'  # Show the values and category name in hover text
        ))
 
 
    custom_y_ticks = list(range(20))
    # Customize the layout
    fig.update_layout(
        barmode='stack',
        yaxis=dict(
            title='Y-Axis Title',
            tickvals=custom_y_ticks,  # Set the custom tick positions
            ticktext=[f' {round(ord1[i],3)}' for i in custom_y_ticks],  # Set custom tick labels
        ),  # Set y-axis range
        xaxis=dict(title='Values', range=[0, 1]),  # Set the x-axis range to [0, 1]
        # title='Stacked Horizontal Bar Chart',
        legend=dict(
            title='Categories',
            title_font=dict(color='white'),  # Set legend title color to white
            font=dict(color='white'),  # Set legend text color to white
        ),
        showlegend=True
    )
    # fig.update_layout(title='WLTC-Ploss by Current at set points',height=400)
    fig.update_layout(
            title_font={'size': 15, 'color': 'white'},
            paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
            xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
            yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
            xaxis_title_font=dict(color="white"),
            yaxis_showline=False,  # Make y-axis line invisible
            yaxis_zeroline=False,  # Make y-axis zero line invisible
            xaxis_showline=False,
            xaxis_showgrid=False,
            xaxis_zeroline=False,
            yaxis_showgrid=False,
            margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
 
        )
    # Show the plot
    fig.update_layout(showlegend=True)
    return fig

@callback(
    Output("ploss-torque-modal", "opened"),
    Output("Tn-drawer", "opened"),
    Output("OrderTableTn1","data"),
    Output("OrderTableTn2","data"),
    Output("OrderTableTn3","data"),
    Output("LossPointTableTn1","data"),
    Output("LossPointTableTn2","data"),
    Output("LossPointTableTn3","data"),
    Output('graphTn1','figure'),
    Output('graphTn2','figure'),
    Output('graphTn3','figure'),
    Input("Next_TnLossButton", "n_clicks"),
    Input('TnLossModeDD', 'value'),
    Input('TnLoss1', 'value'),
    Input('TnLoss2', 'value'),
    Input('TnLoss3', 'value'),
    State("ploss-torque-modal", "opened"),
    prevent_initial_call=True,
)
def Next_TnLossButtonPushed(n_clicks,TnLossModeDD,Tndrrop1,Tndrrop2,Tndrrop3,opened):
    global Tnpoints,ptx,pty
    global TnScale_init,TnScale_inc
    global dp,TnLosstype1, TnLosstype2, TnLosstype3,TnN,avg1,avg2,avg3,y1,ord11,y3,ord33,y2,ord22
    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "Next_TnLossButton":
        
        if Tndrrop1 is None or Tndrrop2 is None or Tndrrop3 is None:
            return not opened,False,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
        
        mode = int(TnLossModeDD)


        if mode == 1:
            ptx = []
            pty = []
        else:
            ptx = [point[0] for point in Tnpoints]
            pty = [point[1] for point in Tnpoints]
    
    
        arr = np.arange(0, 100001, 1000)
        num = len(arr)
        winit = 1000
    
        w1 = np.repeat(arr, 50)
        w2 = w1 + winit
    
        Tn1 = TnScale_init - np.arange(0,50) * TnScale_inc
        Tn1 = np.tile(Tn1, num)
        Tn2 = Tn1 - TnScale_inc
    
    
        sigman = np.zeros(num * 50)
        sumarray1 = np.zeros(num * 50)
        sumarray2 = np.zeros(num * 50)
        sumarray3 = np.zeros(num * 50)
        sumPcu = np.zeros(num * 50)
        sumPFe = np.zeros(num * 50)
        sumPstr = np.zeros(num * 50)
        sumPf = np.zeros(num * 50)
        sumPw = np.zeros(num * 50)
        sumPinv = np.zeros(num * 50)
        for idx in range(num * 50):
            condition = (dp.werpm >= w1[idx]) & (dp.werpm < w2[idx]) & (dp.Tn > Tn2[idx]) & (dp.Tn <= Tn1[idx])
    
            sigman[idx] = np.sum(TnN[condition])  # Column AE
            sumarray1[idx] = np.sum(TnLosstype1[condition])
            sumarray2[idx] = np.sum(TnLosstype2[condition])
            sumarray3[idx] = np.sum(TnLosstype3[condition])
            sumPcu[idx] = np.sum(dp.Pcu[condition])  # Column AJ
            sumPFe[idx] = np.sum(dp.Pfe[condition])  # Column AK
            sumPstr[idx] = np.sum(dp.Pstr[condition])  # Column AL
            sumPf[idx] = np.sum(dp.Pf[condition])  # Column AM
            sumPw[idx] = np.sum(dp.Pw[condition])  # Column AN
            sumPinv[idx] = np.sum(dp.Pinv[condition])  # Column AO
    
    
        if avg1 == 1:
            sumarray1[sigman > 0] = sumarray1[sigman > 0] / sigman[sigman > 0]
    
        if avg2 == 1:
            sumarray2[sigman > 0] = sumarray2[sigman > 0] / sigman[sigman > 0]
    
        if avg3 == 1:
            sumarray3[sigman > 0] = sumarray3[sigman > 0] / sigman[sigman > 0]
    
    
    
        xax = TnScale_init - np.arange(21) * TnScale_inc
        yax = np.arange(21) * 1000
        numx = len(xax) - 1
        numy = len(yax) - 1
    
    
        colnames = ['','Order', 'Pcu(kW)', 'Pfe(kW)', 'Pstr(kW)', 'Pf(kW)', 'Pw(kW)', 'Pinv(kW)']
        rownames = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10']
    
    
        mat1 = np.array(TnLoss1_data1)
        ord11, y1 = OrdMatCalc(mode, mat1, np.round(sumarray1, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord1 = ord11.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord1, np.round(y1,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        OrderTableTn1 = {
            "body": table_data
        }
    
        mat2 = np.array(TnLoss2['data'])
        ord22, y2 = OrdMatCalc(mode, mat2, np.round(sumarray2, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord2 = ord22.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord2, np.round(y2,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        OrderTableTn2 = {
            "body": table_data
        }
    
    
        mat3 = np.array(TnLoss3['data'])
        ord33, y3 = OrdMatCalc(mode, mat3, np.round(sumarray3, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord3 = ord33.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord3, np.round(y3,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        OrderTableTn3 = {
            "body": table_data
        }
    
    
        Ordtab1 = np.zeros((numx, numy))
        Ordtab2 = np.zeros((numx, numy))
        Ordtab3 = np.zeros((numx, numy))
    
        Ordtab1[np.isin(mat1, ord1)] = mat1[np.isin(mat1, ord1)]
        Ordtab2[np.isin(mat2, ord2)] = mat2[np.isin(mat2, ord2)]
        Ordtab3[np.isin(mat3, ord3)] = mat3[np.isin(mat3, ord3)]
    
        ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
        ColNames = [" "] +  ColNames
        RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
    
    
        Ordtab1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, Ordtab1.tolist())]
        Ordtab1_data.insert(0, ColNames)
        LossPointTableTn1 = {
            "body": Ordtab1_data
        }
    
        Ordtab2_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, Ordtab2.tolist())]
        Ordtab2_data.insert(0, ColNames)
        LossPointTableTn2 = {
            "body": Ordtab2_data
        }
    
        Ordtab3_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, Ordtab3.tolist())]
        Ordtab3_data.insert(0, ColNames)
        LossPointTableTn3 = {
            "body": Ordtab3_data
        }
    
        fig1 = TnLoss(y1,ord11)
        fig2 = TnLoss(y2,ord22)
        fig3 = TnLoss(y3,ord33)
    
        return opened,True,OrderTableTn1,OrderTableTn2,OrderTableTn3,LossPointTableTn1,LossPointTableTn2,LossPointTableTn3,fig1,fig2,fig3
    else:
        return [dash.no_update]*11
@app.callback(
    Output('TncurrentTab', 'data'),
    Output('CurrentFreePtsTab', 'columns'),
    Output('CurrentFreePtsTab', 'data'),
    Output('CurrentFreePtsTab', 'style_data_conditional'),
    Output('click-counts', 'data'),  # Add this Output to update the click counts
    Input("tabs", "value"),
    Input('CurrentFreePtsTab', 'active_cell'),  # Add this Input for detecting cell clicks
    Input("clear_im",'n_clicks'),
    State('click-counts', 'data')  # Add this State to get the current click counts
)
def PLossanalysisbyCurrentTabButtonDown(tab, active_cell, clicks, click_counts):
    global dp, curflag, plTnflag, dpflag, TnScale, TnN, Tnfreqmap, Tntab,ImScale_init,ImScale_inc,Imfreqmap_data1,Imfreqmap,ImN
    global tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc
    curflag = 6

    if tab != "ploss-current":
        return [], [], [], [], {}
    
    if plImflag == 1:
        dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
    
    if dpflag == 0:
        tirerw,moi,dcp,Drive_distance,bat_consumption,cruis_distance,Max_rpm,socPe,socPbtt,ploss_td,cop_loss,Iron_loss,Inverter_loss,stray_loss,friction_loss,Windage_loss,effc=DrivepatternmodelingTabButtonDown()

    dp.Id = np.array(dp.Id)
    dp.Iq = np.array(dp.Iq)
    dp.n = np.array(dp.n)

    ImN = np.zeros(dp.num)
    for idx in range(dp.num):
        if dp.n[idx] > 0:
            ImN[idx] = 1
        else:
            ImN[idx] = 0
            
    ImN[dp.n > 0] = 1
    dp.Im = np.sqrt((dp.Id)**2 + (dp.Iq)**2)  # Column Z
    ImScale_init = np.ceil(np.max(dp.Im) / 10) * 10
    # ImScale_init = np.round(np.max(dp.Im), -1)  # Cell BI3
    ImScale_inc = ImScale_init / 20  # Cell BI2

    xax = ImScale_init - np.arange(21) * ImScale_inc
    yax = np.arange(21) * 1000

    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] + ColNames
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]

    Imfreqmap = np.zeros((len(xax) - 1, len(yax) - 1))

    for ind in range(len(xax) - 1):
        for idx in range(len(yax) - 1):
            Imfreqmap[ind, idx] = np.sum(
                (dp.werpm >= yax[idx]) &
                (dp.werpm < yax[idx + 1]) &
                (dp.Im > xax[ind + 1]) &
                (dp.Im <= xax[ind])
            )
    Imfreqmap_data = Imfreqmap.tolist()

    Imfreqmap_data1 = [[row_name] + row_data for row_name, row_data in zip(RowNames, Imfreqmap_data)]
    Imfreqmap_data1.insert(0, ColNames)

    res = {"body": Imfreqmap_data1}

    Currenttab = np.zeros_like(Imfreqmap)

    stlind = Imfreqmap == 0
    Currenttab[stlind] = 1

    fillertab = np.full((len(RowNames), len(ColNames) - 1), "", dtype=str)
    df = pd.DataFrame(fillertab, columns=ColNames[1:], index=RowNames)

    df.insert(0, ColNames[0], RowNames)

    style_data_conditional = [
        {
            'if': {
                'row_index': row,
                'column_id': ColNames[col + 1]
            },
            'backgroundColor': 'black',
            'color': 'white'
        }
        for row, col in zip(*np.where(stlind))
    ]
    impoints=[]
    cols = [{"name": col, "id": col} for col in df.columns]

    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "clear_im":
        return res, cols, df.to_dict('records'), style_data_conditional, {}
    

    # Handle cell clicks to toggle between pink and white
    if active_cell:
        row = active_cell['row']
        col = active_cell['column_id']

        if col != ColNames[0]:  # Ignore clicks on the first column (row headers)
            cell_id = f"{row}-{col}"

            # Check if the cell is black
            is_black_cell = any(
                style['if']['row_index'] == row and style['if']['column_id'] == col and style['backgroundColor'] == 'black'
                for style in style_data_conditional
            )

            if not is_black_cell:  # Only proceed if the cell is not black
                pink_cells_count = sum(1 for count in click_counts.values() if count % 2 == 1)

                if cell_id in click_counts:
                    if click_counts[cell_id] % 2 == 1:  # If pink, allow it to turn white
                        click_counts[cell_id] += 1
                    elif pink_cells_count < 20:  # If white, allow it to turn pink if less than 20 pink cells
                        click_counts[cell_id] += 1
                else:
                    if pink_cells_count < 20:
                        click_counts[cell_id] = 1

    # Style pink and white cells based on click counts
    for cell_id, count in click_counts.items():
        row, col = cell_id.split('-', 1)
        row = int(row)
        if col != ColNames[0]:  # Skip styling for the first column
            if count % 2 == 1:  # Odd clicks - pink
                style_data_conditional.append({
                    'if': {'row_index': row, 'column_id': col},
                    'backgroundColor': 'pink'
                })
            else:  # Even clicks - white
                style_data_conditional.append({
                    'if': {'row_index': row, 'column_id': col},
                    'backgroundColor': 'white'
                })

    plTnflag = 1
    return res, cols, df.to_dict('records'), style_data_conditional, click_counts
 
@app.callback(
    Output('Next_CurrentLossButton', 'disabled'),
    [Input('click-counts', 'data'),
     Input('CurrentLossModeDD','value')]
)
def toggle_button(click_counts,CurrentLossModeDD):
    mode = int(CurrentLossModeDD)
    if mode == 1:
        return False
    
    global Impoints
    Impoints = []

    # Define the mapping of column ranges to their indices
    column_map = {
        "0 - 1000": 0,
        "1000 - 2000": 1,
        "2000 - 3000": 2,
        "3000 - 4000": 3,
        "4000 - 5000": 4,
        "5000 - 6000": 5,
        "6000 - 7000": 6,
        "7000 - 8000": 7,
        "8000 - 9000": 8,
        "9000 - 10000": 9,
        "10000 - 11000": 10,
        "11000 - 12000": 11,
        "12000 - 13000": 12,
        "13000 - 14000": 13,
        "14000 - 15000": 14,
        "15000 - 16000": 15,
        "16000 - 17000": 16,
        "17000 - 18000": 17,
        "18000 - 19000": 18,
        "19000 - 20000": 19
    }
 
 
    # Count the number of cells currently colored pink
    pink_cells_count = sum(1 for count in click_counts.values() if count % 2 == 1)
 
    # Check if there are exactly 20 pink cells
    if pink_cells_count == 20:
        for key, value in click_counts.items():
            if value % 2 == 1:  # Only consider cells that are currently pink
                split_key = key.split('-')
               
                # Extract row and column range
                if len(split_key) == 3:
                    row = int(split_key[0])
                    col_range = f"{split_key[1].strip()} - {split_key[2].strip()}"
                   
                    # Translate the column range to its corresponding index
                    col = column_map.get(col_range, None)
                   
                    if col is not None:
                        Impoints.append((row, col))  # Store as tuple (row, col)
 
    # print("Impoints:", Impoints)
 
    # Enable the button only if there are exactly 20 pink cells
    return pink_cells_count < 20

#roy check
@app.callback(
    Output('CurrentFreePtsTab', 'cell_selectable'),
    [Input('CurrentLossModeDD', 'value')]
)
def update_table(selected_value):
    if selected_value is None:
        return False
   
    if selected_value == "1":
        return False
    else:
        return True


def ploss_current1(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    
        [0.33, '#4472c5'], 
        [0.33, '#af5c24'], 
        [0.66, '#af5c24'], 
        [0.66, '#787878'], 
        [1, '#787878']   
    ]
 
    # Create the surface plot with the custom color scale
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Imlosstype1textsetpoints", "children"),
    Output("Imlosstype1Text", "children"),
    Output('CurrentLossTab1', 'data'),
    Output('graphIm1','figure'),
    [Input('ImLoss1', 'value'),
     Input('ImAvg1', 'value')]
)
def update_table(selected_value,ImAvg1):
    global TnScale_init,TnScale_inc,Tnfreqmap,dp,ImLosstype1,ImLoss1_data1,matf4,avg4
    avg4 = int(ImAvg1)
 
    if selected_value is None:
       return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Im at set points",
        "2": "Pe(kWh) by Im at set points",
        "3": "Pe(kW/s) by Im at set points",
        "4": "Pcu(kW) by Im at set points",
        "5": "Pfe(kW) by Im at set points",
        "6": "Pstr(kW) by Im at set points",
        "7": "Pf(kW) by Im at set points",
        "8": "Pw(kW) by Im at set points",
        "9": "Pinv(kW) by Im at set points",
        "10": "sum Ploss(kW) by Im at set points",
        "11": "Temp by Im at set points",
        "12": "η = Pe/Pbatt by Im at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
    dp.Pf = np.array(dp.Pf)
    # ImLosstype1=[]
    # print("ImLosstype1",ImLosstype1)
    if selected_value == "1":
        ImLosstype1 = dp.condPe
    elif selected_value == "2":
        ImLosstype1 = dp.Pekwh
    elif selected_value == "3":
        ImLosstype1 = dp.Pekws
    elif selected_value == "4":
        ImLosstype1 = dp.Pcu
    elif selected_value == "5":
        ImLosstype1 = dp.Pfe
    elif selected_value == "6":
        ImLosstype1 = dp.Pstr
    elif selected_value == "7":
        ImLosstype1 = dp.Pf
    elif selected_value == "8":
        ImLosstype1 = dp.Pw
    elif selected_value == "9":
        ImLosstype1 = dp.Pinv
    elif selected_value == "10":
        ImLosstype1 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        ImLosstype1 = dp.Temp
    elif selected_value == "12":
        ImLosstype1 = dp.n
    
    xax = ImScale_init - np.arange(0, 21) * ImScale_inc
    mat = LossTypeCalc(Imfreqmap, avg4, ImLosstype1, dp.Im,dp.werpm, xax)
    matf4 = mat
    yax = np.arange(21) * 1000
    # print("mat",mat)
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
    ImLoss1_data = mat.tolist()
    ImLoss1_data1 = mat.tolist()

    ImLoss1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, ImLoss1_data)]
    ImLoss1_data.insert(0, ColNames)
 
    # Combine data
    res = {
        "body": ImLoss1_data
    }
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
    fig = ploss_current1(matf4)
 

 
    return selected_label1,selected_label,res,fig


def ploss_current2(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig

@app.callback(
    Output("Imlosstype2textsetpoints", "children"),
    Output("Imlosstype2Text", "children"),
    Output('CurrentLossTab2', 'data'),
    Output('graphIm2','figure'),
    [Input('ImLoss2', 'value'),
     Input('ImAvg2', 'value')]
)
def update_table(selected_value,ImAvg2):
    global TnScale_init,TnScale_inc,Tnfreqmap,dp,ImLosstype2,ImLoss2_data1,ImLoss2,matf5,avg5
    avg5 = int(ImAvg2)
    ImLoss2={}
    if selected_value is None:
        return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Im at set points",
        "2": "Pe(kWh) by Im at set points",
        "3": "Pe(kW/s) by Im at set points",
        "4": "Pcu(kW) by Im at set points",
        "5": "Pfe(kW) by Im at set points",
        "6": "Pstr(kW) by Im at set points",
        "7": "Pf(kW) by Im at set points",
        "8": "Pw(kW) by Im at set points",
        "9": "Pinv(kW) by Im at set points",
        "10": "sum Ploss(kW) by Im at set points",
        "11": "Temp by Im at set points",
        "12": "η = Pe/Pbatt by Im at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
    dp.Pf = np.array(dp.Pf)
    if selected_value == "1":
        ImLosstype2 = dp.condPe
    elif selected_value == "2":
        ImLosstype2 = dp.Pekwh
    elif selected_value == "3":
        ImLosstype2 = dp.Pekws
    elif selected_value == "4":
        ImLosstype2 = dp.Pcu
    elif selected_value == "5":
        ImLosstype2 = dp.Pfe
    elif selected_value == "6":
        ImLosstype2 = dp.Pstr
    elif selected_value == "7":
        ImLosstype2 = dp.Pf
    elif selected_value == "8":
        ImLosstype2 = dp.Pw
    elif selected_value == "9":
        ImLosstype2 = dp.Pinv
    elif selected_value == "10":
        ImLosstype2 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        ImLosstype2 = dp.Temp
    elif selected_value == "12":
        ImLosstype2 = dp.n
 
    xax = ImScale_init - np.arange(0, 21) * ImScale_inc
    mat = LossTypeCalc(Imfreqmap, avg5, ImLosstype2, dp.Im,dp.werpm, xax)
    matf5 = mat
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
 
    ImLoss2_data = mat.tolist()
    ImLoss2['data'] = mat.tolist()
    ImLoss2_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, ImLoss2_data)]
    ImLoss2_data.insert(0, ColNames)
 
    # Combine data
    res = {
        "body": ImLoss2_data
    }
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
    fig = ploss_current2(matf5)

 
    return selected_label1,selected_label,res,fig




def ploss_current3(mat):
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    x = np.arange(0, mat.shape[1])
    y = np.arange(0, mat.shape[0])
    X, Y = np.meshgrid(x, y)
 
    # Define your custom color scale
    color_scale = [
        [0, '#4472c5'],    # Color for values in the range 0-20
        [0.33, '#4472c5'], # Same color for values in the range 0-20
        [0.33, '#af5c24'], # Color for values in the range 20-40
        [0.66, '#af5c24'], # Same color for values in the range 20-40
        [0.66, '#787878'], # Color for values in the range 40-60
        [1, '#787878']     # Same color for values in the range 40-60
    ]
 
    # Create the surface plot with the custom color scale
    fig = go.Figure(data=[go.Surface(z=mat, colorscale=color_scale)])
 
    # Customize labels
    fig.update_layout(scene=dict(xaxis_title='X Label', yaxis_title='Y Label', zaxis_title='Z Label'))
 
    # Add a color bar which maps values to colors
    # fig.update_layout(coloraxis_colorbar=dict(len=0.5, yanchor='top', y=1.2))
    # fig.update_layout(height=400)
    fig.update_layout(
        title_font={'size': 15, 'color': 'white'},
        # paper_bgcolor="rgba(0,0,0,0)",  # Set paper background color to transparent
        # plot_bgcolor="rgba(0,0,0,0)",
        yaxis_title_font=dict(color="white"),  # Set y-axis title color to white
        xaxis_tickfont=dict(color="white"),     # Set x-axis tick labels color to white
        yaxis_tickfont=dict(color="white"),     # Set y-axis tick labels color to white
        xaxis_title_font=dict(color="white"),
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_showgrid=False,
        margin=dict(
            l=20,  
            r=10,  
            b=20,  
            t=30
        ),
    )
    fig.update_layout(showlegend=False)
    return fig



@app.callback(
      Output("Imlosstype3textsetpoints", "children"),
    Output("Imlosstype3Text", "children"),      
    Output('CurrentLossTab3', 'data'),
    Output('graphIm3','figure'),
    [Input('ImLoss3', 'value'),
     Input('ImAvg3', 'value')]
)
def update_table(selected_value,ImAvg3):
    global TnScale_init,TnScale_inc,Tnfreqmap,dp ,ImLosstype3,ImLoss3_data1,ImLoss3,matf6,avg6
    avg6 = int(ImAvg3)
    ImLoss3 = {}
    if selected_value is None:
        return dash.no_update,dash.no_update,[],dash.no_update
   
    label_map = {
        "1": "Pe with regeneration by Im at set points",
        "2": "Pe(kWh) by Im at set points",
        "3": "Pe(kW/s) by Im at set points",
        "4": "Pcu(kW) by Im at set points",
        "5": "Pfe(kW) by Im at set points",
        "6": "Pstr(kW) by Im at set points",
        "7": "Pf(kW) by Im at set points",
        "8": "Pw(kW) by Im at set points",
        "9": "Pinv(kW) by Im at set points",
        "10": "sum Ploss(kW) by Im at set points",
        "11": "Temp by Im at set points",
        "12": "η = Pe/Pbatt by Im at set points",
    }
    dp.condPe= np.array(dp.condPe)
    dp.Pekwh= np.array(dp.Pekwh)
    dp.Pekws= np.array(dp.Pekws)
    dp.Pcu= np.array(dp.Pcu)
    dp.Pfe= np.array(dp.Pfe)
    dp.Pf = np.array(dp.Pf)
    dp.Pstr= np.array(dp.Pstr)
    dp.Pw= np.array(dp.Pw)
    dp.Pinv= np.array(dp.Pinv)
    dp.Temp= np.array(dp.Temp)
    dp.Im= np.array(dp.Im)
    dp.werpm= np.array(dp.werpm)
 
    if selected_value == "1":
        ImLosstype3 = dp.condPe
    elif selected_value == "2":
        ImLosstype3 = dp.Pekwh
    elif selected_value == "3":
        ImLosstype3 = dp.Pekws
    elif selected_value == "4":
        ImLosstype3 = dp.Pcu
    elif selected_value == "5":
        ImLosstype3 = dp.Pfe
    elif selected_value == "6":
        ImLosstype3 = dp.Pstr
    elif selected_value == "7":
        ImLosstype3 = dp.Pf
    elif selected_value == "8":
        ImLosstype3 = dp.Pw
    elif selected_value == "9":
        ImLosstype3 = dp.Pinv
    elif selected_value == "10":
        ImLosstype3 = dp.Pcu + dp.Pfe + dp.Pstr + dp.Pf + dp.Pw + dp.Pinv
    elif selected_value == "11":
        ImLosstype3 = dp.Temp
    elif selected_value == "12":
        ImLosstype3 = dp.n
 
    xax = ImScale_init - np.arange(0, 21) * ImScale_inc
    mat = LossTypeCalc(Imfreqmap, avg6, ImLosstype3, dp.Im,dp.werpm, xax)
    matf6 = mat
    yax = np.arange(21) * 1000
 
    ColNames = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
    ColNames = [" "] +  ColNames
    # RowNames = [f'{xax[i]}' for i in range(len(xax) - 1)]
 
    RowNames = [f'{xax[i]} - {xax[i+1]}' for i in range(len(xax) - 1)]
    ImLoss3_data = mat.tolist()
    ImLoss3['data'] = mat.tolist()
 
    ImLoss3_data = [[row_name] + row_data for row_name, row_data in zip(RowNames, ImLoss3_data)]
    ImLoss3_data.insert(0, ColNames)
 
    # Combine data
    res = {
        "body": ImLoss3_data
    }
 
    fig = ploss_current3(matf6)
    selected_label = label_map.get(selected_value, "Pe")
    selected_label1=f"Loss Distribution for {selected_label}"
 
    return selected_label1,selected_label,res,fig



@callback(
    Output("ploss-current-modal", "opened"),
    Output("imcurrent-drawer", "opened"),
    Output("OrderTab1",'data'),
    Output("OrderTab2",'data'),
    Output("OrderTab3",'data'),
    Output("OrdMatCalc1",'data'),
    Output("OrdMatCalc2",'data'),
    Output("OrdMatCalc3",'data'),
    Output("graphImL1","figure"),
    Output("graphImL2","figure"),
    Output("graphImL3","figure"),
    Input("Next_CurrentLossButton", "n_clicks"),
    Input('CurrentLossModeDD', 'value'),
    Input('ImLoss1', 'value'),
    Input('ImLoss2', 'value'),
    Input('ImLoss3', 'value'),
    State("ploss-current-modal", "opened"),
    prevent_initial_call=True,
)
def Next_ImLossButtonPushed(n_clicks,CurrentLossModeDD,Imdrrop1,Imdrrop2,Imdrrop3,opened):
    global avg4,avg5,avg6,y1,ord11,y2,ord22,y3,ord33

    triggered_input = callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == "Next_CurrentLossButton":

        if Imdrrop1 is None or Imdrrop2 is None or Imdrrop3 is None:
            return not opened,False,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update
        

        mode=int(CurrentLossModeDD)
        # avg1=2
        # avg2=2
        # avg3=2
        if mode == 1:
            ptx = []
            pty=[]
        else:
            ptx = [point[0] for point in Impoints]
            pty = [point[1] for point in Impoints]


        arr = np.arange(0, 100001, 1000)
        num = len(arr)
        winit = 1000  # Equivalent to Cell X3, BL1 in MATLAB

        # Col AA: Repeating elements of arr 50 times
        w1 = np.repeat(arr, 50)

        # Col AB: Adding winit to each element in w1
        w2 = w1 + winit

        # Col AC: Initialize Im1 and Col AD: Im2 calculation
        Im1 =  ImScale_init - np.arange(0, 50) *ImScale_inc
        Im1 = np.tile(Im1, num)  # Replicate Im1 for each element in arr
        Im2 = Im1 - ImScale_inc
    
        sigman = np.zeros(num * 50)
        sumarray1 = np.zeros(num * 50)
        sumarray2 = np.zeros(num * 50)
        sumarray3 = np.zeros(num * 50)
        sumPcu = np.zeros(num * 50)
        sumPFe = np.zeros(num * 50)
        sumPstr = np.zeros(num * 50)
        sumPf = np.zeros(num * 50)
        sumPw = np.zeros(num * 50)
        sumPinv = np.zeros(num * 50)
        for idx in range(num * 50):
            condition = (dp.werpm >= w1[idx]) & (dp.werpm < w2[idx]) & (dp.Im > Im2[idx]) & (dp.Im <= Im1[idx])

            sigman[idx] = np.sum(ImN[condition])  # Column AE
            sumarray1[idx] = np.sum(ImLosstype1[condition])
            sumarray2[idx] = np.sum(ImLosstype2[condition])
            sumarray3[idx] = np.sum(ImLosstype3[condition])
            sumPcu[idx] = np.sum(dp.Pcu[condition])  # Column AJ
            sumPFe[idx] = np.sum(dp.Pfe[condition])  # Column AK
            sumPstr[idx] = np.sum(dp.Pstr[condition])  # Column AL
            sumPf[idx] = np.sum(dp.Pf[condition])  # Column AM
            sumPw[idx] = np.sum(dp.Pw[condition])  # Column AN
            sumPinv[idx] = np.sum(dp.Pinv[condition])  # Column AO


        if avg4 == 1:
            sumarray1[sigman > 0] = sumarray1[sigman > 0] / sigman[sigman > 0]

        if avg5 == 1:
            sumarray2[sigman > 0] = sumarray2[sigman > 0] / sigman[sigman > 0]

        if avg6 == 1:
            sumarray3[sigman > 0] = sumarray3[sigman > 0] / sigman[sigman > 0]

        # AX1:BC21 - x and y values of Free points
        xax = np.arange(ImScale_init, ImScale_init - 21*ImScale_inc, -ImScale_inc)
        yax = np.arange(0, 21) * 1000
        numx = len(xax) - 1
        numy = len(yax) - 1

        widz1 = np.zeros(len(ptx))
        widz2 = np.zeros(len(ptx))
        Imidz1 = np.zeros(len(ptx))
        Imidz2 = np.zeros(len(ptx))
        Nidz = np.zeros(len(ptx))

        for idx in range(len(ptx)):
            # Calculate widz1, widz2, Tnidz1, Tnidz2
            widz1[idx] = yax[pty[idx]-1]
            widz2[idx] = yax[pty[idx] ]
            Imidz1[idx] = xax[ptx[idx]-1]
            Imidz2[idx] = xax[ptx[idx] ]

            # Calculate Nidz
            condition = (
                (dp.werpm >= widz1[idx]) & 
                (dp.werpm < widz2[idx]) & 
                (dp.Im > Imidz2[idx]) & 
                (dp.Im <= Imidz1[idx])
            )
            Nidz[idx] = np.sum(ImN[condition])
        colnames = ['','Order', 'Pcu(kW)', 'Pfe(kW)', 'Pstr(kW)', 'Pf(kW)', 'Pw(kW)', 'Pinv(kW)']
        rownames = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10']

        mat1 = np.array(ImLoss1_data1)


        ord11, y1 = OrdMatCalc(mode, mat1, np.round(sumarray1, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord1 = ord11.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord1, np.round(y1,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        res1 = {
            "body": table_data
        }

        mat2 = np.array(ImLoss2['data'])
        ord22, y2 = OrdMatCalc(mode, mat2, np.round(sumarray2, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord2 = ord22.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord2, np.round(y2,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        res2 = {
            "body": table_data
        }

        mat3 = np.array(ImLoss3['data'])
        ord33, y3 = OrdMatCalc(mode, mat3, np.round(sumarray3, 4), sumPcu, sumPFe, sumPstr, sumPf, sumPw, sumPinv, ptx, pty)
        ord3 = ord33.reshape(-1, 1)  # Reshape ord1 to be 20x1
        data = np.hstack((ord3, np.round(y3,4)))  # Now hstack will work correctly
        table_data = [[row_name] + list(row_data) for row_name, row_data in zip(rownames, data)]
        table_data.insert(0, colnames)
        res3 = {
            "body": table_data
        }

        ColNames1 = [f'{yax[i]} - {yax[i+1]}' for i in range(len(yax) - 1)]
        ColNames1 = [" "] +  ColNames1
        RowNames1 = [f'{xax[i]}' for i in range(len(xax) - 1)]

        Ordtab1 = np.zeros((numx, numy))
        Ordtab2 = np.zeros((numx, numy))
        Ordtab3 = np.zeros((numx, numy))

        Ordtab1[np.isin(mat1, ord1)] = mat1[np.isin(mat1, ord1)]
        Ordtab2[np.isin(mat2, ord2)] = mat2[np.isin(mat2, ord2)]
        Ordtab3[np.isin(mat3, ord3)] = mat3[np.isin(mat3, ord3)]

        Ordtab1_data = [[row_name] + row_data for row_name, row_data in zip(RowNames1, Ordtab1.tolist())]
        Ordtab1_data.insert(0, ColNames1)
        res4 = {
            "body": Ordtab1_data
        }
    
        Ordtab2_data = [[row_name] + row_data for row_name, row_data in zip(RowNames1, Ordtab2.tolist())]
        Ordtab2_data.insert(0, ColNames1)
        res5 = {
            "body": Ordtab2_data
        }
    
        Ordtab3_data = [[row_name] + row_data for row_name, row_data in zip(RowNames1, Ordtab3.tolist())]
        Ordtab3_data.insert(0, ColNames1)
        res6 = {
            "body": Ordtab3_data
        }
    
        fig1 = ImLoss_Current(y1,ord11)
        fig2 = ImLoss_Current(y2,ord22)
        fig3 = ImLoss_Current(y3,ord33)
    
        # print("ptx",ptx)

        return opened,True,res4,res5,res6,res1,res2,res3,fig1,fig2,fig3
    else:
        return [dash.no_update]*11


#full screen tab1
@callback(
    Output(f"modal1", "opened"),
    Output("graphf1","figure"),
    Input(f"open1", "n_clicks"),
    State(f"modal1", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 = TorqueVsSpeed(condition_value='2')
    return not opened,figure1
       
@callback(
    Output(f"modal2", "opened"),
    Output("graphf2","figure"),
    Input(f"open2", "n_clicks"),
    State(f"modal2", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure2 = TempOnTnGraph(condition_value='2')
    return not opened,figure2


@callback(
    Output(f"modal3", "opened"),
    Output("graphf3","figure"),
    Input(f"open3", "n_clicks"),
    State(f"modal3", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure3 = PLoss(condition_value='2')
    return not opened,figure3

@callback(
    Output(f"modal4", "opened"),
    Output("graphf4","figure"),
    Input(f"open4", "n_clicks"),
    State(f"modal4", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure4 = PowerVsSpeed(condition_value='2') 
    return not opened,figure4

@callback(
    Output(f"modal5", "opened"),
    Output("graphf5","figure"),
    Input(f"open5", "n_clicks"),
    State(f"modal5", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure5 = TempOnPower(condition_value='2')
    return not opened,figure5

@callback(
    Output(f"modal6", "opened"),
    Output("graphf6","figure"),
    Input(f"open6", "n_clicks"),
    State(f"modal6", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure6 = IdIqControl(condition_value='2')
    return not opened,figure6

#full screen tab1


#full screen tab2
@callback(
    Output(f"modal7", "opened"),
    Output("graphf7","figure"),
    Input(f"open7", "n_clicks"),
    State(f"modal7", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure7= SpeedAccelDecel(condition_value='2')
    return not opened,figure7
@callback(
    Output(f"modal8", "opened"),
    Output("graphf8","figure"),
    Input(f"open8", "n_clicks"),
    State(f"modal8", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure8 = effMapTn(condition_value='2')
    return not opened,figure8
 
@callback(
    Output(f"modal9", "opened"),
    Output("graphf9","figure"),
    Input(f"open9", "n_clicks"),
    State(f"modal9", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure9 = piegraph(condition_value='2')
    return not opened,figure9
 
 
@callback(
    Output(f"modal10", "opened"),
    Output("graphf10","figure"),
    Input(f"open10", "n_clicks"),
    State(f"modal10", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure10 = wltc_btt(condition_value='2')
    return not opened,figure10
 
@callback(
    Output(f"modal11", "opened"),
    Output("graphf11","figure"),
    Input(f"open11", "n_clicks"),
    State(f"modal11", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure11 = effPower(condition_value='2')
    return not opened,figure11
 
@callback(
    Output(f"modal12", "opened"),
    Output("graphf12","figure"),
    Input(f"open12", "n_clicks"),
    State(f"modal12", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure12 = data_tabg1(condition_value='2')
    return not opened,figure12
#full screen tab2


#full screen ploss torque
@callback(
    Output(f"modal13", "opened"),
    Output("graphf13","figure"),
    Input(f"open13", "n_clicks"),
    State(f"modal13", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 = ploss_torque1(matf1)
    return not opened,figure1
       
@callback(
    Output(f"modal14", "opened"),
    Output("graphf14","figure"),
    Input(f"open14", "n_clicks"),
    State(f"modal14", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure2 = ploss_torque2(matf2)
    return not opened,figure2


@callback(
    Output(f"modal15", "opened"),
    Output("graphf15","figure"),
    Input(f"open15", "n_clicks"),
    State(f"modal15", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure3 = ploss_torque3(matf3)
    return not opened,figure3
#full screen ploss torque



#full screen ploss current
@callback(
    Output(f"modal16", "opened"),
    Output("graphf16","figure"),
    Input(f"open16", "n_clicks"),
    State(f"modal16", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 = ploss_current1(matf4)
    return not opened,figure1
       
@callback(
    Output(f"modal17", "opened"),
    Output("graphf17","figure"),
    Input(f"open17", "n_clicks"),
    State(f"modal17", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure2 = ploss_current2(matf5)
    return not opened,figure2


@callback(
    Output(f"modal18", "opened"),
    Output("graphf18","figure"),
    Input(f"open18", "n_clicks"),
    State(f"modal18", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure3 = ploss_current3(matf6)
    return not opened,figure3
#full screen ploss current


#full screen data tab
# @callback(
#     Output(f"modal19", "opened"),
#     Output("graphf19","figure"),
#     Input(f"open19", "n_clicks"),
#     State(f"modal19", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt1 = data_tabg1() 
#     return not opened,figuredt1
       
# @callback(
#     Output(f"modal20", "opened"),
#     Output("graphf20","figure"),
#     Input(f"open20", "n_clicks"),
#     State(f"modal20", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt2 = data_tabg2() 
#     return not opened,figuredt2


# @callback(
#     Output(f"modal21", "opened"),
#     Output("graphf21","figure"),
#     Input(f"open21", "n_clicks"),
#     State(f"modal21", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt3 = data_tabg3() 
#     return not opened,figuredt3

# @callback(
#     Output(f"modal22", "opened"),
#     Output("graphf22","figure"),
#     Input(f"open22", "n_clicks"),
#     State(f"modal22", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt4 = data_tabg4()
#     return not opened,figuredt4

# @callback(
#     Output(f"modal23", "opened"),
#     Output("graphf23","figure"),
#     Input(f"open23", "n_clicks"),
#     State(f"modal23", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt5 = data_tabg5() 
#     return not opened,figuredt5

# @callback(
#     Output(f"modal24", "opened"),
#     Output("graphf24","figure"),
#     Input(f"open24", "n_clicks"),
#     State(f"modal24", "opened"),
#     prevent_initial_call=True,
# )
# def toggle_modal(n_clicks, opened):
#     figuredt6 = data_tabg6()
#     # figure6 = IdIqControl(condition_value='2')
#     return not opened,figuredt6

#full screen data tab
@callback(
    Output(f"modal25", "opened"),
    Output("graphf25","figure"),
    Input(f"open25", "n_clicks"),
    State(f"modal25", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =TnLoss(y1,ord11)
    return not opened,figure1
@callback(
    Output(f"modal26", "opened"),
    Output("graphf26","figure"),
    Input(f"open26", "n_clicks"),
    State(f"modal26", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =TnLoss(y2,ord22)
    return not opened,figure1
@callback(
    Output(f"modal27", "opened"),
    Output("graphf27","figure"),
    Input(f"open27", "n_clicks"),
    State(f"modal27", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =TnLoss(y3,ord33)
    return not opened,figure1

@callback(
    Output(f"modal28", "opened"),
    Output("graphf28","figure"),
    Input(f"open28", "n_clicks"),
    State(f"modal28", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =ImLoss_Current(y1,ord11)
    return not opened,figure1
@callback(
    Output(f"modal29", "opened"),
    Output("graphf29","figure"),
    Input(f"open29", "n_clicks"),
    State(f"modal29", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =ImLoss_Current(y2,ord22)
    return not opened,figure1
@callback(
    Output(f"modal30", "opened"),
    Output("graphf30","figure"),
    Input(f"open30", "n_clicks"),
    State(f"modal30", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    figure1 =ImLoss_Current(y3,ord33)
    return not opened,figure1

@app.callback(
    Output("ipmloader1","display"),
    Output("ipmloader2","display"),
    Output("ipmloader3","display"),
    Output("ipmloader4","display"),
    Output("ipmloader5","display"),
    Output("ipmloader6","display"),
    Output("InitialEditField","disabled"),
    Output("InitempEditField","disabled"),
    Output("RoomTempEditField","disabled"),
    Output("EffMaxSpeed","disabled"),
    Output("MaxSpeedRpmEditField","disabled"),
    Output("ipm-edit-confirm", "children"),
    Output("next-link","disable_n_clicks"),
    Output("ipmedit","children"),
    Input("ipm-edit-confirm", "n_clicks"),
    prevent_initial_call=True,
    allow_duplicate=True
)
def toggle_icon(n_clicks):
    global IPMflag,dpflag
    if n_clicks % 2 == 1:
        return "hide","hide","hide","hide","hide","hide",False,False,False,False,False,DashIconify(icon="fluent-emoji:check-mark-button"),True,True
    else:
        IPMflag = 0
        dpflag = 0
        return "hide","hide","hide","hide","hide","hide",True,True,True,True,True,DashIconify(icon="fluent-emoji-flat:pencil"),None,None

#ipm edit confirm


#dp edit confirm
@app.callback(
    Output("dp-edit-confirm", "children"),
    Output("dploader1","display"),
    Output("dploader2","display"),
    Output("dploader3","display"),
    Output("dploader4","display"),
    Output("dploader5","display"),
    Output("dploader6","display"),
    Output("GravityEditField","disabled"),
    Output("frEditField","disabled"),
    Output("VWindEditField","disabled"),
    Output("CdEditField","disabled"),
    Output("AfEditField","disabled"),
    Output("pEditField","disabled"),
    Output("ndrEditField","disabled"),
    Output("sxEditField","disabled"),
    Output("RoadGradeEditField","disabled"),
    Output("LowEditField","disabled"),
    Output("MediumEditField","disabled"),
    Output("HighEditField","disabled"),
    Output("ExHighEditField","disabled"),
    Output("dpedit","children"),
    Input("dp-edit-confirm", "n_clicks"),
    prevent_initial_call=True
)
def toggle_icon(n_clicks):
    global dpflag
    if n_clicks % 2 == 1:
        return DashIconify(icon="fluent-emoji:check-mark-button"),"hide","hide","hide","hide","hide","hide",False,False,False,False,False,False,False,False,False,False,False,False,False,True
    else:
        dpflag = 0
        return DashIconify(icon="fluent-emoji-flat:pencil"),"hide","hide","hide","hide","hide","hide",True,True,True,True,True,True,True,True,True,True,True,True,True,None


#help cllckback
@callback(
    Output("help-modal", "opened"),
    Input("help-button", "n_clicks"),
    State("help-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_modal(n_clicks, opened):
    return not opened

@app.callback(
    Output("modal-content", "children"),
    Input("segment-control", "value")
)
def update_modal_content(selected_value):
    if selected_value == "xEV Document":
        return Introduction_contents
    elif selected_value == "User Manual":
        return User_Manual
    return None
#dp edit confirm
# @app.callback(
#     Output("simulator_page", "style"),
#     [Input("url", "pathname")]
# )
# def toggle_button_visibility(pathname):
#     if pathname == "/":  # Home page, button in the card (visible)
#         return {"display": "block",}  # Button is visible in the card
#     elif pathname == "/xev-simulator":  # On xEV Simulator page (header)
#         return {"display": "none", "color": "black"}  # Button is hidden in the header
#     return {"display": "block"}  # Default to visible


def points_near_hull(points, hull_indices, distance_threshold):
    hull_points = points[hull_indices]
    distances = np.linalg.norm(points[:, None] - hull_points, axis=2)
    close_points = np.any(distances < distance_threshold, axis=1)
    return np.where(close_points)[0]


@app.callback(
    # Output('TnLossTab1', 'data'),
    Output('graphpl1','figure'),
    [Input("tabs", "value"),
        Input('ploss_types', 'value'),
     ]
)
def LosstypeDropDownValueChanged(tab ,selected_value):
    global IPMflag

    # TnLoss1={}
    # global TnScale_init,TnScale_inc,Tnfreqmap,dp
 
    # if selected_value is None:
    #     return [],dash.no_update
    # global ploss,ipm 
    if tab != "ploss-tab":
        return dash.no_update

    # Ensure selected value is available
    if selected_value is None:
        return dash.no_update

    if IPMflag == 0:
        crr = np.array([S1K, S5K, S10K, S15K]) + ipm.initial
        ipm.plaId,ipm.plaIq = ipmclass.filter(crr,ipm.rpm,ipm.Id,ipm.Iq)
        num=len(ipm.rpm)
        ipmclass.losscalc(ipm,mot,inv,igbt,Temp,Flag,num)
        gt = ipmclass.graphtool(ipm.IPMstatus,ipm.Id,ipm.Iq,ipm.Tn,ipm.Pe)
        IPMflag = 1

    ipm.Pbtt=np.real(ipm.Pbtt)
    ipm.Ploss=np.real(ipm.Ploss)
    ipm.Pcu=np.real(ipm.Pcu)
    ipm.Pfe=np.real(ipm.Pfe)
    ipm.Pstr=np.real(ipm.Pstr)
    ipm.Pfric=np.real(ipm.Pfric)
    ipm.Pinv=np.real(ipm.Pinv)
    ipm.Pwind=np.real(ipm.Pwind)
    ipm.posin=np.real(ipm.posin)
    ipm.negan=np.real(ipm.negan)
    ipm.n =np.real(ipm.n )

    print("ipm.Pstr",ipm.Pstr)
    if selected_value == "1":
        ploss = ipm.Pbtt
    elif selected_value == "2":
        ploss = ipm.Ploss
    elif selected_value == "3":
        ploss = ipm.Pcu
    elif selected_value == "4":
        ploss =ipm.Pfe
    elif selected_value == "5":
        ploss = ipm.Pstr
    elif selected_value == "6":
        ploss = ipm.Pfric
    elif selected_value == "7":
        ploss = ipm.Pwind
    elif selected_value == "8":
        ploss = ipm.Pinv
    elif selected_value == "9":
        ploss = ipm.posin
    elif selected_value == "10":
        ploss = ipm.negan
    elif selected_value == "11":
        ploss = ipm.n

    y=np.real(ipm.Tn)
    x = np.real(ipm.rpm[:len(y)])

    # Ensure all data are column vectors and reshape them
    x = x.reshape(-1, 1)
    y = y.reshape(-1, 1)
    ploss = ploss.reshape(-1, 1)

    # Remove duplicate points by averaging
    unique_points, idx = np.unique(np.hstack((x, y)), axis=0, return_inverse=True)
    x = unique_points[:, 0]
    y = unique_points[:, 1]
    ploss = np.array([np.mean(ploss[idx == i]) for i in range(len(unique_points))])

    # Create the scatter plot
    scatter = go.Scatter(
        x=x.flatten(),
        y=y.flatten(),
        mode='markers',
        marker=dict(
            color=ploss.flatten(),
            colorscale='Jet',
            size=10,
            colorbar=dict(
                title="Loss"
            ),
            line=dict(width=1, color='black')  # Edge color (similar to 'edgecolor' in Matplotlib)
        )
    )

    # Create figure


    # Add axis color and grid
    # fig.update_xaxes(showgrid=True, gridcolor='white', color='white')
    # fig.update_yaxes(showgrid=True, gridcolor='#4DBEEE', color='#4DBEEE')  

    # y=np.real(ipm.Tn)
    # x = np.real(ipm.rpm[:len(y)])

    # x = x.reshape(-1, 1).flatten()
    # y = y.reshape(-1, 1).flatten()
    # ploss = ploss.reshape(-1, 1).flatten()

    # # Remove duplicate points by averaging
    # unique_points, idx = np.unique(np.column_stack((x, y)), axis=0, return_inverse=True)
    # x = unique_points[:, 0]
    # y = unique_points[:, 1]
    # ploss = np.array([np.mean(ploss[idx == i]) for i in range(len(unique_points))])

    # # Create the scatter plot using Plotly
    # scatter = go.Scatter(
    #     x=x,
    #     y=y,
    #     mode='markers',
    #     marker=dict(size=8, color=ploss,  showscale=True, colorbar=dict(title='Ploss')),
    #     name='Scatter'
    # )

    # # Define the convex hull
    # hull = ConvexHull(np.column_stack((x, y)))
    # points = np.column_stack((x, y))
    # hull = ConvexHull(points)
    # k = hull.vertices
    # pgX = x[hull.vertices]
    # pgY = y[hull.vertices]
    points = np.column_stack((x, y))  # Assuming x and y are your data points
    distance_threshold = 5.0  # Adjust this threshold to get more points
    hull = ConvexHull(points)
     # k = hull.vertices
    extra_points = points_near_hull(points, hull.vertices, distance_threshold)

    print("extra_points",extra_points)
    pgX = x[extra_points]
    pgY = y[extra_points]
    # print("k",k)

    # # Create a grid within the polygon
    Xq, Yq = np.meshgrid(np.linspace(min(x), max(x), 100), np.linspace(min(y), max(y), 100))

    # Create a mask for points inside the polygon
    polygon = Path(np.column_stack((pgX, pgY)))
    in_polygon = polygon.contains_points(np.column_stack((Xq.ravel(), Yq.ravel()))).reshape(Xq.shape)

    zmin = np.min(ploss)
    zmax = np.max(ploss)
    pitch = 10  # Replace this with the actual value from your slider
    levels = np.linspace(zmin, zmax, pitch)

    # Interpolate the ploss values over the grid using 'cubic' interpolation
    Zq = griddata((x, y), ploss, (Xq, Yq), method='cubic')

    # Apply the mask: set values outside the polygon to NaN
    Zq[~in_polygon] = np.nan

    # Plot the contour map using Plotly
    contour = go.Contour(
        z=Zq,
        x=Xq[0, :],
        y=Yq[:, 0],
        colorscale='Jet',
        showscale=True,
        colorbar=dict(title='Ploss'),
        contours=dict(
            start=zmin,
            end=zmax,
            size=(zmax - zmin) / pitch
        )
    )
    fig = go.Figure(data=[scatter])

    # Add axis labels
    fig.update_layout(
        xaxis_title='RPM',
        yaxis_title='Tn',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_showline=False,  # Make y-axis line invisible
        yaxis_zeroline=False,  # Make y-axis zero line invisible
        xaxis_showline=False,
        xaxis_showgrid=False,
        # paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black')
    )
 
    return fig
    # else:
    #     # figure1=TorqueVsSpeed(condition_value='1')
    #     return None
    
server = app.server

# Run the server
if __name__ == "__main__":
    # app.run_server(host='0.0.0.0', port=8050)
    app.run_server(debug=True)