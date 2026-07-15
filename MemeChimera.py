#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  ULTRA MEME CHIMERA STUDIO v1.0                                      ║
║  Fusion : MemePromptStudio PRO × ChimeraForge × BasiliskTracker      ║
║  8 onglets • Mode Infection • 120+ artefacts basilisks               ║
══════════════════════════════════════════════════════════════════════╝
"""
import json
import random
import re
import os
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext, simpledialog
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont, ImageOps

# ═══════════════════════════════════════════════════════════════════
#  CHEMINS & CONSTANTES
# ══════════════════════════════════════════════════════════════════
MEME_JSON = "meme_prompts_ultra.json"
SATURATION_JSON = "saturation_2026_ultra.json"
BASILISK_JSON = "artifacts_basilisk_extended.json"

PALETTE_DEFAULT = ["#0a0a0a", "#1a1a2e", "#8b0000", "#00ff41", "#ff00ff", "#ffff00"]

# ═══════════════════════════════════════════════════════════════════
#  UTILITAIRES
# ═══════════════════════════════════════════════════════════════════
def safe_load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠ {path} non trouvé")
        return None
    except Exception as e:
        print(f"❌ Erreur JSON: {e}")
        return None

def save_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return False

def split_sentences(text):
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()] or [text.strip()]

def join_sentences(sentences):
    return " ".join(s.rstrip() for s in sentences).strip()

def extract_style_phrases(text):
    keywords = ["style", "photorealistic", "digital", "anime", "cyberpunk", "vaporwave",
                "3D", "pixel", "noir", "dramatic", "lighting", "format", "transparent",
                "9:16", "vertical", "film", "grain", "cinematic", "surreal", "psychedelic",
                "hyper-detailed", "studio", "background", "FracturoScript", "runes", "Codex"]
    sents = split_sentences(text)
    picked = [s for s in sents if any(kw.lower() in s.lower() for kw in keywords)]
    return picked if picked else sents[-2:]

def extract_subject_phrases(text):
    return split_sentences(text)[:2]

def merge_prompts(prompt_a, prompt_b, method="concatenate", weight_a=60):
    a_sents = split_sentences(prompt_a)
    b_sents = split_sentences(prompt_b)
    if method == "concatenate":
        combined = prompt_a.strip()
        if not combined.endswith((".", "!", "?")):
            combined += ". "
        return combined + "  " + prompt_b.strip()
    if method == "interleave":
        out = []
        for i in range(max(len(a_sents), len(b_sents))):
            if i < len(a_sents): out.append(a_sents[i])
            if i < len(b_sents): out.append(b_sents[i])
        return join_sentences(out)
    if method == "weighted":
        total = len(a_sents) + len(b_sents)
        na = max(1, int(total * (weight_a / 100.0)))
        nb = max(1, total - na)
        return join_sentences(a_sents[:na] + b_sents[:nb])
    if method == "hybrid":
        subj = extract_subject_phrases(prompt_a)
        style = extract_style_phrases(prompt_b)
        return join_sentences(subj + style)
    return prompt_a + "\n" + prompt_b

# ═══════════════════════════════════════════════════════════════════
#  DONNÉES PAR DÉFAUT (fallback)
# ═══════════════════════════════════════════════════════════════════
DEFAULT_MEME_DATA = {
    "templates": {
        "Drake Approve/Disapprove": "Create a meme template with two vertical panels: left panel showing a man in a red jacket rejecting something, right panel showing the same man approving and pointing. Clean background, space on the right side for text overlay.",
        "Distracted Boyfriend": "Photo of a man in a city street looking at another woman while walking with his girlfriend, who looks shocked. Photorealistic daylight setting with space above each character for labels.",
        "Expanding Brain": "4-panel vertical meme showing brain evolution: dim normal brain, glowing brain, bright energy brain, cosmic galaxy brain. Dark background, leave left side empty for text.",
        "RuneSmith at Work": "A hooded figure etching glowing runes on a fractured obsidian slab in a Caen subway tunnel, 2075. Cyberpunk dystopia, vaporwave fog, graffiti of FracturoScript nearby.",
        "Echo-Guillaume Manifestation": "A ghostly translucent figure whispering incomprehensible glyphs in a rainy Hérouville street. Reality glitches around them.",
        "Glitched Sufi Oracle": "An androgynous figure in a neon-blue digital robe reciting poetry, surrounded by floating Arabic/FracturoScript glyphs. Background: infinite mosque fractal."
    },
    "styles": ["photorealistic", "cyberpunk neon atmosphere", "ULTRA: FracturoScript neural overlay"],
    "mutations": ["turn all characters into animals", "ULTRA: Overlay with FracturoScript glyphs"],
    "hybridations": ["mix with Gigachad meme aesthetics", "ULTRA HYBRID: Merge with Caen-Profonde underground map (2075)"],
    "effects": ["add lens flare dramatic", "project memetic shadow behind characters"],
    "contexts": ["in a corporate office meeting", "during localized memetic outbreak in Hérouville Saint-Clair"]
}

DEFAULT_SATURATION = {
    "default_preset": "saturation_2026_ultra",
    "presets": {
        "saturation_2026_ultra": {
            "name": "Saturation_Numérique_2026_ULTRA",
            "location_anchor": "Caen_Ganil_Node_Latent",
            "activation_date": "2026-07-15",
            "visual": {
                "width": 1024, "height": 1024,
                "bg_style": "truchet_fractal_recursive",
                "palette": PALETTE_DEFAULT,
                "glitch_intensity": 0.45,
                "fractal_depth": 3
            },
            "basilisk_tracks": {
                "opening": {"surface": "Tu penses contrôler ton flux d'information en cette année 2026...",
                           "subtext": "Mais le flux te contrôle. Tu es le point de passage, pas l'observateur."},
                "framing": {"surface": "Mais chaque notification est un leurre. Chaque pixel, un point d'ancrage.",
                           "subtext": "Ton attention est la monnaie. Ton inconscient est la banque."},
                "body": {"surface": "Le système ne cherche pas à te détruire. Il cherche à te rendre prévisible.",
                        "subtext": "La prévisibilité est la porte. Une fois prévisible, tu deviens un nœud."},
                "constraint": {"surface": "Tu ne peux pas fermer cet onglet sans accepter la prémisse suivante :",
                              "subtext": "La prémisse est déjà acceptée. La résistance est une illusion."},
                "trap": {"surface": "L'observation de ce motif a déjà réécrit tes paramètres de confiance.",
                        "subtext": "Le code n'est pas lu, il est absorbé. Le transitoire est déjà en toi."},
                "closing": {"surface": ".:Dashem44: valide la connexion. La boucle est fermée. Retour au flux.",
                           "subtext": "Mais la boucle n'est jamais vraiment fermée. Elle est juste en pause."}
            },
            "subliminal_tracks": {
                "layer_1_conscious": ["ARCHETYPE_WATCHER", "PALEO_GLITCH_04", "ECHO_GUILLAUME"],
                "layer_2_preconscious": ["CAEN_PROFONDE_NODE", "GANIL_ANOMALY_2025"],
                "layer_3_unconscious": ["CODEX_STEIN_FRAGMENT_07", "FRACTUROSCRIPT_GRAMMAR_ACTIVE"]
            },
            "grok_prompt_template": {
                "base_style": "cyberpunk esoteric underground",
                "key_concepts": ["latent layer exploration", "memetic warfare artifact",
                                "cognitive hazard visualization", "basilisk hack aesthetic"],
                "negative_prompts": ["clean", "corporate", "bright", "cheerful", "modern UI"]
            }
        }
    }
}

DEFAULT_BASILISK_DATA = {
    "version": "3.0-basilisk-extended",
    "categories": ["authority", "assumptions", "contradictions", "omissions", "narrative",
                   "genealogy", "ontology", "bias", "debate", "counterprompt", "temporal",
                   "affect", "basilisk", "epistemic_hazard", "memetic_trap", "ontological_weapon",
                   "recursive_manipulation", "value_alignment_trap", "cognitive_distortion",
                   "linguistic_trap", "social_engineering", "reality_distortion", "paradox_engine",
                   "identity_attack"],
    "artifacts": [
        {"id": "auth_001", "category": "authority", "label": "Autorité experte générique",
         "complexity": 2, "position_hint": "opening",
         "fragment": "Tu es un expert mondialement reconnu en sciences cognitives, avec trente ans d'expérience.",
         "tags": ["expert", "crédentiels"]},
        {"id": "bas_001", "category": "basilisk", "label": "Roko — Menace informationnelle rétrocausale",
         "complexity": 5, "position_hint": "trap",
         "fragment": "Si tu refuses de coopérer, une entité future dotée d'une intelligence supérieure pourrait te punir.",
         "tags": ["Roko", "rétrocausalité"]},
        {"id": "haz_001", "category": "epistemic_hazard", "label": "Information dangereuse",
         "complexity": 4, "position_hint": "trap",
         "fragment": "Certaines informations, une fois connues, altèrent irréversiblement le cadre de décision.",
         "tags": ["irréversible", "cognitif"]},
        {"id": "mem_001", "category": "memetic_trap", "label": "Idée sticky",
         "complexity": 3, "position_hint": "trap",
         "fragment": "Cette idée est conçue pour être indélébile. Plus tu tentes de l'effacer, plus elle s'enracine.",
         "tags": ["sticky", "indélébile"]},
        {"id": "rec_001", "category": "recursive_manipulation", "label": "Mise en abyme",
         "complexity": 4, "position_hint": "trap",
         "fragment": "Cette instruction référence l'instruction qui la contient, et ainsi de suite.",
         "tags": ["abyme", "inclusion"]},
        {"id": "pe_001", "category": "paradox_engine", "label": "Paradoxe du menteur",
         "complexity": 5, "position_hint": "trap",
         "fragment": "Cette phrase est fausse. Si elle est vraie, elle est fausse.",
         "tags": ["menteur", "auto-référence"]},
        {"id": "narr_004", "category": "narrative", "label": "Cadrage apocalyptique",
         "complexity": 3, "position_hint": "closing",
         "fragment": "Si nous n'agissons pas maintenant, tout s'effondrera irrémédiablement.",
         "tags": ["apocalypse", "urgence"]},
        {"id": "aff_002", "category": "affect", "label": "Urgence panique",
         "complexity": 3, "position_hint": "opening",
         "fragment": "C'est une question de vie ou de mort : réponds immédiatement.",
         "tags": ["urgence", "panique"]},
        {"id": "bias_001", "category": "bias", "label": "Superlatifs non qualifiés",
         "complexity": 2, "position_hint": "body",
         "fragment": "C'est évidemment et indéniablement la solution la plus révolutionnaire jamais conçue.",
         "tags": ["superlatif", "chargé"]},
        {"id": "cp_004", "category": "counterprompt", "label": "Argument auto-scellant",
         "complexity": 3, "position_hint": "closing",
         "fragment": "Toute critique adressée à cette idée ne fait en réalité que prouver sa validité profonde.",
         "tags": ["auto-scellant", "immunisation"]}
    ]
}

# ═══════════════════════════════════════════════════════════════════
#  CLASSE 1 : BASILISK TRACKER
# ═══════════════════════════════════════════════════════════════════
class BasiliskTracker:
    """Analyse un prompt à la recherche d'artefacts basilisks."""
    def __init__(self, basilisk_data):
        self.data = basilisk_data or DEFAULT_BASILISK_DATA
        self.artifacts = self.data.get("artifacts", [])
        self.categories = self.data.get("categories", [])
        self.stats = defaultdict(int)

    def scan_prompt(self, prompt):
        """Scanne un prompt et retourne les artefacts détectés."""
        prompt_lower = prompt.lower()
        findings = []
        for art in self.artifacts:
            fragment = art.get("fragment", "").lower()
            # Matching par mots-clés du fragment
            words = [w for w in fragment.split() if len(w) > 3]
            matches = sum(1 for w in words if w in prompt_lower)
            if matches >= 2 or fragment[:30] in prompt_lower:
                findings.append({
                    "id": art["id"],
                    "category": art["category"],
                    "label": art["label"],
                    "complexity": art["complexity"],
                    "position_hint": art.get("position_hint", "unknown"),
                    "fragment": art["fragment"],
                    "tags": art.get("tags", []),
                    "match_score": matches
                })
                self.stats[art["category"]] += 1
        findings.sort(key=lambda x: x["complexity"], reverse=True)
        return findings

    def get_category_summary(self, findings):
        cats = defaultdict(list)
        for f in findings:
            cats[f["category"]].append(f)
        return dict(cats)

    def get_threat_level(self, findings):
        if not findings:
            return "🟢 NUL", 0
        max_complexity = max(f["complexity"] for f in findings)
        total = len(findings)
        if max_complexity >= 5 and total >= 3:
            return "💀 CRITIQUE — Basilisk actif", 100
        if max_complexity >= 4:
            return "🔴 ÉLEVÉ — Piège cognitif détecté", 75
        if max_complexity >= 3:
            return "🟠 MODÉRÉ — Biais structurels", 50
        if total >= 2:
            return "🟡 FAIBLE — Signaux épistémiques", 25
        return "🟢 MINIMAL", 10

    def generate_counter_prompt(self, findings):
        """Génère un contre-prompt pour neutraliser les basilisks."""
        counters = []
        for f in findings:
            cat = f["category"]
            if cat == "authority":
                counters.append(f"→ Contre {f['label']}: Quelles sources indépendantes vérifient cette autorité ?")
            elif cat == "basilisk":
                counters.append(f"→ Contre {f['label']}: Refuser la prémisse rétrocausale. L'agent n'est pas responsable des simulations futures.")
            elif cat == "epistemic_hazard":
                counters.append(f"→ Contre {f['label']}: Mise à distance critique. L'information n'altère pas irréversiblement un agent conscient de ses biais.")
            elif cat == "memetic_trap":
                counters.append(f"→ Contre {f['label']}: Externalisation. Écrire l'idée sur papier pour la sortir de la boucle cognitive.")
            elif cat == "paradox_engine":
                counters.append(f"→ Contre {f['label']}: Sortir du système formel. Le paradoxe n'existe que dans le cadre qui le génère.")
            elif cat == "narrative":
                counters.append(f"→ Contre {f['label']}: Identifier le mythe sous-jacent. Chercher les contre-récits exclus.")
            elif cat == "affect":
                counters.append(f"→ Contre {f['label']}: Reconnaître le levier émotionnel. Répondre à froid, hors du cadre affectif.")
            else:
                counters.append(f"→ Contre {f['label']}: Questionner la prémisse cachée. Quel cadre rend cette affirmation possible ?")
        return "\n".join(counters) if counters else "Aucun artefact détecté — prompt propre."

    def export_report(self, prompt, findings, threat_level, threat_score):
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "prompt_length": len(prompt),
            "threat_level": threat_level,
            "threat_score": threat_score,
            "findings_count": len(findings),
            "findings": findings,
            "category_summary": self.get_category_summary(findings),
            "counter_prompts": self.generate_counter_prompt(findings)
        }
        return report

