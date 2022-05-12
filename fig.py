import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

txtpath = "C:\\Users\\user\\Desktop\\temp\\Egyption-license-plate-segmentor\\csv\\"
data = pd.read_csv(txtpath + '47.csv')
hist = data['value']

# print(data.shape)
# print(time_series.shape)

kernel_size = 7
kernel = np.ones(kernel_size) / kernel_size
hist = np.convolve(hist, kernel, mode='same')

indices = find_peaks(hist, prominence=7)[0]
# print(indices)

fig = go.Figure()
fig.add_trace(go.Scatter(
    y=hist,
    mode='lines+markers',
    name='Original Plot'
))

fig.add_trace(go.Scatter(
    x=indices,
    y=[hist[j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
))

fig.show()