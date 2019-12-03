import json


class FileHandler():
    def __init__(self):
        super().__init__() 
    
    def print_data(self, data: dict):
        for k, v in data.items():
                    print('{}: {}'.format(k, v))
    
    def write_json_file(self, path: str, data: dict, indent=4):
        try:
            with open(path, 'w') as f:
                json.dump(data, f, indent=indent)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
            
    def write_json_file_wo_indent(self, path: str, data: dict):
        try:
            with open(path, 'w') as f:
                json.dump(data, f)
        except:
            print("Error: cannot write the data to the file with this path:")
            print("Path: " + str(path))
        return None
    
    def read_json_file(self, path: str):
        try:
            with open(path) as f:
                data = json.load(f)
            return data
        except:
            print("Error: cannot read the data from the file with this path:")
            print("Path: " + str(path))
        return None
             

class OptimizedSchedule():
    def __init__(self):
        super().__init__() 
        self.list_of_lists_of_times = None # T
        self.deadline = None # V
        self.list_of_important_indexes = None # I
        self.time_of_the_start = None # U
        self.valid_length_of_list = None # N
 
    def init(self, data: dict):
        self.list_of_lists_of_times = data['T'] # list_of_lists_of_times
        self.deadline = data['V'] # deadline
        self.list_of_important_indexes = data['I'] # list_of_important_indexes
        self.time_of_the_start = data['U'] # time_of_the_start
        self.valid_length_of_list = data['N'] # valid_length_of_list
 
    def find_the_best_list(self):
        list_of_valid_lists_of_times = self._validate_each_list_of_times()
        if list_of_valid_lists_of_times:
            list_of_sum = []
            for i, v in enumerate(list_of_valid_lists_of_times):
                list_of_sum.append(sum(range(len(v))))
            index_of_the_best_list = list_of_sum.index(min(list_of_sum))
            return list_of_valid_lists_of_times[index_of_the_best_list]
        return None
        
    def _validate_each_list_of_times(self):
        raw_list_of_valid_lists_of_times = []
        for i, list_of_times in enumerate(self.list_of_lists_of_times):
            raw_list_of_valid_lists_of_times.append(self._check_validation(list_of_times))
        list_of_valid_lists_of_times = [i for i in raw_list_of_valid_lists_of_times if i]
        return list_of_valid_lists_of_times
        
    def _check_validation(self, list_of_times: list):
        _sum = self.time_of_the_start
        try:
            if len(list_of_times) == self.valid_length_of_list:
                if self.list_of_important_indexes:  
                    for i in range(0, max(self.list_of_important_indexes)):
                        _sum += list_of_times[i]
                else:  # if list_of_important_indexes is empty then we compare sum of all elements with the deadline 
                    for i in range(0, len(list_of_times)):
                        _sum += list_of_times[i]
                if self.deadline > _sum:
                    return list_of_times
        except:
            print('Error: Input is not correct.')
        return None
        
            
class ScheduleManager():
    def __init__(self):
        super().__init__() 
        self.file_handler = FileHandler()
    
    def set_schedule_by_raw_data(self, data: dict):
        schedule = OptimizedSchedule()
        schedule.list_of_lists_of_times = data['T'] # list_of_lists_of_times
        schedule.deadline = data['V'] # deadline
        schedule.list_of_important_indexes = data['I'] # list_of_important_indexes
        schedule.time_of_the_start = data['U'] # time_of_the_start
        schedule.valid_length_of_list = data['N'] # valid_length_of_list
        return schedule
    
    def _dump(self, schedule: OptimizedSchedule):
        data = {
            'T': tuple(schedule.list_of_lists_of_times),
            'V': schedule.deadline,
            'I': tuple(schedule.list_of_important_indexes),
            'U': schedule.time_of_the_start,
            'N': schedule.valid_length_of_list
        }
        return data
    
    def write_the_best_list_to_file(self, path: str, schedule: OptimizedSchedule):
        try:
            pass
            # data = self._dump(schedule)
            # the_best_list = schedule.find_the_best_list()
        except:
            print('Error: Could not find the best list.')
        return None
    
    def write_data_to_json(self, path: str, schedule: OptimizedSchedule):
        try:
            data = self._dump_to_dict(schedule)
            self.file_handler.write_json_file(path, data)
        except:
            print('Error: Cannot write the data to the file.')
        return None
    
    def read_data_from_json(self, path: str):
        try:
            raw_data = self.file_handler.read_json_file(path)
            return self.set_schedule_by_raw_data(
                self._get_correct_dict_out_of_raw_data(raw_data))
        except:
            print('Error: Cannot read the data from the file.')
        return None
    
    def _get_correct_dict_out_of_raw_data(self, raw_data: dict):
        try:
            dict_to_return = {
                'T': raw_data['T'], # list_of_lists_of_times
                'V': raw_data['V'], # deadline
                'I': raw_data['I'], # list_of_important_indexes
                'U': raw_data['U'], # time_of_the_start
                'N': raw_data['N'], # valid_length_of_list
            }
            return dict_to_return
        except:
            print('Error: Input is not correct.')
        return None
    
    
def demo_0():
    # given values
    N = 5 # N is number of items, just the length of the list
    V = 4 # V is deadline, items with important indexes must be processed by this value of time
    K, L = 2, 4 # K and L are two important indexes
    I = [K, L] # list of important indexes
    U = 0 # the time of the start
    
    # lists down below are the lists of time of processing each item
    # (each element is the time of processing current item with that index)
    T = [  # list_of_lists_with_times
        [2, 2, 1, 1, 1],
        [1, 1, .5, .5, .5], # this one is the best out of all given samples
        [2, 2, 4, 4, 4],
        [1, 1, 1, .5, .5],
        [1, 2, 2, 2, 2]    
    ]
    
    # Main issue: if the sum of elements(until the last important index) more than a deadline value
    #  and there is missing one or more of important elements with indexes K, L (etc)
    #  then the current list is not valid
    
    # Main task: find the shortest time to process all the elements
    #  so there is one list to find: valid list with the minimum sum of all elements
    
    data_to_dump = {
        'N': N,
        'V': V,
        'I': tuple([K, L]),
        'U': U,
        'T': tuple(T)
    }
    schedule = OptimizedSchedule()
    schedule.init(data_to_dump)
    
    sm = ScheduleManager()
    sm.write_data_to_json('input_0.json', schedule)


def demo_1():
    
    sm = ScheduleManager()
    schedule = sm.read_data_from_json('input_0.json')
    sm.write_data_to_json('input_1.json', schedule)
    
    print(schedule.find_the_best_list())

        
if __name__ == "__main__":
    
    demo_1()
    