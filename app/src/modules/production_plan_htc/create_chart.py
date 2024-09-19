#import packages
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px


def create_gantt_chart(df):
    #
    df["Class"] = np.where(df["FMF"]=="FMF", "FMF", (
        np.where(df["OG"], "OG", "Non-FMF")))
    
    df["GRADE_VIEW"] = np.where(df["INFO"].str.len()>0,
                               """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>"""+"<b>" + df["GRADE"] + " (" + df["Production"] + "MT)" + "</b> <br>" + df["INFO"].str.replace("\n", "<br>"),
                               np.where(df["OG"].str.len()>0,
                                        """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>"""+"<b>" + df["GRADE"] + " (" + df["Production"] + "MT)" + "</b> <br>" + "(" +df["OG"] + ")" +"<br>" + """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;""",
                                        """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>"""+"<b>" + df["GRADE"] + " (" + df["Production"] + "MT)" + "</b> <br>" + """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"""))

    df["GRADE_VIEW"] = np.where(df["Class"]=="FMF",
                                "<span style='color:blue'>" + df["GRADE_VIEW"] + "</span>",
                                np.where(df["Class"]=="OG",
                                         "<span style='color:red'>" + df["GRADE_VIEW"] + "</span>",
                                         df["GRADE_VIEW"]))
    
    range_x=[pd.Timestamp(min(df["Start"]).strftime('%Y-%m-%d')),
             pd.Timestamp((max(df["End"]) + pd.Timedelta(1,"d")).strftime('%Y-%m-%d'))]


    fig = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="GRADE_VIEW",
        custom_data=["GRADE", "Production", "Class"],
        color="Class",
        color_discrete_sequence=["orange", "green", "red"],
        category_orders={"Class": ["Normal", "FMF", "OG"]},
        #title="FMF and OG Grade Production Gantt Chart",
        #labels={"GRADE": "Grade"},
        template="plotly_white",
        range_x=range_x
    )

    fig.update_layout(
        height=900, 
        width=1000,
        bargap=0.6,
        showlegend=False,
        #xaxis
        xaxis=dict(
            side="top",
            ticklabelmode="period",
            tickformat="%H",
            tickmode="linear",
            dtick=7200000, # 7200000 milliseconds = 2 hours
        ),
        #yaxis: order
        yaxis={'categoryorder':'array', 'categoryarray':df.sort_values(by="Start", ascending=False)[["GRADE_VIEW"]].drop_duplicates(keep="last")},
        #hover: backgroud color
        ##hoverlabel_bgcolor="white",
    )

    fig.update_xaxes(#line
                     showline=True,
                     linewidth=2,
                     linecolor='gray',
                     mirror=True,
                     tickfont=dict(size=10),
                     #grid
                     showgrid=True,
                     gridwidth=1,
                     gridcolor='gray',
                     #ticks
                     ticks="outside",
                     tickwidth=1,
                     tickcolor='gray',
                     ticklen=10,
                     griddash='dot',
                     #title
                     title=None)
    
    fig.update_yaxes(#line
                     showline=True,
                     linewidth=2,
                     linecolor='gray',
                     mirror=True,
                     tickfont=dict(size=10),
                     #grid
                     showgrid=True,
                     gridwidth=1,
                     gridcolor='gray',
                     #ticks
                     ticks="outside",
                     tickwidth=1,
                     tickcolor='gray',
                     ticklen=10,
                     col=1,
                     #title
                     title=None)

    for x in list(pd.date_range(start=range_x[0], end=range_x[1])):
        fig.add_vline(x=x, line_color="gray", line_width=2, y1=1)
        
        fig.add_annotation(dict(font=dict(color="black",size=12),
                                    x=x+pd.Timedelta(12,"h"),
                                    y=1.0,
                                    showarrow=False,
                                    text="<b>"+(x+pd.Timedelta(12,"h")).strftime('%Y-%m-%d')+"</b>",
                                    textangle=0,
                                    xref="x",
                                    yref="paper"
                                ))

    fig.update_traces(marker_line_color="black", marker_line_width=2, opacity=0.9,
        hovertemplate="<b>%{customdata[0]} (%{customdata[1]}MT)</b><br>%{customdata[2]}<br><br><b>시작 :</b><br>%{base|%Y-%m-%d %H:%M} <br><b>종료 :</b><br>%{x|%Y-%m-%d %H:%M} <extra></extra>")
    
    return fig

def create_quality_chart(df,range_x):
    
    df["Quality_VIEW"] = """&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; <br>"""+"<b>" + df["Quality"] + "</b>" + """<br>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"""

    #
    fig = px.scatter(df, 
                       x='Period', 
                       y='Quality_VIEW', 
                       range_x=range_x,
                       color="Class",
                       color_discrete_sequence=["orange", "red", "green", "chartreuse"],
                       category_orders={"Class": ["Non-FMF","OG" ,"FMF", "Grade Change"]},
                       custom_data=["Quality", "Class"],
                      )
    
    fig.update_layout(
        template="plotly_white",
        height=300, 
        width=1000,
        bargap=0.6,
        showlegend=False,
        #xaxis
        xaxis=dict(
            side="top",
            ticklabelmode="period",
            tickformat="%H",
            tickmode="linear",
            dtick=7200000, # 7200000 milliseconds = 2 hours
        ),
    )
    
    fig.update_xaxes(#line
                     showline=True,
                     linewidth=2,
                     linecolor='gray',
                     mirror=True,
                     tickfont=dict(size=10),
                     #grid
                     showgrid=True,
                     gridwidth=1,
                     gridcolor='gray',
                     #ticks
                     ticks="outside",
                     tickwidth=1,
                     tickcolor='gray',
                     ticklen=10,
                     griddash='dot',
                     #title
                     title=None)
    
    fig.update_yaxes(#order
                     categoryorder="array",
                     categoryarray=df.sort_values(by="Quality_VIEW", ascending=False)[["Quality_VIEW"]].drop_duplicates(keep="last"), #["I.V", "X.S", "B-C2", "MI"],
                     #line
                     showline=True,
                     linewidth=2,
                     linecolor='gray',
                     mirror=True,
                     tickfont=dict(size=10),
                     #grid
                     showgrid=True,
                     gridwidth=1,
                     gridcolor='gray',
                     #ticks
                     ticks="outside",
                     tickwidth=1,
                     tickcolor='gray',
                     ticklen=10,
                     col=1,
                     #title
                     title=None)
    
    fig.update_traces(marker=dict(size=11, line=dict(width=2, color="black"), opacity=0.9),
                      hovertemplate="<b>%{customdata[0]}</b><br><b>%{customdata[1]}</b><br>측정시간 :</b><br> %{x|%Y-%m-%d %H:%M} <extra></extra>"
                     )
    
    for x in list(pd.date_range(start=range_x[0], end=range_x[1])):
        fig.add_vline(x=x, line_color="gray", line_width=2, y1=1)
    
    return fig




