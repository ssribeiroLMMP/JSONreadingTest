import json
import pandas as pd
from pickletools import markobject
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from wellGeometryTest import print_well

with open('../data/simentar_exemplo_publicacao.json') as f:
    testJSON = json.load(f)

fig,inner,outer = print_well(testJSON)
print(type(fig))

def fluid(x0,y0,x1,y1,label,color):
    return go.Scatter(x=[x0, x1], y=[-y0, -y1], 
                    name=label,
                    mode='lines',
                    line=dict(width=2),
                    hoverinfo='name',
                    line_shape='linear')

pump_seq = testJSON["pumping_sequence"]

fluids = []

for ps_item in pump_seq['valid_fluid_entries']:
    aux = dict();    
    aux2 = ps_item['annular_fluid_sequence_entry'];
    aux3 = ps_item['fluid_sequence_entry'];
    aux4 = ps_item['plug_annular_fluid_sequence_entry'];
    if len(aux2) > 0:
        aux['label'] = ps_item['label']
        aux['volume'] = aux2['volume']
        aux['type'] = 'annular_fluid_sequence_entry'
        aux['top'] = aux2['top']
        aux['annulus_length']= aux2['annulus_length']
        aux['fluid_id'] = aux2['fluid_id']
        fig.add_trace(fluid(-20,aux['top'],20,aux['top'],aux['label'],'black'))
    elif len(aux3) > 0:
        aux['label'] = ps_item['label']
        aux['volume'] = aux3['volume']
        aux['type'] = 'fluid_sequence_entry'
        aux['fluid_id'] = aux3['fluid_id']
    elif len(aux4) > 0:
        aux['label'] = ps_item['label']
        aux['volume'] = aux4['volume']
        aux['type'] = 'plug_annular_fluid_sequence_entry'
        aux['fluid_id'] = aux4['fluid_id']
        
    print(aux)
    

fig.show()
    
