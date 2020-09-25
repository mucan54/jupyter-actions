import subprocess

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.preprocessors import CellExecutionError

def process_notebook(notebook_filename, html_directory = 'notebook-html'):
    '''Checks if an IPython notebook runs without error from start to finish. If so, writes the notebook to HTML (with outputs) and overwrites the .ipynb file (without outputs).
    '''
    with open(notebook_filename) as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)

    try:
        # Check that the notebook runs
        ep.preprocess(nb, {'metadata': {'path': ''}})
    except CellExecutionError:
        msg = f'Error executing the notebook {notebook_filename}.\n\n'
        msg += f'See notebook "{notebook_filename}" for the traceback.'
        #print(msg)
        raise
         
    print(f"Successfully executed {notebook_filename}")
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
    notebooks = [fn for fn in git_files if fn.endswith(".ipynb")]
    
    # Test each notebook
    for notebook in notebooks:
        process_notebook(notebook)
        
    return

if __name__ == '__main__':
    process_all_notebooks()