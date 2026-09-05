# Razorpay Integration Boundary

Sentinel should integrate only with Razorpay capabilities that are actually available and appropriate for the hackathon environment.

Use:
- Razorpay Test Mode where appropriate.
- Supported Razorpay APIs.
- Razorpay webhooks for payment events.
- Synthetic transactions for controlled demonstrations.

Do not claim:
- autonomous control of Razorpay's complete routing infrastructure;
- access to APIs that are not actually available;
- guaranteed recovery percentages;
- guaranteed revenue savings.

For any action not exposed by the available API surface, use `execution_mode=controlled_simulation` and clearly label it in the UI/demo.
