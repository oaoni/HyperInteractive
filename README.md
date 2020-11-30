# HyperInteractive
Interactive ipywidget and plotly framework for exploration hyperparamter tuning results



![Hyper Explore Demo](demo/demo.gif)

# Requirements
plotly == 4.12.0 <br>
ipywidgets == 7.5.1

# Usage

```import pandas as pd
from HyperInteractive import hyperExplore

data = pd.read_csv('./HyperInteractive/demo/modeltune.csv')

initial_axis = ['best_test_loss','best_test_corr']
initial_surface_axis = ['mu','alpha','best_test_corr']
legend_group = 'model'

tab = hyperExplore(data,initial_axis,initial_surface_axis,legend_group)
tab```