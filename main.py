import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from scipy.ndimage import gaussian_filter
from pathlib import Path
import matplotlib.lines as mlines

def create_3d_surface_plot(df, smooth_factor = 0, use_color_scales = False):
      """
      Generates a 3D surface plot from a DataFrame containing multiple data series.

      Parameters:
            df (pd.DataFrame): DataFrame with columns 'series', 'x', 'y', and 'z'.
            smooth_factor (float): Value between 0 and 1 to control the degree of 
                  Gaussian smoothing applied to 'z' (higher = smoother).
            use_color_scales (bool): If True, apply continuous color scales; 
                  otherwise, use distinct plain colors for each series.
      """
      fig = go.Figure()
      color_scales = ['Viridis', 'Cividis', 'Inferno', 'Magma', 'Plasma', 'Turbo']
      colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
      unique_series = df['series'].unique()
      color_scales_map = {series: color_scales[i % len(color_scales)] for i, series in enumerate(unique_series)}
      color_map = {series: colors[i % len(colors)] for i, series in enumerate(unique_series)}
      
      for series in unique_series:
            
            series_subset = df[df['series'] == series]
            pivot_table = series_subset.pivot(index='x', columns='y', values='z')
            x = pivot_table.columns.values
            y = pivot_table.index.values
            z = pivot_table.values
    
            if smooth_factor > 0:
                  sigma = [smooth_factor, smooth_factor]
                  z = gaussian_filter(z, sigma)
            
            colorscale = color_scales_map[series] if use_color_scales else [[0, color_map[series]], [1, color_map[series]]]
            fig.add_trace(go.Surface(
                  x=x,
                  y=y,
                  z=z,
                  colorscale=colorscale,
                  showscale=False,
                  name=series,
                  opacity=1.0,
                  showlegend=True,
                  contours=dict(
                  x=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(x=True)),
                  y=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(y=True)),
                  z=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(z=True)),
                  ),
                  hovertemplate=f'Series: {series}<br>X-Value: %{{x}}<br>Y-Value: %{{y}}<br>Z-Value: %{{z}}<extra></extra>',
                  lighting=dict(
                  ambient=0.5,
                  diffuse=0.7,
                  specular=0.4,
                  roughness=0.7,
                  fresnel=0.2
                  ),
                  lightposition=dict(
                  x=1000,
                  y=1000,
                  z=5000
                  )
            ))

      fig.update_layout(
            scene=dict(
                  xaxis_title='X Axis Title',
                  yaxis_title='Y Axis Title',
                  zaxis_title='Z Axis Title',
                  xaxis=dict(range=[df['x'].min(), df['x'].max()]),
                  yaxis=dict(range=[df['y'].min(), df['y'].max()]),
                  zaxis=dict(range=[df['z'].min(), df['z'].max()]),
                  aspectratio=dict(x=4, y=3, z=2),
                  camera=dict(
                  eye=dict(x=10, y=5, z=2)
                  ),
            ),
            title='My 3D Surface Plot',
            legend_title_text='Data Series',
      )

      pio.write_html(fig, 'surface_plot.html')


def main():
    # Load the CSV file
    csv_file_path = 'data_small.csv'
    if not Path(csv_file_path).is_file():
        raise FileNotFoundError(f"CSV file '{csv_file_path}' not found.")
    
    df = pd.read_csv(csv_file_path, sep=';')

    # Group by 'series' and create datasets
    datasets = []
    for series_name, group in df.groupby('series'):
        x = group['x'].values
        y = group['y'].values
        z = group['z'].values
        datasets.append({
            'x': x,
            'y': y,
            'z': z,
            'name': series_name
        })

    # Create the 3D surface plot
    create_3d_surface_plot(df, smooth_factor=0.6, use_color_scales=False)

if __name__ == '__main__':
    main()
