from typing import Set

from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species
import unittest

svc = VogService('/home/sigi/Documents/fastAPI/data')
# filename = "/home/sigi/Documents/fastAPI/data"

print("Testing Search:")
# both names have to be contained. OR functionality?
result = svc.species.search(name=['India', 'leaf'], phage=False)
res2 = svc.species[1002724]
# IDs are unique -> when asking for ids, everything else is ignored.
res3 = svc.species.search(ids=[1002724, 1000664], name=['India'])
print(res3)
print("res3: ")
print(res3)
for val in res3:
    print(val)


# result = svc.species.search(ids=[1032892])
# print(result)
# for val in result:
#     print(val)


class TestSpeciesMethods(unittest.TestCase):

    def test_species_id(self):
        # test get single species by ID:
        self.assertEqual(svc.species[1002724],
                         Species(id=1002724, name='Shigella virus Shfl1', phage=True, source='NCBI Refseq'))

        # test search by ID:
        self.assertEqual(list(svc.species.search(ids=[1002724, 1000664])),
                         [Species(id=1002724, name='Shigella virus Shfl1', phage=True, source='NCBI Refseq'),
                          Species(id=1000664, name='Chilli leaf curl Vellanad virus [India/Vellanad/2008]', phage=False,
                                  source='NCBI Refseq')])


if __name__ == '__main__':
    unittest.main()
