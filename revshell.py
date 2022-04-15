




def revshell_packer(revshell):
    #f'{revshell} & echo '
    totally_obfuscated = []
    for index,char in enumerate([i for i in revshell]):
        if find_char(char):
            query = find_char(char)
            q_index = query['index']
            if q_index == 2:
                q_index = "_+_"
            elif q_index == 3:
                q_index = "_ + _ + _"
            elif q_index == 4:
                q_index = "_ + _ +_ +_"
            elif q_index == 5:
                q_index = "_ +_ +_ +_ +_"
            elif q_index == 0:
                q_index = "_ - _"
            elif q_index == 6:
                q_index = "___ +_ + _ +_"
            elif q_index == 7:
                q_index = "____ + _ +_ +_"
            elif q_index == 8:
                q_index = "______ + __"
            elif q_index == 1:
                q_index = "_"
            totally_obfuscated.append(f"{query['to_eval']}[{q_index}]\n")
        else:
            return "Error"
    totally_obfuscated.append(' "&"')

    return obfuscated_revshell

print(revshell_packer('powershell -c gci '))