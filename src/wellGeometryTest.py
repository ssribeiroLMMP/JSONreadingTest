import json
from pickletools import markobject
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
 
with open('../data/simentar_exemplo_publicacao.json') as f:
    testJSON = json.load(f)
    
# print(type(testJSON))
def print_well(testJSON):

    def casing(x0,y0,x1,y1,label,fillpattern,linecolor):
        return go.Scatter(x=[x0, x0, x1, x1, x0], y=[y0, y1, y1, y0, y0],
                        fill='toself',
                        fillpattern=dict(bgcolor='white',
                                        fgcolor=linecolor,
                                        shape =fillpattern),
                        mode='lines+markers',
                        hoveron='points+fills',
                        line_color=linecolor,
                        name=label,
                        hoverinfo='text')

    ext_geo = testJSON["external_geometry"]
    external_geometry = []
    z = [0]

    for lc_item in ext_geo['last_casing']:
        aux = lc_item["casing_element_item"]
        aux['label'] = 'last_casing';
        external_geometry.append(aux)

    for oh_item in ext_geo['open_hole']:
        aux = oh_item["open_hole_element_item"]
        aux['label'] = "open_hole";
        external_geometry.append(aux)

    # print(external_geometry)

    scenery = testJSON["scenery"]
    rotary_table = -scenery['air_gap']
    water_depth = -scenery['water_depth']-scenery['air_gap']

    int_geo = testJSON["internal_geometry"]
    internal_geometry = []

    for wc_item in int_geo['work_column']:
        aux = wc_item["pipe_element_item"]
        aux['label'] = 'work_column';
        internal_geometry.append(aux)

    for c_item in int_geo['casing']:
        aux = c_item["casing_element_item"]
        aux['label'] = 'casing';
        internal_geometry.append(aux)


    # print(internal_geometry)

    fig = go.Figure()
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.add_trace(go.Scatter(x = [-20, -20, 20, 20 ,-20], 
                            y= [rotary_table, water_depth, water_depth, rotary_table, rotary_table], 
                            mode="none",
                            fill='toself',))



    total_depth = 0

    for outer in external_geometry:
        outer['rect'] = [-outer['inside_diameter']/2,
                        -outer['measured_depth'],
                        outer['inside_diameter']/2,
                        outer['segment_length']-outer['measured_depth']
                        ];
        outer['left_wall'] = [-outer['outside_diameter']/2,
                            -outer['measured_depth'],
                            -outer['inside_diameter']/2,
                            outer['segment_length']-outer['measured_depth']
                            ];
        outer['right_wall'] = [outer['outside_diameter']/2,
                            -outer['measured_depth'],
                            outer['inside_diameter']/2,
                            outer['segment_length']-outer['measured_depth']
                            ];
        print(outer['rect'])      
        fig.add_trace(casing(x0=outer['right_wall'][0], 
                            y0=outer['right_wall'][1], 
                            x1=outer['right_wall'][2], 
                            y1=outer['right_wall'][3],linecolor='green',fillpattern='/',label=outer['label']))

        fig.add_trace(casing(x0=outer['left_wall'][0], 
                            y0=outer['left_wall'][1], 
                            x1=outer['left_wall'][2], 
                            y1=outer['left_wall'][3],linecolor='green',fillpattern='/',label=outer['label']))

        total_depth = min([total_depth,outer['rect'][1]])

    # test = [-6.125, -6112, 6.125, -5527]
    # # test = [2, 4, 5, 7]
    # fig.add_shape(type="rect",
    #                 x0=test[0], 
    #                 y0=test[1], 
    #                 x1=test[2], 
    #                 y1=test[3],
    #                 line=dict(width=10)
    #                 )

    for inner in internal_geometry:
        inner['rect'] = [-inner['inside_diameter']/2,
                            -inner['measured_depth'],
                            inner['inside_diameter']/2,
                            inner['segment_length']-inner['measured_depth']
                            ];
        inner['left_wall'] = [-inner['outside_diameter']/2,
                            -inner['measured_depth'],
                            -inner['inside_diameter']/2,
                            inner['segment_length']-inner['measured_depth']
                            ];
        inner['right_wall'] = [inner['outside_diameter']/2,
                            -inner['measured_depth'],
                            inner['inside_diameter']/2,
                            inner['segment_length']-inner['measured_depth']
                            ];
        print(inner['rect'])     
        
        fig.add_trace(casing(x0=inner['right_wall'][0], 
                            y0=inner['right_wall'][1], 
                            x1=inner['right_wall'][2], 
                            y1=inner['right_wall'][3],linecolor='blue',fillpattern='/',label=inner['label']))

        fig.add_trace(casing(x0=inner['left_wall'][0], 
                            y0=inner['left_wall'][1], 
                            x1=inner['left_wall'][2], 
                            y1=inner['left_wall'][3],linecolor='blue',fillpattern='/',label=inner['label']))

        total_depth = min([total_depth,inner['rect'][1]])
    
    fig.update_xaxes(range=[-20, 20])
    fig.update_yaxes(range=[total_depth,0])
    fig.update_shapes(dict(xref='x', yref='y'))
    fig.update_traces(dict(marker_size=1))
    fig.update_layout(showlegend=True,hovermode='closest')
    fig.update_layout(showlegend=False)
    # fig.show()
    return fig,inner,outer


fig,_,_ = print_well(testJSON)

fig.show()