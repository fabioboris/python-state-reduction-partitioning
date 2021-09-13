from debug import DEBUG
from state import State
from type_aliases import InputMatrix, PartitionBlocks, StatesTable


class PartitionBlock:
    def __init__(self):
        self.states: list[State] = []

    def __str__(self) -> str:
        _output = map(lambda state: 'S' + str(state.index), self.states)
        return '(' + ', '.join(_output) + ')'

    def __eq__(self, other) -> bool:
        return set(self.states) == set(other.states)


class Partition:
    def __init__(self):
        self.blocks: PartitionBlocks = []

    def __str__(self) -> str:
        _output = map(lambda block: str(block), self.blocks)
        return '{' + '; '.join(_output) + '}'


def create_states_table(input_matrix: InputMatrix) -> StatesTable:
    """Create the state objects list from the inputs table"""

    states: StatesTable = {}

    # create states
    for index, row in enumerate(input_matrix):
        _x0, _y0, _x1, _y1 = row
        states[index] = State(index, _x0, _y0, _x1, _y1)

    # associate next states
    for index, state in states.items():
        state.x0 = states[state._x0]
        state.x1 = states[state._x1]

    return states


def output_values_from_states(states: StatesTable) -> list:
    """Get a list of existing output values (y0,y1) list from the states table
       Eg. (0,0), (0,1), (1,0), (1,1)"""

    values = []

    for _, state in states.items():
        value = (state.y0, state.y1)

        if value not in values:
            values.append(value)

    return values


def partition_from_states(states: StatesTable) -> Partition:
    """Get the first partition fom states table based on output values"""

    values = output_values_from_states(states)
    partition = Partition()

    for value in values:
        block = PartitionBlock()

        for _, state in states.items():
            if (state.y0, state.y1) == value:
                block.states.append(state)

        partition.blocks.append(block)

    return partition


def partition_from_partition(partition: Partition, states: StatesTable) -> Partition:
    """Get the next partition from a given partition 😵"""

    _partition = Partition()

    for block in partition.blocks:
        # create x0 and x1 groups
        # associate the block number with states list
        _groups: list[dict[int, list[State]]] = [{}, {}]

        for state in block.states:
            for i, index in enumerate([state.x0.index, state.x1.index]):
                _block = None

                # search for block of current state
                for j, group_blocks in enumerate(partition.blocks):
                    if states[index] in group_blocks.states:
                        _block = j
                        break

                # create dict for first time
                if _block not in _groups[i]:
                    _groups[i][_block] = []

                _groups[i][_block].append(state)

        # no different blocks in x0 and x1 groups
        if len(_groups[0].keys()) == 1 and len(_groups[1].keys()) == 1:
            _partition.blocks.append(block)

        # create new blocks on different x0 and x1 groups
        else:
            for i in [0, 1]:
                if len(_groups[i].keys()) > 1:
                    for j, group in _groups[i].items():
                        _block = PartitionBlock()

                        # create new blocks
                        for state in group:
                            _block.states.append(state)

                        # add new block to partition
                        if (_block) not in _partition.blocks:
                            _partition.blocks.append(_block)

    return _partition


def search_partitions(partition: Partition, states: StatesTable) -> Partition:
    current_partition = partition

    while (True):
        next_partition = partition_from_partition(current_partition, states)

        if len(next_partition.blocks) == len(current_partition.blocks):
            return next_partition
        else:
            if DEBUG:
                print("\n\nNext partition:\n")
                print(next_partition)

            current_partition = next_partition


def remove_eq_states(partition: Partition, states: StatesTable):
    """Remove the remaining equivalent states"""

    if DEBUG:
        print("\n")

    for block in partition.blocks:
        if len(block.states) > 1:
            for i in reversed(range(1, len(block.states))):
                _key = block.states[i].index

                if _key in states.keys():
                    del states[_key]

                    if DEBUG:
                        print(f"Remove state: S{_key}")
