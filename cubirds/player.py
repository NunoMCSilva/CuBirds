'''
@dataclass
class Player:

    @dataclass
    class DictHand:
        dict_hand: dict[Bird, int] = field(
            default_factory=lambda: defaultdict(int))  # TODO: use defaultdict(int) as annot?

        def add(self, bird: Bird):
            self.dict_hand[bird] += 1

    id: int     # is this necessary?
    hand: DictHand = field(default_factory=DictHand)
    collection: DictHand = field(default_factory=DictHand)

    @property
    def bird_species_in_hand(self):
        return self.hand.dict_hand.keys()   # TODO: improve this a bit...

    def take_birds_from_hand(self, bird: Bird) -> list[Bird]:
        # TODO: ok, it needs some work, as well as dict hand -> remove to own file
        num = self.hand.dict_hand[bird]
        self.hand.dict_hand[bird] = 0
        return [bird] * num
'''