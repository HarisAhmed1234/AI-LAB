def card_probabilities():
    total_cards = 52
    red_cards = 26
    hearts = 13
    face_cards = 12
    diamond_face = 3
    spade_face = 3
    queens = 4
    queen_spade = 1

    print(f"P(Red) = {red_cards/total_cards:.2f}")
    print(f"P(Heart | Red) = {hearts/red_cards:.2f}")
    print(f"P(Diamond | Face) = {diamond_face/face_cards:.2f}")
    print(f"P(Spade or Queen | Face) = {(spade_face + queens - queen_spade)/face_cards:.2f}")

card_probabilities()