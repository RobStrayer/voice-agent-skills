"""Speakable read-back, ambiguity flags and a transcript-support check for spoken data.

Usage:
    python readback.py phone "+1 (415) 555-0123"
    python readback.py phone "+44 0123 456789" --cc 44   # a made-up number; --cc keeps the country code in its own group
    python readback.py code "B7D4-P0T9"
    python readback.py email "jon.smith42@example.com"
    python readback.py heard "four one five, double five five, oh one two three"
    python readback.py support "+14155550123" "four one five five five five oh one two three" --assume 1
    python readback.py support "+14155550123" "four one five five five five oh one two three" --assume 1 --exact
    python readback.py checksym 16J            # append a Crockford check symbol
    python readback.py checksym 16JD --verify  # check a code that ends in one
    python readback.py --selftest

phone, code and email also take --json. Standard library only.

These are speaking and sanity helpers, not validators. Use libphonenumber or a lookup
service for phone numbers and your own system for codes, names and addresses. The
protocols and the reasons for each flag are in ../references/.
"""
import argparse
import difflib
import json
import re
import sys

SAY = dict(zip('0123456789', 'zero one two three four five six seven eight nine'.split()))
DIGIT_WORDS = {w: d for d, w in SAY.items()}  # English digit words only; add the words of your other languages
# 'oh' and 'o' are also words and letters, so treat the result as a candidate and read it back.
DIGIT_WORDS.update({'oh': '0', 'o': '0', 'nought': '0', 'naught': '0'})
MULT = {'double': 2, 'triple': 3}
# Number words this script does not turn into digits. If one appears, ask the caller for
# the digits one at a time instead of guessing ("fifty five" could be 55 or 5 5).
BIG = set('ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen '
          'twenty thirty forty fifty sixty seventy eighty ninety hundred thousand'.split())
# ICAO and NATO code words. If your text-to-speech stumbles on Alfa or Juliett, use Alpha
# and Juliet. The X word appears as X-ray and as Xray: use the spelling your voice says best.
NATO = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ', (
    'Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike November '
    'Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu').split()))
# Symbols that get swapped. Letters: Cole and Fanty 1990 (E-set, M/N, J/K). Digit and
# letter look-alikes: Crockford's Base32 page (I and L read as 1, O as 0).
CONFUSABLE = (('E-set letters', 'BCDEGPTVZ'), ('M/N', 'MN'), ('J/K', 'JK'),
              ('0/O', '0O'), ('1/I/L', '1IL'))
LOOKALIKE = {c for _, m in CONFUSABLE for c in m if c.isalpha()}  # letters to say with the alphabet
CROCKFORD = '0123456789ABCDEFGHJKMNPQRSTVWXYZ'
CHECK = CROCKFORD + '*~$=U'  # values 32 to 36 exist only as check symbols
# Five providers and five top-level domains said as words. Add the domains your callers use.
PROVIDERS = ('gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com')
TLD_WORDS = ('com', 'org', 'net', 'edu', 'gov')
PUNCT = {'.': 'dot', '_': 'underscore', '-': 'dash', '+': 'plus', '@': 'at', "'": 'apostrophe'}


def digits(s):
    """The digits of a phone-style value. Anything but digits, spaces and + - ( ) . is an
    error, and so is a + after the first character: ask again instead of dropping it."""
    s = s.strip()
    if re.search(r'[^0-9\s+().-]', s) or '+' in s[1:]:
        raise ValueError('digits, spaces and - ( ) . only, with + first: ask again')
    return re.sub(r'[^0-9]', '', s)


