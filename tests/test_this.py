import pytest
from dependencies import Injector, this
from dependencies.exceptions import DependencyError
from helpers import CodeCollector


# Declarative attribute access.


def test_attribute_getter():
    """
    We can describe attribute access in the `Injector` in declarative
    manner.
    """

    class Foo(object):

        def __init__(self, one, two):
            self.one = one
            self.two = two

        def do(self):
            return self.one + self.two

    class Container(Injector):

        class SubContainer(Injector):
            foo = Foo
            one = 1
            two = 2

        foo = this.SubContainer.foo

    foo = Container.foo
    assert isinstance(foo, Foo)
    assert foo.do() == 3


def test_attribute_getter_few_attributes():
    """
    We resolve attribute access until we find all specified
    attributes.
    """

    class Foo(object):

        def __init__(self, one):
            self.one = one

    class Container(Injector):

        class SubContainer(Injector):
            foo = Foo
            one = 1

        foo = this.SubContainer.foo.one

    assert Container.foo == 1


parent_attr = CodeCollector()


@parent_attr.parametrize
def test_attribute_getter_parent_access(code):
    """We can access attribute of outer container."""

    Container = code()
    assert Container.SubContainer.bar == 1


@parent_attr
def ac7814095628():
    """Declarative injector."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):
            bar = (this << 1).foo

    return Container


@parent_attr
def f607abc82079():
    """Let notation."""

    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):
        bar = (this << 1).foo

    Container = OuterContainer.let(SubContainer=SubContainer)

    return Container


few_parent_attr = CodeCollector()


@few_parent_attr.parametrize
def test_attribute_getter_few_parents(code):
    """We can access attribute of outer container in any nesting depth."""

    Container = code()
    assert Container.SubContainer.SubSubContainer.bar == 1


@few_parent_attr
def e477afc961b6():
    """Declarative injector."""

    class Container(Injector):
        foo = 1

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                bar = (this << 2).foo

    return Container


@few_parent_attr
def c4ed4c61e154():
    """Let notation."""

    class OuterContainer(Injector):
        foo = 1

    class SubContainer(Injector):

        class SubSubContainer(Injector):
            bar = (this << 2).foo

    Container = OuterContainer.let(SubContainer=SubContainer)

    return Container


def test_one_subcontainer_multiple_parents():
    """
    Same sub container can be used in many parent containers.  This
    usage should not overlap those containers.
    """

    class SubContainer(Injector):
        bar = (this << 1).foo

    class Container1(Injector):
        foo = 1
        sub = SubContainer

    class Container2(Injector):
        foo = 2
        sub = SubContainer

    assert Container1.sub.bar == 1
    assert Container2.sub.bar == 2


item_access = CodeCollector()


@item_access.parametrize
def test_item_getter(code):
    """
    We can describe item access in the `Injector` in the
    declarative manner.
    """

    result = code()
    assert result == 1


@item_access
def ce642f492941():
    """Get item with string key."""

    class Container(Injector):
        foo = {"one": 1}
        one = this.foo["one"]

    result = Container.one

    return result


@item_access
def ffa208dc1130():
    """Get items as many times as we want."""

    class Container(Injector):
        foo = {"one": {"two": 1}}
        two = this.foo["one"]["two"]

    result = Container.two

    return result


@item_access
def e5c358190fef():
    """Get item from the outer container."""

    class Container(Injector):
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):
            spam = (this << 1).foo["bar"]["baz"]

    result = Container.SubContainer.spam

    return result


@item_access
def ab4cdbf60b2f():
    """Get item from the outer container of any depth level."""

    class Container(Injector):
        foo = {"bar": {"baz": 1}}

        class SubContainer(Injector):

            class SubSubContainer(Injector):
                spam = (this << 2).foo["bar"]["baz"]

    result = Container.SubContainer.SubSubContainer.spam

    return result


@item_access
def be332433b74d():
    """Get items from list."""

    class Container(Injector):
        foo = [1, 2, 3]
        bar = this.foo[0]

    result = Container.bar

    return result


@item_access
def fe150d5ebe93():
    """Get items from dict with digit keys."""

    class Container(Injector):
        foo = {2: 1}
        bar = this.foo[2]

    result = Container.bar

    return result


@item_access
def dc4fedcd09d8():
    """Get items from dict with tuple keys."""

    class Container(Injector):
        foo = {("x", 1): 1}
        bar = this.foo[("x", 1)]

    result = Container.bar

    return result


call = CodeCollector()


@call.parametrize
def test_call(code):
    """
    We can describe call to the `Injector` attribute in the
    declarative manner.
    """

    Container = code()
    assert Container.foo == 1


@call.xfail
def zVaXyVseCxYS():
    """Attribute call."""

    class Container(Injector):

        foo = this.bar()
        bar = lambda: 1

    return Container


@call.xfail
def pKanncCIsUww():
    """Let notation."""

    return Injector.let(foo=this.bar(), bar=lambda: 1)


def test_item_getter_non_printable_key():
    """
    We can describe item access for keys which can't be presented as
    normal strings.
    """

    class Boom(object):

        def __init__(self, salt):
            self.salt = salt

        def __hash__(self):
            return hash(self.salt)

        def __str__(self):
            return "<boom>"

    boom = Boom("hello")

    class Container(Injector):
        foo = {boom: 1}
        bar = this.foo[boom]

    assert Container.bar == 1


def test_attribute_access_after_item_getter():
    """
    Check we can use attribute access notation after item getter
    notation.
    """

    class Foo(object):
        x = 1

    class Bar(object):
        y = {"foo": Foo}

    class Container(Injector):
        bar = Bar
        baz = this.bar.y["foo"].x

    assert Container.baz == 1


# FIXME: Check `test_attribute_access_after_call` and
# `test_item_access_after_call`.


def test_docstrings():
    """Check we can access all API entry points documentation."""

    assert (
        this.__doc__
        == ("Declare attribute and item access during dependency injection.")
    )


direct_proxy = CodeCollector()


@direct_proxy.parametrize
def test_deny_this_without_attribute_access(code):
    """
    `Thisable` instances can't be injected without pointing to any
    other attribute.
    """

    with pytest.raises(DependencyError) as exc_info:
        code()

    message = str(exc_info.value)
    assert message == "You can not use 'this' directly in the 'Injector'"


@direct_proxy
def b648b6f6a712():
    """Declarative injector."""

    class Container(Injector):
        foo = this


@direct_proxy
def c147d398f4be():
    """Declarative injector with parent access."""

    class Container(Injector):
        foo = (this << 1)


@direct_proxy
def a37783b6d1ad():
    """Let notation."""

    Injector.let(foo=this)


@direct_proxy
def bd05271fb831():
    """Let notation with parent access."""

    Injector.let(foo=(this << 1))


def test_this_deny_non_integers():
    """We can't shift `this` with non number argument."""

    with pytest.raises(ValueError) as exc_info:
        this << "boom"

    assert str(exc_info.value) == "Positive integer argument is required"


