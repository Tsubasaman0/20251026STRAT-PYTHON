def add_item(item, container=[]):
    container.append(item)
    return container

print(id(add_item.__defaults__), add_item.__defaults__)
add_item(1)
print(id(add_item.__defaults__),add_item.__defaults__)
add_item(2)
print(id(add_item.__defaults__),add_item.__defaults__)


def f(x=[]):
    x = [1]
    return x

print(f.__defaults__)
f()
print(f.__defaults__)

def g(x=[]):
    x += [1]
    return x

print("_________________")
print(g.__defaults__)
g()
print(g.__defaults__)
g()
print(g.__defaults__)