'''Project for Operating Systems class: mock CPU scheduling.'''
import sys
import copy

class CPU:
    '''Mock CPU implementation.'''
    def __init__(self, scheduler, process_list):
        '''Initialize CPU.'''
        self.scheduler = scheduler
        self.process_list = process_list
        self.processes_remaining = len(process_list)

        self.clock = 0

        # Process queues
        self.executing = []
        self.ready = []
        self.done = []

        self.run()
        self.print_output()

    def step(self):
        '''Execute one CPU cycle.'''

        # Check for new processes
        for process in self.process_list:
            if process['creation_time'] == self.clock:
                self.ready.append(process)

        # Advance execution of process currently in CPU
        for process in self.executing:
            process['never_executed'] = False
            process['duration_remaining'] -= 1
            process['return_time'] += 1

            # Check if process has finished
            if process['duration_remaining'] == 0:
                self.done.append(process)
                self.executing.remove(process)
                self.processes_remaining -= 1

        # Do the process scheduling
        if not self.executing:
            if self.scheduler == 'FCFS':
                if self.ready:
                    process = self.ready[0]

                    self.executing.append(process)
                    self.ready.remove(process)

            elif self.scheduler == 'SJF':
                if self.ready:
                    sorted_process_list = sorted(self.ready, key=lambda t: t['duration_remaining'])
                    process = sorted_process_list[0]

                    self.executing.append(process)
                    self.ready.remove(process)

        if self.scheduler == 'RR':
            quantum = 2

            if self.clock % quantum == 0:
                if self.executing:
                    executing_process = self.executing[0]
                    self.executing.remove(executing_process)
                    self.ready.append(executing_process)

                if self.ready:
                    next_process = self.ready[0]
                    self.executing.append(next_process)
                    self.ready.remove(next_process)

        # Count time spent waiting
        for process in self.ready:
            process['wait_time'] += 1
            process['return_time'] += 1

            if process['never_executed']:
                process['response_time'] += 1

        # Done with this cycle!
        self.clock += 1

    def run(self):
        '''Run until all processes exit.'''
        while self.processes_remaining:
            self.step()

    def print_output(self):
        '''Prints average return time, response time and wait time.'''
        return_time = 0
        response_time = 0
        wait_time = 0

        for process in self.done:
            return_time += process['return_time']
            response_time += process['response_time']
            wait_time += process['wait_time']

        return_time /= len(self.done)
        response_time /= len(self.done)
        wait_time /= len(self.done)

        print('{0} {1:.1f} {2:.1f} {3:.1f}'.format(
            self.scheduler, return_time, response_time, wait_time)
        )

if __name__ == '__main__':
    process_list = []

    # Receive input from stdin
    for pid, line in enumerate(sys.stdin):
        line_split = line.split()

        if len(line_split) == 2:
            process = dict({
                'pid': pid,
                'creation_time': int(line_split[0]),
                'duration_remaining': int(line_split[1]),
                'return_time': 0,
                'response_time': 0,
                'wait_time': 0,
                'never_executed': True
                })
            process_list.append(process)
        else:
            pass # Not a valid input.

    # Instantiate CPUs with schedulers
    fcfs = CPU('FCFS', copy.deepcopy(process_list))
    sjf = CPU('SJF', copy.deepcopy(process_list))
    rr = CPU('RR', copy.deepcopy(process_list))
