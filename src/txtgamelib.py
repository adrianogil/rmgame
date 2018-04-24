import re
import sys
import inspect
import readline  # noqa: adds readline semantics to input()
import textwrap
import random
from copy import deepcopy

try:
    from shutil import get_terminal_size
except ImportError:
    try:
        from backports.shutil_get_terminal_size import get_terminal_size
    except ImportError:
        def get_terminal_size(fallback=(80, 24)):
            return fallback


__all__ = (
    'when',
    'start',
    'say',
    'set_context'
)

current_context = 'default'


def set_context(new_context):
    """Set current context."""
    global current_context

    if new_context != 'default':
        new_context = 'default.' + new_context

    current_context = new_context


class InvalidCommand(Exception):
    """A command is not defined correctly."""


class InvalidDirection(Exception):
    """The direction specified was not pre-declared."""


class InvalidContext(Exception):
    """Current context is not defined correctly."""


class Placeholder:
    """Match a word in a command string."""
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name.upper()

def _register(command, func, context='default', kwargs={}):
    """Register func as a handler for the given command."""
    pattern = Command(command, context)
    sig = inspect.signature(func)
    func_argnames = set(sig.parameters)
    when_argnames = set(pattern.argnames) | set(kwargs.keys())
    if func_argnames != when_argnames:
        raise InvalidCommand(
            'The function %s%s has the wrong signature for @when(%r)' % (
                func.__name__, sig, command
            ) + '\n\nThe function arguments should be (%s)' % (
                ', '.join(pattern.argnames + list(kwargs.keys()))
            )
        )

    commands.append((pattern, func, kwargs))


class Command:
    """A pattern for matching a command.

    Commands are defined with a string like 'take ITEM' which corresponds to
    matching 'take' exactly followed by capturing one or more words as the
    group named 'item'.
    """

    def __init__(self, pattern, context='default'):
        self.orig_pattern = pattern
        self.pattern_context = context
        words = pattern.split()
        match = []
        argnames = []
        self.placeholders = 0
        for w in words:
            if not w.isalpha():
                raise InvalidCommand(
                    'Invalid command %r' % pattern +
                    'Commands may consist of letters only.'
                )
            if w.isupper():
                arg = w.lower()
                argnames.append(arg)
                match.append(Placeholder(arg))
                self.placeholders += 1
            elif w.islower():
                match.append(w)
            else:
                raise InvalidCommand(
                    'Invalid command %r' % pattern +
                    '\n\nWords in commands must either be in lowercase or ' +
                    'capitals, not a mix.'
                )
        self.argnames = argnames
        self.prefix = []
        for w in match:
            if isinstance(w, Placeholder):
                break
            self.prefix.append(w)
        self.pattern = match[len(self.prefix):]
        self.fixed = len(self.pattern) - self.placeholders

    def __repr__(self):
        return '%s(%r)' % (
            type(self).__name__,
            self.orig_pattern
        )

    @staticmethod
    def word_combinations(have, placeholders):
        """Iterate over possible assignments of words in have to placeholders.

        `have` is the number of words to allocate and `placeholders` is the
        number of placeholders that those could be distributed to.

        Return an iterable of tuples of integers; the length of each tuple
        will match `placeholders`.

        """
        if have < placeholders:
            return
        if have == placeholders:
            yield (1,) * placeholders
            return
        if placeholders == 1:
            yield (have,)
            return

        # Greedy - start by taking everything
        other_groups = placeholders - 1
        take = have - other_groups
        while take > 0:
            remain = have - take
            if have >= placeholders - 1:
                combos = Command.word_combinations(remain, other_groups)
                for buckets in combos:
                    yield (take,) + tuple(buckets)
            take -= 1  # backtrack

    def is_active(self):
        """Verify if a command is active considering current context."""
        global current_context

        if current_context is None:
            raise InvalidContext('Context is invalid!')

        context = self.pattern_context

        if context is not None:
            if context != 'default':
                context = 'default.' + context
            if context == current_context:
                return True
            uppercontext = context + '.'
            context_len = len(context)+1
            if uppercontext == current_context[:context_len]:
                return True

        return False

    def match(self, input_words):
        """Match a given list of input words against this pattern.

        Return a dict of captured groups if the pattern matches, or None if
        the pattern does not match.

        """
        global current_context

        if not self.is_active():
            return None

        if len(input_words) < len(self.argnames):
            return None

        if input_words[:len(self.prefix)] != self.prefix:
            return None

        input_words = input_words[len(self.prefix):]

        if not input_words and not self.pattern:
            return {}
        if bool(input_words) != bool(self.pattern):
            return None

        have = len(input_words) - self.fixed

        for combo in self.word_combinations(have, self.placeholders):
            matches = {}
            take = iter(combo)
            inp = iter(input_words)
            try:
                for cword in self.pattern:
                    if isinstance(cword, Placeholder):
                        count = next(take)
                        ws = []
                        for _ in range(count):
                            ws.append(next(inp))
                        matches[cword.name] = ws
                    else:
                        word = next(inp)
                        if cword != word:
                            break
                else:
                    return {k: ' '.join(v) for k, v in matches.items()}
            except StopIteration:
                continue
        return None


