"""Aura Core 0.1 — a tiny character-level language model trained from scratch.

This is a transparent proof of concept, not a general-purpose assistant.
The model learns character transitions from the bundled Czech corpus.
It uses only Python's standard library so it can run on modest cloud hosting.
"""
from __future__ import annotations
from collections import defaultdict, Counter
from pathlib import Path
import json
import random
import re

class AuraCore:
    engine_name = "Aura Core 0.1 · character n-gram"

    def __init__(self, data_dir: Path):
        self.data_dir = Path(data_dir)
        self.corpus_path = self.data_dir / "train.txt"
        self.model_path = self.data_dir / "aura_model.json"
        self.context = 3
        self.transitions = defaultdict(Counter)
        self.vocab = set(" ")
        self.trained = False
        self._load_corpus()
        if self.model_path.exists():
            try:
                self._load_model()
            except Exception:
                self.train()
        else:
            self.train()

    def _load_corpus(self):
        if not self.corpus_path.exists():
            self.corpus_path.write_text(
                "Ahoj. Jsem Aura AI, experimentální český jazykový model společnosti TG a.s.\\n",
                encoding="utf-8"
            )
        self.corpus = self.corpus_path.read_text(encoding="utf-8").strip()

    def train(self):
        self._load_corpus()
        self.transitions = defaultdict(Counter)
        text = (" " * self.context) + self.corpus.lower()
        self.vocab = set(text)
        for i in range(self.context, len(text)):
            ctx = text[i-self.context:i]
            self.transitions[ctx][text[i]] += 1
        serial = {k: dict(v) for k, v in self.transitions.items()}
        self.model_path.write_text(json.dumps({
            "context": self.context, "vocab": sorted(self.vocab),
            "transitions": serial
        }, ensure_ascii=False), encoding="utf-8")
        self.trained = True
        return {"ok": True, "message": "Aura Core byl natrénován na přiloženém textu.",
                "characters": len(self.corpus), "contexts": len(self.transitions),
                "note": "Jde o malý experimentální model; větší a kvalitnější korpus zlepší výsledky."}

    def _load_model(self):
        obj = json.loads(self.model_path.read_text(encoding="utf-8"))
        self.context = int(obj["context"])
        self.vocab = set(obj["vocab"])
        self.transitions = defaultdict(Counter, {
            k: Counter(v) for k, v in obj["transitions"].items()
        })
        self.trained = True

    def status(self):
        return {
            "name": "Aura AI",
            "engine": self.engine_name,
            "trained": self.trained,
            "corpus_characters": len(self.corpus),
            "learned_contexts": len(self.transitions),
            "mode": "cloud-ready"
        }

    def reply(self, prompt: str) -> str:
        if not self.trained:
            self.train()
        # Give the model a prompt-conditioned continuation. This is deliberately
        # character-level; it does not understand meaning like a modern LLM.
        seed = re.sub(r"\\s+", " ", prompt.lower()).strip()
        if not seed:
            seed = "ahoj"
        context = (" " * self.context + seed)[-self.context:]
        rng = random.Random()
        output = []
        for _ in range(220):
            choices = self.transitions.get(context)
            if not choices:
                # Back off to any learned context sharing the final character.
                candidates = [v for k, v in self.transitions.items()
                              if k[-1:] == context[-1:]]
                if not candidates:
                    break
                choices = Counter()
                for candidate in candidates:
                    choices.update(candidate)
            chars, weights = zip(*choices.items())
            nxt = rng.choices(chars, weights=weights, k=1)[0]
            output.append(nxt)
            context = (context + nxt)[-self.context:]
            if nxt in ".!?" and len(output) > 45:
                break
        result = "".join(output).strip()
        if len(result) < 8:
            result = "Zatím nemám dost naučených dat. Zkus mě nejprve natrénovat nebo rozšířit data/train.txt."
        return result[:500]
