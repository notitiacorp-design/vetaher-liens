#!/usr/bin/env python3
"""Build a portable, JS-free LittleLink page from reviewed configuration."""
from __future__ import annotations
import html
import json
import pathlib
import re
import shutil
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent
PUBLIC = ROOT / 'public'
ALLOWED_HOSTS = {'www.vetaher.fr', 'fondation.vetaher.fr', 'v.vetaher.fr', 'www.instagram.com', 'www.facebook.com', 'www.youtube.com', 'youtu.be', 'youtube.com'}

ARROW = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none"><path d="M5 12h14m-6-6 6 6-6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def esc(value: str) -> str:
    return html.escape(value, quote=True)

def validate(data):
    items = data['links'] + data['socials'] + [data['website']]
    ids = [x['id'] for x in items]
    assert len(ids) == len(set(ids)), 'Duplicate link identifiers'
    assert len([x for x in data['links'] if x.get('primary')]) == 1
    for item in items:
        u = urlparse(item['href'])
        assert u.scheme == 'https' and u.hostname in ALLOWED_HOSTS, item
        assert not u.username and not u.password and not u.fragment, item
        assert item['label'].strip(), item
        assert not any(c in item['label'] for c in ['—', '–']), item
    assert not any('fondation' in x['label'].lower() for x in items)
    return items

def build():
    data = json.loads((ROOT / 'links.json').read_text())
    items = validate(data)
    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / 'css').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'vetaher.css', PUBLIC / 'css/vetaher.css')
    entries = []
    for item in data['links']:
        kind = ' primary' if item.get('primary') else ''
        hint = f'<small>{esc(item["hint"])}</small>' if item.get('hint') else ''
        label = f'<span class="link-copy"><span>{esc(item["label"])}</span>{hint}</span>'
        entries.append(f'<li><a class="button link{kind}" data-link-id="{esc(item["id"])}" href="{esc(item["href"])}">{label}{ARROW}</a></li>')
    socials = ''.join(f'<a class="social" data-link-id="{esc(x["id"])}" href="{esc(x["href"])}">{esc(x["label"])}</a>' for x in data['socials'])
    w = data['website']
    document = f'''<!doctype html>
<html lang="fr" class="theme-light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<meta name="referrer" content="no-referrer">
<meta name="theme-color" content="#173661">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'self'; img-src 'self'; font-src 'self'; script-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
<title>Vetaher | Actions et services</title>
<meta name="description" content="Les liens de l’association Vetaher : actions, services, réseaux et soutien.">
<link rel="icon" type="image/png" href="assets/favicon.png">
<link rel="stylesheet" href="css/reset.css">
<link rel="stylesheet" href="css/littlelink.css">
<link rel="stylesheet" href="css/vetaher.css">
</head>
<body>
<a class="skip" href="#liens">Accéder aux liens</a>
<div class="preview-notice" role="note">Aperçu à valider · les profils existants sont inchangés</div>
<main class="container" id="contenu">
<header class="identity">
<img class="avatar avatar--none" src="assets/logo.png" alt="Logo de l’association Vetaher" width="112" height="112" fetchpriority="high">
<p class="eyebrow">ASSOCIATION</p>
<h1>Vetaher</h1>
<p class="intro">Actions et services</p>
</header>
<nav id="liens" aria-label="Actions et services de Vetaher">
<ul class="links">{''.join(entries)}</ul>
</nav>
<nav class="socials" aria-label="Réseaux sociaux de Vetaher">{socials}</nav>
<footer>
<a class="website" data-link-id="{esc(w['id'])}" href="{esc(w['href'])}">{esc(w['label'])}</a>
<p>Page sans cookies ni suivi publicitaire.</p>
<a class="credits" href="credits.html">À propos de cette page</a>
</footer>
</main>
</body>
</html>'''
    assert 'don.vetaher.com' not in document and 'allodons' not in document
    assert 'linktr.ee' not in document
    (PUBLIC / 'index.html').write_text(document, encoding='utf-8')
    (PUBLIC / 'robots.txt').write_text('User-agent: *\nDisallow: /\n')
    (PUBLIC / '.nojekyll').touch()
    provenance = json.loads((ROOT / 'PROVENANCE.json').read_text())
    credit = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>À propos | Vetaher</title><link rel="stylesheet" href="css/reset.css"><link rel="stylesheet" href="css/littlelink.css"><link rel="stylesheet" href="css/vetaher.css"></head><body><main class="container legal"><a href="index.html">Retour aux liens</a><h1>À propos</h1><p>Cette version est un aperçu préparé pour validation. Elle ne remplace pas encore le lien des profils existants.</p><h2>Vie privée</h2><p>Cette page ne comporte ni formulaire, ni cookie, ni stockage local, ni outil de mesure d’audience. Les sites ouverts depuis les liens appliquent leurs propres règles. L’hébergeur peut conserver ses journaux techniques habituels.</p><h2>Logiciel libre</h2><p>Cette page utilise le CSS de LittleLink, créé par Seth Cottle et distribué sous licence MIT. Les adaptations de la page sont également sous licence MIT ; le logo appartient à l’association Vetaher.</p><p>Version source : <code>{esc(provenance['upstream_commit'])}</code>.</p><p><a href="LICENSE.txt">Lire la licence MIT</a></p><h2>Liens et paiements</h2><p>La page fournit uniquement des liens vers les services existants. Elle ne collecte aucun paiement et ne modifie ni coordonnées bancaires ni compte bénéficiaire.</p></main></body></html>'''
    (PUBLIC / 'credits.html').write_text(credit, encoding='utf-8')
    print(json.dumps({'build': 'ok', 'outbound_buttons': len(data['links']), 'social_links': len(data['socials']), 'outbound_links_total': len(items), 'files': sorted(str(x.relative_to(PUBLIC)) for x in PUBLIC.rglob('*') if x.is_file())}, ensure_ascii=False))

if __name__ == '__main__':
    build()
