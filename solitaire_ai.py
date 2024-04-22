import random


class SolitaireGame:
    def __init__(self):
        # Initialize the game components
        self.stock = []
        self.waste = []
        self.foundation = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(7)]
        self.state_counts = {}  # Used to detect cycles
        self.setup_game()

    def setup_game(self):
        # Create a standard deck and shuffle it
        deck = [(num, suit) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
                for num in range(1, 14)]
        random.shuffle(deck)
        # Distribute cards to tableau
        for i in range(7):
            self.tableau[i] = [(num, suit, 'down') for num, suit in deck[:i+1]]
            # Turn the last card face up
            self.tableau[i][-1] = (self.tableau[i][-1][0],
                                   self.tableau[i][-1][1], 'up')
            deck = deck[i+1:]
        self.stock = deck  # Remaining cards go to the stock

    def flip_cards(self):
        '''Flips all top level cards from tableau to up.'''
        for pile in self.tableau:
            if pile:
                card = pile[-1]
                if len(card) == 3 and card[2] == 'down':
                    pile[-1] = (card[0], card[1], 'up')

    def is_game_over(self):
        # The game is over when all cards are in the foundation piles
        return all(len(pile) == 13 for pile in self.foundation)

    def is_game_unwinnable(self, allowed_repetitions=300):
        current_state = self.get_current_state()
        if current_state in self.state_counts:
            if self.state_counts[current_state] >= allowed_repetitions:
                print(f"State has repeated {allowed_repetitions} times - cycle likely.")
                return True
            self.state_counts[current_state] += 1
        else:
            self.state_counts[current_state] = 1
        return False

    def get_possible_actions(self):
        actions = []
        for i, pile in enumerate(self.tableau):
            if pile:
                top_card = pile[-1]
                # Using exception handling to catch tuple index errors which can be useful for debugging
                try:
                    if top_card[2] == 'up':  # Directly check for 'up' status
                        actions.extend([('move_tableau_to_foundation', i, f) for f in range(
                            4) if self.can_move_to_foundation(top_card, f)])
                        for j in range(7):
                            if i != j and self.can_stack(top_card, self.tableau[j]):
                                actions.append(
                                    ('move_tableau_to_tableau', i, j))
                except IndexError:
                    print(f"IndexError: Incorrect tuple size for card {top_card} in tableau index {i}")
        # Adding similar safety checks and error handling for waste
        if self.waste:
            waste_card = self.waste[-1]
            try:
                if waste_card[2] == 'up':  # Checking if the top waste card is face up
                    actions.extend([('move_waste_to_foundation', f) for f in range(
                        4) if self.can_move_to_foundation(waste_card, f)])
                    for j in range(7):
                        if self.can_stack(waste_card, self.tableau[j]):
                            actions.append(('move_waste_to_tableau', j))
            except IndexError:
                print(f"IndexError: Incorrect tuple size for waste card {waste_card}")
        # Check for other actions like drawing a card from stock or resetting the stock
        if self.stock:
            actions.append(('draw_card',))
        elif self.waste:
            actions.append(('reset_stock',))
        return actions

    def can_move_to_foundation(self, card, foundation_index):
        foundation = self.foundation[foundation_index]
        if not foundation and len(card) == 3:
            return card[0] == 1  # Ace must start the foundation
        elif foundation:
            top_card = foundation[-1]
            if len(top_card) == 3 and len(card) == 3:
                # same suit and added card is the next sequential card
                return card[1] == top_card[1] and card[0] == top_card[0] + 1
        return False

    def can_stack(self, card, pile):
        if not pile:
            return False  # Cannot stack on an empty pile
        top_card = pile[-1]
        if len(card) < 3 or len(top_card) < 3:  # Safe check before accessing
            print(f"Error in card data: {card}, {top_card}")
            return False
        return top_card[2] == 'up' and self.alternate_color(card, top_card) and card[0] == top_card[0] - 1

    def alternate_color(self, card1, card2):
        # Check if two cards have alternating colors
        red_suits = {'Hearts', 'Diamonds'}
        card1_red = card1[1] in red_suits
        card2_red = card2[1] in red_suits
        return card1_red != card2_red

    def display_game(self):
        # Maps the suit text to symbols
        suit_symbols = {'Hearts': '♥️', 'Diamonds': '♦️',
                        'Clubs': '♣️', 'Spades': '♠️'}
        print("Foundations:")
        for i, foundation in enumerate(self.foundation):
            if foundation:
                print(f"Foundation {i+1}: " + ' '.join(f"{num}{suit_symbols[suit]}" for num, suit, _ in foundation))
            else:
                print(f"Foundation {i+1}: Empty")
        print("\nTableaus:")
        for i, tableau in enumerate(self.tableau):
            if tableau:
                print(f"Tableau {i+1}: " + ' '.join(f"{num}{suit_symbols[suit]}{'↑' if state == 'up' else '↓'}" for num, suit, state in tableau))
            else:
                print(f"Tableau {i+1}: Empty")
        print("\nWaste Top Card: ", end="")
        if self.waste:
            num, suit, _ = self.waste[-1]
            print(f"{num}{suit_symbols[suit]}")
        else:
            print("Empty")
        print("Stock Remaining: ", len(self.stock))
        print("-" * 40)

    def perform_action(self, action):
        # Execute a given action
        if action[0] == 'move_tableau_to_foundation':
            card = self.tableau[action[1]].pop()
            # Make sure card has three elements
            self.foundation[action[2]].append((card[0], card[1], 'up'))
            if self.tableau[action[1]]:
                self.flip_cards()  # Ensure the top card is face up
        elif action[0] == 'move_waste_to_foundation':
            card = self.waste.pop()
            self.foundation[action[1]].append((card[0], card[1], 'up'))
        elif action[0] == 'move_tableau_to_tableau':
            source, target = action[1], action[2]
            card = self.tableau[source].pop()
            self.tableau[target].append((card[0], card[1], 'up'))
            if self.tableau[source]:
                self.flip_cards()
        elif action[0] == 'move_waste_to_tableau':
            card = self.waste.pop()
            self.tableau[action[1]].append((card[0], card[1], 'up'))
        elif action[0] == 'draw_card':
            card = self.stock.pop()
            self.waste.append((card[0], card[1], 'up'))
        elif action[0] == 'reset_stock':
            # recycles waste back into stock
            self.stock = [(card[0], card[1], 'down')
                          for card in self.waste[::-1]]
            self.waste = []
        self.flip_cards()

    def get_current_state(self):
        # Generate a hashable representation of the current state
        # to be used as a key in the Q-table
        tableau_state = tuple(tuple(pile) for pile in self.tableau)
        waste_state = tuple(self.waste)
        foundation_state = tuple(tuple(pile) for pile in self.foundation)
        stock_size = len(self.stock)
        return (tableau_state, waste_state, foundation_state, stock_size)

    def get_reward(self, old_state, new_state):
        # Define rewards based on the progression of the game
        old_foundation_cards = sum(len(pile) for pile in old_state[2])
        new_foundation_cards = sum(len(pile) for pile in new_state[2])
        # Reward increasing the number of cards in the foundation
        reward = (new_foundation_cards - old_foundation_cards) * 10
        # Punish if no cards are in the waste and stock and no move to foundation is possible
        if new_state[1] == () and new_state[3] == 0 and new_foundation_cards == old_foundation_cards:
            reward -= 5  # this could be tuned based on how penalizing you want to be
        return reward

    def is_action_possible(self):
        # Check if any actions are possible to continue the game
        possible_actions = self.get_possible_actions()
        if not possible_actions:
            return False  # No possible actions, game might be unwinnable/stuck
        return True


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, epsilon_min=0.01):
        self.q_table = {}  # State-action pair Q-values
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.epsilon_decay = epsilon_decay  # Decay rate for epsilon
        self.epsilon_min = epsilon_min  # Minimum value for epsilon

    def choose_action(self, state, possible_actions):
        # Choose an action using an epsilon-greedy strategy
        if random.random() < self.epsilon:
            return random.choice(possible_actions)  # Explore: random action
        else:
            # Exploit: best known action
            return self.best_action(state, possible_actions)

    def best_action(self, state, possible_actions):
        # Return the best action for a given state from the Q-table
        self.ensure_state_action(state, possible_actions)
        return max(possible_actions, key=lambda action: self.q_table[state][action])

    def update_q_table(self, state, action, reward, next_state):
        try:
            old_value = self.q_table[state][action]
        except KeyError:
            self.ensure_state_action(state, [action])
            old_value = self.q_table[state].get(action, 0)
        future_rewards = max(self.q_table.get(
            next_state, {}).values(), default=0)
        new_value = (1 - self.alpha) * old_value + self.alpha * \
            (reward + self.gamma * future_rewards)
        self.q_table[state][action] = new_value
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def ensure_state_action(self, state, actions):
        if state not in self.q_table:
            self.q_table[state] = {}
        for action in actions:
            if action not in self.q_table[state]:
                self.q_table[state][action] = 0  # Initialize Q-values


