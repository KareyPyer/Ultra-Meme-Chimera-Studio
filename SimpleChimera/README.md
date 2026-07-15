# CHIMERA_FORGE v3.5

Générateur d'artefacts visuels "glitch" à double lecture (texte de surface / sous-texte), avec calque procédural de type Truchet et export optionnel de prompt pour génération d'image IA (Grok). Le projet s'inscrit dans l'univers créatif **Corpus Vauvillensis 2075** (esthétique cyberpunk/occulte-technique, thème de la saturation attentionnelle).

## Fichiers

| Fichier | Rôle |
|---|---|
| `chimera_forge.py` | Script principal (Python 3, dépendance : `Pillow`) |
| `saturation_2026_ultra.json` | Preset de configuration (visuel + textes + template de prompt) |

## Principe

Le script compose une image (fond généré ou photo fournie) avec :
1. **Un calque procédural Truchet** — pavage récursif de pieslices semi-transparentes, dont l'intensité du "glitch" est pilotée par le paramètre `glitch_intensity` du preset.
2. **Un bloc de texte à double lecture** — chaque section (`opening`, `framing`, `body`, `constraint`, `trap`, `closing`) possède un texte `surface` (affiché en clair) et un `subtext` optionnel (affiché en gris, en retrait), assemblés puis centrés/habillés sur l'image.
3. **Des métadonnées** — identifiant unique de rendu, nœud d'ancrage narratif, date, version.

Deux modes de rendu :
- **Mode procédural** (par défaut, sans `--fuse`) : fond uni + rectangle opaque derrière le texte pour la lisibilité.
- **Mode fusion** (`--fuse <image>`) : l'image fournie sert de fond ; le texte flotte sans rectangle, avec contour épais et léger décalage chromatique ("ombre glitchée"), sauf si `--with-background` force le rectangle.

## Installation

```bash
pip install Pillow
```

Polices utilisées si disponibles sur le système : `DejaVuSansMono` (texte principal) et `DejaVuSansMono-Oblique` (sous-textes) ; sinon repli sur la police par défaut de Pillow.

## Usage

```bash
# Rendu procédural simple, preset par défaut
python chimera_forge.py

# Rendu procédural avec preset explicite
python chimera_forge.py --preset saturation_2026_ultra

# Fusion sur une image existante (sans rectangle de fond)
python chimera_forge.py --fuse photo.jpg

# Fusion avec rectangle forcé
python chimera_forge.py --fuse photo.jpg --with-background

# Désactiver les sous-textes (affichage "surface" uniquement)
python chimera_forge.py --no-subtext

# Générer en plus un fichier de prompt Grok
python chimera_forge.py --grok

# Utiliser un autre fichier de config
python chimera_forge.py --config mon_preset.json
```

### Arguments CLI

| Argument | Description |
|---|---|
| `--preset NAME` | Nom du preset à utiliser (défaut : `default_preset` du JSON) |
| `--fuse PATH` | Image source à utiliser comme fond (active le mode fusion) |
| `--grok` | Génère en plus un fichier `.txt` de prompt pour génération d'image IA |
| `--no-subtext` | N'affiche que les textes de surface |
| `--config PATH` | Chemin vers le fichier de preset JSON (défaut : `saturation_2026_ultra.json`) |
| `--with-background` | Force le rectangle opaque même en mode fusion |

### Sorties

- `chimera_<preset>_<timestamp>.png` — image générée
- `grok_prompt_<ID>.txt` — prompt texte (si `--grok`), construit à partir de `location_anchor`, palette, `key_concepts` et `negative_prompts` du preset

## Structure du preset (`saturation_2026_ultra.json`)

```
_metadata            → version, référence de codex narratif
default_preset        → nom du preset chargé par défaut
presets.<nom>
  ├── visual           → dimensions, palette, intensité de glitch, calque caché
  ├── basilisk_tracks  → les 6 blocs de texte (surface + subtext) assemblés dans l'image
  ├── subliminal_tracks→ listes thématiques (mots-clés narratifs, non rendus visuellement)
  ├── fusion_directives→ paramètres de blend pour le mode fusion
  └── grok_prompt_template → base de génération du prompt IA (style, concepts-clés, negative prompts)
_basilisk_nesting     → documentation narrative interne (lore Corpus Vauvillensis) décrivant
                         les différents niveaux de lecture du fichier ; n'affecte pas le rendu
```

Le vocabulaire "basilisk" / "subliminal" / "cerveau reptilien" présent dans le JSON relève de la **couche narrative et esthétique** du projet (cf. lore Corpus Vauvillensis / Fravian Cognitive Archaeology) — il documente l'intention artistique et le sous-texte fictionnel des blocs de texte, mais ne correspond à aucun mécanisme technique d'influence réelle : le calque `_hidden_layer` à 8% d'opacité est un simple effet visuel discret (hexagramme semi-transparent), sans effet psychologique démontré.

## Notes techniques

- `_generate_truchet_overlay` : construit le pavage par cellules de 32px, avec pondération des couleurs de la palette selon `glitch_intensity`.
- `_assemble_basilisk_text` : assemble les 6 blocs dans l'ordre `opening → framing → body → constraint → trap → closing`, avec préfixes distincts par section.
- `_wrap_text` : retour à la ligne automatique selon la largeur max calculée à partir de l'image.
- `_draw_text_with_outline` : contour multi-directionnel utilisé en mode fusion sans fond, pour garantir la lisibilité sur image complexe.

## Licence / Usage

Projet interne INGEN Systems — outil de génération d'art génératif expérimental. Pas de dépendance réseau, fonctionne entièrement en local.
