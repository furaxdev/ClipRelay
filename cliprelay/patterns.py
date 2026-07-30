"""Default regex patterns used to detect questions and sensitive content.

These are intentionally shape-based (key formats) or keyword-based (question
phrasing), never value-based: we never store an actual secret value here.
Users can extend/override every list from config.json.
"""

DEFAULT_QUESTION_PATTERNS = [
    r"peux[- ]tu me (donner|fournir|coller|passer)",
    r"colle (ta|ton|la|le)\b",
    r"quelle est (ta|ton|la|le)\b.*\?",
    r"j'ai besoin (de|d')\b.*(cl[ée]|token|mot de passe|password|api key)",
    r"what'?s the value of",
    r"please (paste|provide|share) (your|the)",
    r"can you (give|provide|paste|share) (me )?(your|the)",
    r"enter (your|the) .*(key|token|password|secret)",
]

# Disabled by default: matches ANY line ending in "?". Very high recall,
# very low precision. Opt in via config ("enable_loose_question_fallback").
LOOSE_QUESTION_FALLBACK = r"\?\s*$"

# Shape-based secret detectors: match the *format* of a credential, not a
# stored value, so the config file itself never contains real secrets.
DEFAULT_SECRET_PATTERNS = {
    "aws_access_key_id": r"AKIA[0-9A-Z]{16}",
    "aws_secret_access_key": r"(?i)aws_secret_access_key\s*=\s*[A-Za-z0-9/+=]{40}",
    "github_token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "openai_api_key": r"sk-[A-Za-z0-9]{20,}",
    "slack_token": r"xox[baprs]-[A-Za-z0-9-]{10,}",
    "private_key_block": r"-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "jwt": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
    "generic_bearer_token": r"(?i)bearer\s+[A-Za-z0-9._-]{20,}",
}

# Keywords in the *question line* that mark the expected answer as sensitive,
# even if the clipboard content doesn't match a known secret shape.
DEFAULT_SENSITIVE_CONTEXT_KEYWORDS = [
    "api key", "api_key", "clé api", "cle api",
    "token", "jeton",
    "mot de passe", "password", "passwd",
    "secret", "secrète", "secrete",
    "private key", "clé privée", "cle privee",
    "credential", "identifiant",
    "connection string", "chaîne de connexion",
]
