from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species

svc = VogService('/home/sigi/Documents/fastAPI/data')
#filename = "/home/sigi/Documents/fastAPI/data"

print("Testing Search:")
result = svc.species.search(name='India')
print(result)




