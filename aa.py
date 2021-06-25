class C:
    a = True


class A():
    def __init__(self, ob) -> None:
        self.ob = ob

    def fn1(self) -> None:

        self.ob.a = 'A'


class B():
    def __init__(self, ob) -> None:
        self.ob = ob

    def fn1(self) -> None:

        self.ob.a = 'B'

    def hold(s):
        a = 1


class Y():
    def get(self):
        c = C()
        a = A(c)
        b = B(c)

        print(c.a)
        a.fn1()
        print(c.a)
        b.fn1()
        print(c.a)


y = Y()
y.get()
