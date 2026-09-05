from fastapi import FastAPI
from .models import AnalyzeRequest, PolicyRequest, ExecuteRequest, VerifyRequest
from .services.sentinel import analyze, simulate, check_policy, execute, verify, novakart_demo

app = FastAPI(
    title="Sentinel — AI Business Autopilot",
    version="0.1.0",
    description="Predictive merchant decision-and-action MVP."
)

@app.get("/health")
def health():
    return {"status": "ok", "service": "sentinel"}

@app.get("/api/v1/demo/novakart")
def demo():
    return novakart_demo()

@app.post("/api/v1/analyze")
def analyze_endpoint(req: AnalyzeRequest):
    return analyze(req.model_dump())

@app.post("/api/v1/simulate")
def simulate_endpoint(req: AnalyzeRequest):
    return simulate(req.model_dump())

@app.post("/api/v1/policy/check")
def policy_endpoint(req: PolicyRequest):
    return check_policy(req.model_dump())

@app.post("/api/v1/execute")
def execute_endpoint(req: ExecuteRequest):
    return execute(req.model_dump())

@app.post("/api/v1/verify")
def verify_endpoint(req: VerifyRequest):
    return verify(req.model_dump())
