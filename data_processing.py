import csv, os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
movies = []
with open(os.path.join(__location__, "movies.csv"))as f:
    rows = csv.DictReader(f)
    for r in rows:
        movies.append(dict(r))

class DB:
    def __init__(self):
        self.database = []

    def insert(self, table):
        self.database.append(table)

    def search(self, table_name):
        for table in self.database:
            if table.table_name == table_name:
                return table
        return None
    
import copy
class Table:
    def __init__(self, table_name, table):
        self.table_name = table_name
        self.table = table
    
    def join(self, other_table, common_key):
        joined_table = Table(self.table_name + '_joins_' + other_table.table_name, [])
        for item1 in self.table:
            for item2 in other_table.table:
                if item1[common_key] == item2[common_key]:
                    dict1 = copy.deepcopy(item1)
                    dict2 = copy.deepcopy(item2)
                    dict1.update(dict2)
                    joined_table.table.append(dict1)
        return joined_table
    
    def filter(self, condition):
        filtered_table = Table(self.table_name + '_filtered', [])
        for item1 in self.table:
            if condition(item1):
                filtered_table.table.append(item1)
        return filtered_table

    def __is_float(self, element):
        if element is None: 
            return False
        try:
            float(element)
            return True
        except ValueError:
            return False

    def aggregate(self, function, aggregation_key):
        temps = []
        for item1 in self.table:
            if self.__is_float(item1[aggregation_key]):
                temps.append(float(item1[aggregation_key]))
            else:
                temps.append(item1[aggregation_key])
        return function(temps)
    
    def select(self, attributes_list):
        temps = []
        for item1 in self.table:
            dict_temp = {}
            for key in item1:
                if key in attributes_list:
                    dict_temp[key] = item1[key]
            temps.append(dict_temp)
        return temps

    def pivot_table(self, keys_to_pivot_list, keys_to_aggreagte_list, aggregate_func_list):

        unique_values_list = []
        for key_item in keys_to_pivot_list:
            temp = []
            for dict in self.table:
                if dict[key_item] not in temp:
                    temp.append(dict[key_item])
            unique_values_list.append(temp)

        # combination of unique value lists
        import combination_gen
        comb_list = combination_gen.gen_comb_list(unique_values_list)

        pivot_table = []
        # filter each combination
        for item in comb_list:
            temp_filter_table = self
            for i in range(len(item)):
                temp_filter_table = temp_filter_table.filter(lambda x: x[keys_to_pivot_list[i]] == item[i])

            # aggregate over the filtered table
            aggregate_val_list = []
            for i in range(len(keys_to_aggreagte_list)):
                aggregate_val = temp_filter_table.aggregate(aggregate_func_list[i], keys_to_aggreagte_list[i])
                aggregate_val_list.append(aggregate_val)
            pivot_table.append([item, aggregate_val_list])
        return pivot_table

    def insert_row(self, dict):
        '''
        This method inserts a dictionary, dict, into a Table object, effectively adding a row to the Table.
        '''
        dict = {}
        with open(os.path.join(__location__, "movies.csv")) as f:
            rows = csv.DictWriter(f)
            rows.writeheader(dict)
            rows.writerow(dict)
            rows.writerows(dict)




    def update_row(self, primary_attribute, primary_attribute_value, update_attribute, update_value):
        '''
        This method updates the current value of update_attribute to update_value
        For example, my_table.update_row('Film', 'A Serious Man', 'Year', '2022') will change the 'Year' attribute for the 'Film'
        'A Serious Man' from 2009 to 2022
        '''

        with open(os.path.join(__location__, "movies.csv")) as f:
            rows = csv.DictWrite(f)
            rows.writeheader(primary_attribute)
            rows.writerow(primary_attribute_value)
            rows.writerows(update_attribute)
            rows.writerows(update_value)

    def __str__(self):
        return self.table_name + ':' + str(self.table)

table1 = Table('movies', movies)

my_db = DB()
my_db.insert(table1)

table1_filters = my_db.search('movies')
comedy = table1.filter(lambda x: x['Genre'] == 'Comedy')
worldwide = comedy.aggregate(lambda x: sum(x)/len(x),'Worldwide Gross')
print(f"average value of worldwide Gross in comedy is {worldwide}")

drama = table1.filter(lambda x: x['Genre'] == 'Drama')
score = drama.aggregate(lambda x: min(x), 'Audience score %')
print(score)

fantasy = table1.filter(lambda x: x['Genre'] == 'Fantasy')
count = len(fantasy.table)
print(count)