def prompt():
    """Called to get the prompt text."""
    return '> '


def no_command_matches(command):
    """Called when a command is not understood."""
    print("I don't understand '%s'." % command)


def when(command, context='default', **kwargs):
    """Decorator for command functions."""
    def dec(func):
        _register(command, func, context, kwargs)
        return func
    return dec


def help():
    """Print a list of the commands you can give."""
    print('Here is a list of the commands you can give:')
    cmds = sorted(c.orig_pattern for c, _, _ in commands if c.is_active())
    for c in cmds:
        print(c)

def create_alias(alias, cmd):
    for pattern, func, kwargs in commands:
        args = kwargs.copy()
        matches = pattern.match(cmd)
        if matches is not None:
            args.update(matches)
            aliases.append({'alias' : alias, 'func':func, 'args':args})
            # func(**args)
            break
    else:
        no_command_matches(str(cmd))

def _handle_pattern(ws, cmd):
    for pattern, func, kwargs in commands:
        args = kwargs.copy()
        matches = pattern.match(ws)
        if matches is not None:
            args.update(matches)
            func(**args)
            break
    else:
        for a in aliases:
            alias  = a['alias'] 
            func   = a['func']
            kwargs = a['args']
            args = kwargs.copy()
            if ws[0] == alias:
                func(**args)
                break
        else: 
            no_command_matches(cmd)

def _handle_command(cmd, jump_line=True):
    """Handle a command typed by the user."""
    ws = cmd.lower().split()
    wset = []
    wcmd = ''
    i = 0
    concat_mode = True

    for w in ws:
        if i == 0 and w == 'alias':
            create_alias(ws[1], ws[2:])
            concat_mode = False
            break
        if w == "&&":
            if len(wset) > 0:
                _handle_pattern(wset, wcmd)
            wset = []
            wcmd = ''
        else:
            wset.append(w)
            wcmd = wcmd + w
    if concat_mode and len(wset) > 0:
        _handle_pattern(wset, wcmd)
    # Jump line
    if jump_line:
        print()


def start(help=True):
    """Run the game."""
    if help:
        # Ugly, but we want to keep the arguments consistent
        help = globals()['help']
        qmark = Command('help')
        qmark.prefix = ['?']
        qmark.orig_pattern = '?'
        commands.insert(0, (Command('help'), help, {}))
        commands.insert(0, (qmark, help, {}))
    global turn_number
    turn_number = 0
    while True:
        try:
            cmd = input(prompt()).strip()
        except EOFError:
            print()
            break

        if not cmd:
            continue
        _handle_command(cmd)


def say(msg):
    """Print a message.

    Unlike print(), this deals with de-denting and wrapping of text to fit
    within the width of the terminal.

    Paragraphs separated by blank lines in the input will be wrapped
    separately.

    """
    msg = str(msg)
    msg = re.sub(r'^[ \t]*(.*?)[ \t]*$', r'\1', msg, flags=re.M)
    width = get_terminal_size()[0]
    paragraphs = re.split(r'\n(?:[ \t]*\n)', msg)
    formatted = (textwrap.fill(p.strip(), width=width) for p in paragraphs)
    print('\n\n'.join(formatted))


def quit():
    sys.exit()

commands = [
    (Command('quit'), quit, {}),  # quit command is built-in
]
aliases = [
]
