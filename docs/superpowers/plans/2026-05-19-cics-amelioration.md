# Amelioration section CICS — Plan d'implementation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Aligner la section CICS de l'interface web sur le niveau de Batch/DB2 : categories, descriptions, bouton CODE, coherence visuelle, info banner avec schema.

**Architecture:** Les ecrans MAJO/DELG sont deja ajoutes dans cics_screens.py (travail en cours). Le plan enrichit les metadata (category, descriptions), etend le backend (source CICS), et modifie le frontend (categories, CODE, rendu coherent).

**Tech Stack:** Python/Flask (server.py), HTML/JS vanilla (index.html), Docker

**Etat actuel :** MAJO et DELG existent deja dans cics_screens.py (ajout utilisateur en cours, pas encore commit). Le plan part de cet etat.

---

### Task 1: Enrichir metadata cics_screens.py (categories + descriptions)

**Files:**
- Modify: `docker/cics_screens.py:5-472`

- [ ] **Step 1: Ajouter le champ `category` et mettre a jour `description` pour chaque transaction**

Editer chaque entree du dict SCREENS pour ajouter `"category"` et aligner les descriptions sur celles validees dans le spec.

AFFI :
```python
"description": "Lecture VSAM KSDS par cle, SEND MAP avec donnees client",
"category": "Consultation",
```

AJOU :
```python
"description": "Saisie formulaire complet, WRITE VSAM avec controle DUPKEY",
"category": "Saisie",
```

LIST :
```python
"description": "Navigation paginee STARTBR/READNEXT, grille 15 lignes, PF7/PF8",
"category": "Navigation",
```

STAT :
```python
"description": "Parcours via AIX region, totalisation debiteurs/crediteurs par zone geographique",
"category": "Navigation",
```

SUPP :
```python
"description": "Affichage recapitulatif puis confirmation O/N, DELETE VSAM",
"category": "Saisie",
```

MAJO :
```python
"description": "3 phases (recherche/affichage/validation), READ UPDATE + REWRITE, cle protegee dynamiquement via attribut ASKIP",
"category": "Saisie",
```

DELG :
```python
"description": "Suppression par prefixe (1-6 car), STARTBR/READNEXT pour comptage, DELETE en lot avec table de cles",
"category": "Saisie",
```

- [ ] **Step 2: Mettre a jour `get_screens_list()` pour retourner `category`**

```python
def get_screens_list():
    """Return a list of screen metadata (id, transaction, program, title, description, category)."""
    result = []
    for screen_id, data in SCREENS.items():
        result.append({
            "id": screen_id,
            "transaction": data["transaction"],
            "program": data["program"],
            "title": data["title"],
            "description": data["description"],
            "category": data.get("category", ""),
            "steps_count": len(data["steps"]),
        })
    return result
```

- [ ] **Step 3: Verifier que l'API retourne les nouveaux champs**

Run: `cd /Users/josuexavierrocha/Projets/fil-rouge-mainframe && python3 -c "from docker.cics_screens import get_screens_list; import json; print(json.dumps(get_screens_list(), indent=2))"`

Expected: 7 transactions, chacune avec `category` et `description` enrichie.

- [ ] **Step 4: Commit**

```bash
git add docker/cics_screens.py
git commit -m "feat: categories et descriptions techniques CICS (7 transactions)"
```

---

### Task 2: Etendre /api/source/ pour les sources CICS

**Files:**
- Modify: `docker/server.py:105-118`
- Modify: `docker/Dockerfile:14-21`
- Modify: `.dockerignore`

- [ ] **Step 1: Ajouter COBOL_CICS_DIR dans server.py**

A la ligne 107 (apres `COBOL_DB2_DIR`), ajouter :

```python
COBOL_CICS_DIR = "/app/03-cics/cobol"
```

Modifier la boucle de `get_source()` (ligne 112) :

```python
for src_dir in [COBOL_BATCH_DIR, COBOL_DB2_DIR, COBOL_CICS_DIR]:
```

- [ ] **Step 2: Mettre a jour le Dockerfile**

Ajouter apres la ligne `COPY 02-db2/cobol/ /app/02-db2/cobol/` :

