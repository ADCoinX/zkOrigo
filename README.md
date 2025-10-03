# zkOrigo - MVP (Stateless Validator + zkProof Exporter)

**zkOrigo** is a minimal MVP to demonstrate a multi-chain stateless validator that combines:
- AI heuristic risk scoring (rule-based, v1)
- ISO 20022 export (pain.001) for compliance
- zkProof placeholder (deterministic SHA256 "dummy" hash)

## What's included
- Single FastAPI service (backend + simple UI served via Jinja templates)
- Support for multiple chains via a modular validate endpoint
- ISO XML generator (basic pain.001)
- Dummy zkProof generator (replaceable with real SNARK/STARK later)

## How to run (local / Render)
1. Create a Python 3.10+ virtualenv
2. `pip install -r requirements.txt`
3. `uvicorn app:app --host 0.0.0.0 --port 10000`
4. Open `http://localhost:10000` and test

## Files
- `app.py` - FastAPI main app
- `iso_export.py` - ISO 20022 (pain.001) XML generator
- `zk_proof.py` - Dummy proof generator (SHA256)
- `templates/index.html` - UI (dark, lavish theme)
- `static/style.css` - dark theme styles
- `static/zkorigo_logo.png` - placeholder (replace with your logo)

## Notes
- This is an MVP. zk proof currently a deterministic hash for demonstration.
- Replace `zk_proof.generate_dummy_proof` with a real ZK pipeline (circom/snarkjs or Halo2) in Phase 2.
- Add your `zkorigo_logo.png` into `static/` to display branding.

## Roadmap (short)
- Phase 1: MVP + traction (dummy proofs)
- Phase 2: Integrate SNARK/STARK circuits (real ZKP)
- Phase 3: On-chain verifiers + RWA validator
