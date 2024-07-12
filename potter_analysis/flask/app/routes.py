from flask import Blueprint, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    # Load data from CSV
    df = pd.read_csv('data/your_data.csv')
    
    # Example visualizations with Plotly

    # Example Plot: Distribution of a numerical column
    fig_hist = px.histogram(df, x='numerical_column', title='Distribution of Numerical Column')
    plot_hist = pio.to_html(fig_hist, full_html=False)

    # Example Plot: Scatter plot between two columns
    fig_scatter = px.scatter(df, x='column1', y='column2', title='Scatter Plot')
    plot_scatter = pio.to_html(fig_scatter, full_html=False)

    return render_template('index.html', plot_hist=plot_hist, plot_scatter=plot_scatter)
