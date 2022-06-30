from clue_model import ClueModel
import interface.interface as inf

SHORT_RUN = False
DIFFERENT_STRATEGIES = False
STRAT_VS_RANDOM = True
NUM_WEAPONS = 7
NUM_SUSPECTS = 4


def run(strategy_agent1, strategy_other_agents):
    clue_model = ClueModel(3, NUM_WEAPONS, NUM_SUSPECTS, strategy_agent1, strategy_other_agents)
    # interface = inf.GameInterface(clue_model)
    # Create a Clue model with three players
    # Let the players take turns in a game of Clue
    turn = 0
    while not clue_model.check_end_state():
        print(turn)
        # input("press enter to continue")
        clue_model.step()
        turn += 1


def next_to_interface():
    if DIFFERENT_STRATEGIES:
        strats = ["RANDOM", "NOT_OWN", "ONE_OWN", "UNKNOWN", "ONE_UNKNOWN", "REASONING"]
        for strategy_agent1 in strats:
            for strategy_other_agents in strats:
                print("------------------------------------------------------------------------")
                print("Agent 1: " + strategy_agent1 + ", other agents: " + strategy_other_agents)
                run(strategy_agent1, strategy_other_agents)

    if STRAT_VS_RANDOM:
        strats = ["NOT_OWN", "ONE_OWN", "UNKNOWN", "ONE_UNKNOWN", "REASONING"]
        strategy_other_agents = "RANDOM"
        for strategy_agent1 in strats:
            print("------------------------------------------------------------------------")
            print("Agent 1: " + strategy_agent1 + ", other agents: " + strategy_other_agents)
            run(strategy_agent1, strategy_other_agents)


if __name__ == "__main__":
    if SHORT_RUN:
        strat_agent1 = "RANDOM"
        strat_other_agents = "RANDOM"
        run(strat_agent1, strat_other_agents)

        next_to_interface()
    next_to_interface()