def train_agent(episodes):
    agent = QLearningAgent()
    for episode in range(1, episodes+1):
        game = SolitaireGame()
        game.display_game()
        action_count = 0
        # TODO also check for stock being empty. what about reset_stock?
        while not game.is_game_over() and not game.is_game_unwinnable() and game.is_action_possible():
            state = game.get_current_state()
            actions = game.get_possible_actions()
            action = agent.choose_action(state, actions)
            game.perform_action(action)
            action_count += 1
            # game.display_game()
            new_state = game.get_current_state()
            reward = game.get_reward(state, new_state)
            agent.update_q_table(state, action, reward, new_state)
        print(f"Episode {episode} complete. Actions Taken: {action_count}")
    return agent


if __name__ == "__main__":
    print("Starting Solitaire AI Training...")
    trained_agent = train_agent(5)
    print("Training completed.\n")
    # Start a game using the trained agent
    game = SolitaireGame()
    print("Let's play a game with the trained agent:")
    while not game.is_game_over() and not game.is_game_unwinnable() and game.is_action_possible():
        state = game.get_current_state()
        actions = game.get_possible_actions()
        if not actions:
            print("No possible actions left. Ending game.")
            break
        action = trained_agent.choose_action(state, actions)
        print(f"Agent chooses action: {action}")
        game.perform_action(action)
    print("Game Over. Here's the final state:")
    print(game.get_current_state())
