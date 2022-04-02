import ast
import random
from ast import *
from ast import Compare, Global, ClassDef
from ast import Subscript, Slice, Attribute, GeneratorExp, comprehension
from base64 import b64encode,b32encode
from astunparse import unparse


from utils import random_string


def import_node(name, newname):
    """Import module obfuscation"""
    # import sys -> sys = __import__('sys', globals(), locals(), [], -1)
    return Assign(
        targets=[Name(id=newname, ctx=Store())],
        value=Call(func=Name(id='__import__', ctx=Load()),
                   args=[Str(s=name),
                         Call(func=Name(id='globals', ctx=Load()), args=[],
                              keywords=[], starargs=None, kwargs=None),
                         Call(func=Name(id='locals', ctx=Load()), args=[],
                              keywords=[], starargs=None, kwargs=None),
                         List(elts=[], ctx=Load()), Num(n=-1)],
                   keywords=[], starargs=None, kwargs=None))


def obfuscate_string(s,placeholder=None):
    """Various String Obfuscation routines."""
    randstr = random_string(3, 10)
    #print('here for', s)

    table0 = [
        # '' -> ''
        lambda: Str(s=''),
    ]

    table1 = [
        # 'a' -> 'a'
        lambda x: Str(s=chr(x)),
        # 'a' -> chr(0x61)
        lambda x: Call(func=Name(id='chr', ctx=Load()), args=[Num(n=x)],
                       keywords=[], starargs=None, kwargs=None),
    ]

    table = [
        # 'abc' -> 'abc'
        lambda x: Str(s=x),
        # 'abc' -> 'a' + 'bc'
        lambda x: BinOp(left=Str(s=x[:round(len(x) / 2)]),
                        op=Add(),
                        right=Str(s=x[round(len(x) / 2):])),
        # 'abc' -> 'cba'[::-1]
        lambda x: Subscript(value=Str(s=x[::-1]),
                            slice=Slice(lower=None, upper=None,
                                        step=Num(n=-1)),
                            ctx=Load()),
        # 'abc' -> ''.join(_x for _x in reversed('cba'))
        lambda x: Call(
            func=Attribute(value=Str(s=''), attr='join', ctx=Load()), args=[
                GeneratorExp(elt=Name(id=randstr, ctx=Load()), generators=[
                    comprehension(target=Name(id=randstr, ctx=Store()),
                                  iter=Call(func=Name(id='reversed',
                                                      ctx=Load()),
                                            args=[Str(s=x[::-1])],
                                            keywords=[], starargs=None,
                                            kwargs=None),
                                  ifs=[])])],
            keywords=[], starargs=None, kwargs=None),
        lambda x: Expr(value=Call(func=Attribute(value=Constant(value='', kind=None), attr='join', ctx=Load()),
                                  args=[ListComp(elt=Call(func=Attribute(value=Subscript(value=Call(func=Name
                                  (id='globals', ctx=Load()), args=[], keywords=[]), slice=Index(value=Constant
                                  (value='__builtins__', kind=None)), ctx=Load()), attr='chr', ctx=Load()),
                                args=[Call(func=Name(id='ord', ctx=Load()),
                                args=[Name(id=randstr, ctx=Load())], keywords=[])],
                            keywords=[]), generators=[comprehension(target=Name
                            (id=randstr, ctx=Store()), iter=Subscript(value=Constant(value=x[::-1],
                            kind=None), slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(),
                                operand=Constant(value=1, kind=None))), ctx=Load()), ifs=[], is_async=0)])], keywords=[])),


    lambda x: Call(func=Attribute(value=Call(func=Attribute(value=Call(func=Name(id='getattr',
        ctx=Load()), args=[Call(func=Subscript(value=Attribute(value=Subscript(value=Call(func=Name(id='globals',
    ctx=Load()), args=[], keywords=[]), slice=Index(value=Constant(value='__builtins__', kind=None)),
ctx=Load()), attr='__dict__', ctx=Load()), slice=Index(value=Constant(value='__import__', kind=None)),
        ctx=Load()), args=[Call(func=Attribute(value=Constant(value='', kind=None), attr='join', ctx=Load()),
    args=[ListComp(elt=Call(func=Name(id='chr', ctx=Load()), args=[Call(func=Name(id='ord', ctx=Load()),
        args=[Name(id=randstr, ctx=Load())], keywords=[])], keywords=[]),
            generators=[comprehension(target=Name(id=randstr, ctx=Store()), iter=Subscript(value=Constant(value='46esab', kind=None),
            slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))),
            ctx=Load()), ifs=[], is_async=0)])], keywords=[])], keywords=[]),
                    BinOp(left=BinOp(left=BinOp(left=Constant(value='b', kind=None), op=Add(),
        right=Subscript(value=Constant(value='46', kind=None),
            slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))),
    ctx=Load())), op=Add(), right=Subscript(value=Constant(value='ced', kind=None),
        slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))),
        ctx=Load())), op=Add(), right=Subscript(value=Constant(value='edo', kind=None),
            slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))),
                ctx=Load()))], keywords=[]), attr='__call__', ctx=Load()),
                        args=[Subscript(value=Constant(value=b64encode(x.encode()).decode()[::-1], kind=None),
                slice=Slice(lower=None, upper=None, step=UnaryOp(op=USub(), operand=Constant(value=1, kind=None))), ctx=Load())],
                                                        keywords=[]), attr='decode', ctx=Load()), args=[], keywords=[]),


]
    # 'abc' -> 'cba'[::-1]

    #
    if placeholder == "formatString":
        return table[-1](s)
    if not len(s):
        return random.choice(table0)()

    if len(s) == 1:
        return random.choice(table1)(ord(s))

    return random.choice(table)(s)


