import argparse
import os
import subprocess

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ClearOutputPreprocessor, ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

def get_tags_flat(nb):
    cells = nb['cells']
    tags = [cell['metadata'].get('tags') for cell in cells]
    tags = [tag for tag in tags if tag]

    tags_flat = [tag for cell_tag in tags for tag in cell_tag]

    return tags_flat

def save_html(nb, notebook_filename, html_directory):
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'

    html_filename = notebook_filename.replace('.ipynb', '.html')
    html_destination = os.path.join(html_directory, html_filename)

    with open(html_destination, 'w') as f:
        html_out, resources = html_exporter.from_notebook_node(nb)
        f.write(html_out)

def process_notebook(notebook_filename, html_directory = 'notebook-html', execute=True):
    '''Checks if an IPython notebook runs without error from start to finish. If so, writes the notebook to HTML (with outputs) and overwrites the .ipynb file (without outputs).
    '''
    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
        
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    clear = ClearOutputPreprocessor()
    
    try:
        # Check that the notebook runs
        ep.preprocess(nb, {'metadata': {'path': ''}})
        msg = ''
    except CellExecutionError:
        out = None
        msg = f'\n  Error executing the notebook "{notebook_filename}".\n'
        msg += f'  See notebook "{notebook_filename}" for the traceback.'
    finally:
        tags_flat = get_tags_flat(nb)

        if 'save_html' in tags_flat:
            print("Writing html")
            save_html(nb, notebook_filename, html_directory)

        # Clear notebook outputs and save as .ipynb
        cleared = clear.preprocess(nb, {})
        with open(notebook_filename, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)
         
    print(f"Processed {notebook_filename}{msg}")
    return
    


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='read some notebok files')
    parser.add_argument('notebooks', metavar='Notebooks', type=str, nargs='+',
                        help='notebooks')
    args = parser.parse_args()

    notebooks = args.notebooks

    for fn in notebooks:
        if not fn.endswith('.ipynb'):
            print(f'Error: file {fn} is not an IPython notebook.')
            raise
        
    for fn in notebooks:
        process_notebook(fn)
    
