# ClipRelay

Un watcher local qui automatise l'aller-retour "Claude Code demande une info
que tu viens de copier" (clé API, token, chemin, URL...) : il détecte la
question, surveille le prochain changement de presse-papier, compose le
message de réponse, et — après une fenêtre d'annulation — l'envoie.

**Tout tourne en local. Rien n'est envoyé à un serveur externe.**

## Stack

Python + [`pyperclip`](https://pypi.org/project/pyperclip/), cross-platform
(Windows/Linux/macOS). Choisi plutôt qu'Electron+Node car le besoin réel est
"lire le clipboard + un flux de texte + éventuellement simuler des touches
clavier" — pas d'UI complexe à construire. `pyautogui`/`xdotool`/`pywinauto`
(phase 2, voir Roadmap) s'intègrent nativement en Python, sans le poids d'un
runtime Electron pour un outil qui tourne en arrière-plan sans fenêtre.

## Statut actuel : prototype (phase 1)

Ce prototype **ne tape rien dans un vrai terminal**. Il :

1. Tail un fichier log texte (`session.log` par défaut) qui représente la
   sortie de session de Claude Code.
2. Détecte les lignes qui ressemblent à une question en attente de réponse
   (regex configurables, FR + EN).
3. Une fois une question détectée, arme une fenêtre de surveillance du
   presse-papier (60s par défaut).
4. Au premier changement de presse-papier dans cette fenêtre, compose un
   message en tirant au hasard une phrase parmi ~45 variantes (`cliprelay/messages.py`)
   pour éviter de toujours répéter "Voici la valeur demandée : ...".
5. Si le contenu ressemble à un secret (clé AWS, token GitHub, clé privée,
   JWT...) **ou** si la question mentionne un mot-clé sensible (password,
   api key, token...), il demande une **confirmation manuelle explicite**
   (pas de délai, pas d'envoi automatique).
6. Sinon, il affiche un **compte à rebours annulable (3s par défaut)**
   avant de logger l'envoi.
7. Tout est écrit dans `cliprelay_events.log` (détection, armement,
   capture, décision, envoi/annulation) - rien n'est cassé silencieusement.

"Envoi" = pour l'instant, une ligne `[SENT] message="..."` dans le log
d'événements, pas une vraie frappe clavier. C'est la phase 2 (voir plus bas).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

Sur Linux, `pyperclip` a besoin d'un outil presse-papier système :
```bash
sudo apt install xclip   # ou xsel
```

## Essayer le prototype

Terminal A - simule une session Claude Code qui pose une question :
```bash
python tools/simulate_session.py --log session.log
```

Terminal B - lance le watcher :
```bash
cp config.example.json config.json
python main.py --config config.json
```

Quand la question apparaît dans `session.log`, copie n'importe quel texte
(ex: `sk-test-1234567890abcdef`) dans les 60 secondes : ClipRelay va le
détecter, reconnaître le format "clé API" et te demander une confirmation
manuelle avant de logger l'envoi. Copie un texte anodin ("Paris") à la
place pour voir le chemin non-sensible avec le compte à rebours annulable.

Ou en un coup avec `--auto-copy` (copie automatiquement un faux secret
d'exemple après la question, pour tester le flux complet sans manipulation) :
```bash
python tools/simulate_session.py --log session.log --auto-copy
```

## Éviter les faux positifs

- Le presse-papier n'est surveillé **que** dans la fenêtre qui suit une
  question détectée (`arm_window_seconds`), jamais en continu.
- Un changement de presse-papier hors fenêtre est ignoré.
- La fenêtre expire d'elle-même (`DISARMED` loggé) si rien n'est copié.

## Secrets : liste de contrôle

Deux mécanismes indépendants dans `config.json`, aucun ne demande de stocker
une vraie valeur de secret dans le fichier de config :

- `secret_patterns` : regex qui reconnaissent le **format** d'un secret
  (clé AWS, token GitHub `ghp_...`, clé privée PEM, JWT, bearer token...).
- `sensitive_context_keywords` : mots-clés qui, s'ils apparaissent dans la
  **question** posée par Claude Code, forcent une confirmation manuelle
  (ex: `"password"`, `"api key"`, mais aussi des noms de secrets projet
  comme `"PROD_DB_PASSWORD"` ou `"STRIPE_SECRET_KEY"` - le nom, pas la
  valeur).

`always_require_confirmation: true` force la confirmation manuelle pour
*tout* envoi, sensible ou non, si tu préfères désactiver l'auto-send
complètement.

## Configuration

Voir `config.example.json`. Champs principaux :

| Champ | Rôle |
|---|---|
| `session_log_path` | fichier tail-é comme sortie de session |
| `output_log_path` | log d'événements ClipRelay |
| `arm_window_seconds` | durée pendant laquelle un changement de clipboard est pris en compte après une question |
| `confirm_delay_seconds` | fenêtre d'annulation avant un envoi non-sensible |
| `message_templates` | liste de gabarits (`{clipboard}`) - un est tiré au hasard à chaque envoi, jamais deux fois de suite le même ; ~45 variantes par défaut dans `cliprelay/messages.py`, surchargeable |
| `question_patterns` | regex de détection de question (par défaut dans `cliprelay/patterns.py`) |
| `enable_loose_question_fallback` | active un fallback "toute ligne finissant par ?" (beaucoup de faux positifs, désactivé par défaut) |
| `backend` | `"logfile"` (défaut, log-only) ou `"tmux"` (envoi réel, voir plus bas) |
| `tmux_target` | session/fenêtre/pane tmux à surveiller, requis si `backend="tmux"` |

## Backend tmux (phase 2, partielle) : le vrai terminal

En plus du backend `logfile` (phase 1, log-only), il existe un backend
`tmux` qui lit et écrit dans un **vrai pane tmux** - donc un vrai terminal,
plus une simulation de fichier texte :

- **Lecture réelle** : `tmux capture-pane` sur la cible configurée, diffé
  à chaque poll pour n'extraire que les lignes réellement nouvelles.
- **Envoi réel** : `tmux send-keys -l <message>` puis `Enter` - le texte est
  **vraiment tapé** dans le pane, pas juste loggé.
- Toute la logique de décision (fenêtre d'armement, détection sensible,
  countdown annulable / confirmation manuelle) reste identique - seul
  le "SENT" devient une vraie frappe clavier au lieu d'une ligne de log.

Config :
```json
{
  "backend": "tmux",
  "tmux_target": "nom-de-session"
}
```
`tmux_target` accepte la syntaxe tmux standard (`session`, `session:fenêtre`,
`session:fenêtre.pane`). La session doit déjà exister - ClipRelay ne crée
ni ne tue jamais de session à ta place.

Testé de bout en bout (session tmux réelle + `tmux send-keys`/`capture-pane`,
presse-papier système réel via `xclip`/`Xvfb` en environnement sans écran) :
question détectée dans le pane, secret bloqué en confirmation manuelle sans
rien taper, réponse non-sensible réellement tapée après le countdown.

**Limitation connue** : si le pane change très vite (ex: un `Ctrl-C` suivi
d'un redémarrage immédiat du process, provoquant un vrai scroll du buffer),
la même ligne peut être détectée deux fois d'affilée (double `ARMED`). Sans
conséquence pratique (le pire cas est un ré-armement redondant, pas un
double-envoi), mais à améliorer si ça devient gênant en usage réel.

Ce qui reste pour un vrai usage Windows :
- `pywinauto` ou `pyautogui.write()` ciblé sur la fenêtre active (pas de
  tmux natif sous Windows sans WSL).
- Sur Linux hors tmux (terminal graphique classique) : `xdotool` pour lire/
  écrire dans une fenêtre par son titre.

## Sécurité

- Aucun appel réseau, aucune dépendance qui téléphone à un service externe.
- Le fichier de config ne doit jamais contenir de vraie valeur de secret -
  seulement des motifs/mots-clés.
- Le log d'événements (`cliprelay_events.log`) contient un aperçu tronqué
  (60 caractères) du contenu envoyé pour audit - à traiter comme sensible
  au même titre que le clipboard lui-même si tu manipules de vrais secrets
  en test.
