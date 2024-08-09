# 3D Surface Plot

Example of 3D surface plots with [`plotly`](https://plotly.com/python/).
See [live demo](https://seg-unibe.github.io/surface-plots/) to try it yourself.

https://github.com/user-attachments/assets/357fac2b-d11e-4a89-9c79-0cd0f1b8eebc

Code example:

```python
import plotly.graph_objects as go
import plotly.io as pio
import scipy.ndimage

def create_3d_surface_plot(x, y, z, smooth: bool = True):
    if smooth:
        range = z.max() - z.min()
        sigma = [0.2 * range, 0.2 * range]
        z = scipy.ndimage.filters.gaussian_filter(z, sigma)

    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=x,
        y=y,
        z=z,
        colorscale='#1f77b4',
        showscale=False,
        name='Series-Title',
        opacity=1,
        showlegend=True,
        contours=dict(
            x=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(x=True)),
            y=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(y=True)),
            z=dict(show=True, color='black', width=1, highlightwidth=1, highlightcolor='black', project=dict(z=True)),
        ),
        hovertemplate='X-Value: %{x}<br>Y-Value: %{y}<br>Z-Value: %{z}<extra></extra>',
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

    # Labels
    fig.update_layout(
        scene=dict(
            xaxis_title='X Axis Title',
            yaxis_title='Y Axis Title',
            zaxis_title='Z Axis Title',
            xaxis=dict(range=[x.min(), x.max()]),
            yaxis=dict(range=[y.min(), y.max()]),
            zaxis=dict(range=[z.min(), z.max()]),
            aspectratio=dict(x=4, y=3, z=2),  # Adjust aspect ratio to stretch the cube
            camera=dict(
                eye=dict(x=10, y=5, z=2) # Default zoom and viewing angle
            ),
        ),
        title=f'My 3D Surface Plot',
        legend_title_text='Legend',
    )

    pio.write_html(fig, '3d_surface_plot.html')
```