negative_integers = CodeCollector()


@negative_integers.parametrize
def test_this_deny_negative_integers(code):
    """We can't shift `this` with negative integer."""

    with pytest.raises(ValueError) as exc_info:
        code()

    assert str(exc_info.value) == "Positive integer argument is required"


@negative_integers
def xsJWb2lx6EMs():
    """Minus one."""

    this << -1


@negative_integers
def nvm3ybp98vGm():
    """Zero."""

    this << 0


too_many = CodeCollector()


@too_many.parametrize
def test_require_more_parents_that_injector_actually_has(code):
    """
    If we shift more that container levels available, we should
    provide meaningful message to user.
    """

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert (
        str(exc_info.value)
        == ("You tries to shift this more " "times that Injector has levels")
    )


@too_many
def s6lduD7BJpxW():
    """Declarative Injector."""

    class Container(Injector):

        foo = (this << 1).bar

    Container.foo


@too_many
def bUICVObtDZ4I():
    """Declarative Injected with nested layer."""

    class Container(Injector):

        class SubContainer(Injector):

            foo = (this << 2).bar

    Container.SubContainer.foo


@too_many
def ww6xNI4YrNr6():
    """Let notation."""

    Injector.let(foo=(this << 1).bar).foo


@too_many
def rN3suiVzhqMM():
    """Let notation with nested layer."""

    Injector.let(SubContainer=Injector.let(foo=(this << 2).bar)).SubContainer.foo


attribute_error = CodeCollector()


@attribute_error.parametrize
def test_attribute_error_on_parent_access(code):
    """
    We should raise `AttributeError` if we have correct number of
    parents but specify wrong attribute name.
    """

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in {
        "'Container' can not resolve attribute 'bar'",
        "'Injector' can not resolve attribute 'bar'",
        "'Container' can not resolve attribute 'bar' while building 'foo'",
        "'Injector' can not resolve attribute 'bar' while building 'foo'",
    }


@attribute_error
def t1jn9RI9v42t():
    """Declarative Injector."""

    class Container(Injector):

        foo = this.bar

    Container.foo


@attribute_error
def yOEj1qQfsXHy():
    """Declarative Injected with nested layer."""

    class Container(Injector):

        class SubContainer(Injector):

            foo = (this << 1).bar

    Container.SubContainer.foo


@attribute_error
def vnmkIELBH3MN():
    """Let notation."""

    Injector.let(foo=this.bar).foo


@attribute_error
def pG9M52ZRQr2S():
    """Let notation with nested layer."""

    Injector.let(SubContainer=Injector.let(foo=(this << 1).bar)).SubContainer.foo