```dockerfile
COPY 03-cics/cobol/ /app/03-cics/cobol/
```

- [ ] **Step 3: Mettre a jour .dockerignore**

Remplacer la ligne `03-cics` par :

```
03-cics/jcl
```

Cela autorise `03-cics/cobol/` et `03-cics/bms/` dans le contexte Docker.

- [ ] **Step 4: Verifier que le source CICS est trouvable localement**

Run: `python3 -c "import os; print(os.path.isfile('03-cics/cobol/PRGMAJ.cbl'))"`

Expected: `True`

- [ ] **Step 5: Commit**

```bash
git add docker/server.py docker/Dockerfile .dockerignore
git commit -m "feat: endpoint /api/source/ etendu aux sources CICS"
```

---

### Task 3: Frontend — categories et descriptions inline dans la grille CICS

**Files:**
- Modify: `docker/static/index.html` — fonction `renderCICS()` (~ligne 1133)

- [ ] **Step 1: Modifier renderCICS() pour grouper par categorie**

Remplacer le contenu de `renderCICS()` a partir de `body.innerHTML = ...`. La grille doit etre groupee par categorie, avec un en-tete amber par groupe. Ordre des categories : Consultation, Saisie, Navigation.

```javascript
async function renderCICS(body) {
    body.innerHTML = `<div class="terminal"><span class="t-info loading">Chargement transactions CICS </span></div>`;

    try {
        const res = await fetch("/api/cics/screens");
        cicsScreens = await res.json();
    } catch(e) {
        cicsScreens = [];
    }

    if (!cicsScreens || cicsScreens.length === 0) {
        body.innerHTML = `<div class="terminal"><span class="t-error">Impossible de charger les ecrans CICS.</span>\n<span class="t-dim">Verifier que l'API est disponible sur /api/cics/screens</span></div>`;
        return;
    }

    // Group by category
    const categoryOrder = ["Consultation", "Saisie", "Navigation"];
    const grouped = {};
    cicsScreens.forEach(s => {
        const cat = s.category || "Autres";
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(s);
    });

    let gridHtml = "";
    const orderedCats = [...categoryOrder.filter(c => grouped[c]), ...Object.keys(grouped).filter(c => !categoryOrder.includes(c))];
    orderedCats.forEach(cat => {
        const screens = grouped[cat];
        if (!screens || screens.length === 0) return;
        gridHtml += `<div style="padding:4px 12px;color:var(--amber);font-size:11px;border-bottom:1px solid var(--border)">${cat}</div>`;
        gridHtml += `<div class="pgm-grid">`;
        screens.forEach(s => {
            gridHtml += `
        <div class="pgm-item" data-id="${esc(s.id)}" onclick="selectScreen('${esc(s.id)}')">
            <span class="pgm-id">${esc(s.transaction)} <span style="color:var(--green-dim)">${esc(s.program)}</span></span>
            <div style="flex:1;min-width:0">
                <span class="pgm-name">${esc(s.title || "")}</span>
                <span style="color:var(--green-dim);font-size:11px;display:block;margin-top:2px">${esc(s.description || "")}</span>
            </div>
        </div>`;
        });
        gridHtml += `</div>`;
    });

    body.innerHTML = `
        <div class="info-banner" id="cics-info">
<span class="t-dim">  Replay des ecrans BMS — mode pseudo-conversationnel, COMMAREA.</span>
<span class="t-dim">  </span><span class="t-head">CLIAFF</span><span class="t-dim"> ──┐              </span><span class="t-head">FCLIENT</span><span class="t-dim"> (VSAM KSDS)</span>
<span class="t-dim">  </span><span class="t-head">CLIMAJ</span><span class="t-dim"> ──┤── 7 PRG ──── 20 enregistrements</span>
<span class="t-dim">  </span><span class="t-head">CLIDEL</span><span class="t-dim"> ──┘    |</span>
<span class="t-dim">            COMMAREA      AIX: region, activite</span>
        </div>
        <div id="cics-grid">${gridHtml}</div>`;

    document.getElementById("screen-info").textContent = cicsScreens.length + " transactions";

    // Reset nav bar
    document.getElementById("cics-prev-btn").disabled = true;
    document.getElementById("cics-next-btn").disabled = true;
    document.getElementById("cics-code-btn").disabled = true;
    document.getElementById("cics-step-info").textContent = "";
    document.getElementById("cics-nav-hint").textContent = "Selectionner une transaction";
}
```

- [ ] **Step 2: Mettre a jour selectScreen() pour changer le banner au clic**

```javascript
function selectScreen(id) {
    const s = cicsScreens.find(s => s.id === id);
    if (!s) return;
    selectedScreen = s;
    currentStep = 0;

    document.querySelectorAll(".pgm-item").forEach(el => {
        el.classList.toggle("selected", el.dataset.id === id);
    });

    const banner = document.getElementById("cics-info");
    if (banner) {
        banner.innerHTML = `<span class="t-head">  ${esc(s.transaction)} — ${esc(s.title)}</span>\n<span class="t-dim">  ${esc(s.description || "")}</span>\n<span class="t-info">  Programme : ${esc(s.program)}   Naviguer avec PF7/PF8</span>`;
    }

    document.getElementById("cics-code-btn").disabled = false;

    showCicsStep(id, 0);
}
```

- [ ] **Step 3: Commit**

```bash
git add docker/static/index.html
git commit -m "feat: categories, descriptions inline et schema CICS"
```

---

### Task 4: Frontend — bouton CODE dans la barre CICS

**Files:**
- Modify: `docker/static/index.html` — HTML cics-nav (~ligne 446) et fonction `viewSource()` (~ligne 676)

- [ ] **Step 1: Ajouter le bouton CODE dans le HTML de cics-nav**

Remplacer le bloc `<div class="cics-nav">` :

```html
<div class="cics-nav" id="cics-nav" style="display:none">
    <button class="nav-btn" id="cics-code-btn" onclick="viewSource()" disabled style="background:var(--amber);color:var(--bg)">CODE</button>
    <button class="nav-btn" id="cics-prev-btn" onclick="cicsPrev()" disabled>PF7 Prec</button>
    <button class="nav-btn" id="cics-next-btn" onclick="cicsNext()" disabled>PF8 Suiv</button>
    <span class="step-info" id="cics-step-info"></span>
    <span class="nav-hint" id="cics-nav-hint">Selectionner une transaction</span>
