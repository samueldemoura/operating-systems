import sys
from math import inf as infinite

if __name__ == '__main__':
    pages_to_access = []
    possible_algorithms = ['FIFO', 'OTM', 'LRU']
    memory_size = int(sys.stdin.readline())
    max_number_of_pages = 5 # change this later

    for line in sys.stdin:
        pages_to_access.append(int(line.strip()))

    for pagination_algorithm in possible_algorithms:
        # Array of page numbers already in memory
        memory = [None for i in range(0, memory_size)]

        # When was a certain position in memory accessed last
        last_access = [-1 for i in range(0, memory_size)]

        page_faults = 0

        for clock, page_number in enumerate(pages_to_access):
            if page_number not in memory:
                # Page fault
                page_faults += 1

                if None in memory:
                    # Enough space left, just add it to memory
                    first_free_slot = memory.index(None)
                    memory.remove(None)
                    memory.insert(first_free_slot, page_number)
                else:
                    # Memory full. Need to do a page swap
                    if pagination_algorithm == 'FIFO':
                        # Get number of page with smallest clock (first in)
                        index_to_remove = last_access.index(min(last_access))

                        # ...first out (swap out)
                        memory[index_to_remove] = page_number
                        last_access[index_to_remove] = clock

                    elif pagination_algorithm == 'OTM':
                        # Find the page farthest away from the current clock time.
                        # Look into the future
                        future = pages_to_access[clock + 1:]

                        # Calculate, for each page currently in memory, how many
                        # clock cycles in the future will it be used again
                        how_long = []
                        for page in memory:
                            try:
                                cycles_until_used_again = len(future) - list(reversed(future)).index(page)
                            except ValueError:
                                # Page will never be used again!
                                cycles_until_used_again = infinite

                            how_long.append(cycles_until_used_again)

                        # Swap out the page that will take the longest to be referenced again
                        index_to_remove = how_long.index(max(how_long))
                        memory[index_to_remove] = page_number
                        last_access[index_to_remove] = clock

                    elif pagination_algorithm == 'LRU':
                        # Find least recently used page. The algorithm is as follows:
                        # Get history of pages accessed until now (backwards)
                        history = list(reversed(pages_to_access[0:clock]))

                        # Calculate how many clock cycles ago each page that is
                        # currently in memory (that is, a candidate for being
                        # swapped out) was seen
                        last_seen = [history.index(page) for page in memory]


                        # Swap out page with highest 'last seen' value
                        index_to_remove = last_seen.index(max(last_seen))
                        memory[index_to_remove] = page_number
                        last_access[index_to_remove] = clock

        # Output
        print('{0} {1}'.format(pagination_algorithm, page_faults))
