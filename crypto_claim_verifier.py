# v0.2.16
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import json


class CryptoClaimVerifier(gl.Contract):
    last_url: str
    last_claim: str
    last_result: str

    def __init__(self):
        self.last_url = ""
        self.last_claim = ""
        self.last_result = "NOT_VERIFIED"

    @gl.public.write
    def verify_claim(self, url: str, claim: str) -> None:

        def analyze_source() -> str:
            page = gl.nondet.web.render(url, mode="text")

            prompt = f"""
You are an evidence verification engine.

Evaluate the CLAIM using ONLY the SOURCE CONTENT below.

CLAIM:
{claim}

SOURCE CONTENT:
{page}

Classify the claim as exactly one of:

SUPPORTED
CONTRADICTED
INCONCLUSIVE

Rules:
- SUPPORTED only when the source provides clear evidence for the claim.
- CONTRADICTED only when the source provides clear evidence against the claim.
- INCONCLUSIVE when evidence is missing, ambiguous, or insufficient.
- Do not use outside knowledge.
- Do not guess.

Return valid JSON only:

{{
  "verdict": "SUPPORTED | CONTRADICTED | INCONCLUSIVE",
  "reason": "brief explanation based only on the source"
}}
"""

            result = gl.nondet.exec_prompt(prompt)
            return result.replace("```json", "").replace("```", "").strip()

        result = gl.eq_principle.prompt_comparative(
            analyze_source,
            """
The verdict must agree on whether the supplied source supports,
contradicts, or provides insufficient evidence for the claim.
The reasoning may use different wording, but it must be grounded
only in the supplied source.
"""
        )

        parsed = json.loads(result)

        verdict = parsed["verdict"]

        if verdict not in [
            "SUPPORTED",
            "CONTRADICTED",
            "INCONCLUSIVE"
        ]:
            raise gl.UserError("Invalid verdict returned")

        self.last_url = url
        self.last_claim = claim
        self.last_result = verdict

    @gl.public.view
    def get_last_verification(self) -> str:
        return json.dumps({
            "url": self.last_url,
            "claim": self.last_claim,
            "verdict": self.last_result
        })