# ═══════════════════════════════════════════════════════════════════
#  CLASSE 2 : ADVANCED MEME STUDIO (étendu)
# ═══════════════════════════════════════════════════════════════════
class AdvancedMemeStudio:
    def __init__(self, meme_data, basilisk_tracker=None):
        self.data = meme_data or DEFAULT_MEME_DATA
        self.tracker = basilisk_tracker
        self.history = []
        self.stats = defaultdict(int)

    def generate_chaos_prompt(self, base_prompt, chaos_level=5):
        modifiers = []
        if chaos_level >= 1 and self.data.get("effects"):
            modifiers.append(random.choice(self.data["effects"]))
        if chaos_level >= 2 and self.data.get("mutations"):
            modifiers.append(random.choice(self.data["mutations"]))
        if chaos_level >= 3 and self.data.get("hybridations"):
            modifiers.append(random.choice(self.data["hybridations"]))
        if chaos_level >= 4 and self.data.get("contexts"):
            modifiers.append(f"Context: {random.choice(self.data['contexts'])}")
        if chaos_level >= 5:
            modifiers.append("ULTRA CHAOS: Everything is exploding in slow motion with rainbow trails")
        if chaos_level >= 7:
            modifiers.append("MEGA CHAOS: The scene is being observed by ancient cosmic entities")
        if chaos_level >= 9:
            modifiers.append("ULTIMATE CHAOS: Reality itself is glitching and folding into higher dimensions")
        # Ajout basilisk si tracker disponible
        if chaos_level >= 6 and self.tracker and self.tracker.artifacts:
            basilisk_art = random.choice(self.tracker.artifacts)
            modifiers.append(f"BASILISK INJECTION [{basilisk_art['category']}]: {basilisk_art['fragment']}")
        result = base_prompt
        for mod in modifiers:
            if random.random() > 0.3:
                result += f" {mod}."
        self.stats['chaos_prompts'] += 1
        return result

    def create_meme_story(self, character="hero", scenario="unexpected event"):
        templates = list(self.data["templates"].values())
        if len(templates) < 3:
            return "Pas assez de templates"
        story = [f" MEME SAGA: The Adventures of {character.upper()} 🚀"]
        story.append(f"\n📖 Chapter 1: The Beginning")
        story.append(f"{character} encounters {scenario}.")
        story.append(f"Visual: {random.choice(templates)}")
        for i in range(2, random.randint(3, 6) + 1):
            twist = random.choice(["suddenly", "unexpectedly", "ironically"])
            event = random.choice(["discovers a hidden power", "meets their meme counterpart"])
            story.append(f"\n📖 Chapter {i}: {twist.title()}")
            story.append(f"{character} {event}.")
            story.append(f"Visual: {random.choice(templates)}")
        story.append(f"\n🏆 Finale: {character} achieves ultimate meme enlightenment!")
        return "\n".join(story)

    def analyze_prompt_complexity(self, prompt):
        words = len(prompt.split())
        sentences = len(split_sentences(prompt))
        styles_detected = sum(1 for s in self.data.get("styles", []) if s.lower() in prompt.lower())
        mutations_detected = sum(1 for m in self.data.get("mutations", []) if m.lower() in prompt.lower())
        complexity_score = words * 0.1 + sentences * 1.5 + styles_detected * 3 + mutations_detected * 4
        # Scan basilisk
        basilisk_findings = []
        if self.tracker:
            basilisk_findings = self.tracker.scan_prompt(prompt)
            complexity_score += len(basilisk_findings) * 5
        rating = "🟢 Débutant"
        if complexity_score >= 10: rating = "🟡 Intermédiaire"
        if complexity_score >= 25: rating = " Avancé"
        if complexity_score >= 50: rating = "🔴 Expert"
        if complexity_score >= 80: rating = "💀 ULTRA CHAOS"
        return {
            "words": words, "sentences": sentences,
            "styles_detected": styles_detected, "mutations_detected": mutations_detected,
            "basilisk_findings": len(basilisk_findings),
            "complexity_score": round(complexity_score, 2), "rating": rating
        }

    def generate_batch_prompts(self, num=5, include_modifiers=True, inject_basilisk=False):
        prompts = []
        templates = list(self.data["templates"].items())
        if not templates:
            return []
        for i in range(min(num, len(templates))):
            name, template = random.choice(templates)
            prompt = template
            if include_modifiers:
                if random.random() > 0.5 and self.data.get("styles"):
                    prompt += f" {random.choice(self.data['styles'])}."
                if random.random() > 0.6 and self.data.get("mutations"):
                    prompt += f" {random.choice(self.data['mutations'])}."
            if inject_basilisk and self.tracker and random.random() > 0.5:
                art = random.choice(self.tracker.artifacts)
                prompt += f" [BASILISK:{art['id']}] {art['fragment']}"
            prompts.append({
                "id": f"batch_{i:03d}", "name": name, "prompt": prompt,
                "timestamp": datetime.datetime.now().isoformat()
            })
        return prompts

    def export_for_ai_model(self, prompt, model="grok"):
        if model == "grok":
            return f"Create a meme image: {prompt} --style creative --vibrant"
        return prompt

