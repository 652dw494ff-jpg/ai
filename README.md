# Aura AI Web 0.1 — TG a.s.

První webová aplikace napojená na vlastní experimentální Aura Core 0.1.

## Co projekt obsahuje
- webový chat v češtině, responzivní pro mobil i počítač
- tmavý i světlý vzhled (volba se ukládá v prohlížeči)
- Flask API `/api/chat` a `/api/status`
- Aura Core 0.1: malý znakový n-gram model trénovaný od začátku z `data/train.txt`
- možnost znovu natrénovat model přes `POST /api/train`

## Důležité upozornění
Tohle je skutečný malý model trénovaný z přiložených textových dat, ale není to velký jazykový model typu ChatGPT. Nechápe spolehlivě význam vět a může generovat nesmysly. Je to technický základ a důkaz, že web komunikuje s vlastním modelem TG a.s. Neobsahuje API OpenAI, Gemini ani jiného externího chatbota.

Model je jednoduchý znakový n-gram, zvolený kvůli tomu, aby šel spustit i na malém cloudovém serveru bez GPU a bez velkých knihoven. Je odlišný od pozdějšího neuronového Transformeru; další verze může nahradit tento engine pokročilejším Aura Core.

## Spuštění na Windows (HP)
1. Nainstaluj Python 3.11 nebo novější z python.org a při instalaci zaškrtni **Add Python to PATH**.
2. Rozbal ZIP.
3. Otevři složku projektu, klikni do adresního řádku Průzkumníka, napiš `cmd` a stiskni Enter.
4. Spusť:
   ```bash
   py -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt
   python app.py
   ```
5. Otevři `http://127.0.0.1:8000`.

## Nasazení do cloudu přes Render
1. Vytvoř si účet na Render a účet na GitHubu (pokud je ještě nemáš).
2. Nahraj celý obsah této složky do nového GitHub repository.
3. V Renderu zvol **New → Blueprint** a připoj repository.
4. Render načte `render.yaml` a vytvoří webovou službu. Potvrď nasazení.
5. Po dokončení otevři přidělenou adresu `https://...onrender.com`.

Poznámky:
- Bezplatné instance mohou po nečinnosti usnout a první otevření pak chvíli trvá.
- Bezplatný hosting a jeho limity se mohou měnit; dostupnost a podmínky ověř přímo v Renderu.
- Model se při prvním startu natrénuje z `data/train.txt`. Na bezplatném hostingu se souborový systém může po restartu nebo novém nasazení obnovit. Proto si změny modelu a vlastní data vždy uchovávej v GitHubu nebo záloze. Do chatu neposílej soukromé údaje.
- Aplikace je veřejná, pokud ji nasadíš veřejně. V této verzi není přihlášení uživatelů ani ochrana soukromých konverzací. Nepoužívej ji pro citlivé informace.

## Rozšíření trénovacích dat
Přidávej vlastní krátké, legálně použitelné české texty do `data/train.txt`. Pak restartuj aplikaci nebo zavolej endpoint `/api/train` metodou POST. Čím víc kvalitních a různorodých dat, tím lépe se model naučí statistické vzory. Samotné přidání textu z něj ale neudělá znalostní databázi.

## API
- `GET /api/status` — stav modelu
- `POST /api/chat` — JSON `{"message":"Ahoj"}`
- `POST /api/train` — spustí trénování nad `data/train.txt`
