import graphviz

def create_survey_pipeline_dag():
    """
    Creates a DAG representing a data orchestration pipeline from survey ingestion 
    to API publication and final CSV download generation.
    """
    dot = graphviz.Digraph(comment='Survey Data Pipeline', engine='neato')
    dot.attr(rankdir='LR', size='10,8', ratio='fill', splines='curved')
    dot.attr('node', shape='box', style='rounded,filled', fontname='Arial', width='1.5', height='0.8')
    dot.attr('edge', style='bold', color='#666666')
    
    # Define node styles
    ingestion_style = {'fillcolor': '#e1f5fe', 'color': '#0277bd'}
    processing_style = {'fillcolor': '#f3e5f5', 'color': '#7b1fa2'}
    validation_style = {'fillcolor': '#fff3e0', 'color': '#ef6c00'}
    storage_style = {'fillcolor': '#e8f5e8', 'color': '#388e3c'}
    api_style = {'fillcolor': '#fce4ec', 'color': '#c2185b'}
    publication_style = {'fillcolor': '#f1f8e9', 'color': '#689f38'}
    
    # Data Ingestion Layer
    dot.node('ingest_survey', 'Ingest Survey\nData', **ingestion_style)
    dot.node('validate_data', 'Validate &\nClean Data', **validation_style)
    
    # Data Processing Layer
    dot.node('process_data', 'Process &\nTransform', **processing_style)
    dot.node('store_data', 'Store to\nWarehouse', **storage_style)
    
    # Analytics Layer
    dot.node('compute_stats', 'Compute\nStatistics', **processing_style)
    
    # API Layer
    dot.node('publish_api', 'Publish to\nAPI', **api_style)
    
    # Publication Layer
    dot.node('generate_csv', 'Generate CSV\nfrom API', **publication_style)
    dot.node('publish_website', 'Publish to\nWebsite', **publication_style)
    
    # Define the DAG edges (dependencies) - simplified linear flow
    dot.edge('ingest_survey', 'validate_data')
    dot.edge('validate_data', 'process_data')
    dot.edge('process_data', 'store_data')
    dot.edge('store_data', 'compute_stats')
    dot.edge('compute_stats', 'publish_api')
    dot.edge('publish_api', 'generate_csv')
    dot.edge('generate_csv', 'publish_website')
    
    return dot

# Create and render the DAG
if __name__ == "__main__":
    dag = create_survey_pipeline_dag()
    
    # Render to various formats
    dag.render('survey_pipeline_dag', format='svg', cleanup=True)
    # dag.render('survey_pipeline_dag', format='png', cleanup=True)
    # dag.render('survey_pipeline_dag', format='pdf', cleanup=True)
    
    # # Print the DOT source code
    # print("Graphviz DOT source:")
    # print(dag.source)
    
    # # Save DOT file
    # with open('survey_pipeline_dag.dot', 'w') as f:
    #     f.write(dag.source)