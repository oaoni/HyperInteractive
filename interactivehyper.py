import numpy as np
from ipywidgets import interact, SelectionSlider, Layout, HBox, VBox, Dropdown, interactive, Tab
import plotly.graph_objects as go
import plotly.express as px
from ipywidgets import widgets
import datetime

def hyperExplore(df,initial_axis,initial_surface_axis,legend_group,hover_items):

    data = df.assign(x=df[initial_axis[0]],y=df[initial_axis[1]])\
       .sort_values(legend_group)\
       .reset_index(drop=True)

    group_ops = data[legend_group].sort_values().unique()
    num_groups = len(group_ops)
    axis_ops = data.columns.values
    lenSlide = '500px'

    fig = px.scatter(data, x="x", y="y", color=legend_group,hover_data=hover_items,
                 log_x=True, title='Hyperparameter Exploration',height=600)

    fig.update_layout(
        legend=dict(
        orientation="v",
        yanchor="top",
        y=1.02,
        xanchor="left",
        x=1),
        xaxis=dict(title=initial_axis[0],
                   titlefont=dict(size=14)),
        yaxis=dict(title=initial_axis[1],
                    titlefont=dict(size=14))
        )

    fig.update_traces(marker=dict(size=20,line=dict(width=1.5,
                                            color='DarkSlateGrey')),
                      selector=dict(mode='markers'))

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showgrid=True, gridwidth=.1, gridcolor='lightgrey')
    fig.update_yaxes(showgrid=True, gridwidth=.1, gridcolor='lightgrey')

    param_drop1 = Dropdown(
        value='None',
        options=np.insert(axis_ops,0,'None'),
        description='Parameter 1:'
    )

    slider1 = widgets.SelectionSlider(
        options=['Select Parameter'],
        value='Select Parameter',
        layout=Layout(width=lenSlide),
        continuous_update=True
    )

    size_drop = Dropdown(
        value='None',
        options=np.insert(axis_ops,0,'None'),
        description='Size:'
    )

    size_slider = widgets.IntSlider(
        value=20,
        min=10,
        max=50,
        step=1,
        disabled=False,
        continuous_update=True,
        orientation='horizontal',
        layout=Layout(width=lenSlide),
        readout=True,
        readout_format='d'
    )

    slider_group1 = widgets.HBox([param_drop1, slider1])
    slider_group2 = widgets.HBox([size_drop, size_slider])

    xaxis = Dropdown(
        value=initial_axis[0],
        options=axis_ops,
        description='X-axis:'
    )

    yaxis = Dropdown(
        value=initial_axis[1],
        options=axis_ops,
        description='Y-axis:'
    )

    container = widgets.VBox(children=[slider_group1,slider_group2,xaxis,yaxis])

    g = go.FigureWidget(data=fig,
                        layout=go.Layout(
                            title=dict(
                                text='Hyperparameter Exploration'
                            )
                        ))

    x_surface = Dropdown(
        value=initial_surface_axis[0],
        options=axis_ops,
        description='X-axis'
    )
    y_surface = Dropdown(
        value=initial_surface_axis[1],
        options=axis_ops,
        description='Y-axis'
    )
    z_surface = Dropdown(
        value=initial_surface_axis[2],
        options=axis_ops,
        description='Z-axis'
    )

    surface_buttons = widgets.RadioButtons(
        options=group_ops,
        value=group_ops[0], # Defaults to 'pineapple'
        description=legend_group+":",
        disabled=False
    )


    z_vals = data.query('{} == "{}"'\
            .format(legend_group,surface_buttons.value))[[x_surface.value,y_surface.value,z_surface.value]]\
            .groupby([x_surface.value,y_surface.value])\
            .median().reset_index()\
            .pivot(index=x_surface.value,columns=y_surface.value,values=z_surface.value)

    fig2 = go.Figure(data=[go.Surface(z=z_vals)])
    fig2.update_layout(title='Hyperparameter Surface: '+surface_buttons.value, autosize=False,
                      margin=dict(l=65, r=50, b=65, t=90),
                      height=600)

    layout = go.Layout(
                    scene = dict(
                        xaxis = dict(
                            title = initial_surface_axis[0]),
                        yaxis = dict(
                            title = initial_surface_axis[1]),
                        zaxis = dict(
                            title = initial_surface_axis[2]),
                                ))
    fig2.update_layout(layout)

    container2 = widgets.HBox(children=[surface_buttons,x_surface,y_surface,z_surface])


    g2 = go.FigureWidget(data=fig2,
                        layout=go.Layout(
                            title=dict(
                                text='Hyperparameter Surface: '+surface_buttons.value
                            )
                        ))


    def axis_response(change):
        with g.batch_update():
            #Gets the widget that was altered
            modified = change.owner.description

            if modified == xaxis.description:
                for i in range(num_groups):
                    #Get data for legend group
                    filtered_data = data.query("{} == '{}'".format(legend_group,g.data[i].name))

                    #Query filtered data for slider specs
                    query_filt(filtered_data,i)

                    g.layout.xaxis.title = xaxis.value

            elif modified == yaxis.description:
                for i in range(num_groups):
                    #Get data for legend group
                    filtered_data = data.query("{} == '{}'".format(legend_group,g.data[i].name))

                    #Query filtered data for slider specs
                    query_filt(filtered_data,i)

                    g.layout.yaxis.title = yaxis.value

    def slider1_response(change):
        with g.batch_update():
            for i in range(num_groups):
                #Get data for legend group
                filtered_data = data.query("{} == '{}'".format(legend_group,g.data[i].name))#make key var that iters

                #Query filtered data for slider specs
                query_filt(filtered_data,i)

    def query_filt(filtered_data,i):
        #Query filtered data for slider specs
    #     filt_bool = (filtered_data.learning_rate == lr_slider.value)#make learning_rate var
        if param_drop1.value == 'None':
            #Assign data to graph
            g.data[i].x = filtered_data[xaxis.value]
            g.data[i].y = filtered_data[yaxis.value]
        else:
            filt_bool = (filtered_data[param_drop1.value] == slider1.value)#make learning_rate var
            #Filter out data
            xfilt = [v if b else None for v,b in zip(filtered_data[xaxis.value],filt_bool)]
            yfilt = [v if b else None for v,b in zip(filtered_data[yaxis.value],filt_bool)]
            #Assign data to graph
            g.data[i].x = xfilt
            g.data[i].y = yfilt

    def create_slider_options(drop_value):
        if drop_value == 'None':
            slide_ops = ['Select Parameter']
        else:
            slide_ops = data[drop_value].sort_values().unique()
        return slide_ops

    def param_update(change):
        #everytime we change param, update the slider options and current value
        slider1.options = create_slider_options(param_drop1.value)
        slider1.value = slider1.options[0]

    def size_response(change):
         with g.batch_update():
                if size_drop.value == 'None':
                    g.update_traces(marker=dict(size=size_slider.value))
                else:
                    sizeFig = px.scatter(data, x="x", y="y", color="model",
                                         size=size_drop.value, size_max=size_slider.value)
                    traceSizes = [x.marker.size for x in sizeFig.data]

                    for i in range(num_groups):
                        g.data[i].marker.size = traceSizes[i]
                        g.data[i].marker.sizeref = sizeFig.data[0].marker.sizeref
                        g.data[i].marker.sizemode = sizeFig.data[0].marker.sizemode
                        g.data[i].marker.sizemin = 4

    def surface_response(change):
        with g.batch_update():
            z_vals = data.query('{} == "{}"'\
            .format(legend_group,surface_buttons.value))[[x_surface.value,y_surface.value,z_surface.value]]\
            .groupby([x_surface.value,y_surface.value])\
            .median().reset_index()\
            .pivot(index=x_surface.value,columns=y_surface.value,values=z_surface.value)

            g2.data[0].z = z_vals.values

            layout = go.Layout(
                        scene = dict(
                            xaxis = dict(
                                title = x_surface.value),
                            yaxis = dict(
                                title = y_surface.value),
                            zaxis = dict(
                                title = z_surface.value),
                                    ),
                         title=dict(
                                text='Hyperparameter Surface: '+surface_buttons.value
                            ))

            g2.update_layout(layout)

    surface_buttons.observe(surface_response,"value")
    x_surface.observe(surface_response,"value")
    y_surface.observe(surface_response,"value")
    z_surface.observe(surface_response,"value")

    size_drop.observe(size_response,"value")
    size_slider.observe(size_response, "value")
    slider1.observe(slider1_response, names="value")
    xaxis.observe(axis_response, names="value")
    yaxis.observe(axis_response, names="value")
    param_drop1.observe(param_update, names="value")

    scatterTab = widgets.VBox([container,g])
    surfaceTab = widgets.VBox([container2,g2])
    tab = widgets.Tab([scatterTab,surfaceTab])
    tab.set_title(0,'Scatter')
    tab.set_title(1,'Surface')

    return tab
