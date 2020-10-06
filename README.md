# Github Actions for Jupyter Notebook projects
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fmcullan%2Fjupyter-actions%2Fbadge%3Fref%3Dmaster&style=flat)](https://actions-badge.atrox.dev/mcullan/jupyter-actions/goto?ref=master)

## Overview

This repository acts as a demo for implementing some Continuous Integration testing with GitHub Actions for a project containing / based on Jupyter notebooks.

This contains features addressing the following three ideas:
1. Ensure reproducible results / environments. (Solved by using conda)
2. Avoid pushing notebooks with cell outputs. (Solved by using pre-commit git hooks)
3. Avoid merging notebooks that run with errors. (Solved by using GitHub Actions)

## Conda: `environment.yml`

We're using conda for package management. The YAML file `environment.yml` contains a specification for Python packages, etc, that need to be installed for this repository to run correctly.

**Note:** There are two ways to create a YAML file for a conda environment: manually or using `conda env export`. We are constructing this file manually. In other words, we are directly editing `environment.yml` and **only** installing packages by specifying them in this file.

If we need to add another package to the environment, we must update our YAML file and run `conda env update -f environment.yml`. We are not interactively calling `conda install` each time we need another package in our environment. 

Our approach is admittedly inconvenient. Why do we do this? 
1. Manually editing `environment.yml` makes it far easier to ensure that we are only including the minimal set of necessary packages.
2. Creating an environment file with `conda env export` lists ALL packages including dependencies, so it can be a bit messier and harder to read. It also can include some OS-specific packages that don't play nice when we try to install the environment somewhere else. 


## Clean/test notebooks: `.githooks/pre-commit`

A common complaint with Jupyter/Git workflows: accidentally pushing notebooks with cell outputs. Sometimes this is what we want, e.g. if we're using a notebook as a report and we want to share results, but perhaps we should be saving notebooks as HTML for that.

To address the former issue (pushing unintended cell outputs) we will use a **pre-commit hook**. This is a script that is called every time we `git commit`. Technically, it is run right before the commit actually happens. 

Our git hook does three things:
1. Get all file paths of IPython notebooks currently staged for commit.
2. Call `process_notebooks.py` on each notebook to strip its output.
3. Call `git add` on those notebooks again so that they are cleaned before commit. 

## GitHub Actions: `.github/workflows`

Another common issue with repositories of Jupyter Notebooks: we think everything works correctly, we push our changes, our collaborators (or audience) tries to use the notebooks, and they run into errors that we didn't catch.

How can we ensure that notebooks run correctly? We could implement some automated testing in our pre-commit hook (again using `nbconvert`), but we're going to introduce another tool, [GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions).

GitHub Actions is built for Continuous Integration / Continuous Deployment workflows, and can handle far more sophisticated projects than the one we're using here. Essentially, it lets us specify *workflows*, tests that are run on external Docker containers in response to something we do in our remote repository (for example: pushing a commit).

That's precisely what we're doing here. Our workflow builds a Docker container, installs our conda environment from `environment.yml`, and runs `pytest`. We're using `pytest` for the following:
* Test that all notebooks run
* Test that the above testing function works 

For more on GitHub Actions, there is a wonderful [tutorial](https://lab.github.com/githubtraining/github-actions:-hello-world) in the GitHub Learning Lab. In fact, this is a great resource for all kinds of GitHub tutorials! 


## Build
Run the following command to set the `pre-commit` hook:
```bash
git config --local core.hooksPath .githooks
```

Run the following command to install the conda environment:
```bash
conda env create -f environment.yml
```