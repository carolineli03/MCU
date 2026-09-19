#!/usr/bin/env python3
"""Write a plain-HTML copy of the watch order, the characters and the threads
into index.html, so crawlers (and anyone whose JavaScript fails) see the real
content. The page's own scripts replace each block on load, so what a visitor
sees is unchanged.

Run after editing DATA, CHARS or THREADS:   python3 tools/prerender.py
"""
import re, sys, pathlib, html as H

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = ROOT / 'index.html'
s = SRC.read_text(encoding='utf-8')

def dec(x):   # \uXXXX escapes as written in the data arrays
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), x).replace("\\'", "'")
def esc(x):
    return H.escape(dec(x), quote=False)
def block(name):
    i = s.index(f'const {name} = ['); return s[i:s.index('\n];', i)]

def field(row, key, num=False):
    m = re.search(key + r":(\d+(?:\.\d+)?)" if num else key + r":'((?:[^'\\]|\\.)*)'", row)
    return (m.group(1) if m else '')

titles, chars, threads = [], [], []
for row in re.findall(r"\{t:'i',[^\n]*", block('DATA')):
    titles.append({k: field(row, k) for k in ('id','title','rel','set','kind','tier','why')} | {'m': field(row,'m',True)})
for row in re.findall(r"\{n:'(?:[^'\\]|\\.)*',[^\n]*(?:\n [^\n]*)*", block('CHARS')):
    if not row.lstrip().startswith('{n:'): continue
    chars.append({k: field(row, k) for k in ('n','r','a','g','d','y','b','best')})
tb = block('THREADS')
for head in re.finditer(r"\{id:'([^']+)', name:'((?:[^'\\]|\\.)*)', sub:'((?:[^'\\]|\\.)*)',\n blurb:'((?:[^'\\]|\\.)*)',\n steps:\[", tb):
    seg = tb[head.end(): tb.find('\n{id:', head.end()) if tb.find('\n{id:', head.end()) > 0 else len(tb)]
    steps = [(m.group(1), m.group(2)) for m in re.finditer(r"\{id:'([^']+)',\s*n:'((?:[^'\\]|\\.)*)'", seg)]
    threads.append({'name': head.group(2), 'sub': head.group(3), 'blurb': head.group(4), 'steps': steps})
by_id = {t['id']: t['title'] for t in titles}

def runtime(m):
    m = int(m); return (f'{m//60}h {m%60}m' if m >= 60 else f'{m}m')

chart = []
for i, t in enumerate(titles, 1):
    chart.append(
      f'<div class="node"><div class="card" data-id="{t["id"]}"><span class="row1">'
      f'<span class="num">{i:02d}</span><span class="ttl">{esc(t["title"])}</span></span>'
      f'<span class="why">{esc(t["why"])}</span>'
      f'<span class="dates"><span class="dcell"><span class="dk">Released</span><span class="dv">{esc(t["rel"])}</span></span>'
      f'<span class="dcell"><span class="dk">Set in</span><span class="dv">{esc(t["set"])}</span></span></span>'
      f'<span class="tags"><span class="tag {t["tier"]}">{esc(t["tier"])}</span>'
      f'<span class="tag kind">{esc(t["kind"])}</span><span class="tag time">{runtime(t["m"])}</span></span>'
      f'</div></div>')

roster = []
for c in chars:
    real = f'<span class="cr">{esc(c["r"])}</span>' if c['r'] and dec(c['r']) != '—' else ''
    roster.append(
      f'<article class="ch"><span class="gtag">{esc(c["g"])}</span>'
      f'<div class="chead"><div class="chid"><span class="cn">{esc(c["n"])}</span>{real}</div></div>'
      f'<p class="cb">{esc(c["b"])}</p>'
      f'<span class="cmeta"><span class="dcell"><span class="dk">First appears</span>'
      f'<span class="dv">{esc(c["d"])}<br>{esc(c["y"])}</span></span>'
      f'<span class="dcell"><span class="dk">Played by</span><span class="dv">{esc(c["a"])}</span></span></span>'
      f'<span class="cbest">Best in: {esc(c["best"])}</span></article>')

thl = []
for t in threads:
    steps = ''.join(f'<li><span class="cht">{esc(by_id.get(i, i))}</span><span class="chn">{esc(n)}</span></li>'
                    for i, n in t['steps'])
    thl.append(f'<article class="th"><div class="thhead"><span><span class="thname">{esc(t["name"])}</span>'
               f'<span class="thsub">{esc(t["sub"])}</span></span></div>'
               f'<p class="thblurb">{esc(t["blurb"])}</p><ol class="chain">{steps}</ol></article>')

def put(container_open, container_id, parts):
    """replace whatever sits inside the container with the generated markup"""
    global s
    i = s.index(container_open); j = s.index('>', i) + 1
    close = '</main>' if container_open.startswith('<main') else '</div>'
    k = s.index(close, j)
    s = s[:j] + '\n' + '\n'.join(parts) + '\n' + ' ' * 2 + s[k:]

put('<main class="chart" id="chart"', 'chart', chart)
put('<div id="roster"', 'roster', roster)
put('<div class="thlist" id="thlist"', 'thlist', thl)
SRC.write_text(s, encoding='utf-8')
print(f'pre-rendered {len(chart)} titles, {len(roster)} characters, {len(thl)} threads '
      f'({SRC.stat().st_size//1024} KB)')
