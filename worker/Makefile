CONDA_ENV=cee-hacks-2020-images-worker

# creates environment from the file
conda-create:
	conda env create -f conda.yml --name $(CONDA_ENV)

# exports all changes made locally - then one must copy the changes to conda.yml
conda-export:
	conda env export --from-history

# updates environment when some changes were applied to the file
conda-update:
	conda env update --file conda.yml --prune --name $(CONDA_ENV)

# does not actually work, has to be called manually
conda-activate:
	conda activate $(CONDA_ENV)
