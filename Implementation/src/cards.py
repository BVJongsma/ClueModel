import random

class Cards():
    """The cards that are present in the game"""

    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.weapons = ["candle", "dagger", "rope", "wrench"]
        self.suspects = ["Green", "Mustard", "Plum", "Scarlet"]
        self.all_cards = self.weapons + self.suspects
        self.available_cards = self.weapons + self.suspects

    # Get all of the cards that are in the game
    def get_all_cards(self):
        return self.all_cards

    # Get all of the weapon cards that are in the game
    def get_all_weapon_cards(self):
        return self.weapons

    # Get all of the suspect cards that are in the game
    def get_all_suspect_cards(self):
        return self.suspects

    # Pick a random card from all of the cards
    def get_random_cards(self, num_random_cards):
        return random.sample(self.all_cards, num_random_cards)

    # Pick a random weapon card
    def get_random_weapon(self):
        return random.choice(self.weapons)

    # Pick a random suspect card
    def get_random_suspect(self):
        return random.choice(self.suspects)

    # Get a weapon card for the envelope. Make sure this card is not available anymore for the agents' cards
    def get_envelope_weapon(self):
        envelope_weapon = self.get_random_weapon()
        self.available_cards.remove(envelope_weapon)
        return envelope_weapon

    # Get a suspect card for the envelope. Make sure this card is not available anymore for the agents' cards
    def get_envelope_suspect(self):
        envelope_suspect = self.get_random_suspect()
        self.available_cards.remove(envelope_suspect)
        return envelope_suspect

    # Get a card for an agent. Make sure this card is not available anymore fot the other agents' cards
    def get_agent_cards(self):
        num_cards = int(len(self.all_cards) / self.num_agents)
        agent_cards = random.sample(self.available_cards, num_cards)
        # Sort the agent cards alphabetically
        agent_cards = sorted(agent_cards, key=str.lower)
        self.available_cards = [card for card in self.available_cards if card not in agent_cards]
        return agent_cards