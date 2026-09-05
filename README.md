# Sentinel — AI Business Autopilot

Sentinel is a predictive merchant decision-and-action layer that detects revenue-impacting problems before they become major losses, predicts likely impact, simulates permitted interventions, and safely recommends or executes the best response.

## Core loop
**Observe → Predict → Quantify → Explain → Simulate → Decide → Policy Check → Act → Verify → Audit**

## MVP: NovaKart payment degradation
Sentinel demonstrates a merchant whose payment success rate falls from 97.8% to 91.2%.

The system:
1. Detects abnormal payment performance.
2. Estimates probability that the disruption will continue.
3. Estimates revenue exposure.
4. Produces evidence-backed root-cause factors.
5. Compares intervention scenarios against a digital-twin state.
6. Applies a deterministic policy engine.
7. Executes a permitted simulated action.
8. Verifies the measured outcome.
9. Stores an audit trail.

> Sentinel does not claim to control all of Razorpay's payment infrastructure. Razorpay APIs/webhooks are used only where genuinely supported; unsupported actions are represented in a controlled simulation.

## Architecture

```text
Payment events / synthetic data
            |
            v
      Observation Layer
            |
            v
   ML + Statistical Engine
   | anomaly | prediction |
   | impact | risk score  |
            |
            +---------> Evidence
            |               |
            v               v
       Digital Twin ----> LLM Explanation
            |
            v
       Scenario Engine
            |
            v
      Decision Engine
            |
            v
      Policy Engine
       /          \
    BLOCK        APPROVE
                    |
                    v
                 Executor
                    |
                    v
               Verification
                    |
                    v
                Audit Log
```

## Tech stack
- Python
- FastAPI
- Pandas / NumPy / scikit-learn
- React/Next.js (planned dashboard)
- PostgreSQL/Azure SQL (planned persistence)
- Azure / Azure OpenAI where useful
- Razorpay Test Mode/webhooks where genuinely supported

## Run backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## Demo endpoints
- `GET /health`
- `GET /api/v1/demo/novakart`
- `POST /api/v1/analyze`
- `POST /api/v1/simulate`
- `POST /api/v1/policy/check`
- `POST /api/v1/execute`
- `POST /api/v1/verify`

## Important product boundary
The AI proposes. Policy controls. Software executes. Verification checks the result.

This repository is an MVP/hackathon implementation, not a production payment-routing system.
