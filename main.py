from datetime import datetime
import math
from multiprocessing import Pool
from subprocess import Popen, PIPE
import random, sys
from time import time

def usage():
    print("Usage:")
    print("python3 main.py [path to pushswap exec] [number of tests] [random number from] [random number to] [number of arguments]")
    print("")
    print("Example:")
    print("python3 main.py 100 0 10 5")
    print("> 100 tests with list of 5 arguments generated randomly from 0 to 10")
    print("")
    print("python3 main.py 5 0 1 4")
    print("> 5 tests with list of 4 arguments with number generated randomly from 0 to 1")


def ft_progress(lst, max_len):
    current_index = 0
    elapsed_time = datetime.now()

    for i in lst:
        current_index += 1

        percentage = math.ceil(current_index / max_len * 100)
        one_p_in_s = (datetime.now() - elapsed_time).total_seconds() / percentage
        eta = one_p_in_s * (100 - percentage)

        print("ETA: {:.2f}s [{:3>d}%][{:10}] {}/{} | elapsed time {:.2f}s".format(
            eta,
            percentage,
            "="*(math.ceil(percentage/10) - 1) + ">",
            current_index,
            max_len,
            (datetime.now() - elapsed_time).total_seconds()
        ), end="\r")

        yield i
    print()

def generate_number_test(unique_elements = True):
    global nb_from, nb_to, size_test
    test_set = []

    if unique_elements and nb_to - nb_from < size_test:
        raise Exception("Can't generate unique lists with range that is smaller than the range size")

    if unique_elements:
        for _ in range(0, size_test):
            gen = str(random.randint(nb_from, nb_to))
            while gen in test_set:
                gen = str(random.randint(nb_from, nb_to))
            test_set.append(gen)
    else:
        for _ in range(0, size_test):
            gen = str(random.randint(nb_from, nb_to))
            test_set.append(gen)
    return test_set

def test_push_swap(test_id):
    global path_pushswap

    test_set = generate_number_test()

    start = time()
    process = Popen([path_pushswap] + test_set, stdout=PIPE, stderr=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    end = time()
    
    err = err.splitlines(False)
    if b"Error" in err:
        return (exit_code > 0, 0, end - start, )

    output = [el.decode('utf-8') for el in output.splitlines(False)]
    
    test_set
    return (exit_code == 0, len(output), end - start, )

if __name__ == "__main__":
    if len(sys.argv) != 6:
        usage()
        exit(1)

    try:
        path_pushswap = sys.argv[1]
        nb_tests = int(sys.argv[2])
        assert nb_tests > 0, "You can't set negative number of tests..."
        nb_from = int(sys.argv[3])
        nb_to = int(sys.argv[4])
        size_test = int(sys.argv[5])
    except Exception as e:
        print(f"Please, respect the rules of the tester: {e}")
        exit(1)

    print(f"Number of tests: {nb_tests}")
    with Pool(10) as p:
        results = []
        for res in ft_progress(p.imap_unordered(test_push_swap, list(range(0, nb_tests))), max_len=nb_tests):
            results.append(res)
    good_results = [el for el in results if el[0] == True]
    print(f"Success: {len(good_results)} ({math.ceil(len(good_results)*100/len(results))}%)")

    print("============ Resolution stats ==============")
    resolution_stats = [el[1] for el in good_results]
    print(f"Mean: {math.ceil(sum(resolution_stats) / len(good_results)):d}")
    print(f"Min: {min(resolution_stats)}")
    print(f"Max: {max(resolution_stats)}")
    if nb_tests > 3 and min(resolution_stats) == max(resolution_stats):
        print("Radix sort is used")

    print("============ Time to resolve ==============")
    print(f"Mean : {sum([el[2] for el in good_results]) / len(good_results):0.2f} sec")
    print(f"Min : {min([el[2] for el in good_results]):0.2f} sec")
    print(f"Max : {max([el[2] for el in good_results]):0.2f} sec")
