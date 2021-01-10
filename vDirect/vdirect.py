from API_requests import *
import sys
import argparse

"""
This is the implementation of the Argument Parser
"""


def main():
    parser = argparse.ArgumentParser(description='Welcome to vDirect!', epilog='Thank you for using vDirect!')
    subparsers = parser.add_subparsers(dest='command', help='Subcommands')

    vsearch_parser = subparsers.add_parser('vsearch', help='vsearch subparser help')
    vsummary_parser = subparsers.add_parser('vsummary', help='vsummary subparser help')
    vfetch_parser = subparsers.add_parser('vfetch', help='vfetch subparser help')

    # add subparsers for vSearch:
    vsearch_sps = vsearch_parser.add_subparsers(dest='type', help='subparsers for vsearch_parser')
    vog_search_parser = vsearch_sps.add_parser('vog', help='vsearch subparser for vog search')
    species_search_parser = vsearch_sps.add_parser('species', help='vsearch subparser for species search')
    protein_search_parser = vsearch_sps.add_parser('protein', help='vsearch subparser for protein search')

    # add arguments for vog_search_parser:
    vog_search_parser.add_argument('-id', type=str, action='append', nargs='+', dest='ids',
                                   help="VOG ID(s)")
    vog_search_parser.add_argument('-pmin', type=int, action='store', nargs='?', dest='pmin',
                                   help="minimum number of proteins in the VOG")
    vog_search_parser.add_argument('-pmax', type=int, action='store', nargs='?', dest='pmax',
                                   help="maximum number of proteins in the VOG")
    vog_search_parser.add_argument('-smin', type=int, action='store', nargs='?', dest='smin',
                                   help="minimum number of species in the VOG")
    vog_search_parser.add_argument('-smax', type=int, action='store', nargs='?', dest='smax',
                                   help="maximum number of species in the VOG")
    vog_search_parser.add_argument('-mingLCA', type=int, action='store', nargs='?', dest='mingLCA',
                                   help="minimum number of genomes in the Last common ancestor")
    vog_search_parser.add_argument('-maxgLCA', type=int, action='store', nargs='?', dest='maxgLCA',
                                   help="maximum number of genomes in the Last common ancestor")
    vog_search_parser.add_argument('-mingGLCA', type=int, action='store', nargs='?', dest='mingGLCA',
                                   help="minimum number of genomes in the Group of the Last common ancestor")
    vog_search_parser.add_argument('-maxgGLCA', type=int, action='store', nargs='?', dest='maxgGLCA',
                                   help="maximum number of genomes in the Group of the Last common ancestor")
    vog_search_parser.add_argument('-fctcat', type=str, action='append', nargs='+', dest='fctcat',
                                   choices=['Xu', 'Xh', 'Xp', 'Xr', 'Xs'],
                                   help="functional category: Xu, Xh, Xp, Xr, Xs. If providing more than one, separate"
                                        " them by a space.")
    vog_search_parser.add_argument('-confct', type=str, action='append', nargs='+', dest='confct',
                                   help="Concensus function")
    vog_search_parser.add_argument('-anc', '-ancestors', type=str, action='append', nargs='+', dest='anc',
                                   help="Ancestors")
    vog_search_parser.add_argument('-hs', '-highstringency', type=int, action='store', nargs='?', dest='hs',
                                   choices=[0, 1],
                                   help="High stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-ms', '-mediumstringency', type=int, action='store', nargs='?', dest='ms',
                                   choices=[0, 1],
                                   help="Medium stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-ls', '-lowstringency', type=int, action='store', nargs='?', dest='ls',
                                   choices=[0, 1],
                                   help="Low stringency? '1' for True and '0' for False")
    vog_search_parser.add_argument('-vs', '-virusspecific', type=int, action='store', nargs='?', dest='vs',
                                   choices=[0, 1],
                                   help="Virus specific? '1' for True and '0' for False")
    vog_search_parser.add_argument('-p', '-phage', type=str, action='store', nargs='?', dest='phage',
                                   choices=['mixed', 'phages_only', 'np_only'],
                                   help="specify phages_only, nonphages only or mixed")
    vog_search_parser.add_argument('-prot', '-proteins', type=str, action='append', nargs='+', dest='prot',
                                   help="Protein IDs")
    vog_search_parser.add_argument('-species', type=str, action='append', nargs='+', dest='species',
                                   help="Species Names, enclose names in quotes")
    vog_search_parser.add_argument('-tid', '-taxonid', type=int, action='append', nargs='+', dest='tid',
                                   help="Taxonomy ID(s)")
    vog_search_parser.add_argument('-u', '-union', type=str, action='store', default='i', nargs='+', dest='union',
                                   help="Do you want an (u)nion or an (i)ntersection search? Default = 'i'.")
    vog_search_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                   choices=['json', 'df', 'stdout'],
                                   help="specify a format: 'json' or 'df' or 'stdout'")

    # add arguments for species_search_parser:
    species_search_parser.add_argument('-id', type=int, action='append', nargs='+', dest='ids',
                                       help="species ID(s)")
    species_search_parser.add_argument('-n', '-name', type=str, action='store', nargs='?', dest='name',
                                       help="search for species name or part of a species name")
    species_search_parser.add_argument('-p', '-phage', type=int, action='store', nargs='?', dest='phage',
                                       help="Enter '1' for searching for phages only and '0' when wanting to search "
                                            "for nonphages only")
    species_search_parser.add_argument('-s', '-source', type=str, action='store', nargs='?', dest='source',
                                       help="search for species found in the specified source")
    species_search_parser.add_argument('-v', '-version', type=int, action='store', nargs='?', dest='version',
                                       help="search for species found in the specified version")
    species_search_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                       choices=['json', 'df', 'stdout'],
                                       help="specify a format: 'json' or 'df' or 'stdout'")

    # add arguments for protein_search_parser:
    protein_search_parser.add_argument('-tid', '-taxonid', type=int, action='append', nargs='+', dest='taxon_id',
                                       help="taxon ID(s) of the species")
    protein_search_parser.add_argument('-n', '-name', type=str, action='append', nargs='+', dest='species_name',
                                       help="search for species name or part of species name")
    protein_search_parser.add_argument('-vid', '-vogid', type=str, action='append', nargs='+', dest='vog_id',
                                       help="search for VOG IDs")
    protein_search_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                       choices=['json', 'df', 'stdout'],
                                       help="specify a format: 'json', 'df' or 'stdout'")

    # add subparsers for vSummary:
    vsummary_sps = vsummary_parser.add_subparsers(dest='type', help='subparsers for vsummary_parser')
    vog_summary_parser = vsummary_sps.add_parser('vog', help='vsummary subparser for vog summary')
    species_summary_parser = vsummary_sps.add_parser('species', help='vsummary subparser for species summary')
    protein_summary_parser = vsummary_sps.add_parser('protein', help='vsummary subparser for protein summary')

    # add arguments for vog_summary_parser:
    vog_summary_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                    help="VOG unique ID(s)")
    vog_summary_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                    choices=['json', 'df'], help="specify a format: 'json' or 'df'")

    # add arguments for protein_summary_parser:
    protein_summary_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                        help="protein ID(s)")
    protein_summary_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                        choices=['json', 'df'], help="specify a format: 'json' or 'df'")

    # add arguments for species_summary_parser:
    species_summary_parser.add_argument('-id', type=int, nargs='+', dest='taxon_ids', default=sys.stdin,
                                        help="taxon ID(s)")
    species_summary_parser.add_argument('-f', '-format', type=str, action='store', nargs='?', dest='format',
                                        choices=['json', 'df'], help="specify a format: 'json' or 'df'")

    # add subparsers for vFetch:
    vfetch_sps = vfetch_parser.add_subparsers(dest='type', help='subparsers for vfetch_parser')
    vog_fetch_parser = vfetch_sps.add_parser('vog', help='vfetch subparser for vog fetch')
    # # species fetch does not exist
    # species_fetch_parser = vfetch_sps.add_parser('species', help='vfetch subparser for species fetch')
    protein_fetch_parser = vfetch_sps.add_parser('protein', help='vfetch subparser for protein fetch')

    # add arguments for vog_fetch_parser:
    vog_fetch_parser.add_argument(type=str, action='store', choices=['hmm', 'msa'],
                                  dest='returntype', help="choose 'hmm' or 'msa'")
    vog_fetch_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,
                                  help="VOG unique identifiers")

    # add arguments for protein_fetch_parser:
    protein_fetch_parser.add_argument(type=str, action='store', choices=['faa', 'fna'],
                                      dest='returntype', help="choose 'faa' or 'fna'")
    protein_fetch_parser.add_argument('-id', type=str, nargs='+', dest='id', default=sys.stdin,  #action='append',
                                      help="Protein identifiers")

    args = parser.parse_args()

    if args.command == 'vfetch':
        if not sys.stdin.isatty():
            id = args.id.read().split()
        else:
            id = args.id

        response = vfetch(return_object=args.type, return_type=args.returntype, id=id)

        print(response)


    elif args.command == 'vsummary':
        if args.type == 'species':
            if not sys.stdin.isatty():
                id = args.taxon_ids.read().split()
            else:
                id = args.taxon_ids

            print(vsummary(return_object=args.type, format=args.format, taxon_id=id))

        elif args.type == 'protein':
            if not sys.stdin.isatty():
                id = args.id.read().split()
            else:
                id = args.id
            print(vsummary(return_object=args.type, format=args.format, id=id))

        elif args.type == 'vog':
            if not sys.stdin.isatty():
                id = args.id.read().split()
            else:
                id = args.id

            print(vsummary(return_object=args.type, format=args.format, id=id))


    elif args.command == 'vsearch':
        if args.type == 'species':
            print(vsearch(return_object=args.type, format=args.format, ids=args.ids, name=args.name,
                          phage=args.phage, source=args.source, version=args.version))

        if args.type == 'protein':
            print(vsearch(return_object=args.type, format=args.format, taxon_id=args.taxon_id,
                          species_name=args.species_name, VOG_id=args.vog_id))

        if args.type == 'vog':
            print(vsearch(return_object=args.type, format=args.format, id=args.ids, pmin=args.pmin, pmax=args.pmax,
                          smin=args.smin, smax=args.smax, mingLCA=args.mingLCA, maxgLCA=args.maxgLCA,
                          mingGLCA=args.mingGLCA, maxgGLCA=args.maxgGLCA, functional_category=args.fctcat,
                          consensus_function=args.confct, ancestors=args.anc, h_stringency=args.hs,
                          m_stringency=args.ms, l_stringency=args.ls, virus_specific=args.vs,
                          phages_nonphages=args.phage, proteins=args.prot, species=args.species, tax_id=args.tid,
                          inclusive=args.union))


if __name__ == '__main__':
    main()
