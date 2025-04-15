import math

def alpha_beta(cards, max_score, min_score, alpha, beta, is_max_turn):
    # Base case: returning max score as no cards leftt
    if len(cards) == 0:
        return max_score
    
    if is_max_turn:
        value = -math.inf
        #leftmost card picking
        new_cards = cards[1:]
        new_max_score = max_score + cards[0]
        child_value = alpha_beta(new_cards, new_max_score, min_score, alpha, beta, False)
        value = max(value, child_value)
        alpha = max(alpha, value)
        if alpha >= beta:
            return value
        
        #rightmost card picking
        new_cards = cards[:-1]
        new_max_score = max_score + cards[-1]
        child_value = alpha_beta(new_cards, new_max_score, min_score, alpha, beta, False)
        value = max(value, child_value)
        alpha = max(alpha, value)
        if alpha >= beta:
            return value
        return value
    else:  # Min'sturn
        left_card = cards[0]
        right_card = cards[-1]
        # min pik smaller card
        if left_card <= right_card:
            new_cards = cards[1:]
            new_min_score = min_score + left_card
        else:
            new_cards = cards[:-1]
            new_min_score = min_score + right_card
        value = alpha_beta(new_cards, max_score, new_min_score, alpha, beta, True)
        beta = min(beta, value)
        return value

def play_game(initial_cards):
    cards = initial_cards[:]
    max_score = 0
    min_score = 0
    turn = 0  # 0 for Max, 1 for Min
    
    print(f"Initial Cards: {cards}")
    
    while cards:
        if turn == 0:  
            left_card = cards[0]
            right_card = cards[-1]
            
            # Evaluate picking left, right
            new_cards_left = cards[1:]
            value_left = alpha_beta(new_cards_left, max_score + left_card, min_score, -math.inf, math.inf, False) 
            new_cards_right = cards[:-1]
            value_right = alpha_beta(new_cards_right, max_score + right_card, min_score, -math.inf, math.inf, False)
            
            if value_left > value_right:
                print(f"Max picks {left_card}, Remaining Cards: {new_cards_left}")
                max_score += left_card
                cards = new_cards_left
            else:
                print(f"Max picks {right_card}, Remaining Cards: {new_cards_right}")
                max_score += right_card
                cards = new_cards_right
        else:  # Min's turn
            left_card = cards[0]
            right_card = cards[-1]
            if left_card <= right_card:
                print(f"Min picks {left_card}, Remaining Cards: {cards[1:]}")
                min_score += left_card
                cards = cards[1:]
            else:
                print(f"Min picks {right_card}, Remaining Cards: {cards[:-1]}")
                min_score += right_card
                cards = cards[:-1]
        turn = 1 - turn
    
    print(f"Final Scores - Max: {max_score}, Min: {min_score}")
    if max_score > min_score:
        print("Winner: Max")
    elif min_score > max_score:
        print("Winner: Min")
    else:
        print("Draw")

initial_cards = [4, 10, 6, 2, 9, 5]
play_game(initial_cards)