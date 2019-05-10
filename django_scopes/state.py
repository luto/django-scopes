from contextlib import contextmanager
from threading import local

state = local()


def scopes_disabled(f):
    def wrapper(*args, **kwargs):
        with scope(_enabled=False):
            return f(*args, **kwargs)

    return wrapper


@contextmanager
def scope(**scope_kwargs):
    if not hasattr(state, 'scope'):
        state.scope = {}

    previous_scope = getattr(state, 'scope', {})
    new_scope = dict(previous_scope)
    new_scope['_enabled'] = True
    new_scope.update(scope_kwargs)
    state.scope = new_scope
    try:
        yield
    finally:
        state.scope = previous_scope


def get_scope():
    return dict(getattr(state, 'scope', {}))
