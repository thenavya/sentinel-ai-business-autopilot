# Sentinel Architecture

## Components

### Observation
Consumes Razorpay webhook events where available and synthetic transaction events for the demo.

### ML/statistics
- Baseline comparison
- Anomaly detection
- Continuation probability
- Risk score
- Exposure estimation

### Evidence layer
Converts raw event data into structured evidence for explanations.

### LLM layer
Only explains/synthesizes structured evidence and simulation results. It is not the source of financial truth or policy authority.

### Digital Twin
Represents the merchant's current operating state and allows scenario comparison.

### Policy Engine
Deterministic rules for confidence, monetary limits, action permissions, restricted categories, and merchant preferences.

### Executor
Performs only approved actions. Unsupported external actions remain controlled simulations.

### Verification
Measures post-action results against expected outcomes.

### Audit
Records detection, evidence, prediction, simulation, decision, policy result, execution and verification.

## Safety principle

**AI proposes. Policy controls. Software executes. Verification checks.**
