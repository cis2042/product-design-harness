# Red-Team Prompt

Use this when a product plan sounds convincing.

## Prompt

Red-team this product direction using Product Design Harness.

Do not list supporting reasons first.

Start with:

| Field | Required answer |
|---|---|
| Five failure modes | Ways this direction can fail. |
| Disconfirming tests | Evidence that would prove it wrong. |
| Hidden affected people | People affected without direct operation. |
| Current workaround | What users do today instead. |
| Substitute threats | Direct, indirect, platform, workflow, and doing-nothing substitutes. |
| Trust risk | What could damage confidence or dignity. |
| Stop condition | What should block execution. |

Then provide a verdict using `continue`, `verify`, or `stop_reframe`.

If this becomes a complete review, return
`schemas/review-result.schema.json`.
