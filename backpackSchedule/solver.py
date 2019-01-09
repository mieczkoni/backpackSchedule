#coding: utf-8
"""
popularnosc przedmiotu
ocena przedmiotu
waznosc przedmiotu

"""

import math
import random
import re

ALPHA = 0.95
RATING = 1
POPULARITY = 1


def annealing_algorithm(number, capacity, weight_cost, init_temp=1000, steps=1000):
    """

    :param number: quantity of items
    :param capacity: quantity of sotrage in bp
    :param weight_cost: how much wight the item
    :param init_temp: ilosc prob
    :param steps: w ktorym kroku znalazl rozwiazanie, pierdole to pisanie po angielsku

    :return: przekazywane argumenty dalej, najoptymalniejsze przypisanie przedmiotu do nauczyciela

    """
    start_sol = init_solution(weight_cost, capacity)
    best_cost, solution = simulate(start_sol, weight_cost, capacity, init_temp, steps)
    best_combination = [0] * number
    for idx in solution:
        best_combination[idx] = 1
    return best_cost, best_combination


def init_solution(weight_cost, max_weight):
    """ Uzywana do generowania przykladowych rozwiazan.
        Dodając losowy przedmiot, podczas gdy waga jest mniejsza niż maksymalna.
    """
    solution = []
    allowed_positions = list(range(len(weight_cost)))
    main_param = (RATING + POPULARITY)/2

    for wc in list(weight_cost):
        wc[0] *= main_param
    while len(allowed_positions) > 0:
        idx = random.randint(0, len(allowed_positions) - 1)
        selected_position = allowed_positions.pop(idx)
        if get_cost_and_weight_of_knapsack(solution + [selected_position], weight_cost)[1] <= max_weight:
            solution.append(selected_position)
        else:
            break
    return solution


def get_cost_and_weight_of_knapsack(solution, weight_cost):
    """Get cost and weight of knapsack - fitness function
    """
    cost, weight = 0, 0
    for item in solution:
        weight += weight_cost[item][0]
        cost += weight_cost[item][1]
    return cost, weight


def moveto(solution, weight_cost, max_weight):
    """All possible moves are generated"""
    moves = []
    for idx, _ in enumerate(weight_cost):
        if idx not in solution:
            move = solution[:]
            move.append(idx)
            if get_cost_and_weight_of_knapsack(move, weight_cost)[1] <= max_weight:
                moves.append(move)
    for idx, _ in enumerate(solution):
        move = solution[:]
        del move[idx]
        if move not in moves:
            moves.append(move)
    return moves


def simulate(solution, weight_cost, max_weight, init_temp, steps):
    """Simulated annealing approach for Knapsack problem

    :param solution: primary, not the best current solution
    :param weight_cost: construct os weight and cost structures
    :param max_weight: backpack param
    :param init_temp: initial teperature for algorithm
    :param steps: quantinity of steps"""
    temperature = init_temp
    best = solution
    best_cost = get_cost_and_weight_of_knapsack(solution, weight_cost)[0]

    current_sol = solution
    while True:
        current_cost = get_cost_and_weight_of_knapsack(best, weight_cost)[0]
        for i in range(0, steps):
            moves = moveto(current_sol, weight_cost, max_weight)
            idx = random.randint(0, len(moves) - 1)
            random_move = moves[idx]
            delta = get_cost_and_weight_of_knapsack(random_move, weight_cost)[0] - best_cost
            if delta > 0:
                best = random_move
                best_cost = get_cost_and_weight_of_knapsack(best, weight_cost)[0]
                current_sol = random_move
            else:
                if math.exp(delta / float(temperature)) > random.random():
                    current_sol = random_move

        temperature *= ALPHA
        if current_cost >= best_cost or temperature <= 0:
            break
    return best_cost, best

def parse_line(line):
    """Line parser method
    :param line: line from input file
    :return: list like: (instance id, number of items, knapsack capacity,
                            list of lists like: [(weight, cost), (weight, cost), ...])
    """
    parts = [int(value) for value in line.split()]
    inst_id, number, capacity = parts[0:3]
    weight_cost = [[parts[i], parts[i + 1]] for i in range(3, len(parts), 2)]
    return inst_id, number, capacity, weight_cost


def get_bp_id(inst_file_path):
    """Find all backpack ID, helper method

    :param inst_file_path: input file path
    :return bp_ids: all backpacks id
    """
    bp_ids = []
    holder = open(inst_file_path, "r+")
    for line in holder:
        bp_ids.append(re.match("^(\d{4})", line))
    return bp_ids


def solver(inst_file_path, solution_file_path):
    """Main method that solves knapsack problem using simulated annealing method

    :param inst_file_path: path to file with input instances
    :param solution_file_path: path to file where solver should write output data
    """
    inst_file = open(inst_file_path, "r+")
    sol_file = open(solution_file_path, "w+")

    for line in inst_file:
        inst_id, number, capacity, weight_cost = parse_line(line)
        best_cost, best_combination = annealing_algorithm(number, capacity, weight_cost)
        best_combination_str = " ".join("%s" % i for i in best_combination)
        sol_file.write("%s %s %s  %s\n" % (inst_id, number, best_cost, best_combination_str))

    inst_file.close()
    sol_file.close()
    return "success"