def heard_digits(text):
    """Digits a caller said, plus the words that may hide digits: number words, a non-ASCII
    digit, and a "double" or "triple" that is not followed by one digit.
    Any other word between two digits puts a space in the result, so a value cannot match
    across it. That fails safe: 'for', 'to', 'um' or a dropped word means ask again."""
    out, pend, odd, gap = [], '', [], False
    for tok in re.findall(r'[^\W_]+', text.lower()):
        if tok in MULT:
            if pend:  # "double double": the first one has no digit
                odd.append(pend)
            pend = tok
            continue
        d = DIGIT_WORDS.get(tok) or (tok if tok.isascii() and tok.isdigit() else None)
        if d is None or (pend and len(d) > 1):
            if d is not None:  # "double 15" has no single reading: report it, add nothing
                odd.append('%s %s' % (pend, tok))
            else:
                if pend:  # "double" then a word
                    odd.append(pend)
                if tok in BIG or any(c.isdigit() for c in tok):  # number word or non-ASCII digit
                    odd.append(tok)
            gap, pend = True, ''
            continue
        if gap and out:
            out.append(' ')
        out.append(d * MULT.get(pend, 1))
        gap, pend = False, ''
    if pend:  # a trailing "double" or "triple" hides a digit
        odd.append(pend)
    return ''.join(out), odd


def supported(value, transcript, assume='', exact=False):
    """True if the digits of value appear, in order and unbroken, in what the caller said.
    False when the answer holds a number word ("fifteen") or a dangling "double", because
    either may hide digits: ask for the digits one at a time. exact=True: the answer must
    hold those digits and nothing else, which catches a value cut short. assume is a prefix
    your code added (a country code). Catches digits the model invented; does not prove the
    digits belong to the right question."""
    want, pre = digits(value), digits(assume)
    heard, odd = heard_digits(transcript)
    opts = [want[len(pre):], want] if pre and want.startswith(pre) else [want]
    return not odd and any(o and (heard == o if exact else o in heard) for o in opts)


