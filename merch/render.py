#!/usr/bin/env python3
"""Render a prompt from prompts.md with the Grok CLI, headless, and file the image.

    python3 merch/render.py CONCEPT KIND [N]      e.g. solhvarf art 4 (KIND auto = first prompt)
    PROMPTS=angles.md python3 merch/render.py outrun auto   another prompt file in merch/
    python3 merch/render.py --prompt "text" NAME   a one-off prompt

CONCEPT is the first word of a "## " heading in prompts.md (case and accents
ignored), KIND one of flat, art, body, detail. N images (default 1) are made
one after the other. Keepers land in merch/renders/<concept>/<kind>-<stamp>.jpg
(gitignored). Grok runs with only its image tool, no shell, no web, so the
session can do nothing but draw. Needs ~/.grok/bin/grok signed in.
"""
import glob, os, re, shutil, subprocess, sys, time, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
GROK = os.path.expanduser('~/.grok/bin/grok')
SESS = os.path.expanduser('~/.grok/sessions')
KINDS = {'flat': 'Flat lay', 'art': 'Art only', 'body': 'On body', 'detail': 'Detail'}
RATIO = {'flat': '16:9 landscape', 'art': '3:4 portrait', 'body': '4:5 portrait', 'detail': '1:1 square'}


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).lower()


NAMES = ['SÓLHVARF', 'MIDVINTER', 'ELDSJÄL', 'ASKEGRAV', 'VÅRDKASE', 'GJENREIST', 'NEDBRENT', 'ÅTERFÖDD', 'NOLLSTÄLLD', 'ROTVÄLTA', 'ENDRBORINN']


def band(text):
    """BAND=gjenfodt: Gjenfødt is the band on every concept. Where a prompt
    already carries both words (logo + record), the record becomes Sólhvarf;
    where it carries only Gjenfødt, it stays."""
    if os.environ.get('BAND') != 'gjenfodt':
        return text
    both = 'GJENFØDT' in text and 'SÓLHVARF' in text
    if both:
        for a, b in (('GJENFØDT', '\0'), ('Gjenfødt', '\1'), ('gjenfødt', '\2')):
            text = text.replace(a, b)
    for n in NAMES:
        text = text.replace(n, 'GJENFØDT').replace(n.title(), 'Gjenfødt').replace(n.lower(), 'gjenfødt')
    return text.replace('\0', 'SÓLHVARF').replace('\1', 'Sólhvarf').replace('\2', 'sólhvarf')


def prompt_for(concept, kind):
    md = open(os.path.join(HERE, os.environ.get('PROMPTS', 'prompts.md')), encoding='utf-8').read()
    for m in re.finditer(r'^## (.+?)\n(.*?)(?=^## |\Z)', md, re.S | re.M):
        if fold(m.group(1).split()[0]) == fold(concept):
            pat = r'^### (%s)[^\n]*\n\n```\n(.*?)\n```' % ('|'.join(KINDS.values()) if kind == 'auto' else re.escape(KINDS[kind]))
            sec = re.search(pat, m.group(2), re.S | re.M)
            if sec:
                return sec.group(2).strip(), [k for k, v in KINDS.items() if v == sec.group(1)][0]
            block = re.search(r'```\n(.*?)\n```', m.group(2), re.S) if kind == 'auto' else None
            if not block:
                sys.exit('no %s prompt for %s' % (kind, concept))
            text = block.group(1).strip()
            return text, 'flat' if 'flat lay' in text.lower() else 'art'
    sys.exit('no concept %s in prompts.md' % concept)


def render(text, out, ratio=None):
    before = set(glob.glob(os.path.join(SESS, '*', '*', 'images', '*')))
    ask = 'Generate exactly one image with your image generation tool%s. Prompt: %s\nAfter it is made, reply with the word done.' % (
        ', aspect ratio %s' % ratio if ratio else '', text)
    r = subprocess.run([GROK, '-p', ask, '--tools', 'image_gen', '--disable-web-search', '--no-subagents',
                        '--max-turns', '4', '--no-auto-update', '--output-format', 'plain'],
                       cwd=HERE, capture_output=True, text=True, timeout=300)
    new = [p for p in glob.glob(os.path.join(SESS, '*', '*', 'images', '*')) if p not in before]
    if not new:
        sys.exit('grok made no image\n%s\n%s' % (r.stdout[-800:], r.stderr[-800:]))
    src = max(new, key=os.path.getmtime)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    shutil.copy2(src, out)
    return out


def main(a):
    if a[:1] == ['--prompt']:
        text, name = a[1], a[2]
        out = os.path.join(HERE, 'renders', 'oneoff', '%s-%s.jpg' % (name, time.strftime('%H%M%S')))
        print(render(text, out))
        return
    concept, kind = fold(a[0]), a[1]
    n = int(a[2]) if len(a) > 2 else 1
    text, kind = prompt_for(concept, kind)
    text = band(text)
    if os.environ.get('BAND') == 'gjenfodt':
        concept += '-g'
    for i in range(n):
        out = os.path.join(HERE, 'renders', concept, '%s-%s.jpg' % (kind, time.strftime('%H%M%S')))
        print(render(text, out, RATIO[kind]), flush=True)


if __name__ == '__main__':
    main(sys.argv[1:])
