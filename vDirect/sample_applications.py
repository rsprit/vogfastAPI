from vDirect_demo import *

""" Here we are trying different use cases. Those examples (and many others) will eventually be used for testing
You run this script and then type in the console number of example you want to try out e.g. 1 for example_1()
"""

def example_1():
    """Example_1: retrieve hmm profile of two vogs"""
    response = vfetch(return_object='hmm', uid=['VOG00001', 'VOG00002'])
    return response

def example_2():
    """Example_2: save text object (hmm,msa)"""
    response = vfetch(return_object='hmm', uid=['VOG00001', 'VOG00002'])

    save_object(response, output_path="/home/nikicajea/Desktop/vogs.hmm")

    return "File saved!"

def example_3():
    """Example_2: get summary table of two vogs """
    response = vsummary(return_object='vog', format="dataframe", uid=['VOG00001', 'VOG00002'])

    return response


def example_4():
    """Example_2: get summary table of two species """
    response = vsummary(return_object='species', format="dataframe", taxon_id=['2713308', '2591111'])

    return response



if __name__ == "__main__":
    functions = [example_1, example_2, example_3, example_4]

    docs = [f.__doc__.split('\n')[0] for f in functions]  # 1st line of docs

    while True:
        for i in range(len(functions)):
            print('  %3d - %s' % (i + 1, docs[i]))
        try:
            choice = int(input('Sample to run: ')) - 1
            assert 0 <= choice < len(functions)
        except (ValueError, AssertionError, KeyboardInterrupt, EOFError):
            print('\n This sample does not exist.Bye!')
            break
        print(functions[choice]())