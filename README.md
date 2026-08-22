# GenLayer Crypto Claim Verifier

An Intelligent Contract built on GenLayer that verifies claims against web sources using AI-powered consensus.

## Overview

Crypto Claim Verifier allows a user to provide:

- A web source URL
- A claim about the information contained in that source

The contract retrieves the source content and uses GenLayer's nondeterministic execution and consensus mechanisms to evaluate whether the supplied source supports the claim.

The result is classified as one of three possible verdicts:

- `SUPPORTED` — the source provides clear evidence supporting the claim.
- `CONTRADICTED` — the source provides clear evidence against the claim.
- `INCONCLUSIVE` — the available evidence is missing, ambiguous, or insufficient.

## Why GenLayer?

Traditional smart contracts cannot easily evaluate unstructured information from web pages or reason about natural-language claims.

GenLayer Intelligent Contracts make this possible by combining web access, AI-powered execution, and validator consensus.

This contract uses:

- `gl.nondet.web.render()` to retrieve web content.
- `gl.nondet.exec_prompt()` to analyze the source using an AI model.
- `gl.eq_principle.prompt_comparative()` to reach consensus on the resulting verdict.

The contract therefore does not rely on a single AI response. Validators evaluate the nondeterministic execution under an equivalence principle designed specifically for claim verification.

## How It Works

1. The user submits a URL and a claim.
2. The contract retrieves the web page as text.
3. An AI model evaluates the claim using only the supplied source.
4. The result is classified as `SUPPORTED`, `CONTRADICTED`, or `INCONCLUSIVE`.
5. GenLayer validators compare the outputs using the contract's equivalence principle.
6. After consensus, the final verdict is stored in the contract state.
7. The latest verification can be retrieved using `get_last_verification()`.

## Contract Methods

### `verify_claim(url, claim)`

Verifies a claim against the supplied web source.

**Inputs**

- `url` — URL of the source to analyze.
- `claim` — Natural-language claim to verify.

**Possible verdicts**

- `SUPPORTED`
- `CONTRADICTED`
- `INCONCLUSIVE`

### `get_last_verification()`

Returns the most recently finalized verification, including:

- Source URL
- Claim
- Verdict

## Example

Source:

`https://example.com/`

Claim:

`Example Domain is intended for use in illustrative examples in documents.`

Result:

```json
{
  "url": "https://example.com/",
  "claim": "Example Domain is intended for use in illustrative examples in documents.",
  "verdict": "SUPPORTED"
}
