"""Phrasings used to compose the reply sent back with the clipboard content.

A large, multilingual pool so ClipRelay doesn't always answer
"Voici la valeur demandée : ...". One is picked at random each time (never
the same one twice in a row when the pool has more than one entry). Every
entry must contain the `{clipboard}` placeholder.
"""

_FR = [
    "Voici la valeur demandée : {clipboard}",
    "Voici : {clipboard}",
    "Tiens, voilà : {clipboard}",
    "Voilà ce que tu demandes : {clipboard}",
    "C'est ça : {clipboard}",
    "La voici : {clipboard}",
    "Le voici : {clipboard}",
    "Voici la valeur : {clipboard}",
    "Voici ce qu'il te faut : {clipboard}",
    "Voici la réponse : {clipboard}",
    "Voici l'info demandée : {clipboard}",
    "Ça y est, je l'ai copié : {clipboard}",
    "Je viens de le copier : {clipboard}",
    "Tiens : {clipboard}",
    "Voilà : {clipboard}",
    "C'est celui-ci : {clipboard}",
    "C'est celle-ci : {clipboard}",
    "Voici ce que j'ai copié : {clipboard}",
    "Voici ce que je viens de copier : {clipboard}",
    "Voici la donnée demandée : {clipboard}",
    "Voici la valeur à utiliser : {clipboard}",
    "Voici ce qu'il fallait : {clipboard}",
    "Voici quoi utiliser : {clipboard}",
    "Voici l'élément demandé : {clipboard}",
    "Utilise ceci : {clipboard}",
    "Prends ceci : {clipboard}",
    "Voici l'information : {clipboard}",
    "Je te donne ça : {clipboard}",
    "Réponse : {clipboard}",
    "Voici, comme demandé : {clipboard}",
    "Comme demandé, voici : {clipboard}",
    "Voici ce que tu as demandé : {clipboard}",
    "Voici ce que je viens de coller : {clipboard}",
    "C'est bon, voici : {clipboard}",
    "Ok, voici : {clipboard}",
    "Voici la clé/valeur : {clipboard}",
    "Voici : {clipboard}. Dis-moi si ce n'est pas la bonne valeur.",
    "Voici ce qui vient d'être copié : {clipboard}",
    "Voilà, c'est ça : {clipboard}",
    "Voici, fraîchement copié : {clipboard}",
]

_EN = [
    "Here you go: {clipboard}",
    "Here's the value: {clipboard}",
    "Here it is: {clipboard}",
    "Just copied this: {clipboard}",
    "This is it: {clipboard}",
    "Use this: {clipboard}",
    "As requested: {clipboard}",
    "Got it, here you go: {clipboard}",
    "This should be it: {clipboard}",
]

_ES = [
    "Aquí tienes: {clipboard}",
    "Toma, esto es lo que pediste: {clipboard}",
    "Aquí está el valor: {clipboard}",
    "Aquí lo tienes: {clipboard}",
    "Esto es: {clipboard}",
]

_DE = [
    "Hier ist es: {clipboard}",
    "Hier hast du den Wert: {clipboard}",
    "Hier, wie gewünscht: {clipboard}",
    "Bitte sehr: {clipboard}",
    "Hier: {clipboard}",
]

_IT = [
    "Ecco: {clipboard}",
    "Ecco il valore richiesto: {clipboard}",
    "Tieni, ecco qua: {clipboard}",
    "Ecco fatto: {clipboard}",
]

_PT = [
    "Aqui está: {clipboard}",
    "Aqui tem o valor: {clipboard}",
    "Toma, aqui está: {clipboard}",
    "Segue: {clipboard}",
]

_NL = [
    "Hier is het: {clipboard}",
    "Alsjeblieft: {clipboard}",
    "Hier heb je het: {clipboard}",
]

_SV = [
    "Här är det: {clipboard}",
    "Varsågod: {clipboard}",
]

_PL = [
    "Proszę: {clipboard}",
    "Oto wartość: {clipboard}",
    "Masz to: {clipboard}",
]

_RO = [
    "Iată: {clipboard}",
    "Poftim, iată valoarea: {clipboard}",
]

_CS = [
    "Tady to je: {clipboard}",
    "Prosím: {clipboard}",
]

_TR = [
    "İşte: {clipboard}",
    "Al bakalım: {clipboard}",
    "Buyur: {clipboard}",
]

_FI = [
    "Tässä se on: {clipboard}",
    "Ole hyvä: {clipboard}",
]

_ID = [
    "Ini dia: {clipboard}",
    "Ini nilainya: {clipboard}",
]

_VI = [
    "Đây là: {clipboard}",
    "Đây rồi: {clipboard}",
]

_RU = [
    "Вот: {clipboard}",
    "Вот значение: {clipboard}",
    "Держи: {clipboard}",
    "Пожалуйста, вот: {clipboard}",
]

_UK = [
    "Ось: {clipboard}",
    "Тримай: {clipboard}",
]

_EL = [
    "Ορίστε: {clipboard}",
    "Να το: {clipboard}",
]

_AR = [
    "ها هي: {clipboard}",
    "تفضل: {clipboard}",
]

_HE = [
    "הנה: {clipboard}",
    "בבקשה: {clipboard}",
]

_HI = [
    "यह लीजिए: {clipboard}",
    "ये रहा: {clipboard}",
]

_TH = [
    "นี่ไง: {clipboard}",
    "นี่ครับ/ค่ะ: {clipboard}",
]

_JA = [
    "はい、こちらです: {clipboard}",
    "これです: {clipboard}",
    "どうぞ: {clipboard}",
]

_ZH = [
    "给你: {clipboard}",
    "这是你要的: {clipboard}",
    "拿去: {clipboard}",
]

_KO = [
    "여기 있어요: {clipboard}",
    "여기요: {clipboard}",
]

DEFAULT_MESSAGE_TEMPLATES = (
    _FR + _EN + _ES + _DE + _IT + _PT + _NL + _SV + _PL + _RO + _CS + _TR
    + _FI + _ID + _VI + _RU + _UK + _EL + _AR + _HE + _HI + _TH + _JA + _ZH + _KO
)
