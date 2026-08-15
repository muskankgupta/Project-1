"""
llm_service.py

Optional business-friendly response synthesis layer.

The service uses an external LLM provider only when credentials are present.
Otherwise it falls back to a deterministic summary so the backend remains
usable and testable without cloud keys.
"""

from __future__ import annotations

import json
import logging
import os
import re
import urllib.parse
import urllib.request
from typing import Any

from loader import SemanticLoader, get_semantic_loader


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Google Gemini provider
#
# Implemented against the public Generative Language REST API using only the
# Python standard library (urllib). This keeps Gemini support dependency-free
# and mirrors the codebase's "optional provider, graceful fallback" pattern.
#
# The provider only activates when a GEMINI_API_KEY is present. If the key is
# missing, the network request fails, or the API returns an error, we fall
# back to the deterministic executive summary exactly like the other providers.
# No secrets are ever hardcoded -- the key always comes from the environment.
# ---------------------------------------------------------------------------

GEMINI_REST_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "{model}:generateContent"
)


class GeminiClient:
    """Thin REST client for Google Gemini generateContent (std-lib only)."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("Gemini api_key is required.")
        self.api_key = api_key
        self.default_model = "gemini-1.5-flash"

    def generate_content(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model: str | None = None,
        temperature: float = 0.2,
    ) -> str:
        selected_model = model or self.default_model
        url = GEMINI_REST_URL.format(model=selected_model)
        url = f"{url}?key={urllib.parse.quote(self.api_key, safe='')}"

        system_block: list[dict[str, Any]] = []
        if system_prompt:
            system_block = [
                {
                    "text": system_prompt,
                }
            ]

        payload: dict[str, Any] = {
            "system_instruction": {"parts": system_block} if system_block else None,
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}],
                }
            ],
            "generationConfig": {
                "temperature": temperature,
            },
        }

        if not system_block:
            payload.pop("system_instruction", None)

        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))

        candidates = body.get("candidates") or []
        if not candidates:
            return ""
        parts = candidates[0].get("content", {}).get("parts") or []
        texts: list[str] = []
        for part in parts:
            text = part.get("text")
            if text:
                texts.append(str(text))
        return "\n".join(texts).strip()


class LLMService:
    def __init__(self, semantic_loader: SemanticLoader | None = None) -> None:
        self.semantic = semantic_loader or get_semantic_loader()
        self.provider = self._detect_provider()
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    def _detect_provider(self) -> str:
        """Return the configured LLM provider.

        Gemini is the only external provider. It activates when a
        GEMINI_API_KEY is present in the environment. When no key is
        configured we fall back to the deterministic executive summary.
        """
        if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY").strip():
            return "gemini"

        return "fallback"

    def generate(self, context: dict[str, Any]) -> dict[str, Any]:
        prompt = self._build_prompt(context)

        if self.provider == "gemini":
            try:
                client = GeminiClient(os.getenv("GEMINI_API_KEY") or "")
                text = client.generate_content(
                    self._system_prompt(),
                    prompt,
                    model=self.gemini_model,
                    temperature=0.2,
                )
                return {"provider": "gemini", "model": self.gemini_model, "text": text}
            except Exception as exc:  # pragma: no cover - provider runtime path
                logger.exception("Gemini response generation failed.")
                return {"provider": "fallback", "model": None, "text": self._fallback_text(context, str(exc))}

        return {"provider": "fallback", "model": None, "text": self._fallback_text(context)}

    def _system_prompt(self) -> str:
        return (
            "You are the business explanation layer for an analytics assistant. "
            "Summarize the final answer clearly and concisely. Do not change the computed values, "
            "invent missing data, or bypass the semantic, SQL, and reasoning layers."
        )

    def _build_prompt(self, context: dict[str, Any]) -> str:
        return (
            f"User question: {context.get('question', '')}\n"
            f"Rewritten question: {context.get('rewritten_question', '')}\n"
            f"Answer: {context.get('answer', '')}\n"
            f"Insights: {context.get('insights', [])}\n"
            f"Explanation: {context.get('explanation', '')}\n"
            f"Chart: {context.get('chart', '')}\n"
            f"SQL: {context.get('sql', '')}"
        )

    def _fallback_text(self, context: dict[str, Any], error: str | None = None) -> str:
        if error:
            # The provider was configured but the call failed (e.g. quota/billing).
            return self._executive_summary(context) + (
                f"\n\n[Live LLM unavailable — the provider call failed ({error}). "
                "Showing deterministic fallback.]"
            )

        if self.provider == "fallback":
            return self._executive_summary(context) + (
                "\n\n[Live LLM unavailable — no credentials configured. Showing deterministic fallback.]"
            )

        return self._executive_summary(context)

    # ------------------------------------------------------------------
    # Deterministic, executive-style narrative (no external provider)
    # ------------------------------------------------------------------
    def _executive_summary(self, context: dict[str, Any]) -> str:
        """Compose a business-grade narrative from the answer + insights.

        Produces concise executive framing such as:
        "Total revenue reached ₹7.18 Cr. Maharashtra contributed the highest
        share, indicating strong regional performance."
        """
        answer = context.get("answer", "") or ""
        insights = context.get("insights", []) or []
        explanation = context.get("explanation", "") or ""
        chart = context.get("chart", "") or ""

        story: list[str] = []

        headline = self._synth_answer_headline(answer)
        if headline:
            story.append(headline)

        for insight in insights:
            stripped = str(insight).strip()
            if not stripped:
                continue
            enriched = self._executive_insight(stripped)
            if enriched:
                story.append(enriched)

        if explanation and len(story) < 4:
            story.append(str(explanation).strip())

        if chart and chart != "No chart recommended." and len(story) < 5:
            story.append(f"Recommended visual: {chart}.")

        return " ".join(story).strip() or "No LLM response available."

    def _synth_answer_headline(self, answer: str) -> str:
        """Turn a flat answer string into a short executive headline."""
        if not answer or not answer.strip():
            return ""

        text = answer.strip()
        rupee_value = self._extract_inr_value(text)

        if rupee_value is not None:
            cr = rupee_value / 100_000_00
            # Context-like phrasing using the question if present.
            topic = self._topic_from_text(text) or "metric"
            if cr >= 1:
                return (
                    f"Total {topic} reached ₹{cr:.2f} Cr "
                    f"(₹{rupee_value:,.0f}), reflecting overall business scale."
                )
            if cr >= 0.01:
                return f"Total {topic} came to ₹{cr:.2f} Cr (₹{rupee_value:,.0f})."
            return f"Total {topic} was ₹{rupee_value:,.0f}."

        if text:
            return text

        return ""

    def _executive_insight(self, insight: str) -> str | None:
        """Turn an insight line into executive-framed language where detectable."""
        low = insight.lower()
        if "highest" in low or "top 3" in low or "contributes" in low or "top" in low:
            return f"{insight.rstrip('.')}, indicating a notable concentration driver."
        if "lowest" in low:
            return f"{insight.rstrip('.')}, highlighting an area for potential attention."
        if text := re.search(r"^\d+\.\d+%", insight):
            return f"{insight.rstrip('.')} in share terms."
        return None

    def _extract_inr_value(self, text: str) -> float | None:
        """Extract the leading large INR amount (e.g. '71,810,565.00') from a string."""
        match = re.search(r"\d{1,3}(?:,\d{3})+|\d+", text)
        if not match:
            return None
        try:
            return float(match.group(0).replace(",", ""))
        except ValueError:
            return None

    def _topic_from_text(self, text: str) -> str:
        """Best-effort topic label (revenue / sales / order / value)."""
        low = text.lower()
        if "revenue" in low or "sales" in low or "amount" in low:
            return "revenue"
        if "order" in low:
            return "order count"
        if "unit" in low or "value" in low:
            return "value"
        return "metric"