class Obfuscator(NodeTransformer):
    def __init__(self):
        NodeTransformer.__init__(self)

        # imported modules
        self.imports = {}
        self.assignments = {}

        # global values (can be renamed)
        self.globs = {}
        self.functions = []
        self.inclass = False
        self.in_init = False

        # local values
        self.locs = {}
        self.fNames = {}
        # inside a function
        self.indef = False

    def obfuscate_global(self, name):
        newname = random_string(3, 10)
        if self.imports.get(name):
            return self.imports.get(name)
        if self.globs.get(name):
            return self.globs.get(name)
        self.globs[name] = newname
        return newname

    def obfuscate_local(self, name):
        newname = random_string(3, 10)
        self.locs[name] = newname
        return newname

    def visit_alias(self, node: alias):
        self.globs[node.name] = node.name
        return node


    def visit_ImportFrom(self, node: ImportFrom):
        node.names = [self.visit(name) for name in node.names]
        self.imports[node.module] = node.module
        return node
    def visit_Import(self, node):
        if self.imports.get(node.names[0].name):
            return node
        self.imports[node.names[0].name] = self.obfuscate_global(node.names[0].name)
        node.names[0].asname = self.imports[node.names[0].name]
        return node

    def visit_Expr(self, node: Expr):
        if isinstance(node.value, Call):
            node.value = self.visit_Call(node.value)
        return node

    def visit_IfExp(self, node: IfExp):
        node.test = self.visit(node.test)
        node.body = self.visit(node.body)
        node.orelse = self.visit(node.orelse)
        return node

    def visit_BoolOp(self, node: BoolOp):
        node.values = [self.visit(value) for value in node.values]
        return node


    def visit_ListComp(self, node: ListComp):
        node.elt = self.visit(node.elt)
        node.generators = [self.visit(x) for x in node.generators]
        return node

    def visit_SetComp(self, node: SetComp):
        node.elt = self.visit(node.elt)
        node.generators = [self.visit(x) for x in node.generators]
        return node

    def visit_DictComp(self, node: DictComp):
        node.elt = self.visit(node.elt)
        node.generators = [self.visit(x) for x in node.generators]
        return node

    def visit_With(self, node: With):
        node.body = [self.visit(x) for x in node.body]
        node.items = [self.visit(x) for x in node.items]
        return node

    def visit_Yield(self, node: Yield):
        node.value = self.visit(node.value)
        return node

    def visit_YieldFrom(self, node: YieldFrom):
        node.value = self.visit(node.value)
        return node



    def visit_In(self, node: In):
        return node

    def visit_NameConstant(self, node: NameConstant):
        return node

    def visit_Expression(self, node: Expression):
        return node



    def visit_Continue(self, node: Continue):
        return node

    def visit_ExceptHandler(self, node: ExceptHandler):
        node.type = self.visit(node.type)
        node.body = [self.visit(x) for x in node.body]
        return node

    def visit_While(self, node: While):
        return node
    def visit_Tuple(self, node: Tuple):
        return node

    def visit_For(self, node: For):
        #print(node.__dict__)
        node.target = self.visit_Name(node.target)
        node.iter = self.visit(node.iter)
        node.body = [self.visit(x) for x in node.body ]
        #node.target = self.visit(node.target)
        #node.body = [self.visit(x) for x in node.body]
        #node.iter = self.visit(node.iter)
        #node.orelse = [self.visit(x) for x in node.orelse]
        return node
    def visit_Try(self, node: Try):
        node.body = [self.visit(x) for x in node.body]
        node.handlers = [self.visit(x) for x in node.handlers]
        node.orelse = [self.visit(x) for x in node.orelse]
        node.finalbody = [self.visit(x) for x in node.finalbody]
        return node

    def visit_UnaryOp(self, node: UnaryOp):
        node.operand = self.visit(node.operand)

        return node

    def visit_Compare(self, node: Compare) :
        node.left = self.visit(node.left)
        node.ops = [self.visit(x) for x in node.ops]
        node.comparators = [self.visit(x) for x in node.comparators]
        return node

    def visit_comprehension(self, node: comprehension):
        node.target = self.visit_Name(node.target)
        node.iter = self.visit(node.iter)
        node.ifs = [self.visit(x) for x in node.ifs]
        return node
    def visit_GeneratorExp(self, node: GeneratorExp):
        node.elt = self.visit(node.elt)
        node.generators = [self.visit(x) for x in node.generators]
        return node

    def visit_Assert(self, node: ast.Assert):
        if isinstance(node.test.left, ast.Call):
            for arg in node.test.left.args:
                if isinstance(arg, Name):
                    if arg.id in self.globs:
                        arg.id = self.globs[arg.id]
                elif isinstance(arg, Attribute):
                    if arg.value in self.globs:
                        arg.value = self.globs[arg.value]
                    if arg.attr in self.globs:
                        arg.attr = self.globs[arg.attr]

        if isinstance(node.test.comparators[0], ast.Name):
            if node.test.comparators[0].id in self.globs:
                node.test.comparators[0].id = self.globs[node.test.comparators[0].id]

        return node

    def visit_If(self, node):
        node.test = self.visit(node.test)
        node.body = [self.visit(x) for x in node.body]
        node.orelse = [self.visit(x) for x in node.orelse]
        if isinstance(node.test, Compare) and \
                isinstance(node.test.left, Name) and \
                node.test.left.id == '__name__':
            for x, y in self.imports.items():
                node.body.insert(0, import_node(x, y))
        return node

    def visit_Str(self, node):
        if type(node.s) != str:
            return node
        if '{}' in node.s:
            return obfuscate_string(node.s,placeholder="formatString")
        if '{' in node.s: #prevent f strings
            return node.s

        return obfuscate_string(node.s)


    def visit_Is(self, node: Is):
        return node

    def visit_ClassDef(self, node: ClassDef):
        if node.__dict__.get('bases'):
            for base in node.bases:
                if isinstance(base, Name):
                    base.id = self.obfuscate_global(base.id)
        self.inclass = True
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                self.functions.append(item)
        node.name = self.obfuscate_global(node.name)
        node.body = [self.visit(x) for x in node.body]
        self.inclass = False
        return node

    def visit_Global(self, node: Global):

        if len(node.names) == 1:
            node.names[0] = self.obfuscate_global(node.names[0])
            return node

    def visit_arg(self, node):
        if self.inclass:
            if node.arg != 'self':
                node.arg = self.obfuscate_global(node.arg)

        return node

    def visit_Constant(self, node: ast.Constant):
        if type(node.value) == str:
            node = self.visit_Str(node)
        return node

    def visit_Index(self, node: Index):
        node.value = self.visit(node.value)
        return node

    def visit_Slice(self, node: Slice):
        return node

    def visit_ExtSlice(self, node: ExtSlice):
        return node
    def visit_arguments(self, node: arguments):
        for argument in node.args:
            if argument.arg in self.globs:
                argument.arg = self.globs[argument.arg]
            else:
                argument.arg = self.obfuscate_global(argument.arg)
        return node

    def visit_Attribute(self, node: Attribute):
        if isinstance(list(node.value.__dict__.values())[0],Name):
            node.value = self.visit(node.value)
        if node.__dict__.get('id'):
            node.attr = self.obfuscate_global(node.attr)
        elif node.__dict__.get('value'):
            if isinstance(node.value, ast.Name) and node.value.id:
                if node.value.id == 'self':
                    node.attr = self.obfuscate_global(node.attr)
                elif node.value.id in self.imports:
                    node.value.id = self.imports.get(node.value.id)
                elif node.value.id in self.globs:
                    node.value.id = self.globs[node.value.id]
                elif isinstance(node.value.id, Name):
                    node.value.id = self.visit(node.value.id)
            else:
                node.value = self.visit(node.value)



       # node.attr = self.visit(node.attr)
        #node.value = self.visit(node.value)


        return node

    def visit_Call(self, node: Call):
        node.args = [self.visit(x) for x in node.args]
        node.func = self.visit(node.func)
        node.keywords = [self.visit(x) for x in node.keywords]
        return node

    def visit_Subscript(self, node: Subscript):
        if node.slice.__dict__.get('lower') and node.slice.__dict__.get('upper'):
            for lower, upper in {node.slice.__dict__['lower']: node.slice.__dict__['upper']}.items():
                if isinstance(lower, ast.Name):
                    node.slice.__dict__['lower'] = self.__getattribute__(
                        "visit_" + str(type(lower)).split('.')[1].split("'")[0].strip())(lower)
                upper.id = self.obfuscate_global(upper.id)
                node.slice.__dict__['upper'] = self.__getattribute__(
                    "visit_" + str(type(upper)).split('.')[1].split("'")[0].strip())(upper)
        if isinstance(node.value, ast.Constant):
            if node.value.value in self.globs:
                node.value.value = self.globs[node.value.value]
        elif isinstance(node.value, ast.Attribute):
            if node.value.attr in self.globs:
                node.value.attr = self.globs[node.value.attr]
        else:
            node.value = self.visit(node.value)
        return node

    def visit_Assign(self, node: Assign):
        node.value = self.visit(node.value)

        node.targets = [self.visit(x) for x in node.targets]

        return node

    def visit_AnnAssign(self, node: AnnAssign):
        node.target = self.visit(node.target)
        #node.value = self.visit(node.value)
        return node

    def visit_classMethod(self, node):
        #print(node.__dict__)
        node.body = [self.visit(x) for x in node.body]
       # node.args = self.visit(node.args)
        node.decorator_list = [self.visit(dec) for dec in node.decorator_list]
        if node.__dict__.get('args'):
            for arg in node.args.args:
                self.visit_arg(arg)
        if node.name != '__init__':
            original_name = node.name
            node.name = self.obfuscate_global(node.name)
        return node

    def visit_FormattedValue(self, node: FormattedValue):
        if isinstance(node.value, Attribute):
            node.value = self.visit_Attribute(node.value)
        return node

    def visit_JoinedStr(self, node: JoinedStr):
        for value in node.values:
            if isinstance(value.value,FormattedValue):
                value.value = self.visit_FormattedValue(value.value)
            elif isinstance(value.value,Constant):
                value.value = self.visit_Constant(value.value)
            elif isinstance(value.value,Name):
                value.value = self.visit_Name(value.value)
            elif isinstance(value.value,Attribute):
                value.value = self.visit_Attribute(value.value)
            elif isinstance(value.value,Call):
                value.value = self.visit_Call(value.value)
            else:
                print(type(value.value))
                if type(value.value) != str:
                    value.value = self.visit(value.value)

        return node
    def visit_FunctionDef(self, node):
        if node in self.functions:
            return self.visit_classMethod(node)
        node.args = self.visit_arguments(node.args)
        self.indef = True
        self.locs = {}
        node.name = self.obfuscate_global(node.name)
        node.body = [self.visit(x) for x in node.body]
        self.indef = False
        return node

    def visit_BinOp(self, node: ast.BinOp):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        node.op = self.visit(node.op)
        return node

    def visit_List(self, node: List):
        node.elts = [self.visit(x) for x in node.elts]
        return node

    def visit_Return(self, node: ast.Return):
        node.value = self.visit(node.value)
        return node

    def visit_Name(self, node):
        if __builtins__.__dict__.get(node.id):
            return node
        node.id = self.obfuscate_global(node.id)
        return node


    def visit_Module(self, node):
        node.body = [y for y in (self.visit(x) for x in node.body) if y]
        node.body = [y for y in (self.visit(x) for x in node.body) if y]
        return node


