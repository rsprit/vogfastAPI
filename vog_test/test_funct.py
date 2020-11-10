from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species

svc = VogService('/home/sigi/Documents/fastAPI/data')
#filename = "/home/sigi/Documents/fastAPI/data"

print("Testing Search:")
#result = svc.species.search(name='India')
result = svc.species.search(id=1032892)
print(result)
for val in result:
    print(val)




