from tryalgo import bipartite_vertex_cover, max_bipartite_matching
import heapq

def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

def make_pizzas(toppings: set, prefs: list) -> list:
    
    toppings_powerset = [x for x in powerset(list(toppings))]
    toppings_powerset.remove([])

    adj_list = [[[], powerset] for powerset in toppings_powerset]

    for i, topping_set in enumerate(toppings_powerset):

        for j, pref in enumerate(prefs):

            if set(topping_set).issubset(pref):

                # adj_list[i + len(prefs)].append(j)
                # adj_list[j].append(i + len(prefs))

                #adj_list.append((pref, topping_set))
                #adj_list[j] = adj_list[j] + 1
                adj_list[j][0].append(pref)

    # print(toppings_powerset)
    # print(adj_list)
    # # cover = bipartite_vertex_cover(adj_list[len(prefs):])
    # cover = min_vertex_cover(adj_list, len(prefs))
    # print(cover)

    # print(adj_list)
    adj_list = sorted(adj_list, key = lambda x: -len(x[0]))
    print(adj_list)

    visited = set()
    selected_lists = []
    i = 0
    while i < len(adj_list) and len(visited) < len(prefs):

        curr_list, topping_set = adj_list[i]
        if not len(set(curr_list).intersection(visited)):
            selected_lists.append(tuple((topping_set, len(curr_list))))
            visited = visited.union(curr_list)

        i += 1

    print(selected_lists)

def make_pizzas_two(toppings, prefs):

    toppings_powerset = [x for x in powerset(list(toppings))]
    toppings_powerset.remove([])

    topping_set_to_users = []

    for i, topping_set in enumerate(toppings_powerset):

        topping_set_to_users.append([0, 0, [], topping_set])
        for j, user in enumerate(prefs):

            if set(topping_set).issubset(prefs[user]):
                topping_set_to_users[i][2].append(user)

    for i in range(len(topping_set_to_users)):
        topping_set_to_users[i][0] = -len(topping_set_to_users[i][2])
        topping_set_to_users[i][1] = -len(topping_set_to_users[i][3])


    heapq.heapify(topping_set_to_users)

    print(topping_set_to_users)

    selected_pizzas = []
    covered_users = set()

    while topping_set_to_users and len(covered_users) < len(prefs):

        size_users, size_pizza, users, t = heapq.heappop(topping_set_to_users)

        if not len(covered_users.intersection(users)):
            selected_pizzas.append((t, len(users)))
            covered_users = covered_users.union(users)

            i += 1

        else:
            new_userset = list(set(topping_set_to_users[i][0]) - covered_users)
            new_entry = (-len(new_userset), size_pizza, new_userset, t)

            heapq.heappush(topping_set_to_users, new_entry)

    print(selected_pizzas)


make_pizzas_two({'a', 'b', 'c', 'd'}, {'jackson': {'a','b','c'}, 'baru': {'b', 'd'}, 'badri':{'a','c'}, 'hawkins':{'d'}})