#!/bin/sh
#

STASH_NAME="pre-commit-$(date +%s)"
git stash save  --include-untracked -q --keep-index $STASH_NAME


# Test prospective commit
num_notebooks=`git diff --cached --name-only | grep  -c .ipynb`
notebooks=`git diff --cached --name-only | grep  .ipynb`

if [ ${num_notebooks} -eq 0 ]; then
     echo "No notebooks to process."
 else
 	echo "processing notebooks: $notebooks"
     python test_and_clear_notebooks.py $notebooks
 fi
git add .


STASHES=$(git stash list)
if [[ $STASHES == "$STASH_NAME" ]]; then
  git stash pop -q
fi

