'''
# TODO: put in it's own file
@dataclass
class Table:
    table: list[list[Bird]]

    def add_to_row(self, *args):        ### birds, row, side):
        raise NotImplementedError

        """
        if bird in self.table[row]:
            raise NotImplementedError
        else:
            if side == Side.RIGHT:
                self.table[row].extend(bird)
        """
'''
'''
@dataclass
class Table:
    table: list[list[Species]] = field(default=None)

    def add_to_row(self, row, side, species, num):
        # check presence
        surrounded = species in self.table[row]
        print(surrounded)

        def add(row, side, cards):
            if side == Side.LEFT:
                # TODO: needs work
                for c in cards:
                    row.insert(0, c)
            else:
                row.extend(cards)

        if surrounded:
            raise NotImplementedError
        else:
            add(self.table[row], side, [species] * num)
            return None

        """
        if surrounded:
            self.table[row].index(species)
            self.table[row].count(species)
        """
        """
        # add
        print(self.table[row])

        if side == Side.LEFT:
            # TODO: needs work
            for _ in range(num):
                self.table[row].insert(0, species)

            print(self.table[row])
        """

        """
        if side == Side.LEFT:
            # TODO: needs work
            start = num
            for _ in range(num):
                self.table[row].insert(0, species)
            print(start, self.table[row], self.table[row][start:])
        else:
            end = len(self.table[row])
            self.table[row].extend([species] * num)
            print(end, self.table[row], self.table[row][:end])

        if surrounded:
            print(self.table[row])
        else:
            return None
        """
'''