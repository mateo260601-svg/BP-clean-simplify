INSTALLATION BACKEND V3

Logiciels à installer sur ton PC:
1. GitHub Desktop = synchroniser ton repo GitHub
2. Visual Studio Code = modifier le code proprement
3. Python 3.11 = tester localement si besoin

Fichiers à remplacer/ajouter à la racine GitHub:
server.py
requirements.txt
extractor.py
financial_schema.py
financial_normalizer.py
excel_model_builder.py
deck_generator.py
template_selector.py
pptx_builder.py
quality_checks.py
.python-version
runtime.txt
nixpacks.toml

Ordre:
1. Upload tous les fichiers à la racine GitHub
2. Commit changes
3. Railway -> Clear build cache
4. Railway -> Redeploy latest commit

Endpoints compatibles avec l'UI:
POST /api/auth/login
POST /api/import
POST /api/generate
POST /api/generate_deck
GET /api/download/{file_id}
GET /api/download_deck/{file_id}
GET /health
