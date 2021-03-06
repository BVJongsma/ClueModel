# From https://github.com/erohkohl/mlsolver

"""Kripke module

Provides a tool to model Kripke structures and solve them in addition to a
modal logic formula.
"""

import copy

from itertools import chain, combinations

PRINT = False

class KripkeStructure:
    """
    This class describes a Kripke Frame with it's possible worlds and their
    transition relation.
    """

    def __init__(self, worlds, relations):
        if isinstance(worlds, list) or isinstance(worlds, dict):
            self.worlds = worlds
            self.relations = relations
        else:
            raise TypeError

    def solve(self, formula):
        """Returns a Kripke structure with minimum sub set of nodes, that each
        of it's nodes forces a given formula.
        """
        for i, subset in enumerate(self.get_power_set_of_worlds()):
            ks = KripkeStructure(self.worlds.copy(), copy.deepcopy(self.relations))
            for element in subset:
                ks.remove_node_by_name(element)
            if ks.nodes_not_follow_formula(formula) == []:
                return ks

    # Solve a kripke model and only delete relations instead of worlds
    # Updated from https://github.com/JohnRoyale/MAS2018/blob/master/mlsolver/kripke.py#L36
    def relation_solve(self, agent, formula, asked_agent):
        nodes_to_remove = self.nodes_not_follow_formula(formula, asked_agent)

        if len(nodes_to_remove) == 0:
            # print("zero nodes to remove")
            return self

        # Remove a relation for an agent if the announcement was false in that node.
        relations_to_remove = []
        for relation in self.relations[str(agent.get_unique_id())]:
            for node in nodes_to_remove:
                if node in relation:
                    relations_to_remove.append(relation)
                    break
        if PRINT:
            print("The relations of agent ", agent.get_unique_id(), "are changed as following:")
            print("Relations previously: " + str(len(self.relations[str(agent.get_unique_id())])))
            print("Relations to remove: " + str(len(relations_to_remove)))
        self.relations[str(agent.get_unique_id())] = set(self.relations[str(agent.get_unique_id())]).difference(set(relations_to_remove))
        if PRINT:
            print("Relations now: " + str(len(self.relations[str(agent.get_unique_id())])))
        return self

    def remove_node_by_name(self, node_name):
        """Removes ONE node of Kripke frame, therefore we can make knowledge
        base consistent with announcement.
        """
        for world in self.worlds.copy():
            if node_name == world.name:
                self.worlds.remove(world)

        if isinstance(self.relations, set):
            for (start_node, end_node) in self.relations.copy():
                if start_node == node_name or end_node == node_name:
                    self.relations.remove((start_node, end_node))

        if isinstance(self.relations, dict):
            for key, value in self.relations.items():
                for (start_node, end_node) in value.copy():
                    if start_node == node_name or end_node == node_name:
                        value.remove((start_node, end_node))

    def get_power_set_of_worlds(self):
        """Returns a list with all possible sub sets of world names, sorted
        by ascending number of their elements.
        """
        sub_set = [{}]
        worlds_by_name = []
        for w in self.worlds:
            worlds_by_name.append(w.name)
        for z in chain.from_iterable(
                combinations(worlds_by_name, r + 1)
                for r in range(len(worlds_by_name) + 1)):
            sub_set.append(set(z))
        return sub_set

    def nodes_not_follow_formula(self, formula, asked_agent):
        """Returns a list with all worlds of Kripke structure, where formula
         is not satisfiable
        """
        nodes_not_follow_formula = []
        cnt = 0
        for nodes in self.worlds:
            if not formula.semantic(self, cnt, asked_agent):
                nodes_not_follow_formula.append(nodes.name)
            cnt = cnt + 1
        return nodes_not_follow_formula

    def __eq__(self, other):
        """Returns true iff two Kripke structures are equivalent
        """
        if (self.worlds == [] and not other.worlds == []) \
                or (not self.worlds == [] and other.worlds == []):
            return False
        for (i, j) in zip(self.worlds, other.worlds):
            if not i.__eq__(j):
                return False

        if isinstance(self.relations, set):
            for (i, j) in zip(self.relations, other.relations):
                if not i == j:
                    return False

        if isinstance(self.relations, dict):
            for key, value in self.relations.items():
                try:
                    if not value == other.relations[key]:
                        return False
                except KeyError:
                    if not value == set():
                        return False
        return True

    def __str__(self):
        worlds_str = "(W = {"
        for world in self.worlds:
            worlds_str += str(world)
        return worlds_str + '}, R = ' + str(self.relations) + ')'


class World:
    """
    Represents the nodes of Kripke and it extends the graph to Kripke
    Structure by assigning a subset of propositional variables to each world.
    """

    def __init__(self, name, assignment):
        self.name = name
        self.assignment = assignment

    def __eq__(self, other):
        return self.name == other.name and self.assignment == other.assignment

    def __str__(self):
        return "(" + self.name + ',' + str(self.assignment) + ')'
