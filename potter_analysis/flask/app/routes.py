import os
from flask import Blueprint, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

bp = Blueprint('routes', __name__)

path_to_data = os.path.join('data', 'final_data_without_text.csv')
# os.path.join(os.path.join(os.path.dirname(os.getcwd()), 'data'),'final_data_without_text.csv')
df = pd.read_csv(path_to_data, index_col=0)

@bp.route('/', methods=['GET', 'POST'])
def index():
    selected_book = request.form.get('Book_Number', 'All')
    selected_entity = request.form.get('Entities', 'All')

    df_filtered = df
    if selected_book != 'All':
        df_filtered = df_filtered[df_filtered['Book_Number'] == int(selected_book)]
    if selected_entity != 'All':
        df_filtered = df_filtered[df_filtered['Entities'] == selected_entity]

    df_aggregated = df_filtered.drop(['Sentiment', 'Subjectivity'], axis=1).groupby(['Book_Number', 'Page_Number', 'Entities']).agg({'Polarity': 'sum'}).reset_index()

    fig = px.line(df_aggregated,
                  x='Page_Number',
                  y='Polarity',
                  color='Entities',
                  facet_col='Book_Number',
                  title='Sum of Sentiment by Book Number and Page Number',
                  labels={'Page_Number': 'Page Number', 'Polarity': 'Sum of Sentiment', 'Entities': 'Entity Type'},
                  template='plotly_white')

    plot_html = pio.to_html(fig, full_html=False)

    entities = df['Entities'].unique()
    entities = sorted(entities.tolist() + ['All'])
    
    books = df['Book_Number'].unique()
    books = sorted(books.tolist() + ['All'])

    return render_template('index.html', plot_html=plot_html, entities=entities, books=books, selected_entity=selected_entity, selected_book=selected_book)