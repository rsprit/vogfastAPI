from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species

svc = VogService('data')
filename = "data/vog.species.list"

sp_srch = SpeciesService(filename)

sp_srch.search(name='India')

print(sp_srch[99930])

