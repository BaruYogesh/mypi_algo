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
    tolerance = 0.51 # tolerance for how much less users a topping set can cover and still be selected if it has more toppings

    toppings_powerset = [x for x in powerset(list(toppings))]
    toppings_powerset.remove([])

    topping_set_to_users = []

    for i, topping_set in enumerate(toppings_powerset):
        topping_set_to_users.append([[], topping_set])
        for j, user in enumerate(prefs):
            if set(topping_set).issubset(prefs[user]):
                topping_set_to_users[i][0].append(user)

    topping_set_to_users = sorted(topping_set_to_users, key=lambda x: -len(x[0]))
    #print(topping_set_to_users)

    selected_pizzas = []
    covered_users = set()

    # remove any topping sets that have no users
    topping_set_to_users = [x for x in topping_set_to_users if x[0]]

    i = 0
    while i < len(topping_set_to_users) and len(covered_users) < len(prefs):
        users, t = topping_set_to_users[i]

        # if this topping set has no users that have already been covered, then try to select it
        if not len(covered_users.intersection(users)):

            #print("Checking", t, "with", len(users), "users")

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
                    # print that this topping set has users that have already been covered and who they are
                    #print("Topping set", topping_set_to_users[j][1], "has users that have already been covered:", covered_users.intersection(topping_set_to_users[j][0]))
                    topping_set_to_users[j][0] = list(
                        set(topping_set_to_users[j][0]) - covered_users
                    )
                    p = topping_set_to_users.pop(j)
                    #print("Popped", p[1], "at", j, "with", len(p[0]), "users")
                    if p[0]:
                        for k in range(j, len(topping_set_to_users)):
                            if len(topping_set_to_users[k][0]) <= len(p[0]):
                                topping_set_to_users.insert(k, p)
                                #print("Inserted", p[1], "at", k)
                            # if we reach the end of the list, then append it
                            if(k == len(topping_set_to_users) - 1):
                                topping_set_to_users.append(p)
                                #print("Appended", p[1], "at", j + 1)
                                break

                # else if this topping set no longer has any users, then remove it
                elif len(topping_set_to_users[j][0]) == 0:
                    topping_set_to_users.pop(j)
                # otherwise, we can consider it as a candidate
                else:
                    #print(topping_set_to_users[j])
                    # if there is a topping set with more toppings than candidate, then use that one instead 
                    if(len(topping_set_to_users[j][1]) > len(candidate_topping_set) and len(topping_set_to_users[j][0]) >0):
                        candidate_topping_set = topping_set_to_users[j][1]
                        candidate_users = topping_set_to_users[j][0]
                        candidate_index = j
                    j = j + 1

            selected_pizzas.append((candidate_topping_set, candidate_users))
            covered_users = covered_users.union(candidate_users)

            # if candidate is not at the index we started at, delete candidate, insert original at candidate's index
            # if candidate_index != i:
            #     topping_set_to_users.pop(candidate_index)
            #     topping_set_to_users.insert(candidate_index, [users, t])

            # if candidate is not at the index we started at, swap original with candidate
            # if candidate_index != i:
            #     topping_set_to_users[i], topping_set_to_users[candidate_index] = topping_set_to_users[candidate_index], topping_set_to_users[i]

            # pop selected topping set, don't increment i
            topping_set_to_users.pop(candidate_index)

            #i += 1

        # if this topping set has no users at all, then remove it
        elif len(users) == 0:
            topping_set_to_users.pop(i)
        
        else:
            # print that this topping set has users that have already been covered and who they are
            #print("Topping set", t, "has users that have already been covered:", covered_users.intersection(users))
            topping_set_to_users[i][0] = list(
                set(topping_set_to_users[i][0]) - covered_users
            )
            
            # if this topping set is still the most popular, leave it where it is
            p = topping_set_to_users.pop(i)

            #print("Popped", p[1], "at", i, "with", len(p[0]), "users")

            #print(p)
            if p[0]:
                for j in range(i, len(topping_set_to_users)):
                    #print(j, topping_set_to_users[j][1], len(topping_set_to_users[j][0]))
                    if len(topping_set_to_users[j][0]) <= len(p[0]):
                        topping_set_to_users.insert(j, p)
                        #print("Inserted", p[1], "at", j)
                        break
                    # if we reach the end of the list, then append it
                    if(j == len(topping_set_to_users) - 1):
                        topping_set_to_users.append(p)
                        #print("Appended", p[1], "at", j + 1)
                        break

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

#try make_pizzas_two with a large set of users that like both ham and pineapple, but a few that only like ham
pizzas = make_pizzas_two(
    {"ham", "pineapple", "pepperoni", "sausage", "mushrooms", "onions"},
    {
        "jackson": {"ham", "pineapple"},
        "baru": {"ham", "pineapple"},
        "badri": {"ham", "pineapple"},
        "hawkins": {"ham", "pineapple"},
        "ethan": {"ham", "pineapple"},
        "jackson2": {"ham", "pineapple"},
        "baru2": {"ham", "pineapple"},
        "badri2": {"ham", "pineapple"},
        "ham_only": {"ham"},
        "ham_only2": {"ham"},
        "ham_only3": {"ham"},
        "ham_only4": {"ham"},
        "ham_only5": {"ham"},
        "ham_only6": {"ham"},
        "pepperoni_only": {"pepperoni"},
        "pepperoni_only2": {"pepperoni"},
        "pepperoni_only3": {"pepperoni"},
        "pepperoni_only4": {"pepperoni"},
        "pepperoni_only5": {"pepperoni"},
        "pepperoni_only6": {"pepperoni"},
        "pepperoni_only7": {"pepperoni"},
        "pepperoni_only8": {"pepperoni"},
        "pepperoni_only9": {"pepperoni"},
        "pepperoni_sausage": {"pepperoni", "sausage"},
        "pepperoni_sausage2": {"pepperoni", "sausage"},
        "pepperoni_sausage3": {"pepperoni", "sausage"},
        "pepperoni_sausage4": {"pepperoni", "sausage"},
        "pepperoni_sausage5": {"pepperoni", "sausage"},
        "onions_only": {"onions"},
        "onions_only2": {"onions"},
        "onions_only3": {"onions"},
        "the_works": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works2": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works3": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works4": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works5": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works6": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works7": {"pepperoni", "sausage", "mushrooms", "onions"},
        "the_works8": {"pepperoni", "sausage", "mushrooms", "onions"},
        "mushrooms_only": {"mushrooms"},
        "mushrooms_only2": {"mushrooms"},
    }
)

# get the number of users that like each topping
for pizza in pizzas:
    print(pizza[0], "has", len(pizza[1]), "users")

# make_pizzas_two(
#     {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#     {
#         "jackson": {"a", "b", "c"},
#         "baru": {"b", "d"},
#         "badri": {"a", "c"},
#         "hawkins": {"d"},
#         "ethan": {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
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
#         "baru4": {"b", "d"},
#         "badri4": {"a", "c"},
#         "hawkins4": {"d"},
#         "ethan4": {"a", "b", "c", "d", "e", "f", "g", "h", "i"},
#         "jackson5": {"a", "b"},
#         "baru5": {"b", "d"},
#         "badri5": {"a", "c"},
#         "hawkins5": {"d"},
#     },
# )
