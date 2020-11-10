from typing import Set
from unittest.mock import MagicMock

from vogdb.functionality import VogService, SpeciesService
from vogdb.vogdb_api import Species
import unittest

svc = VogService('/home/sigi/Documents/fastAPI/data')
#filename = "/home/sigi/Documents/fastAPI/data"

print("Testing Search:")
#both names have to be contained. OR functionality?
result = svc.species.search(name=['India', 'leaf'], phage=False)
res2 = svc.species[1002724]
# IDs are unique -> when asking for ids, everything else is ignored.
res3 = svc.species.search(ids=[1002724, 1000664], name=['India'])
print(res3)
print("res3: ")
print(res3)
for val in res3:
    print(val)

#result = svc.species.search(ids=[1032892])
# print(result)
# for val in result:
#     print(val)


class TestSpeciesMethods(unittest.TestCase):

    def test_species_id(self):
        print("Testing species id:")
        self.assertEqual(svc.species[1002724], Species(id=1002724, name='Shigella virus Shfl1', phage=True, source='NCBI Refseq'))

        geno = svc.species.search(ids=[1002724, 1000664])
        print("geno")
        print(geno.__next__())
        print(geno.__next__())

        self.assertEqual(svc.species.search(ids=[1002724, 1000664]),
                          geno)

        mock_foo = MagicMock()
        mock_foo.iter.return_value = iter([1, 2, 3])
        list(mock_foo.iter())

if __name__ == '__main__':
    unittest.main()