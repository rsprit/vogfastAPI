import pandas as pd
from vogdb_api import VOG, Species, Protein, Gene

filename = "data_202/vog.species.list"

class Species_search():
	def __init__(self, filename):
		self._data = pd.read_table(filename,
                                header=0,
                                names=['name', 'id', 'phage', 'source', 'version'],
                                index_col='id') \
			.assign(phage=lambda df: df.phage == 'phage')
		print(self._data)

	def search(self, id=None, name=None, tax=None, phage=None, source=None):
		result = self._data

		#result.query(phage=True)
		#data

		if phage is not None:
			result = result[result.phage == bool(phage)]
		if name is not None:
			result = result[result.name.apply(lambda x: name.lower() in x.lower())]
		for id, row in result.iterrows():
			yield Species(id=id, **row)

