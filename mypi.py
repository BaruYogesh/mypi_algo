from collections import defaultdict


def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]] + item
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

                # adj_list.append((pref, topping_set))
                # adj_list[j] = adj_list[j] + 1
                adj_list[j][0].append(pref)

    # print(toppings_powerset)
    # print(adj_list)
    # # cover = bipartite_vertex_cover(adj_list[len(prefs):])
    # cover = min_vertex_cover(adj_list, len(prefs))
    # print(cover)

    # print(adj_list)
    adj_list = sorted(adj_list, key=lambda x: -len(x[0]))
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


# make_pizzas({'a', 'b', 'c'}, [{'a', 'b'}, {'a', 'b'}, {'c'}, {'a', 'c'}])


def make_pizzas_two(toppings, prefs):
    toppings_powerset = [x for x in powerset(list(toppings))]
    toppings_powerset.remove([])

    topping_set_to_users = []

    for i, topping_set in enumerate(toppings_powerset):
        topping_set_to_users.append([[], topping_set])
        for j, user in enumerate(prefs):
            if set(topping_set).issubset(prefs[user]):
                topping_set_to_users[i][0].append(user)

    topping_set_to_users = sorted(topping_set_to_users, key=lambda x: -len(x[0]))
    print(topping_set_to_users)

    selected_pizzas = []
    covered_users = set()

    i = 0
    while i < len(topping_set_to_users) and len(covered_users) < len(prefs):
        users, t = topping_set_to_users[i]

        if not len(covered_users.intersection(users)):
            selected_pizzas.append((t, len(users)))
            covered_users = covered_users.union(users)

            i += 1

        else:
            topping_set_to_users[i][0] = list(
                set(topping_set_to_users[i][0]) - covered_users
            )
            p = topping_set_to_users.pop(i)
            if p[0]:
                for j in range(i, len(topping_set_to_users)):
                    if len(topping_set_to_users[j][0]) <= len(p[0]):
                        topping_set_to_users.insert(j, p)

    print(selected_pizzas)


make_pizzas_two(
    {"a", "b", "c", "d"},
    {
        "jackson": {"a", "b", "c"},
        "baru": {"b", "d"},
        "badri": {"a", "c"},
        "hawkins": {"d"},
    },
)