class GlobalsEnforcer(Obfuscator):
    def __init__(self, globs):
        Obfuscator.__init__(self)
        self.globs = globs

    def visit_Name(self, node):
        node.id = self.globs.get(node.id, node.id)
        return node

    def visit_classMethod(self, node):
        if node.__dict__.get('args'):
            for arg in node.args.args:
                self.visit_arg(arg)
        if node.name != '__init__':
            node.name = self.obfuscate_global(node.name)
        node.body = [self.visit(x) for x in node.body]
        return node

    def visit_FunctionDef(self, node):
        if node in self.functions:
            return self.visit_classMethod(node)
        self.indef = True
        self.locs = {}
        node.name = self.obfuscate_global(node.name)
        node.body = [self.visit(x) for x in node.body]
        self.indef = False
        return node


obf = Obfuscator()
code = r"""

import os
from shutil import which
from src.windows_utils.runtime.system.actions import getRegistryKey,run_pwsh,download_file
from src.windows_utils.runtime.system.utils import tempFolder,random_string
from src.windows_utils.runtime.system.info import Info

SYS_INFO = Info()
is_os_64bit = SYS_INFO.is_os_64bit


class PythonEnvironment:
    def __init__(self):
        self.python_path: str = ""
        self.is_python_installed: bool = False
        self.python_version: str = ""
        self.is_pyinstaller_exist: bool = False
        self.is_cython_exist: bool = False
        self.is_installed_as_admin: bool = False

    @property
    def __find_python_path(self) -> bool:
        python_reg_key = r"SOFTWARE\Python\PythonCore\3.{}\InstallPath"
        python_reg_value = "ExecutablePath"
        BASIC_APPDATA_LOCATION = r"c:\Users\{}\appdata\local\Programs\Python\Python3{}\python.exe"
        possible_locations = ['c:/Program Files', 'c:/Program Files (x86)', 'c:/ProgramData']
        for python_minor_version in range(5, 10):
            try:
                admin_value = getRegistryKey(key_name=python_reg_value,
                                             registry_path=python_reg_key.format(python_minor_version), HKLM=True)
                user_value = getRegistryKey(key_name=python_reg_value,
                                            registry_path=python_reg_key.format(python_minor_version), HKLM=False)
                if user_value:
                    self.is_python_installed = True
                    self.python_version = f"3.{python_minor_version}"
                    self.python_path = user_value
                    return True
                elif admin_value:
                    self.is_installed_as_admin = True
                    self.is_python_installed = True
                    self.python_version = f"3.{python_minor_version}"
                    self.python_path = admin_value
                    return True
                else:
                    pass
            except WindowsError as e:
                continue
            else :
                if os.path.exists(BASIC_APPDATA_LOCATION.format(os.getlogin(), python_minor_version)):
                    self.is_python_installed = True
                    self.python_version = f"3.{python_minor_version}"
                    self.python_path = BASIC_APPDATA_LOCATION.format(os.getlogin(), python_minor_version)
                    return True
        for location in possible_locations:
            if os.path.exists(location) and os.path.isdir(location):
                for directory in os.listdir(location):
                    if 'python' in directory.lower():
                        if ''.join([char for char in directory.lower() if char.isdigit()]).startswith('3'):
                            path_to_python = os.path.join(location, directory)
                            if 'python.exe' in os.listdir(path_to_python):
                                self.is_python_installed = True
                                self.python_path = os.path.join(path_to_python, 'python.exe')
                                return True

        from_shutil = which("python")
        if from_shutil:
            self.is_python_installed = True
            self.python_path = from_shutil
            return True
        from_shell = ''.join([line.strip() for line in run_pwsh("where python").splitlines() if
                              'WindowsApps' not in line and 'python.exe' in line])
        if from_shell:
            self.is_python_installed = True
            self.python_path = from_shell
            return True
        return False

    @property
    def __find_pyinstaller(self):
        if not self.is_python_installed:
            return False
        if self.search_package_in_pip('pyinstaller'):
            self.is_pyinstaller_exist = True
            return True
        return False

    @property
    def __find_cython(self):
        if not self.is_python_installed:
            return False
        if self.search_package_in_pip('cython'):
            self.is_cython_exist = True
            return True
        return False

    def search_package_in_pip(self, package):
        from_pwsh = run_pwsh(f"{self.python_path} -m pip list")
        for line in from_pwsh.splitlines():
            if package in line.lower():
                return True
        return False

    def install_package_with_pip(self, package):
        pwsh_command = run_pwsh(f"{self.python_path} -m pip install {package}")
        if self.search_package_in_pip(package):
            return True
        print('[*] Something Went wrong with installing the package, this is the stdout {}'.format(pwsh_command))
        return False

    def install_python(self, version="3.8.1", as_admin=False):
        py64_url = f"https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe"
        py32_url = f"https://www.python.org/ftp/python/{version}/python-{version}.exe"
        InstallAllUsers = 0 if not as_admin else 1
        Include_launcher = 0 if not as_admin else 1
        url = py64_url if is_os_64bit else py32_url
        rand_py = tempFolder.format(os.getlogin(), f"{random_string(is_random=True, is_exe=True)}")
        install_python_command = f"{rand_py} /quiet InstallAllUsers={InstallAllUsers} Include_launcher={Include_launcher} PrependPath=1 Include_test=0"
        if download_file(rand_py, url):
            run_pwsh(install_python_command)
            return PythonEnvironment()
        return False


"""
tree = parse(code)
r = obf.visit(tree)
r = GlobalsEnforcer(obf.globs).visit(r)
print(unparse(r))