def _split(n):
    # Threes from the left, and a last group of four instead of three plus one.
    # A speaking habit, not a national format. Use libphonenumber for the real format.
    sizes = [3] * (n // 3)
    if n % 3 == 1 and sizes:
        sizes[-1] = 4
    elif n % 3:
        sizes.append(n % 3)
    return sizes


def phone(value, cc=''):
    """cc is the country calling code, 1 to 3 digits such as '44'. Without it only +1 is split out."""
    if cc and not re.fullmatch(r'[0-9]{1,3}', cc):
        raise ValueError('cc is 1 to 3 digits')
    value = value.strip()
    plus = value.startswith('+')
    d = digits(value)
    if not d:
        raise ValueError('no digits')
    flags = []
    if not plus:
        flags.append('no leading +: the country is unknown. Ask, or say the country you assume and confirm it.')
    elif d.startswith('0'):
        flags.append('a country code never starts with 0 (E.164).')
    if len(d) > 15:
        flags.append('more than 15 digits: too long for E.164.')
    elif len(d) < 7:
        flags.append('fewer than 7 digits: incomplete.')
    if plus and d.startswith('1'):  # +1 is the US, Canada and other NANP countries
        sizes = [1, 3, 3, 4]
        if len(d) != 11:
            flags.append('+1 numbers have 10 digits after the 1; this has %d.' % (len(d) - 1))
    elif plus and cc and d.startswith(cc):
        sizes = [len(cc)] + _split(len(d) - len(cc))
    elif not plus and len(d) == 10:
        sizes = [3, 3, 4]
    else:
        sizes = _split(len(d))
        if plus:
            flags.append('country code length unknown, so it is grouped with the number. Pass --cc, or take the grouping from libphonenumber.')
    if re.search(r'([0-9])\1\1', d):
        flags.append('a digit repeats 3 or more times: say every digit, never "triple", and confirm that group again.')
    groups, i = [], 0
    for s in sizes:
        groups.append(d[i:i + s])
        i += s
    groups = [g for g in groups + [d[i:]] if g]  # the last group keeps any digits left over
    say = ', '.join(' '.join(SAY[c] for c in g) for g in groups)
    return {'value': ('+' if plus else '') + d, 'say': ('plus ' if plus else '') + say, 'flags': flags}


def _ambiguity(chars):
    chars = set(chars.upper())
    mixed = any(c.isalpha() for c in chars) and any(c.isdigit() for c in chars)
    # A digit look-alike (0, 1) only confuses when letters are in the code too.
    return ['%s %s: easy to mix up; use the spelling alphabet.' % (name, ' '.join(sorted(chars & set(m))))
            for name, m in CONFUSABLE if chars & set(m) and (mixed or any(c.isalpha() for c in chars & set(m)))]


def code(value):
    v = re.sub(r'[\s-]', '', value)
    if not (v and v.isascii() and v.isalnum()):  # before upper(), which turns the German sharp s into SS
        raise ValueError('a code is letters and digits only')
    v = v.upper()
    # Groups of 4 are a habit, not a measured optimum. Tune to your code length.
    groups = [v[i:i + 4] for i in range(0, len(v), 4)]
    say = ', '.join(' '.join(SAY.get(c, c) for c in g) for g in groups)
    # spelled: slower. One symbol at a time, the alphabet only for letters that get mixed up,
    # commas inside a group and a period between groups.
    spelled = '. '.join(', '.join(SAY[c] if c.isdigit() else '%s as in %s' % (c, NATO[c]) if c in LOOKALIKE else c
                                  for c in g) for g in groups)
    return {'value': v, 'say': say, 'spelled': spelled, 'flags': _ambiguity(v)}


def email(value, providers=PROVIDERS):
    """ASCII addresses only. Internationalized mailboxes are not handled here."""
    # Lowercased for speaking: spoken letters carry no case. RFC 5321 section 2.4 treats a
    # local part as case-sensitive but discourages relying on that.
    v = value.strip().lower()
    local, _, domain = v.partition('@')
    if v.count('@') != 1 or not local or not domain:
        raise ValueError('need exactly one @ with text on both sides')
    if not re.fullmatch(r"[a-z0-9._+'-]+", local) or '..' in local or local[0] == '.' or local[-1] == '.':
        raise ValueError("before the @: letters, digits and . _ + - ' only, no dot at the ends or doubled. Ask the caller to spell it")
    labels = domain.split('.')
    if len(labels) < 2 or not all(re.fullmatch(r'[a-z0-9]([a-z0-9-]*[a-z0-9])?', x) for x in labels):
        raise ValueError('after the @: at least one dot, and letters, digits and hyphens between dots')
    flags = []
    if re.search(r'[0-9]', local):
        flags.append('digits in the address: say each digit and confirm them.')
    if re.search(r"[._+'-]", local):
        flags.append("punctuation (. _ - + ') is said aloud and often dropped by speech-to-text: confirm it.")
    if re.search(r'([a-z])\1', local):
        flags.append('doubled letter: say both letters ("double l" is read differently in different accents).')
    # ponytail: a string-similarity guess against a short list. Use a typo-domain list if you need more.
    # Only domains with the same number of parts are compared, so yahoo.co.uk is not "yahoo.com".
    same = [p for p in providers if p.count('.') == domain.count('.')]
    near = difflib.get_close_matches(domain, same, n=1, cutoff=0.8)
    if near and domain not in providers:
        flags.append('the domain looks like %s: confirm the spelling.' % near[0])

    def spell(s):
        return [SAY.get(c) or PUNCT.get(c, c) for c in s]
    words = spell(local) + ['at']
    for i, label in enumerate(labels):
        if i:
            words.append('dot')
        words += [label] if domain in providers or label in TLD_WORDS else spell(label)
    return {'value': v, 'say': ', '.join(words), 'flags': flags}


def _crockford_value(body):
    body = re.sub(r'[\s-]', '', body).upper().replace('I', '1').replace('L', '1').replace('O', '0')
    if not body:
        raise ValueError('empty code')
    n = 0
    for c in body:
        if c not in CROCKFORD:
            raise ValueError('not a Crockford symbol: %s' % c)
        n = n * 32 + CROCKFORD.index(c)
    return n


def checksym(body):
    """Crockford check symbol: the code read as a base 32 number, modulo 37."""
    return CHECK[_crockford_value(body) % 37]


def verify(full):
    full = re.sub(r'[\s-]', '', full).upper()
    sym = full[-1:].replace('I', '1').replace('L', '1').replace('O', '0')
    return len(full) > 1 and checksym(full[:-1]) == sym


def raises(fn, *args, **kw):
    try:
        fn(*args, **kw)
    except ValueError:
        return True
    return False


def selftest():
    arabic3 = chr(0x663)  # a non-ASCII digit, built here so the file stays ASCII
    # heard_digits: words, numerals, "oh", double and triple, and what it refuses to guess
    assert heard_digits('four one five, five five five, oh one two three') == ('4155550123', [])
    assert heard_digits('call 415 555 0123 please') == ('4155550123', [])
    assert heard_digits('four one five double five five oh one two three') == ('4155550123', [])
    assert heard_digits('triple seven') == ('777', [])
    assert heard_digits('double 5 five') == ('555', [])                   # a numeral after double
    assert heard_digits('four one five o one') == ('41501', [])
    assert heard_digits('four one five fifty five') == ('415 5', ['fifty'])
    assert heard_digits('four one five um five five') == ('415 55', [])    # another word breaks the run
    assert heard_digits('four one five for five five') == ('415 55', [])   # so does a homophone such as "for"
    assert heard_digits('four %s five' % arabic3) == ('4 5', [arabic3])     # a non-ASCII digit is reported
    assert heard_digits('four double 15 five') == ('4 5', ['double 15'])
    assert heard_digits('four one double') == ('41', ['double'])            # a dangling double hides a digit
    assert heard_digits('four one five double um') == ('415', ['double'])   # also before a word
    assert heard_digits('double double five') == ('55', ['double'])
    # supported: a changed digit or a missing assumption is caught
    said = 'four one five five five five oh one two three'
    assert supported('+14155550123', said, assume='1')
    assert not supported('+14155550124', said, assume='1')
    assert not supported('+14155550123', said)
    assert not supported('', said)
    # fixtures PH-3 (a dropped digit) and PH-4 (number words) in references/test-fixtures.md
    assert not supported('+14155550123', 'four one five five five oh one two three', assume='1')
    assert heard_digits('four fifteen five fifty five oh one twenty three') == (
        '4 5 501 3', ['fifteen', 'fifty', 'twenty'])
    # a number word anywhere in the answer, or a dangling double, fails the check, even at the ends
    for said_odd in ('twenty ' + said, said + ' hundred', said + ' thousand', said + ' ten'):
        for exact in (False, True):
            assert not supported('+14155550123', said_odd, assume='1', exact=exact), said_odd
    assert not supported('1', 'twenty-one', exact=True)
    assert not supported('415', 'four one five ten', exact=True)
    assert not supported('415', 'four one five double um', exact=True)
    assert not supported('+1415555012', 'four one five five five five zero one two double', assume='1', exact=True)
    # a hidden word must not let a value span the gap, and exact mode catches a value cut short
    assert not supported('415555', 'four one five um five five')
    assert not supported('415555', 'four one five for five five')
    assert supported('+1415555012', said, assume='1')                       # a substring of the answer
    assert not supported('+1415555012', said, assume='1', exact=True)       # but not the whole answer
    assert supported('+14155550123', said, assume='1', exact=True)
    assert supported('+14155550123', 'one ' + said, assume='1', exact=True)  # caller said the 1 too
    assert raises(supported, 'abc4155550123xyz', said)                      # letters in a value are an error
    # phone: NANP grouping, generic grouping, no plus, and the flags
    p = phone('+1 (415) 555-0123')
    assert p['value'] == '+14155550123'
    assert p['say'] == 'plus one, four one five, five five five, zero one two three'
    assert len(p['flags']) == 1 and 'repeats' in p['flags'][0]
    assert phone('+14155550100')['say'] == 'plus one, four one five, five five five, zero one zero zero'  # fixture PH-5: no "triple"
    # made up: a real +44 number has no 0 after the country code
    u = phone('+44 0123 456789', cc='44')
    assert u['say'] == 'plus four four, zero one two, three four five, six seven eight nine' and u['flags'] == []
    assert any('country code length unknown' in f for f in phone('+440123456789')['flags'])
    assert phone('4155550123')['say'] == 'four one five, five five five, zero one two three'
    assert any('no leading +' in f for f in phone('4155550123')['flags'])
    assert any('10 digits' in f for f in phone('+1415555012')['flags'])
    assert any('never starts with 0' in f for f in phone('+0123456789')['flags'])
    assert any('more than 15' in f for f in phone('+1234567890123456')['flags'])
    assert any('fewer than 7' in f for f in phone('0123')['flags'])
    # bad input is an error, not a silent drop
    for bad in ('', '+', '+1 ' + arabic3 * 3, '+1415555O123', '+14155550123 ext 12', '1+4155550123'):
        assert raises(phone, bad), bad
    assert raises(phone, '+4155550123', cc='4444') and raises(phone, '+4155550123', cc='4a')
    # the spoken form never drops or adds a digit, whatever the length
    for n in range(7, 17):
        for v in ('+' + '1234567890123456'[:n], '2345678901234567'[:n]):
            assert heard_digits(phone(v)['say'])[0] == re.sub(r'\D', '', v), v
    # code: groups, spelling alphabet, flags, bad input
    assert code('ABCDEFGHJ')['say'] == 'A B C D, E F G H, J'
    c = code('b7d4-p0t9')
    assert c['value'] == 'B7D4P0T9' and c['say'] == 'B seven D four, P zero T nine'
    assert c['spelled'] == 'B as in Bravo, seven, D as in Delta, four. P as in Papa, zero, T as in Tango, nine'
    assert code('a2x9')['spelled'] == 'A, two, X, nine'  # A and X are not in the look-alike sets
    assert [f.split(':')[0] for f in c['flags']] == ['E-set letters B D P T', '0/O 0']
    assert [f.split(':')[0] for f in code('v7')['flags']] == ['E-set letters V']  # fixture CD-2 includes V
    assert code('1204')['flags'] == []  # digits alone are not look-alikes
    assert [f.split(':')[0] for f in code('12O4')['flags']] == ['0/O O', '1/I/L 1']
    assert raises(code, 'AB#1') and raises(code, '') and raises(code, chr(0xdf))
    # email: spoken form, flags, look-alike domain, bad input. Addresses use the reserved example domains.
    ex = ('example.com',)
    e = email('Jon.Smith42@example.com', providers=ex)
    assert e['say'] == 'j, o, n, dot, s, m, i, t, h, four, two, at, example, dot, com'
    assert len(e['flags']) == 2
    assert email('bob@example.com')['say'] == 'b, o, b, at, e, x, a, m, p, l, e, dot, com'
    assert email('bob@example.com')['flags'] == []
    assert any('example.com' in f for f in email('ann@exmaple.com', providers=ex)['flags'])
    assert email('bob@mail.example.com', providers=ex)['flags'] == []       # different shape, no look-alike flag
    assert any('doubled' in f for f in email('anna@example.net')['flags'])
    assert email('anna@example.net')['say'].startswith('a, n, n, a, at')  # fixture EM-7: both letters said
    assert email('jon+tag@example.com')['say'].startswith('j, o, n, plus, t, a, g, at')  # fixture EM-8: + is accepted
    o = email("o'neil@example.org")
    assert 'o, apostrophe, n' in o['say'] and any('punctuation' in f for f in o['flags'])
    e6 = email('john.smith_42-work@example.com')  # fixture EM-6: punctuation said as words
    assert e6['say'].startswith('j, o, h, n, dot, s, m, i, t, h, underscore, four, two, dash, w, o, r, k, at')
    assert any('punctuation' in f for f in e6['flags'])
    for bad in ('not-an-address', 'a@b@example.com', 'a@b', 'a@b..com', 'a@.com', 'a b@example.com',
                '.a@example.com', 'a..b@example.com', 'a#b@example.com', 'a@b.c#m', 'a@-b.com'):
        assert raises(email, bad), bad
    # Crockford check symbol: 16J is 1*1024 + 6*32 + 18 = 1234; 1234 mod 37 = 13, which is D
    assert checksym('16J') == 'D' and verify('16JD')
    assert not verify('1J6D') and not verify('17JD')  # transposed and wrong symbol
    assert verify('l6jd')                              # l reads as 1, case ignored
    assert checksym('16J ') == 'D' and verify(' 16-JD ')  # spaces and hyphens are ignored, as in code()
    assert checksym('IL0O') == checksym('1100') == 'B'
    assert checksym('10') == '*' and checksym('14') == 'U'  # values 32 and 36
    assert raises(checksym, '') and raises(checksym, 'U')
    print('PASS: digit parsing, support check, phone, code, email and check-symbol cases.')


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--selftest', action='store_true')
    sub = ap.add_subparsers(dest='cmd')
    for name in ('phone', 'code', 'email'):
        s = sub.add_parser(name)
        s.add_argument('value')
        s.add_argument('--json', action='store_true')
        if name == 'phone':
            s.add_argument('--cc', default='', help='country calling code, such as 44')
    sub.add_parser('heard').add_argument('text')
    s = sub.add_parser('support')
    s.add_argument('value')
    s.add_argument('text')
    s.add_argument('--assume', default='', help='digits your code added, such as a country code')
    s.add_argument('--exact', action='store_true', help='the answer must hold only these digits')
    s = sub.add_parser('checksym')
    s.add_argument('code')
    s.add_argument('--verify', action='store_true')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    try:
        if a.cmd in ('phone', 'code', 'email'):
            r = phone(a.value, a.cc) if a.cmd == 'phone' else {'code': code, 'email': email}[a.cmd](a.value)
            if a.json:
                print(json.dumps(r, indent=2))
            else:
                for key in ('value', 'say', 'spelled'):
                    if key in r:
                        print('%-9s%s' % (key + ':', r[key]))
                print('flags:   ' + ('none' if not r['flags'] else '\n         '.join(r['flags'])))
        elif a.cmd == 'heard':
            found, odd = heard_digits(a.text)
            print('digits: ' + found)
            if ' ' in found:
                print('a space marks a word between digits: a value cannot match across it.')
            if odd:
                print('may hide digits: %s. Ask for the digits one at a time.' % ', '.join(odd))
        elif a.cmd == 'support':
            ok = supported(a.value, a.text, a.assume, a.exact)
            odd = heard_digits(a.text)[1]
            print('supported' if ok else "NOT supported: the value's digits are not %s what the caller said" % ('exactly' if a.exact else 'in'))
            if odd:
                print('may hide digits: %s. Ask for the digits one at a time.' % ', '.join(odd))
            return 0 if ok else 1
        elif a.cmd == 'checksym':
            if a.verify:
                ok = verify(a.code)
                print('check symbol ok' if ok else 'check symbol does not match')
                return 0 if ok else 1
            sym = checksym(a.code)
            print(a.code + sym)
            if sym in '*~$=U':
                print('note: %s is one of the five check symbols outside the 32 ordinary ones. * ~ $ = cannot be said as a letter: issue another code, or teach a spoken name.' % sym)
        else:
            ap.print_help()
    except ValueError as err:
        sys.exit('error: %s' % err)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
