import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
import flask
import glob
import os

image_directory =  os.getcwd() + '/img/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'
colnames=['Reference','Tissue','Abnormality','Severity','x','y','radius'] 
df = pd.read_csv(os.getcwd() + '/data/Info.txt',sep=" ",names=colnames, header=None,skiprows=102,skipfooter=1,engine='python')

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])

app.layout = dbc.Container(html.Div( children=[
    html.H2('APOLO-N2A'),
    html.Div([
        html.H2('MIAS dataset'),
        html.Hr(),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,
            style_cell={
                'textAlign': 'left',
                'color': 'black'},
            style_header={
                'color': 'white',
                'backgroundColor': 'rgb(30, 30, 30)',
            },
        ),
        html.Hr(),],
        
    ),
    html.Div([
        html.H2('Imagenes procesadas'),
        html.Hr(),
        dcc.Dropdown(
            id='image-dropdown',
            options=[{'label': i, 'value': i} for i in list_of_images],
            value=list_of_images[0]
        ),
        html.Img(id='image')
    ])
    ],
    className="p-5",)
)

@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    return static_image_route + value

# Add a static image route that serves images from desktop
# Be *very* careful here - you don't want to serve arbitrary files
# from your computer or server
@app.server.route('{}<image_path>.png'.format(static_image_route))
def serve_image(image_path):
    image_name = '{}.png'.format(image_path)
    if image_name not in list_of_images:
        raise Exception('"{}" is excluded from the allowed static files'.format(image_path))
    return flask.send_from_directory(image_directory, image_name)

if __name__ == '__main__':
    app.run_server()