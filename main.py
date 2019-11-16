             
class Schedule():
    def __init__(self, list_of_lists_of_times: list, deadline: int, 
                 list_of_important_indexes: list):
        super().__init__() 
        
        self._list_of_lists_of_times = list_of_lists_of_times
        self._deadline = deadline
        self._list_of_important_indexes = list_of_important_indexes
        
        self.list_of_valid_lists_of_times = \
            self.validate_each_list_of_time(self._list_of_lists_of_times)
        self.the_best_list = self.find_the_best_list(self.list_of_valid_lists_of_times)
        
    def print_the_best_list(self):
        if not self.the_best_list:
            print("there is no any valid lists")
        else:
            print(*self.the_best_list, sep='\n')
        
    def find_the_best_list(self, list_of_valid_lists_of_times: list):
        if list_of_valid_lists_of_times:
            list_of_sum = []
            for i, v in enumerate(list_of_valid_lists_of_times):
                list_of_sum.append(sum(range(len(v))))
                
            index_of_the_best_list = list_of_sum.index(min(list_of_sum))
            return list_of_valid_lists_of_times[index_of_the_best_list]
        return None
        
    def validate_each_list_of_time(self, list_of_lists_of_times: list):
        raw_list_of_valid_lists_of_times = []
        for i, list_of_times in enumerate(list_of_lists_of_times):
            raw_list_of_valid_lists_of_times.append(self.check_validation(list_of_times))
        list_of_valid_lists_of_times = [i for i in raw_list_of_valid_lists_of_times if i]
        return list_of_valid_lists_of_times
        
    def check_validation(self, list_of_time: list):
        _sum = 0
        try:
            for i in range(0, max(self._list_of_important_indexes)):
                _sum += list_of_time[i]
            if self._deadline > _sum:
                return list_of_time
        except:
            invalid_input = True
        return None
        
        
if __name__ == "__main__":
    
    # the input
    
    N = 5 # N is number of items, just the length of the list
    # lists below are lists of time of processing each item
    # (each element is the time of processing current item with that index)
    list_1 = [2, 2, 1, 1, 1]
    list_2 = [1, 1, .5, .5, .5] # this one is the best out of all given samples
    list_3 = [2, 2, 4, 4, 4]
    list_4 = [1, 1, 1, .5, .5]
    list_5 = [1, 2, 2, 2, 2]
    V = 4 # V is deadline
    K, L = 2, 4 # K and L are two important indexes
    
    # Main issue: if the sum of elements more than a deadline value
    #  and there is missing one or more of important elements with indexes K, L (etc)
    #  then the current list is not valid
    
    # Main task: find the shortest time to process all the elements
    # so there is one list to find: valid list with the min sum of all elements
    
    # the code:
    
    schedule = Schedule([list_1, list_2, list_3, list_4, list_5], V, [K, L])
    schedule.print_the_best_list()
    
    print('hey')