from models import pizza, topping

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
    #print(adj_list)

    visited = set()
    selected_lists = []
    i = 0
    while i < len(adj_list) and len(visited) < len(prefs):
        curr_list, topping_set = adj_list[i]
        if not len(set(curr_list).intersection(visited)):
            selected_lists.append(tuple((topping_set, len(curr_list))))
            visited = visited.union(curr_list)

        i += 1

    #print(selected_lists)


# make_pizzas({'a', 'b', 'c'}, [{'a', 'b'}, {'a', 'b'}, {'c'}, {'a', 'c'}])


def make_pizzas_two(toppings, prefs):
    tolerance = 0.4 # tolerance for how much less users a topping set can cover and still be selected if it has more toppings

    toppings_powerset = [x for x in powerset(list(toppings))]
    toppings_powerset.remove([])

    topping_set_to_users = []

    for i, topping_set in enumerate(toppings_powerset):
        topping_set_to_users.append([[], topping_set])
        for j, user in enumerate(prefs):
            if set(topping_set).issubset(prefs[user]):
                topping_set_to_users[i][0].append(user)

    topping_set_to_users = sorted(topping_set_to_users, key=lambda x: -len(x[0]))

    selected_pizzas = []
    covered_users = set()

    # remove any topping sets that have no users
    topping_set_to_users = [x for x in topping_set_to_users if x[0]]

    i = 0
    while i < len(topping_set_to_users) and len(covered_users) < len(prefs):
        users, t = topping_set_to_users[i]

        # if this topping set has no users that have already been covered, then try to select it
        if not len(covered_users.intersection(users)):

            # if there is another topping set that covers within X% of the users as this one, but has more toppings, then we should use that one instead.
            lower_bound = len(users) * (1 - tolerance)
            candidate_topping_set = t
            candidate_users = users

            # iterate through topping sets until one has less users than the lower bound
            candidate_index = i
            j = i + 1
            while j < len(topping_set_to_users) and len(topping_set_to_users[j][0]) >= lower_bound:

                # if this topping set has users that have already been covered, then apply the same logic as below to move it to the correct position
                if len(covered_users.intersection(topping_set_to_users[j][0])):
                    topping_set_to_users[j][0] = list(
                        set(topping_set_to_users[j][0]) - covered_users
                    )
                    p = topping_set_to_users.pop(j)
                    if p[0]:
                        for k in range(j, len(topping_set_to_users)):
                            if len(topping_set_to_users[k][0]) <= len(p[0]):
                                topping_set_to_users.insert(k, p)
                # else if this topping set no longer has any users, then remove it
                elif len(topping_set_to_users[j][0]) == 0:
                    topping_set_to_users.pop(j)
                # otherwise, we can consider it as a candidate
                else:
                    #print(topping_set_to_users[j])
                    # if there is a topping set with more toppings than candidate, then use that one instead 
                    if(len(topping_set_to_users[j][1]) > len(candidate_topping_set)):
                        candidate_topping_set = topping_set_to_users[j][1]
                        candidate_users = topping_set_to_users[j][0]
                        candidate_index = j
                    j = j + 1

            selected_pizzas.append((candidate_topping_set, len(candidate_users)))
            covered_users = covered_users.union(candidate_users)

            # if candidate is not at the index we started at, delete candidate, insert original at candidate's index
            if candidate_index != i:
                topping_set_to_users.pop(candidate_index)
                topping_set_to_users.insert(candidate_index, [users, t])

            i += 1

        # if this topping set has no users at all, then remove it
        elif len(users) == 0:
            topping_set_to_users.pop(i)
        
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
    return selected_pizzas


# make_pizzas_two(
#     {"a", "b", "c", "d"},
#     {
#         "jackson": {"a", "b", "c"},
#         "baru": {"b", "d"},
#         "badri": {"a", "c"},
#         "hawkins": {"d"},
#     },
# )

# make_pizzas_two(
#     {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#     {
#         "jackson": {"a", "b", "c"},
#         "baru": {"b", "d"},
#         "badri": {"a", "c"},
#         "hawkins": {"d"},
#         "ethan": {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#         # give me some random pairs with less than 8 toppings
#         "jackson2": {"a", "b"},
#         "baru2": {"b", "d"},
#         "badri2": {"a", "c"},
#         "hawkins2": {"d"},
#         "ethan2": {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#         "jackson3": {"a", "b"},
#         "baru3": {"b", "d"},
#         "badri3": {"a", "c"},
#         "hawkins3": {"d"},
#         "ethan3": {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#         "jackson4": {"a", "b"},
#     },
# )
