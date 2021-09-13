from debug import DEBUG
from file_utils import get_file_name, get_input_from_file, save_states_to_file
from partitions import (create_states_table, partition_from_states,
                        remove_eq_states, search_partitions)

file_name = get_file_name()
input_matrix = get_input_from_file(file_name)
states = create_states_table(input_matrix)

if DEBUG:
    print("\n\nThe original states table:\n")
    for _, state in states.items():
        print(state)

# create first partition
partition = partition_from_states(states)

if DEBUG:
    print("\n\nThe first partition:\n")
    print(partition)

partition = search_partitions(partition, states)

remove_eq_states(partition, states)

if DEBUG:
    print("\n\nThe new states table:\n")
    for _, state in states.items():
        print(state)

save_states_to_file("data/output.txt", states)
