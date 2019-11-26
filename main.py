             
class OptimizedSchedule():
    def __init__(self, list_of_lists_of_times: list, deadline: int, 
                 list_of_important_indexes: list, time_of_the_start: int):
        super().__init__() 
        self._list_of_lists_of_times = list_of_lists_of_times
        self._deadline = deadline
        self._list_of_important_indexes = list_of_important_indexes
        self._time_of_the_start = time_of_the_start
        self.list_of_valid_lists_of_times = \
            self._validate_each_list_of_times(self._list_of_lists_of_times)
        self.the_best_list = self._find_the_best_list(self.list_of_valid_lists_of_times)
        
    def print_the_best_list(self):
        if not self.the_best_list:
            print("there are no any valid lists")
        else:
            print(self.the_best_list) # print(*self.the_best_list, sep='\n')
        
    def _find_the_best_list(self, list_of_valid_lists_of_times: list):
        if list_of_valid_lists_of_times:
            list_of_sum = []
            for i, v in enumerate(list_of_valid_lists_of_times):
                list_of_sum.append(sum(range(len(v))))
                
            index_of_the_best_list = list_of_sum.index(min(list_of_sum))
            return list_of_valid_lists_of_times[index_of_the_best_list]
        return None
        
    def _validate_each_list_of_times(self, list_of_lists_of_times: list):
        raw_list_of_valid_lists_of_times = []
        for i, list_of_times in enumerate(list_of_lists_of_times):
            raw_list_of_valid_lists_of_times.append(self._check_validation(list_of_times))
        list_of_valid_lists_of_times = [i for i in raw_list_of_valid_lists_of_times if i]
        return list_of_valid_lists_of_times
        
    def _check_validation(self, list_of_times: list):
        _sum = self._time_of_the_start
        try:
            if self._list_of_important_indexes:  
                for i in range(0, max(self._list_of_important_indexes)):
                    _sum += list_of_times[i]
            else:  # if _list_of_important_indexes is empty then we compare sum of all elements with the deadline 
                for i in range(0, len(list_of_times)):
                    _sum += list_of_times[i]
            if self._deadline > _sum:
                return list_of_times
        except:
            invalid_input = True
        return None
        
        
if __name__ == "__main__":
    
    N = 5 # N is number of items, just the length of the list
    # lists down below are the lists of time of processing each item
    # (each element is the time of processing current item with that index)
    list_1 = [2, 2, 1, 1, 1]
    list_2 = [1, 1, .5, .5, .5] # this one is the best out of all given samples
    list_3 = [2, 2, 4, 4, 4]
    list_4 = [1, 1, 1, .5, .5]
    list_5 = [1, 2, 2, 2, 2]
    V = 4 # V is deadline, items with important indexes must be processed by this value of time
    K, L = 2, 4 # K and L are two important indexes
    U = 0 # the time of the start
    
    # Main issue: if the sum of elements(until the last important index) more than a deadline value
    #  and there is missing one or more of important elements with indexes K, L (etc)
    #  then the current list is not valid
    
    # Main task: find the shortest time to process all the elements
    #  so there is one list to find: valid list with the minimum sum of all elements
    
    optimized_schedule = OptimizedSchedule([list_1, list_2, list_3, list_4, list_5], V, [K, L], U)
    # init schedule class to process the given list of lists to get the best valid list of times
    optimized_schedule.print_the_best_list()
    # the best list of times out of all given samples is [1, 1, .5, .5, .5]