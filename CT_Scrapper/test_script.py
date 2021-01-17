import json
from registry import RegistryArray


new_json_file = open('Data/test3.json', 'a')
all_the_pairs = []

bla = RegistryArray()
bla = bla.getInstance()



for i in range(10):
    one_pair = {'from_id': f'origin_{i}',
                'to_id': f'destination_{i}',
                'r2r_min_euro_price': None,
                'data': []
                }

    dict_ = {}
    dict_['number'] = i  # reference problem
    bla.append_item(i)


    one_pair['data'].append(dict_)  #  every 'scrap pair' result

    all_the_pairs.append(one_pair)



print()
print(all_the_pairs)

all_the_pairs_json = json.dumps(all_the_pairs)

new_json_file.write(all_the_pairs_json)
print(bla.items)






