import os
import subprocess

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ClearOutputPreprocessor, ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

def process_notebook(notebook_filename, html_directory = 'notebook-html'):
    '''Checks if an IPython notebook runs without error from start to finish. If so, writes the notebook to HTML (with outputs) and overwrites the .ipynb file (without outputs).
    '''
    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
        
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    clear = ClearOutputPreprocessor()
    
    html_exporter = HTMLExporter()
    html_exporter.template_name = 'classic'

    try:
        # Check that the notebook runs
        ep.preprocess(nb, {'metadata': {'path': ''}})
        msg = ''
    except CellExecutionError:
        out = None
        msg = f'\n  Error executing the notebook "{notebook_filename}".\n'
        msg += f'  See notebook "{notebook_filename}" for the traceback.'
    finally:
        # Process and save html with notebook outputs
        html_filename = notebook_filename.replace('.ipynb', '.html')
        html_destination = os.path.join(html_directory, html_filename)
        with open(html_destination, 'w') as f:
            html_out, resources = html_exporter.from_notebook_node(nb)
            f.write(html_out)
            
        # Clear notebook outputs and save as .ipynb
        cleared = clear.preprocess(nb, {})
        with open(notebook_filename, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)
         
    print(f"Processed {notebook_filename}{msg}")
    return
    

        
def process_all_notebooks(remove_fail_test=True):
    '''Runs `process_notebook` on all notebooks in the git repository.
    '''
    # Get all files included in the git repository
    git_files = (subprocess
                 .check_output("git ls-files", shell=True)
                 .decode('utf-8')
                 .splitlines())

    # Get just the notebooks from the git files
    notebooks = {fn:fn for fn in git_files if fn.endswith(".ipynb")}
    
    # Remove the notebook that tested this code
    del notebooks['Notebook-testing-demo.ipynb']
    
    # Remove the notebook that's supposed to fail
    if remove_fail_test:
        del notebooks['notebook-fails.ipynb']
    
    # Test each notebook, save it to HTML with outputs, and clear the outputs from the .ipynb file
    for notebook in notebooks:
        process_notebook(notebook)
        
    return

if __name__ == '__main__':
    process_all_notebooks(remove_fail_test=False)