import types
import struct
import cPickle as pickle
import iterable
import dictionary
import function_husky
import module
import type_husky


dispatches = [
    (types.NoneType, pickle),
    (types.BooleanType, pickle),
    (types.IntType, pickle),
    (types.LongType, pickle),
    (types.FloatType, pickle),
    (types.StringType, pickle),
    (types.ComplexType, pickle),
    (types.UnicodeType, pickle),
    (types.BuiltinFunctionType, pickle),
    (types.XRangeType, pickle),
    (types.TupleType, iterable),
    (types.ListType, iterable),
    (types.GeneratorType, iterable),
    (types.DictType, dictionary),
    (types.DictionaryType, dictionary),
    (types.FunctionType, function_husky),
    (types.LambdaType, function_husky),
    (types.ModuleType, module),
    (type, type_husky),
    (object, pickle)
]


containers = [function_husky, dictionary, iterable]


def tag(s, t):
    return struct.pack(">c", chr(dispatches.index(t)))+s

def untag(s):
    return ord(struct.unpack(">c", s)[0])

def dumps(d, gen_globals=True):
    for item in dispatches:
        if isinstance(d, item[0]):
            if item[1] in containers:
                return tag(item[1].dumps(d, gen_globals), item)
            else:
                return tag(item[1].dumps(d), item)
    return None

def loads(s, use_globals=False):
    t, m = dispatches[untag(s[0])]
    if m in containers:
        f = m.loads(s[1:], use_globals)
    else:
        f = m.loads(s[1:])
    if not isinstance(f, t):
        f = t(f)
    return f

if __name__ == '__main__':
    v = {1:[1,2,3], "v":None}
    b = dumps(v)
    print repr(b)
    v1 = loads(b)
    print v1