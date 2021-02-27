import paydunya

from paydunya import Store

PAYDUNYA_ACCESS_TOKENS = {
    "PAYDUNYA-MASTER-KEY": "tM0Q22he-UWmg-Omcq-ei2t-kkDfaMMogdQi",
    "PAYDUNYA-PRIVATE-KEY": "test_private_iR0R7rUXgYcHFwExwGnnIwDgMX1",
    "PAYDUNYA-TOKEN": "oUjUmBm3BwECMFTrHWSm",
}

# Activer le mode 'test'. Le debug est à False par défaut
paydunya.debug = True

# Configurer les clés d'API
paydunya.API_keys = PAYDUNYA_ACCESS_TOKENS


# Configuration des informations de votre service/entreprise
infos = {
    "name": "Xarala Academy",  # Seul le nom est requis
    "tagline": "La technologie dans votre langue",
    "postal_address": "Sicap Mbao, Extension",
    "phone_number": "763772260",
    "website_url": "https://www.xarala.co",
    "logo_url": "https://www.xarala.co/static/images/logo.32b513268679.png",
}

store = Store(**infos)
