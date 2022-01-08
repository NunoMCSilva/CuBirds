
'''
# TODO: add to tests
def main():
    print(Bird.FLAMINGO)
    print(Bird.FLAMINGO.value)
    print(Bird.FLAMINGO.small_flock)
    print(Bird.FLAMINGO.big_flock)
    print(Bird.FLAMINGO.copies)

    print(list(Bird))
    assert str(list(Bird)) == '[F, O, T, D, P, M, N, R]'
    assert len(Bird) == 8

    print(Bird.get_deck())
    assert str(Bird.get_deck()) == '[[F, F, F, F, F, F, F], [O, O, O, O, O, O, O, O, O, O], [T, T, T, T, T, T, T, T, T, T], [D, D, D, D, D, D, D, D, D, D, D, D, D], [P, P, P, P, P, P, P, P, P, P, P, P, P], [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M], [N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N, N], [R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R, R]]'
    assert len(Bird.get_deck()) == 8
    assert sum(map(len, Bird.get_deck())) == 110


if __name__ == '__main__':
    main()
'''
