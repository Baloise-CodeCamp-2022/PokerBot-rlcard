from rlcard.games.maumau.utils import cards2list, WILD


class MauMauRound:

    def __init__(self, dealer, num_players, np_random):
        ''' Initialize the round class

        Args:
            dealer (object): the object of MauMauDealer
            num_players (int): the number of players in game
        '''
        self.np_random = np_random
        self.dealer = dealer
        self.target = None
        self.current_player = 0
        self.num_players = num_players
        self.direction = 1
        self.played_cards = []
        self.is_over = False
        self.winner = None

    def flip_top_card(self):
        ''' Flip the top card of the card pile

        Returns:
            (object of MauMauCard): the top card in game

        '''
        top = self.dealer.flip_top_card()
        if top.rank == 'J':
            top.suit = self.np_random.choice(WILD)
        self.target = top
        self.played_cards.append(top)
        return top

    def perform_top_card(self, players, top_card):
        ''' Perform the top card

        Args:
            players (list): list of MauMauPlayer objects
            top_card (object): object of MauMauCard
        '''
        if top_card.rank == '8':
            self.current_player = 1
        elif top_card.rank == '7':
            player = players[self.current_player]
            self.dealer.deal_cards(player, 2)

    def proceed_round(self, players, action):
        ''' Call other Classes's functions to keep one round running

        Args:
            player (object): object of MauMauPlayer
            action (str): string of legal action
        '''
        if action == 'draw':
            self._perform_draw_action(players)
            return None
        player = players[self.current_player]
        suit = action[0]
        rank = action[1]
        # remove correspongding card
        remove_index = None
        if rank == 'J':
            for index, card in enumerate(player.hand):
                if rank == card.rank:
                    remove_index = index
                    break
        else:
            for index, card in enumerate(player.hand):
                if suit == card.suit and rank == card.rank:
                    remove_index = index
                    break
        card = player.hand.pop(remove_index)
        if not player.hand:
            self.is_over = True
            self.winner = [self.current_player]
        self.played_cards.append(card)

        if card.rank in ['7', '8', 'J']:
            self._perform_card_action(players, card)

        else:
            self.current_player = (self.current_player + self.direction) % self.num_players
            self.target = card

    def get_legal_actions(self, players, player_id):
        wild_flag = 0
        legal_actions = []
        hand = players[player_id].hand
        target = self.target
        if target.rank == 'J':
            for card in hand:
                if card.rank == 'J':
                    if wild_flag == 0:
                        wild_flag = 1
                        legal_actions.extend(WILD)
                elif card.suit == target.suit:
                    legal_actions.append(card.str)

        # target is action card or number card
        else:
            for card in hand:
                if card.rank == 'J':
                    if wild_flag == 0:
                        wild_flag = 1
                        legal_actions.extend(WILD)
                elif card.suit == target.suit or card.rank == target.rank:
                    legal_actions.append(card.str)
        if not legal_actions:
            legal_actions = ['7']
        return legal_actions

    def get_state(self, players, player_id):
        ''' Get player's state

        Args:
            players (list): The list of MauMauPlayer
            player_id (int): The id of the player
        '''
        state = {}
        player = players[player_id]
        state['hand'] = cards2list(player.hand)
        state['target'] = self.target.str
        state['played_cards'] = cards2list(self.played_cards)
        state['legal_actions'] = self.get_legal_actions(players, player_id)
        state['num_cards'] = []
        for player in players:
            state['num_cards'].append(len(player.hand))
        return state

    def replace_deck(self):
        ''' Add cards have been played to deck
        '''
        self.dealer.deck.extend(self.played_cards)
        self.dealer.shuffle()
        self.played_cards = []

    def _perform_draw_action(self, players):
        # replace deck if there is no card in draw pile
        if not self.dealer.deck:
            self.replace_deck()
            #self.is_over = True
            #self.winner = MauMauJudger.judge_winner(players)
            #return None

        card = self.dealer.deck.pop()

        # draw a wild card
        if card.rank == 'J':
            card.suit = self.np_random.choice(['S', 'H', 'D', 'C'])
            self.target = card
            self.played_cards.append(card)
            self.current_player = (self.current_player + self.direction) % self.num_players

        # draw a card with the same color of target
        elif card.suit == self.target.suit:
            if card.rank in ['7', '8', 'J']:
                self.played_cards.append(card)
                self._perform_card_action(players, card)
            else:
                self.target = card
                self.played_cards.append(card)
                self.current_player = (self.current_player + self.direction) % self.num_players

        # draw a card with the diffrent color of target
        else:
            players[self.current_player].hand.append(card)
            self.current_player = (self.current_player + self.direction) % self.num_players

    def _perform_card_action(self, players, card):
        current = self.current_player
        direction = self.direction
        num_players = self.num_players

        # perfrom skip card
        if card.rank == '8':
            current = (current + direction) % num_players

        # perform draw_2 card
        elif card.rank == '7':
            if len(self.dealer.deck) < 2:
                self.replace_deck()
                #self.is_over = True
                #self.winner = MauMauJudger.judge_winner(players)
                #return None
            self.dealer.deal_cards(players[(current + direction) % num_players], 2)
            current = (current + direction) % num_players

        self.current_player = (current + self.direction) % num_players
        self.target = card