circle_links = CodeCollector()


@circle_links.parametrize
def test_circle_links(code):
    """
    We can detect loops in the container hierarchy which will trigger
    recursion during injection process.  We need to raise
    `DependencyError` the same way we do with circle dependencies.
    """

    with pytest.raises(DependencyError) as exc_info:
        code()

    assert str(exc_info.value) in set(
        [
            "'foo' is a circle link in the 'Container' injector",
            "'foo' is a circle link in the 'Injector' injector",
            "'bar' is a circle link in the 'Container' injector",
            "'bar' is a circle link in the 'Injector' injector",
            "'baz' is a circle link in the 'Container' injector",
            "'baz' is a circle link in the 'Injector' injector",
        ]
    )


@circle_links
def kSSnnkw6CNPx():
    """Declarative injector.  Same level."""

    class Container(Injector):

        foo = this.foo

    Container.foo


@circle_links
def ai0hNOPGX2PI():
    """Declarative injector.  Same level.  Long loop."""

    class Container(Injector):

        foo = this.bar
        bar = this.baz
        baz = this.foo

    Container.foo


@circle_links
def n8NHZqiZN43Q():
    """Let notation.  Same level."""

    Injector.let(foo=this.foo).foo


@circle_links
def ySnRrxW6M79T():
    """Let notation.  Same level.  Long loop."""

    Injector.let(foo=this.bar, bar=this.baz, baz=this.foo).foo


@circle_links
def eaK6IxW88SNh():
    """Declarative injector.  One level deep."""

    class Container(Injector):

        foo = this.SubContainer.bar

        class SubContainer(Injector):

            bar = (this << 1).foo

    Container.foo


@circle_links
def nWhKtJb16yg6():
    """Let notation.  One level deep."""

    Injector.let(
        foo=this.SubContainer.bar, SubContainer=Injector.let(bar=(this << 1).foo)
    ).foo


@circle_links
def mF4akoHlg84C():
    """Declarative injector.  Two level deep."""

    class Container(Injector):

        foo = this.SubContainer.SubSubContainer.bar

        class SubContainer(Injector):

            class SubSubContainer(Injector):

                bar = (this << 2).foo

    Container.foo


@circle_links
def bCw8LPUeVK6J():
    """Let notation.  Two level deep."""

    Injector.let(
        foo=this.SubContainer.SubSubContainer.bar,
        SubContainer=Injector.let(SubSubContainer=Injector.let(bar=(this << 2).foo)),
    ).foo


@circle_links
def eHyErh9kExHG():
    """Declarative injector.  Two level deep.  Each level has link."""

    class Container(Injector):

        foo = this.SubContainer.bar

        class SubContainer(Injector):

            bar = this.SubSubContainer.baz

            class SubSubContainer(Injector):

                baz = (this << 2).foo

    Container.foo


@circle_links
def q0KytyVbE2XA():
    """Let notation.  Two level deep.  Each level has link."""

    Injector.let(
        foo=this.SubContainer.bar,
        SubContainer=Injector.let(
            bar=this.SubSubContainer.baz,
            SubSubContainer=Injector.let(baz=(this << 2).foo),
        ),
    ).foo


@circle_links
def vAyZepNGAUjY():
    """Declarative injector.  Cross injector links."""

    class Container(Injector):

        class SubContainer1(Injector):

            bar = (this << 1).SubContainer2.baz

        class SubContainer2(Injector):

            baz = (this << 1).SubContainer1.bar

    Container.SubContainer1.bar


@circle_links
def bLRoCCj9uNOp():
    """Let notation.  Cross injector links."""

    Injector.let(
        SubContainer1=Injector.let(bar=(this << 1).SubContainer2.baz),
        SubContainer2=Injector.let(baz=(this << 1).SubContainer1.bar),
    ).SubContainer1.bar


@circle_links.xfail  # FIXME: Make this work.
def oClqGRmWJAkA():
    """Declarative injector.  Over item access."""

    class Container(Injector):

        class SubContainer(Injector):

            foo = (this << 1).bar["sub"].foo

        bar = {"sub": SubContainer}

    Container.SubContainer.foo


@circle_links.xfail  # FIXME: Make this work.
def t41yMywZuPhA():
    """Let notation.  Over item access."""

    SubContainer = Injector.let(foo=(this << 1).bar["sub"].foo)
    Injector.let(SubContainer=SubContainer, bar={"sub": SubContainer}).SubContainer.foo


def test_false_positive_loop_lookup_protection():
    """
    We should allow proxy to point to objects with the same name if it
    does not create a circle link.
    """

    class Container(Injector):

        foo = this.SubContainer.baz

        class SubContainer(Injector):

            baz = this.foo
            foo = 1

    assert Container.foo == 1