</div>
```

- [ ] **Step 2: Ajouter le bloc CICS dans viewSource()**

Au debut de la fonction `viewSource()`, avant le bloc `if (currentPhase === "db2")`, ajouter :

```javascript
if (currentPhase === "cics") {
    if (!selectedScreen) return;
    const body = document.getElementById("screen-body");
    body.innerHTML = `<div class="terminal"><span class="t-prompt">SOURCE ${esc(selectedScreen.program)}</span>\n<span class="t-info loading">Chargement source </span></div>`;

    try {
        const res = await fetch(`/api/source/${selectedScreen.program}`);
        const data = await res.json();

        if (data.error) {
            body.innerHTML = `<div class="terminal"><span class="t-error">ERREUR: ${esc(data.error)}</span></div>`;
            return;
        }

        const source = data.source || data.content || "";
        const lines = source.split("\n");

        const cobolKeywords = /\b(IDENTIFICATION|ENVIRONMENT|DATA|PROCEDURE|DIVISION|SECTION|PERFORM|IF|EVALUATE|MOVE|OPEN|CLOSE|READ|WRITE|SORT|MERGE|CALL|STOP|DISPLAY|ACCEPT|EXEC|CICS|END-EXEC|SEND|RECEIVE|RETURN|COMMAREA|STARTBR|READNEXT|ENDBR|REWRITE|DELETE|MAP|MAPSET|ERASE|DATAONLY|CURSOR|RESP|DFHRESP|FILE)\b/g;

        let out = `<button class="back-btn" onclick="showPhase('cics')">F3 Retour</button>`;
        out += `<span class="t-prompt">SOURCE ${esc(selectedScreen.program)}</span>  ${esc(selectedScreen.title)}\n`;
        out += `<span class="t-separator">${"\u2500".repeat(70)}</span>\n`;

        lines.forEach(line => {
            if (line.length >= 7 && line[6] === "*") {
                out += `<span class="t-dim">${esc(line)}</span>\n`;
            } else {
                const escaped = esc(line);
                const highlighted = escaped.replace(cobolKeywords, '<span class="t-prompt">$1</span>');
                out += `<span class="t-white">${highlighted}</span>\n`;
            }
        });

        out += `<span class="t-separator">${"\u2500".repeat(70)}</span>\n`;
        out += `<span class="t-info">${lines.length} lignes</span>`;

        body.innerHTML = `<div class="terminal">${out}</div>`;
    } catch(e) {
        body.innerHTML = `<div class="terminal"><span class="t-error">ERREUR CONNEXION API</span></div>`;
    }
    return;
}
```

- [ ] **Step 3: Commit**

```bash
git add docker/static/index.html
git commit -m "feat: bouton CODE pour afficher les sources COBOL-CICS"
```

---

### Task 5: Frontend — coherence visuelle du rendu showCicsStep

**Files:**
- Modify: `docker/static/index.html` — fonction `showCicsStep()` (~ligne 1181)

- [ ] **Step 1: Modifier showCicsStep() pour ajouter description et footer**

Remplacer le bloc de construction de `out` dans `showCicsStep()` :

```javascript
let out = `<span class="t-head">  ${esc(selectedScreen.transaction)}`;
if (selectedScreen.title) {
    out += ` — ${esc(selectedScreen.title)}`;
}
out += `</span>\n`;
out += `<span class="t-separator">${"\u2500".repeat(70)}</span>\n`;
if (selectedScreen.description) {
    out += `<span class="t-dim">  ${esc(selectedScreen.description)}</span>\n`;
    out += `<span class="t-separator">${"\u2500".repeat(70)}</span>\n`;
}
out += rendered;
out += `\n<span class="t-separator">${"\u2500".repeat(70)}</span>\n`;
out += `<span class="t-info">  Etape ${step + 1}/${data.steps_count} — ${esc(data.label)}</span>`;
```

- [ ] **Step 2: Commit**

```bash
git add docker/static/index.html
git commit -m "feat: coherence visuelle rendu CICS (description + footer etape)"
```

---

### Task 6: Mise a jour du compteur et nettoyage

**Files:**
- Modify: `docker/static/index.html` — fonction `showPhase()` (~ligne 572)
- Modify: `docs/superpowers/specs/2026-05-19-cics-amelioration-design.md`

- [ ] **Step 1: Corriger le compteur en dur dans showPhase()**

Ligne 574, remplacer :

```javascript
info.textContent = "5 transactions";
```

par :

```javascript
info.textContent = "7 transactions";
```

- [ ] **Step 2: Mettre a jour le spec — MAJU devient MAJO**

Dans le fichier spec, remplacer toutes les occurrences de `MAJU` par `MAJO` pour refleter le vrai TRANSID COBOL.

- [ ] **Step 3: Commit**

```bash
git add docker/static/index.html docs/superpowers/specs/2026-05-19-cics-amelioration-design.md
git commit -m "fix: compteur 7 transactions, spec MAJU -> MAJO"
```

---

### Task 7: Test Docker build

- [ ] **Step 1: Build et run Docker**

```bash
docker compose build && docker run -d --name cobol-api-test -p 8082:8080 fil-rouge-mainframe-cobol-api
```

- [ ] **Step 2: Verifier les endpoints**

```bash
# 7 transactions avec category
curl -s http://localhost:8082/api/cics/screens | python3 -m json.tool | head -30

# Ecran MAJO step 0
curl -s "http://localhost:8082/api/cics/screen/MAJO?step=0" | python3 -m json.tool | head -10

# Source CICS
curl -s http://localhost:8082/api/source/PRGMAJ | python3 -m json.tool | head -5
```

Expected:
- 7 transactions, chacune avec `category` et `description`
- Ecran MAJO avec les 24 lignes ASCII
- Source PRGMAJ retourne sans erreur

- [ ] **Step 3: Cleanup**

```bash
docker stop cobol-api-test && docker rm cobol-api-test
```

- [ ] **Step 4: Commit final si ajustements**

Si des corrections ont ete necessaires, commit avec :

```bash
git commit -am "fix: ajustements post-test Docker CICS"
```