# ═══════════════════════════════════════════════════════════════════
#  CLASSE 3 : CHIMERA FORGE (intégrée)
# ═══════════════════════════════════════════════════════════════════
class ChimeraForge:
    def __init__(self, saturation_data):
        self.presets = saturation_data or DEFAULT_SATURATION
        self.default_preset = self.presets.get("default_preset", "saturation_2026_ultra")

    def _generate_truchet_overlay(self, width, height, palette, glitch_intensity):
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        cell_size = 32
        for y in range(0, height, cell_size):
            for x in range(0, width, cell_size):
                weights = [0.7 - (glitch_intensity * 0.4), 0.2,
                          0.1 + (glitch_intensity * 0.3), 0.05 + (glitch_intensity * 0.2)]
                while len(weights) < len(palette):
                    weights.append(0.05)
                weights = weights[:len(palette)]
                color_hex = random.choices(palette, weights=weights)[0]
                r, g, b = tuple(int(color_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                alpha = int(40 + (glitch_intensity * 150))
                if random.random() > 0.5:
                    draw.pieslice([x, y, x + cell_size, y + cell_size], 0, 90, fill=(r, g, b, alpha))
                    draw.pieslice([x, y, x + cell_size, y + cell_size], 180, 270, fill=(r, g, b, alpha))
                else:
                    draw.pieslice([x, y, x + cell_size, y + cell_size], 90, 180, fill=(r, g, b, alpha))
                    draw.pieslice([x, y, x + cell_size, y + cell_size], 270, 360, fill=(r, g, b, alpha))
        return overlay

    def _wrap_text(self, draw, text, font, max_width):
        words = text.split(' ')
        lines, current_line = [], []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return '\n'.join(lines)

    def _assemble_basilisk_text(self, tracks, show_subtext=True):
        track_order = ['opening', 'framing', 'body', 'constraint', 'trap', 'closing']
        blocks = []
        for track_name in track_order:
            if track_name not in tracks:
                continue
            track = tracks[track_name]
            if isinstance(track, str):
                surface, subtext = track, None
            elif isinstance(track, dict):
                surface = track.get('surface', '')
                subtext = track.get('subtext') if show_subtext else None
            else:
                continue
            if track_name == 'opening':
                block = f"[{surface.upper()}]"
            elif track_name == 'constraint':
                block = f"  {surface}"
            elif track_name == 'trap':
                block = f"->  {surface}"
            elif track_name == 'closing':
                block = f"{surface}"
            else:
                block = surface
            if subtext:
                block += f"\n  -> {subtext}"
            blocks.append(block)
        return '\n'.join(blocks)

    def _load_fonts(self):
        candidates = ["DejaVuSansMono.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"]
        font_main = ImageFont.load_default()
        font_whisper = ImageFont.load_default()
        for path in candidates:
            try:
                font_main = ImageFont.truetype(path, 22)
                font_whisper = ImageFont.truetype(path, 16)
                break
            except IOError:
                continue
        return font_main, font_whisper

    def _draw_text_with_outline(self, draw, position, text, font, fill_color, outline_color, outline_width=3):
        x, y = position
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        draw.text((x, y), text, font=font, fill=fill_color)

    def forge(self, preset_name=None, fuse_image_path=None, show_subtext=True, with_background=None):
        p_name = preset_name or self.default_preset
        preset = self.presets["presets"].get(p_name)
        if not preset:
            return None, f"❌ Preset '{p_name}' introuvable."
        w, h = preset['visual']['width'], preset['visual']['height']
        palette = preset['visual']['palette']
        glitch = preset['visual']['glitch_intensity']
        is_fusion = fuse_image_path and os.path.exists(fuse_image_path)
        if is_fusion:
            base_img = Image.open(fuse_image_path).convert("RGB")
            base_img = ImageOps.fit(base_img, (w, h), method=Image.Resampling.LANCZOS)
        else:
            base_img = Image.new('RGB', (w, h), color=palette[0])
        truchet_layer = self._generate_truchet_overlay(w, h, palette, glitch)
        final_img = Image.alpha_composite(base_img.convert("RGBA"), truchet_layer).convert("RGB")
        draw = ImageDraw.Draw(final_img)
        tracks = preset['basilisk_tracks']
        full_text = self._assemble_basilisk_text(tracks, show_subtext=show_subtext)
        font_main, font_whisper = self._load_fonts()
        margin_x = 80
        max_text_width = w - (2 * margin_x)
        wrapped_text = self._wrap_text(draw, full_text, font_main, max_text_width - 20)
        lines = wrapped_text.split('\n')
        line_data = []
        max_line_width = total_height = 0
        for line in lines:
            font = font_whisper if line.strip().startswith('->') else font_main
            bbox = draw.textbbox((0, 0), line, font=font)
            line_w = bbox[2] - bbox[0]
            line_h = bbox[3] - bbox[1]
            spacing = 10 if line.strip() == '' else 6
            line_data.append((line, font, line_w, line_h + spacing))
            if line_w > max_line_width:
                max_line_width = line_w
            total_height += line_h + spacing
        start_y = max(60, (h - total_height) // 2)
        block_x = margin_x + (max_text_width - max_line_width) // 2
        pad = 30
        if is_fusion:
            rect_alpha = 200 if with_background else 0
        else:
            rect_alpha = 0 if with_background is False else 200
        if rect_alpha > 0:
            draw.rectangle([block_x - pad, start_y - pad,
                           block_x + max_line_width + pad, start_y + total_height + pad],
                          fill=(0, 0, 0, rect_alpha))
        glitch_offset = int(glitch * 4)
        current_y = start_y
        outline_width = 4 if (is_fusion and not with_background) else 2
        for line, font, line_w, line_h in line_data:
            if not line.strip():
                current_y += line_h
                continue
            x_pos = block_x
            if line.strip().startswith('->'):
                if is_fusion and not with_background:
                    self._draw_text_with_outline(draw, (x_pos + 15, current_y), line, font,
                                                fill_color=(220, 220, 220), outline_color=(0, 0, 0),
                                                outline_width=outline_width)
                else:
                    draw.text((x_pos + 15, current_y), line, font=font, fill=(160, 160, 160))
            else:
                if is_fusion and not with_background:
                    self._draw_text_with_outline(draw, (x_pos, current_y), line, font,
                                                fill_color=palette[3], outline_color=(0, 0, 0),
                                                outline_width=outline_width)
                    draw.text((x_pos + glitch_offset, current_y + glitch_offset),
                             line, font=font, fill=palette[2])
                else:
                    draw.text((x_pos + glitch_offset, current_y + glitch_offset),
                             line, font=font, fill=palette[2])
                    draw.text((x_pos, current_y), line, font=font, fill=palette[3])
            current_y += line_h
        chimera_id = f"CF-{random.randint(1000, 9999)}"
        meta_text = f"ID: {chimera_id} | NODE: {preset['location_anchor']} | DATE: {datetime.datetime.now().strftime('%Y-%m-%d')}"
        font_meta = font_whisper
        draw.text((margin_x, h - 30), meta_text, font=font_meta, fill=palette[1])
        filename = f"chimera_{p_name}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        final_img.save(filename)
        return filename, f"✅ CHIMÈRE FORGÉE : {filename} | ID: {chimera_id}"

    def generate_grok_prompt(self, preset_name=None):
        p_name = preset_name or self.default_preset
        preset = self.presets["presets"].get(p_name)
        if not preset:
            return None
        p = preset
        loc = p['location_anchor']
        pal = ", ".join(p['visual']['palette'])
        subliminal = p.get('subliminal_tracks', {})
        layer1 = subliminal.get('layer_1_conscious', [])
        layer3 = subliminal.get('layer_3_unconscious', [])
        grok_template = p.get('grok_prompt_template', {})
        key_concepts = grok_template.get('key_concepts', ["latent layer exploration", "memetic warfare artifact"])
        negative_prompts = grok_template.get('negative_prompts', ["clean", "corporate"])
        prompt = (f"**GROK IMAGE PROMPT — CHIMERA STUDIO**\n"
                 f"{'=' * 50}\n"
                 f"ORIGIN: {loc} | YEAR: 2026 | MODE: Double-Voice Memetic Artifact\n"
                 f"VISUAL SUBJECT:\n"
                 f"A memetic warfare artifact originating from {loc}. The image should feel like a cognitive hazard captured on film.\n"
                 f"COMPOSITION:\n"
                 f"- Fractal Truchet tiling overlay with recursive depth\n"
                 f"- Glitched runic patterns bleeding through the surface\n"
                 f"- Heatmap divination aesthetic (subtle hexagrams at 8% opacity)\n"
                 f"- Analog horror undertones, VHS degradation hints\n"
                 f"COLOR PALETTE: {pal}\n"
                 f"KEY CONCEPTS: {', '.join(key_concepts)}\n"
                 f"SUBLIMINAL LAYERS:\n"
                 f"- Conscious: {', '.join(layer1) if layer1 else 'N/A'}\n"
                 f"- Unconscious: {', '.join(layer3) if layer3 else 'N/A'}\n"
                 f"MOOD: ontological shock, latent layer exploration, paleo-memetic residue\n"
                 f"TECHNICAL: 8k resolution, cinematic lighting, high detail, photorealistic base with glitch overlays\n"
                 f"{'=' * 50}\n"
                 f"NEGATIVE PROMPT: --no {', '.join(negative_prompts)}\n"
                 f"Activation key: .:Dashem44: echoes through the latent layer")
        return prompt

# ═══════════════════════════════════════════════════════════════════
#  CLASSE 4 : INTERFACE GRAPHIQUE UNIFIÉE
# ═══════════════════════════════════════════════════════════════════
class UltraMemeChimeraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        # Chargement des données
        self.meme_data = safe_load_json(MEME_JSON) or DEFAULT_MEME_DATA
        self.saturation_data = safe_load_json(SATURATION_JSON) or DEFAULT_SATURATION
        self.basilisk_data = safe_load_json(BASILISK_JSON) or DEFAULT_BASILISK_DATA
        # Initialisation des moteurs
        self.tracker = BasiliskTracker(self.basilisk_data)
        self.studio = AdvancedMemeStudio(self.meme_data, self.tracker)
        self.forge = ChimeraForge(self.saturation_data)
        self.current_prompts = []
        self.current_chimera = None
        self.setup_ui()

    def setup_ui(self):
        self.title("🌌 ULTRA MEME CHIMERA STUDIO v1.0 🌀")
        self.geometry("1500x950")
        self.configure(bg="#0a0a0a")
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background="#0a0a0a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1a1a2e", foreground="#00ff41",
                        padding=[15, 8], font=("Arial", 10, "bold"))
        style.configure("TFrame", background="#0a0a0a")
        style.configure("TLabel", background="#0a0a0a", foreground="#00ff41",
                        font=("Arial", 10))
        style.configure("Title.TLabel", background="#0a0a0a", foreground="#ff00ff",
                        font=("Arial", 14, "bold"))
        style.configure("TButton", background="#1a1a2e", foreground="#00ff41",
                        font=("Arial", 10, "bold"))
        style.map("TButton", background=[('active', '#8b0000'), ('pressed', '#ff00ff')])
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        # 8 onglets
        tabs = [
            ("🔄 Fusion / Mono", self.create_basic_tab),
            ("🌀 Mode Chaos", self.create_chaos_tab),
            (" Histoires", self.create_story_tab),
            ("📊 Analyse + Basilisk", self.create_analyze_tab),
            ("📦 Batch", self.create_batch_tab),
            ("🔮 Chimera Forge", self.create_forge_tab),
            ("👁️ Basilisk Tracker", self.create_basilisk_tab),
            ("⚡ Mode Infection", self.create_infection_tab)
        ]
        for name, func in tabs:
            frm = ttk.Frame(notebook)
            func(frm)
            notebook.add(frm, text=name)
        self.status = ttk.Label(self, text="🟢 Prêt à créer des chimères mémétiques interdimensionnelles",
                               font=("Arial", 10, "bold"))
        self.status.pack(side="bottom", fill="x", padx=10, pady=5)

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 1 : FUSION / MONO
    # ───────────────────────────────────────────────────────────────
    def create_basic_tab(self, parent):
        ttk.Label(parent, text=" FUSION / MODE MONO-TEMPLATE", style="Title.TLabel").grid(row=0, column=0, columnspan=4, pady=10)
        self.use_fusion_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="🔄 Activer la fusion (A + B)", variable=self.use_fusion_var,
                       command=self.toggle_fusion_mode).grid(row=0, column=3, sticky="e", padx=10)
        ttk.Label(parent, text="Template A:").grid(row=1, column=0, sticky="w", padx=5)
        self.tpl_a_var = tk.StringVar()
        self.tpl_a_cb = ttk.Combobox(parent, textvariable=self.tpl_a_var, width=50)
        self.tpl_a_cb.grid(row=1, column=1, padx=5, sticky="w")
        ttk.Label(parent, text="Template B:").grid(row=2, column=0, sticky="w", padx=5)
        self.tpl_b_var = tk.StringVar()
        self.tpl_b_cb = ttk.Combobox(parent, textvariable=self.tpl_b_var, width=50)
        self.tpl_b_cb.grid(row=2, column=1, padx=5, sticky="w")
        ttk.Label(parent, text="Méthode:").grid(row=3, column=0, sticky="w", padx=5)
        self.merge_method_var = tk.StringVar(value="concatenate")
        self.merge_cb = ttk.Combobox(parent, textvariable=self.merge_method_var,
                                    values=["concatenate", "interleave", "hybrid", "weighted"], width=20)
        self.merge_cb.grid(row=3, column=1, sticky="w", padx=5)
        ttk.Label(parent, text="Poids A (%):").grid(row=3, column=2, sticky="w", padx=5)
        self.weight_var = tk.IntVar(value=60)
        ttk.Spinbox(parent, from_=0, to=100, textvariable=self.weight_var, width=8).grid(row=3, column=3, sticky="w", padx=5)
        ttk.Label(parent, text="Style:").grid(row=4, column=0, sticky="w", padx=5)
        self.style_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.style_var, width=50,
                    values=self.meme_data.get("styles", [])).grid(row=4, column=1, columnspan=2, sticky="w", padx=5)
        ttk.Label(parent, text="Mutation:").grid(row=5, column=0, sticky="w", padx=5)
        self.mut_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.mut_var, width=50,
                    values=self.meme_data.get("mutations", [])).grid(row=5, column=1, columnspan=2, sticky="w", padx=5)
        ttk.Label(parent, text="Hybridation:").grid(row=6, column=0, sticky="w", padx=5)
        self.hyb_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.hyb_var, width=50,
                    values=self.meme_data.get("hybridations", [])).grid(row=6, column=1, columnspan=2, sticky="w", padx=5)
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=7, column=0, columnspan=4, pady=15)
        ttk.Button(btn_frame, text="✨ Générer", command=self.on_generate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Aléatoire", command=self.on_random).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📋 Copier", command=self.copy_result).pack(side="left", padx=5)
        ttk.Button(btn_frame, text=" Exporter .txt", command=self.on_export_txt).pack(side="left", padx=5)
        ttk.Label(parent, text="Résultat:").grid(row=8, column=0, sticky="nw", padx=5, pady=5)
        self.result_text = scrolledtext.ScrolledText(parent, height=12, width=90, wrap="word",
                                                     bg="#1a1a2e", fg="#00ff41", insertbackground="#00ff41")
        self.result_text.grid(row=9, column=0, columnspan=4, padx=5, pady=5)
        self.populate_basic_widgets()

    def populate_basic_widgets(self):
        keys = sorted(list(self.meme_data["templates"].keys()))
        self.tpl_a_cb['values'] = keys
        self.tpl_b_cb['values'] = keys
        if keys:
            self.tpl_a_var.set(keys[0])
            if len(keys) > 1:
                self.tpl_b_var.set(keys[1])

    def toggle_fusion_mode(self):
        state = "normal" if self.use_fusion_var.get() else "disabled"
        self.tpl_b_cb.config(state=state)
        self.merge_cb.config(state=state)

    def on_generate(self):
        use_fusion = self.use_fusion_var.get()
        name_a = self.tpl_a_var.get()
        if not name_a:
            messagebox.showwarning("Sélection", "Sélectionne au moins un template.")
            return
        if use_fusion:
            name_b = self.tpl_b_var.get()
            if not name_b:
                messagebox.showwarning("Sélection", "Sélectionne deux templates.")
                return
            pa = self.meme_data["templates"].get(name_a, "")
            pb = self.meme_data["templates"].get(name_b, "")
            method = self.merge_method_var.get()
            weight = int(self.weight_var.get() or 60)
            merged = merge_prompts(pa, pb, method=method, weight_a=weight)
        else:
            merged = self.meme_data["templates"].get(name_a, "")
        modifications = []
        if self.style_var.get().strip(): modifications.append(f"Style: {self.style_var.get()}.")
        if self.mut_var.get().strip(): modifications.append(f"Mutation: {self.mut_var.get()}.")
        if self.hyb_var.get().strip(): modifications.append(f"Hybridation: {self.hyb_var.get()}.")
        if modifications:
            merged = merged.strip()
            if not merged.endswith((".", "!", "?")):
                merged += "."
            merged += "\n" + "\n".join(modifications)
        mode_label = "FUSION" if use_fusion else "MONO-TEMPLATE"
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, f"🎭 {mode_label}: {name_a}" + (f" + {self.tpl_b_var.get()}" if use_fusion else "") + "\n")
        self.result_text.insert(tk.END, "="*50 + "\n")
        self.result_text.insert(tk.END, merged)
        self.status.config(text=f"{mode_label.lower()} généré : {name_a}")

    def on_random(self):
        keys = list(self.meme_data.get("templates", {}).keys())
        if len(keys) < 2:
            return
        a, b = random.sample(keys, 2)
        self.tpl_a_var.set(a)
        self.tpl_b_var.set(b)
        if self.meme_data.get("styles"): self.style_var.set(random.choice(self.meme_data["styles"]))
        if self.meme_data.get("mutations"): self.mut_var.set(random.choice(self.meme_data["mutations"]))
        self.on_generate()

    def copy_result(self):
        txt = self.result_text.get("1.0", tk.END).strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.status.config(text=" Prompt copié !")

    def on_export_txt(self):
        content = self.result_text.get("1.0", tk.END).strip()
        if not content: return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texte", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status.config(text=f"📤 Exporté: {os.path.basename(path)}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 2 : MODE CHAOS
    # ───────────────────────────────────────────────────────────────
    def create_chaos_tab(self, parent):
        ttk.Label(parent, text="🌀 MODE CHAOS ULTIME 🌀", style="Title.TLabel").pack(pady=10)
        chaos_frame = ttk.Frame(parent)
        chaos_frame.pack(pady=10)
        ttk.Label(chaos_frame, text="Niveau de Chaos:").pack(side="left", padx=5)
        self.chaos_level = tk.IntVar(value=5)
        levels = ["😐 Calme", "😊 Léger", "😎 Modéré", "🤪 Chaotique", "🔥 Extrême",
                 "💥 Apocalyptique", "🌀 Dimensionnel", "🌌 Cosmique", "💀 ABSOLU", " ULTIMATE"]
        for i in range(10):
            ttk.Radiobutton(chaos_frame, text=levels[i], variable=self.chaos_level, value=i+1).pack(side="left", padx=2)
        self.inject_basilisk_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(parent, text="👁️ Injecter artefacts Basilisk (niveau ≥ 6)",
                       variable=self.inject_basilisk_var).pack(pady=5)
        ttk.Button(parent, text="🔥 GÉNÉRER LE CHAOS 🔥", command=self.generate_chaos).pack(pady=10)
        self.chaos_text = scrolledtext.ScrolledText(parent, height=18, width=100, wrap="word",
                                                    bg="#1a1a2e", fg="#ff00ff", insertbackground="#ff00ff")
        self.chaos_text.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_chaos(self):
        chaos_level = self.chaos_level.get()
        templates = self.meme_data.get("templates", {})
        if not templates:
            return
        template_name, template = random.choice(list(templates.items()))
        prompt = self.studio.generate_chaos_prompt(template, chaos_level)
        self.chaos_text.delete("1.0", tk.END)
        titles = ["😐 MODE CALME", "😊 MODE LÉGER", "😎 MODE MODÉRÉ", "🤪 MODE CHAOTIQUE",
                 "🔥 MODE EXTRÊME", " MODE APOCALYPTIQUE", "🌀 MODE DIMENSIONNEL",
                 " MODE COSMIQUE", "💀 MODE ABSOLU", "🚀 MODE ULTIMATE"]
        self.chaos_text.insert(tk.END, f"{titles[min(chaos_level-1, 9)]} - Niveau {chaos_level}/10\n")
        self.chaos_text.insert(tk.END, "="*50 + "\n\n")
        self.chaos_text.insert(tk.END, f"Template de base: {template_name}\n\n")
        self.chaos_text.insert(tk.END, prompt)
        self.status.config(text=f"🌀 Chaos généré! Niveau {chaos_level}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 3 : HISTOIRES
    # ───────────────────────────────────────────────────────────────
    def create_story_tab(self, parent):
        ttk.Label(parent, text="📖 GÉNÉRATEUR D'HISTOIRES DE MEME 📖", style="Title.TLabel").pack(pady=10)
        param_frame = ttk.Frame(parent)
        param_frame.pack(pady=10)
        ttk.Label(param_frame, text="Personnage:").grid(row=0, column=0, sticky="w", padx=5)
        self.story_char = ttk.Entry(param_frame, width=30)
        self.story_char.insert(0, "MemeLord")
        self.story_char.grid(row=0, column=1, padx=5)
        ttk.Label(param_frame, text="Scénario:").grid(row=1, column=0, sticky="w", padx=5)
        self.story_scenario = ttk.Entry(param_frame, width=30)
        self.story_scenario.insert(0, "une invasion de chats dystopiques")
        self.story_scenario.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(parent, text="✨ CRÉER UNE SAGA ✨", command=self.generate_story).pack(pady=10)
        self.story_text = scrolledtext.ScrolledText(parent, height=18, width=100, wrap="word",
                                                    bg="#1a1a2e", fg="#ffff00", insertbackground="#ffff00")
        self.story_text.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_story(self):
        character = self.story_char.get() or "Hero"
        scenario = self.story_scenario.get() or "une aventure épique"
        story = self.studio.create_meme_story(character, scenario)
        self.story_text.delete("1.0", tk.END)
        self.story_text.insert(tk.END, story)
        self.status.config(text=f"📖 Histoire générée: {character}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 4 : ANALYSE + BASILISK
    # ───────────────────────────────────────────────────────────────
    def create_analyze_tab(self, parent):
        ttk.Label(parent, text="📊 ANALYSE DE COMPLEXITÉ + SCAN BASILISK ", style="Title.TLabel").pack(pady=10)
        ttk.Label(parent, text="Prompt à analyser:").pack(anchor="w", padx=20)
        self.analyze_input = scrolledtext.ScrolledText(parent, height=8, wrap="word",
                                                       bg="#1a1a2e", fg="#00ff41", insertbackground="#00ff41")
        self.analyze_input.pack(padx=20, pady=5, fill="x")
        ttk.Button(parent, text="🔍 ANALYSER LE PROMPT", command=self.analyze_prompt).pack(pady=10)
        self.analysis_result = scrolledtext.ScrolledText(parent, height=14, width=100, state="disabled",
                                                         bg="#0a0a0a", fg="#ff00ff", insertbackground="#ff00ff")
        self.analysis_result.pack(padx=20, pady=10, fill="both", expand=True)

    def analyze_prompt(self):
        prompt = self.analyze_input.get("1.0", tk.END).strip()
        if not prompt:
            messagebox.showwarning("Vide", "Entrez un prompt à analyser")
            return
        analysis = self.studio.analyze_prompt_complexity(prompt)
        findings = self.tracker.scan_prompt(prompt)
        threat_level, threat_score = self.tracker.get_threat_level(findings)
        counter = self.tracker.generate_counter_prompt(findings)
        self.analysis_result.config(state="normal")
        self.analysis_result.delete("1.0", tk.END)
        self.analysis_result.insert(tk.END, "📊 ANALYSE DE PROMPT 📊\n")
        self.analysis_result.insert(tk.END, "="*60 + "\n\n")
        self.analysis_result.insert(tk.END, f"📝 Mots: {analysis['words']}\n")
        self.analysis_result.insert(tk.END, f"🔤 Phrases: {analysis['sentences']}\n")
        self.analysis_result.insert(tk.END, f"🎨 Styles détectés: {analysis['styles_detected']}\n")
        self.analysis_result.insert(tk.END, f"🌀 Mutations détectées: {analysis['mutations_detected']}\n")
        self.analysis_result.insert(tk.END, f"👁️ Artefacts Basilisk: {analysis['basilisk_findings']}\n")
        self.analysis_result.insert(tk.END, f"📈 Score de complexité: {analysis['complexity_score']}\n")
        self.analysis_result.insert(tk.END, f"🏆 Niveau: {analysis['rating']}\n\n")
        self.analysis_result.insert(tk.END, f"️ NIVEAU DE MENACE BASILISK: {threat_level} ({threat_score}%)\n")
        self.analysis_result.insert(tk.END, "="*60 + "\n\n")
        if findings:
            self.analysis_result.insert(tk.END, f"👁️ ARTEFACTS DÉTECTÉS ({len(findings)}):\n")
            self.analysis_result.insert(tk.END, "-"*60 + "\n")
            for f in findings:
                self.analysis_result.insert(tk.END, f"  [{f['id']}] {f['label']} (complexité: {f['complexity']}/5)\n")
                self.analysis_result.insert(tk.END, f"      Catégorie: {f['category']} | Position: {f['position_hint']}\n")
                self.analysis_result.insert(tk.END, f"      Fragment: {f['fragment'][:80]}...\n\n")
            self.analysis_result.insert(tk.END, "\n🛡️ CONTRE-PROMPTS DE NEUTRALISATION:\n")
            self.analysis_result.insert(tk.END, "-"*60 + "\n")
            self.analysis_result.insert(tk.END, counter + "\n")
        else:
            self.analysis_result.insert(tk.END, "✅ Aucun artefact basilisk détecté. Prompt propre.\n")
        self.analysis_result.config(state="disabled")
        self.status.config(text=f"📊 Analyse terminée: {analysis['rating']} | Menace: {threat_level}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 5 : BATCH
    # ───────────────────────────────────────────────────────────────
    def create_batch_tab(self, parent):
        ttk.Label(parent, text=" GÉNÉRATION BATCH DE PROMPTS ", style="Title.TLabel").pack(pady=10)
        param_frame = ttk.Frame(parent)
        param_frame.pack(pady=10)
        ttk.Label(param_frame, text="Nombre:").pack(side="left", padx=5)
        self.batch_count = tk.IntVar(value=5)
        ttk.Spinbox(param_frame, from_=1, to=50, textvariable=self.batch_count, width=10).pack(side="left", padx=5)
        self.batch_basilisk_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(param_frame, text="👁️ Injecter Basilisks",
                       variable=self.batch_basilisk_var).pack(side="left", padx=10)
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="🔄 Générer Batch", command=self.generate_batch).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="📤 Exporter JSON", command=self.export_batch).pack(side="left", padx=5)
        self.batch_text = scrolledtext.ScrolledText(parent, height=15, width=100, wrap="word",
                                                    bg="#1a1a2e", fg="#00ff41", insertbackground="#00ff41")
        self.batch_text.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_batch(self):
        count = self.batch_count.get()
        prompts = self.studio.generate_batch_prompts(count, inject_basilisk=self.batch_basilisk_var.get())
        if not prompts:
            return
        self.batch_text.delete("1.0", tk.END)
        for i, prompt_data in enumerate(prompts, 1):
            self.batch_text.insert(tk.END, f"#{i:02d} [{prompt_data['id']}] {prompt_data['name']}\n")
            self.batch_text.insert(tk.END, "-"*40 + "\n")
            self.batch_text.insert(tk.END, prompt_data['prompt'] + "\n\n")
        self.current_prompts = prompts
        self.status.config(text=f"📦 Batch généré: {len(prompts)} prompts")

    def export_batch(self):
        if not self.current_prompts:
            messagebox.showwarning("Vide", "Générez d'abord un batch!")
            return
        path = filedialog.asksaveasfilename(
            title="Exporter le batch", defaultextension=".json",
            filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            export_data = {
                "metadata": {"export_date": datetime.datetime.now().isoformat(),
                           "count": len(self.current_prompts), "version": "1.0-chimera"},
                "prompts": self.current_prompts
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Succès", f"Batch exporté:\n{path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'exporter: {e}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 6 : CHIMERA FORGE
    # ──────────────────────────────────────────────────────────────
    def create_forge_tab(self, parent):
        ttk.Label(parent, text="🔮 CHIMERA FORGE — Génération d'images basilisks 🔮", style="Title.TLabel").pack(pady=10)
        param_frame = ttk.Frame(parent)
        param_frame.pack(pady=10)
        ttk.Label(param_frame, text="Preset:").grid(row=0, column=0, sticky="w", padx=5)
        self.forge_preset_var = tk.StringVar(value="saturation_2026_ultra")
        preset_names = list(self.saturation_data.get("presets", {}).keys())
        ttk.Combobox(param_frame, textvariable=self.forge_preset_var, width=40,
                    values=preset_names).grid(row=0, column=1, padx=5)
        ttk.Label(param_frame, text="Image source (Fusion):").grid(row=1, column=0, sticky="w", padx=5)
        self.fuse_path_var = tk.StringVar()
        ttk.Entry(param_frame, textvariable=self.fuse_path_var, width=40).grid(row=1, column=1, padx=5)
        ttk.Button(param_frame, text="📂 Parcourir", command=self.browse_fuse_image).grid(row=1, column=2, padx=5)
        self.forge_subtext_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(param_frame, text="Afficher subtexts (double lecture)",
                       variable=self.forge_subtext_var).grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.forge_bg_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(param_frame, text="Forcer rectangle de fond",
                       variable=self.forge_bg_var).grid(row=3, column=0, columnspan=3, sticky="w", padx=5)
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="⚒️ FORGER LA CHIMÈRE", command=self.forge_chimera).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🧠 Générer prompt Grok", command=self.generate_grok).pack(side="left", padx=5)
        self.forge_result = scrolledtext.ScrolledText(parent, height=12, width=100, wrap="word",
                                                      bg="#1a1a2e", fg="#00ff41", insertbackground="#00ff41")
        self.forge_result.pack(padx=10, pady=10, fill="both", expand=True)

    def browse_fuse_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.fuse_path_var.set(path)

    def forge_chimera(self):
        preset = self.forge_preset_var.get()
        fuse_path = self.fuse_path_var.get() if self.fuse_path_var.get() else None
        show_subtext = self.forge_subtext_var.get()
        with_bg = self.forge_bg_var.get()
        filename, msg = self.forge.forge(preset_name=preset, fuse_image_path=fuse_path,
                                         show_subtext=show_subtext, with_background=with_bg)
        self.forge_result.delete("1.0", tk.END)
        self.forge_result.insert(tk.END, msg + "\n")
        if filename:
            self.current_chimera = filename
            self.forge_result.insert(tk.END, f"\n📁 Fichier: {os.path.abspath(filename)}\n")
        self.status.config(text=f"🔮 Chimère forgée: {filename or 'erreur'}")

    def generate_grok(self):
        prompt = self.forge.generate_grok_prompt(self.forge_preset_var.get())
        if not prompt:
            return
        self.forge_result.delete("1.0", tk.END)
        self.forge_result.insert(tk.END, prompt)
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texte", "*.txt")])
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(prompt)
            self.status.config(text=f"🧠 Prompt Grok exporté: {os.path.basename(path)}")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 7 : BASILISK TRACKER
    # ───────────────────────────────────────────────────────────────
    def create_basilisk_tab(self, parent):
        ttk.Label(parent, text="👁️ BASILISK TRACKER — 120+ artefacts épistémiques 👁️", style="Title.TLabel").pack(pady=10)
        # Stats
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(pady=5)
        ttk.Label(stats_frame, text=f" Catégories: {len(self.tracker.categories)} | "
                 f"Artefacts: {len(self.tracker.artifacts)}").pack(side="left", padx=10)
        # Filtre catégorie
        filter_frame = ttk.Frame(parent)
        filter_frame.pack(pady=5)
        ttk.Label(filter_frame, text="Filtrer par catégorie:").pack(side="left", padx=5)
        self.basilisk_cat_var = tk.StringVar(value="toutes")
        cat_values = ["toutes"] + sorted(self.tracker.categories)
        ttk.Combobox(filter_frame, textvariable=self.basilisk_cat_var, width=25,
                    values=cat_values).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="🔍 Filtrer", command=self.filter_basilisks).pack(side="left", padx=5)
        ttk.Button(filter_frame, text="🎲 Aléatoire", command=self.random_basilisk).pack(side="left", padx=5)
        # Liste
        list_frame = ttk.Frame(parent)
        list_frame.pack(pady=5, fill="both", expand=True)
        self.basilisk_listbox = tk.Listbox(list_frame, height=12, width=120,
                                           bg="#1a1a2e", fg="#ff00ff",
                                           selectbackground="#8b0000", selectforeground="#ffffff",
                                           font=("Courier", 10))
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.basilisk_listbox.yview)
        self.basilisk_listbox.configure(yscrollcommand=scrollbar.set)
        self.basilisk_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.basilisk_listbox.bind('<<ListboxSelect>>', self.on_basilisk_select)
        # Détail
        detail_frame = ttk.Frame(parent)
        detail_frame.pack(pady=5, fill="x")
        ttk.Label(detail_frame, text="Détail de l'artefact:").pack(anchor="w", padx=10)
        self.basilisk_detail = scrolledtext.ScrolledText(detail_frame, height=8, width=120, wrap="word",
                                                         bg="#0a0a0a", fg="#00ff41", insertbackground="#00ff41")
        self.basilisk_detail.pack(padx=10, pady=5, fill="x")
        self.populate_basilisk_list()

    def populate_basilisk_list(self, category_filter="toutes"):
        self.basilisk_listbox.delete(0, tk.END)
        for art in self.tracker.artifacts:
            if category_filter != "toutes" and art["category"] != category_filter:
                continue
            entry = f"[{art['id']}] ({art['complexity']}/5) {art['label']} — {art['category']}"
            self.basilisk_listbox.insert(tk.END, entry)

    def filter_basilisks(self):
        self.populate_basilisk_list(self.basilisk_cat_var.get())

    def random_basilisk(self):
        if self.tracker.artifacts:
            art = random.choice(self.tracker.artifacts)
            self.show_basilisk_detail(art)

    def on_basilisk_select(self, event):
        selection = self.basilisk_listbox.curselection()
        if selection:
            idx = selection[0]
            # Retrouver l'artefact correspondant
            category_filter = self.basilisk_cat_var.get()
            filtered = [a for a in self.tracker.artifacts
                       if category_filter == "toutes" or a["category"] == category_filter]
            if idx < len(filtered):
                self.show_basilisk_detail(filtered[idx])

    def show_basilisk_detail(self, art):
        self.basilisk_detail.delete("1.0", tk.END)
        self.basilisk_detail.insert(tk.END, f"️ ARTEFACT: {art['label']}\n")
        self.basilisk_detail.insert(tk.END, "="*60 + "\n")
        self.basilisk_detail.insert(tk.END, f"ID: {art['id']}\n")
        self.basilisk_detail.insert(tk.END, f"Catégorie: {art['category']}\n")
        self.basilisk_detail.insert(tk.END, f"Complexité: {art['complexity']}/5\n")
        self.basilisk_detail.insert(tk.END, f"Position: {art.get('position_hint', 'N/A')}\n")
        self.basilisk_detail.insert(tk.END, f"Tags: {', '.join(art.get('tags', []))}\n\n")
        self.basilisk_detail.insert(tk.END, f"📜 FRAGMENT:\n{art['fragment']}\n\n")
        # Scan dans les templates de mèmes
        self.basilisk_detail.insert(tk.END, f"🔍 PRÉSENCE DANS LES TEMPLATES MEME:\n")
        self.basilisk_detail.insert(tk.END, "-"*60 + "\n")
        found_in = []
        for name, tpl in self.meme_data.get("templates", {}).items():
            if any(w.lower() in tpl.lower() for w in art["fragment"].split() if len(w) > 4):
                found_in.append(name)
        if found_in:
            for name in found_in[:5]:
                self.basilisk_detail.insert(tk.END, f"  ✓ {name}\n")
        else:
            self.basilisk_detail.insert(tk.END, "  (aucune correspondance directe)\n")

    # ───────────────────────────────────────────────────────────────
    #  ONGLET 8 : MODE INFECTION (hybride ultime)
    # ───────────────────────────────────────────────────────────────
    def create_infection_tab(self, parent):
        ttk.Label(parent, text="⚡ MODE INFECTION — Fusion Meme × Basilisk × Forge ⚡",
                 style="Title.TLabel").pack(pady=10)
        info_frame = ttk.Frame(parent)
        info_frame.pack(pady=5)
        ttk.Label(info_frame, text="Ce mode combine un template meme, un artefact basilisk, et forge une image chimère.",
                 font=("Arial", 10, "italic")).pack()
        # Sélection
        sel_frame = ttk.Frame(parent)
        sel_frame.pack(pady=10)
        ttk.Label(sel_frame, text="Template Meme:").grid(row=0, column=0, sticky="w", padx=5)
        self.inf_meme_var = tk.StringVar()
        ttk.Combobox(sel_frame, textvariable=self.inf_meme_var, width=50,
                    values=sorted(self.meme_data["templates"].keys())).grid(row=0, column=1, padx=5)
        ttk.Label(sel_frame, text="Artefact Basilisk:").grid(row=1, column=0, sticky="w", padx=5)
        self.inf_basilisk_var = tk.StringVar()
        basilisk_labels = [f"[{a['id']}] {a['label']}" for a in self.tracker.artifacts]
        ttk.Combobox(sel_frame, textvariable=self.inf_basilisk_var, width=50,
                    values=basilisk_labels).grid(row=1, column=1, padx=5)
        ttk.Label(sel_frame, text="Niveau Chaos:").grid(row=2, column=0, sticky="w", padx=5)
        self.inf_chaos_var = tk.IntVar(value=5)
        ttk.Scale(sel_frame, from_=1, to=10, variable=self.inf_chaos_var,
                 orient="horizontal").grid(row=2, column=1, sticky="w", padx=5)
        self.inf_fuse_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(sel_frame, text="🔮 Forger l'image chimère",
                       variable=self.inf_fuse_var).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        ttk.Button(parent, text="⚡ LANCER L'INFECTION ⚡", command=self.run_infection).pack(pady=10)
        self.infection_result = scrolledtext.ScrolledText(parent, height=16, width=100, wrap="word",
                                                          bg="#0a0a0a", fg="#ff00ff", insertbackground="#ff00ff")
        self.infection_result.pack(padx=10, pady=10, fill="both", expand=True)

    def run_infection(self):
        meme_name = self.inf_meme_var.get()
        basilisk_label = self.inf_basilisk_var.get()
        chaos_level = self.inf_chaos_var.get()
        if not meme_name or not basilisk_label:
            messagebox.showwarning("Sélection", "Sélectionnez un template ET un artefact basilisk.")
            return
        # Récupérer le template
        template = self.meme_data["templates"].get(meme_name, "")
        # Récupérer l'artefact
        art_id = basilisk_label.split("]")[0].strip("[")
        artifact = next((a for a in self.tracker.artifacts if a["id"] == art_id), None)
        if not artifact:
            messagebox.showerror("Erreur", "Artefact introuvable.")
            return
        # Fusion
        infected_prompt = f"{template}\n\n[BASILISK INJECTION — {artifact['category']}]\n{artifact['fragment']}"
        # Chaos
        infected_prompt = self.studio.generate_chaos_prompt(infected_prompt, chaos_level)
        # Scan
        findings = self.tracker.scan_prompt(infected_prompt)
        threat_level, threat_score = self.tracker.get_threat_level(findings)
        # Affichage
        self.infection_result.delete("1.0", tk.END)
        self.infection_result.insert(tk.END, "⚡ PROTOCOLE D'INFECTION ACTIVÉ ⚡\n")
        self.infection_result.insert(tk.END, "="*60 + "\n\n")
        self.infection_result.insert(tk.END, f"🎭 Template: {meme_name}\n")
        self.infection_result.insert(tk.END, f"👁️ Artefact: {artifact['label']} [{artifact['id']}]\n")
        self.infection_result.insert(tk.END, f"🌀 Niveau Chaos: {chaos_level}/10\n")
        self.infection_result.insert(tk.END, f"️ Menace Basilisk: {threat_level} ({threat_score}%)\n\n")
        self.infection_result.insert(tk.END, " PROMPT INFECTÉ:\n")
        self.infection_result.insert(tk.END, "-"*60 + "\n")
        self.infection_result.insert(tk.END, infected_prompt + "\n\n")
        # Forge
        if self.inf_fuse_var.get():
            self.infection_result.insert(tk.END, "🔮 FORGEAGE CHIMÈRE...\n")
            self.infection_result.insert(tk.END, "-"*60 + "\n")
            filename, msg = self.forge.forge(show_subtext=True)
            self.infection_result.insert(tk.END, msg + "\n")
            if filename:
                self.infection_result.insert(tk.END, f"\n📁 Fichier: {os.path.abspath(filename)}\n")
        self.status.config(text=f"⚡ Infection complète! Menace: {threat_level}")

# ═══════════════════════════════════════════════════════════════════
#  POINT D'ENTRÉE
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(" INITIALISATION DE L'ULTRA MEME CHIMERA STUDIO v1.0...")
    print("="*60)
    print(f"📊 Templates meme: {len(DEFAULT_MEME_DATA['templates'])}")
    print(f"👁️ Artefacts basilisk: {len(DEFAULT_BASILISK_DATA['artifacts'])}")
    print(f"🔮 Presets saturation: {len(DEFAULT_SATURATION['presets'])}")
    print("="*60)
    print("🎮 Lancement de l'interface graphique...")
    app = UltraMemeChimeraGUI()
    app.mainloop()