# zkOrigo – Multi-Chain Stateless Validator

<p align="center">
  <img src="static/zkorigo_logo.png" alt="zkOrigo Logo" width="200"/>
</p>

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ADCoinX_zkOrigo&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ADCoinX_zkOrigo)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=ADCoinX_zkOrigo&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=ADCoinX_zkOrigo)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ADCoinX_zkOrigo&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ADCoinX_zkOrigo)

---

## 🔎 Overview

zkOrigo is a **stateless, multi-chain wallet validator** that provides:

- AI-driven risk scoring (Heuristic v2)
- Stateless validation – no private keys, no funds, no sensitive data stored
- ISO 20022 XML export (audit-ready format trusted by banks)
- zk-Proof hash generation (future upgrade to circom/snarkjs)
- Multi-chain fallback RPC endpoints for reliability

This approach delivers **compliance and risk visibility** for enterprises, RWA projects, and regulators.

---

## 🌐 Live Demo

👉 [zkOrigo MVP](https://zkorigo.onrender.com)

---

## 🏗️ Supported Chains

- Ethereum (ETH)
- Polygon (MATIC)
- Binance Smart Chain (BNB)
- Solana
- XRPL
- Hedera
- Stellar (XLM)

Each chain integrates **three fallback RPC endpoints** to guarantee high availability.

---

## 🛡️ InfoSec Architecture

**How zkOrigo Works:**

```
+-------------------+
|   User Wallet     |
+-------------------+
          |
          v
+---------------------------+
| zkOrigo Stateless Validator|
+---------------------------+
          |
          v
+----------------------------+
| Public RPC Endpoints (x3)  |
+----------------------------+
          |
          v
+------------------------+
| Heuristic AI Engine v2 |
+------------------------+
          |
          v
+--------------------+     +-----------------+
| ISO20022 XML Export|<--->| zk-Proof Hash   |
+--------------------+     +-----------------+
          |
          v
+-----------------+
| Audit Report    |
+-----------------+
```

**Features:**
- **Stateless design:** No keys, no storage, only public blockchain data.
- **AI module:** Heuristic-based scoring v2 (entropy checks, endpoint fallback, dormant wallet detection).
- **Compliance:** ISO20022 pain.001 export for audit readiness.
- **Quality Assurance:** SonarCloud Quality Gate Passed.

---

## 📂 Project Structure

- `/app.py`              – FastAPI main app
- `/chains.py`           – Multi-chain RPC + balance checker
- `/ai_module.py`        – Heuristic AI risk scoring (v2)
- `/iso_export.py`       – ISO20022 XML export (pain.001)
- `/zk_proof.py`         – Dummy zk-proof generator
- `/rwa_module.py`       – RWA Proof generator
- `/templates/`          – Jinja2 templates
- `/static/`             – CSS, logos, UI assets
- `/outputs/`            – Generated ISO20022 XML reports

---

## 📊 Traction

- 3,500+ wallet validations across zkOrigo, HGuard, ProetorX, and CryptoGuard
- Multiple grant programs in due diligence/shortlisted (Hedera, XRPL, Thrive)
- Positive recognition from Ripple VP on LinkedIn
- Published thought leadership: Medium – Blockchain is Broken Without Compliance

---

## 📅 Roadmap

- **M1:** MVP live (multi-chain stateless validation + heuristic AI v2)
- **M2:** Full balance + transaction analysis integration
- **M3:** Advanced ISO20022 mappings (pain.001 + pacs.008)
- **M4:** Upgrade zk-Proofs (dummy → circom/snarkjs)
- **M5:** Enterprise integrations & RWA pilot deployments

---

## ⚠️ Disclaimer

This validator is for informational and compliance purposes only.
- No private keys are collected.
- No funds are accessed or moved.
- Only public blockchain data is queried, validated, and exported.
- Final decisions remain with the end user.
