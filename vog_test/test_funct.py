from typing import Set

from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species, VOG
import unittest

svc = VogService('/home/sigi/Documents/fastAPI/data')

print("Testing Search:")
# both names have to be contained. OR functionality?
res3 = svc.species.search(name=['Joydebpur betasatellite'], phage=False)
res2 = svc.species[1002724]
# IDs are unique -> when asking for ids, everything else is ignored.
res4 = svc.species.search(ids=[1002724, 1000664], name=['India'])
print(res3)

print("res3: ")
for val in res3:
    print(val)

print("Testing VOGSearch:")
#res = svc.groups.search(gmin=1000, gmax=2000, h_stringency=False, protein_names={"260372.YP_024429.1"})
res = svc.groups.search(gmin=1000, gmax=20000, l_stringency=False, names=['VOG00001', 'VOG00029']) # virus_spec=True)
#res = svc.groups.__getitem__("VOG00029")
print(res)
print("result of VOG search: ")
for val in res:
    print(val)
    print("tst5")
#res5 = svc.groups.search(names=['VOG00029', 'VOG00027'], l_stringency=True)
#res5 = svc.groups.search(gmin=1000, gmax=20000, names=['VOG00029', 'VOG00027', 'VOG00818'], virus_spec=False)
res5 = svc.groups.search(names=['VOG00029', 'VOG00027', 'VOG00818'], virus_spec=False)

for val in res5:
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

    def test_group_search(self):
        # test getting VOG by id, check for length:
        self.assertEqual(len(list(svc.groups.search(["VOG00029"]))), 1)
        self.assertEqual(len(list(svc.groups.search(["VOG00029", "VOG00001"]))), 2)
        self.assertEqual(len(list(svc.groups.search(names=['VOG00029', 'VOG00027', 'VOG00818'], virus_spec=True))), 1)
        self.assertEqual(len(list(svc.groups.search(names=['VOG00029', 'VOG00027', 'VOG00818'], virus_spec=False))), 2)


if __name__ == '__main__':
    unittest.main()
