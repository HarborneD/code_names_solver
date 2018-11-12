import requests
# obj = requests.get('http://api.conceptnet.io/c/en/traffic').json()
from itertools import chain, combinations

from example_board import board

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def GetRelatedWordList(search_word):
    search_word = search_word.replace(" ","_")
    offset = 0

    fetch_new =True
    search_word_results = []

    while(fetch_new):
        fetch_new = False
        obj = requests.get('http://api.conceptnet.io/c/en/'+search_word+'?offset='+str(offset*1000)+'&rel=/r/RelatedTo&limit=1000').json()

        

        if("view" in obj):
            if("nextPage" in obj["view"]):
                next_page = obj["view"]["nextPage"]
                fetch_new = True
                offset+=1

        for word_edge in obj["edges"]:
            start_word = word_edge["start"]
            end_word = word_edge["end"]
            
            if(start_word["label"] != search_word):
                if("language" in start_word):
                    if(start_word["language"] == 'en'):
                        search_word_results.append((start_word["label"],word_edge["weight"]))
                
            if(end_word["label"] != search_word):
                if("language" in end_word):
                    if(end_word["language"] == 'en'):
                        search_word_results.append((end_word["label"],word_edge["weight"]))

    return search_word_results


def MergeWeightDict(global_dict,word_dict):
    for k in word_dict.keys():
        if(not k in global_dict):
            global_dict[k] = []

        global_dict[k].append(word_dict[k])

    return global_dict


def PerformSearch(search_words,word_result_store):
    results = []

    weights_dict = {}

    for search_word in search_words:
        word_weight_dict = {}

        if(not search_word in word_result_store):
            word_result_store[search_word] = GetRelatedWordList(search_word)
        search_results = word_result_store[search_word]

        for search_result in search_results:
            if(not search_result[0] in word_weight_dict):
                word_weight_dict[search_result[0]] = search_result[1]
            else:
                word_weight_dict[search_result[0]] = max(search_result[1],word_weight_dict[search_result[0]])
            
        results.append(set([r[0] for r in search_results]))

        weights_dict = MergeWeightDict(weights_dict,word_weight_dict)

    possibilities_set = results[0]
    for results_set in results[1:]:
        possibilities_set = possibilities_set & results_set

    return possibilities_set, weights_dict, word_result_store


def GeneratePotentialGuesses(potential_clue_words):

    word_combos = list(powerset(potential_clue_words))
    word_combos = [list(c) for c in word_combos if len(c) > 1]
    

    word_result_store = {}

    sorted_guess_words = []

    for search_words in word_combos:
        
        link_words, weights, word_result_store = PerformSearch(search_words, word_result_store)
       
        weighted_link_words = []
        for link_word in link_words:
            weighted_link_words.append( (link_word, sum(weights[link_word])/len(weights[link_word])) )

        sorted_link_words = sorted(weighted_link_words, key=lambda x: x[1], reverse=True)

        if(len(sorted_link_words) >0):
            # print("search_words:",search_words)
            # print("best link word:",sorted_link_words[0] )

            sorted_guess_words.append( (tuple(search_words),sorted_link_words[0][0],sorted_link_words[0][1]) )


    sorted_guess_words = sorted(sorted_guess_words, key=lambda x: x[2], reverse=True)


    return sorted_guess_words

def PickGuess(sorted_guess_words):

    working_list = [w for w in sorted_guess_words if w[2] >= 1]

    print(working_list)

    working_list = [(w[0],w[1],w[2]+len(w[0])) for w in working_list]

    working_list = sorted(working_list, key=lambda x: x[2], reverse=True)

    return working_list

def SolveClue(clue_word,board_words):

    related_words = GetRelatedWordList(clue_word)

    possible_words = [w for w in related_words if w[0] in board_words]

    return possible_words

if __name__ == '__main__':

    guessing = True

    if(guessing):
        clue_word = "instrument"
        guesses = SolveClue(clue_word,[w[0].lower() for w in board])

        print(guesses)

    if(not guessing):
        team_words = [w[0].lower() for w in board if w[1] == "r"]
        # clue_words = ["robin","hood","millionaire","pound","cup","ball"]

        eliminated_words = [] #["palm","organ","cloak","track","triangle",'unicorn','england']

        team_words = [w for w in team_words if w not in eliminated_words]
        print(team_words)

        sorted_guess_words = GeneratePotentialGuesses(team_words)

        # print(sorted_guess_words[0][1])
        # print(sorted_guess_words[0][0])

        guess_pick = PickGuess(sorted_guess_words)
        print(guess_pick[0])






