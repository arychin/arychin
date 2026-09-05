### Open Source
- **[Azure/azure-sdk-for-python#48514](https://github.com/Azure/azure-sdk-for-python/issues/48514)** — found `get_history_item_ids()` was keeping the *oldest* N conversation turns instead of the newest, silently degrading multi-turn agents past ~25 turns. Root-caused across both providers; proposed fix shipped verbatim in `azure-ai-agentserver-responses` 2.1.0b2.
