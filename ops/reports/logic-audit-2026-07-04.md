# Logic Audit - 2026-07-04

Audit date: 2026-07-04
Entries audited: 135
Non-null Part A fields judged: 697
Part B rules executed: RULE-1 through RULE-8
Part B rules with zero findings: RULE-1, RULE-2, RULE-3, RULE-6, RULE-7, RULE-8
Findings: 295

## Counts by class

| Class | Count |
| --- | ---: |
| CRITICAL | 41 |
| UNSUPPORTED | 162 |
| AMBIGUOUS | 71 |
| RULE-1 | 0 |
| RULE-2 | 0 |
| RULE-3 | 0 |
| RULE-4 | 15 |
| RULE-5 | 6 |
| RULE-6 | 0 |
| RULE-7 | 0 |
| RULE-8 | 0 |

## Findings

| Entry | Field | Class | Detail |
| --- | --- | --- | --- |
| alibaba/qwen3.6-flash | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| alibaba/qwen3.6-flash-2026-04-16 | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| alibaba/qwen3.6-max-preview | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256K can mean decimal 256000 or binary 262144 tokens |
| alibaba/qwen3.6-plus | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| alibaba/qwen3.6-plus-2026-04-02 | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| alibaba/qwen3.7-max | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| alibaba/qwen3.7-max-2026-05-17 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| alibaba/qwen3.7-max-2026-05-20 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| alibaba/qwen3.7-max-preview | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| alibaba/qwen3.7-plus | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| alibaba/qwen3.7-plus-2026-05-26 | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| amazon/amazon.nova-lite-v1:0 | context_window_tokens | AMBIGUOUS | stored value 300000 only matches ambiguous quote unit(s): 300k can mean decimal 300000 or binary 307200 tokens; 300k can mean decimal 300000 or binary 307200 tokens |
| amazon/amazon.nova-lite-v1:0 | max_output_tokens | AMBIGUOUS | stored value 10000 only matches ambiguous quote unit(s): 10K can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens |
| amazon/amazon.nova-micro-v1:0 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens |
| amazon/amazon.nova-micro-v1:0 | max_output_tokens | AMBIGUOUS | stored value 10000 only matches ambiguous quote unit(s): 10K can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens |
| amazon/amazon.nova-premier-v1:0 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| amazon/amazon.nova-premier-v1:0 | max_output_tokens | AMBIGUOUS | stored value 10000 only matches ambiguous quote unit(s): 10K can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens |
| amazon/amazon.nova-pro-v1:0 | context_window_tokens | AMBIGUOUS | stored value 300000 only matches ambiguous quote unit(s): 300k can mean decimal 300000 or binary 307200 tokens; 300k can mean decimal 300000 or binary 307200 tokens |
| amazon/amazon.nova-pro-v1:0 | max_output_tokens | AMBIGUOUS | stored value 10000 only matches ambiguous quote unit(s): 10K can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens; 10k can mean decimal 10000 or binary 10240 tokens |
| amazon/anthropic.claude-3-5-sonnet-20241022-v2:0 | context_window_tokens | AMBIGUOUS | stored value 200000 only matches ambiguous quote unit(s): 200K can mean decimal 200000 or binary 204800 tokens |
| anthropic/claude-fable-5 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| anthropic/claude-fable-5 | max_output_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens |
| anthropic/claude-haiku-4-5-20251001 | context_window_tokens | AMBIGUOUS | stored value 200000 only matches ambiguous quote unit(s): 200k can mean decimal 200000 or binary 204800 tokens |
| anthropic/claude-haiku-4-5-20251001 | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| anthropic/claude-opus-4-6 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| anthropic/claude-opus-4-7 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens |
| anthropic/claude-opus-4-8 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| anthropic/claude-opus-4-8 | max_output_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens |
| anthropic/claude-sonnet-5 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| anthropic/claude-sonnet-5 | max_output_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens |
| cohere/c4ai-aya-expanse-32b | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens |
| cohere/c4ai-aya-expanse-32b | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command | context_window_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens; 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens; 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-a-03-2025 | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens; 256k can mean decimal 256000 or binary 262144 tokens |
| cohere/command-a-03-2025 | max_output_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8K can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| cohere/command-a-plus-05-2026 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128K can mean decimal 128000 or binary 131072 tokens |
| cohere/command-a-plus-05-2026 | max_output_tokens | AMBIGUOUS | stored value 64000 only matches ambiguous quote unit(s): 64k can mean decimal 64000 or binary 65536 tokens |
| cohere/command-a-reasoning-08-2025 | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens; 256k can mean decimal 256000 or binary 262144 tokens |
| cohere/command-a-reasoning-08-2025 | max_output_tokens | AMBIGUOUS | stored value 32000 only matches ambiguous quote unit(s): 32k can mean decimal 32000 or binary 32768 tokens |
| cohere/command-a-translate-08-2025 | context_window_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8K can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| cohere/command-a-translate-08-2025 | max_output_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8K can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| cohere/command-a-vision-07-2025 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128K can mean decimal 128000 or binary 131072 tokens |
| cohere/command-a-vision-07-2025 | max_output_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8K can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| cohere/command-light | context_window_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens; 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-light | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens; 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-r-03-2024 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens |
| cohere/command-r-03-2024 | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-r-08-2024 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens; 128k can mean decimal 128000 or binary 131072 tokens; 128K can mean decimal 128000 or binary 131072 tokens |
| cohere/command-r-08-2024 | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens; 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-r-plus-04-2024 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens |
| cohere/command-r-plus-04-2024 | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/command-r-plus-08-2024 | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128k can mean decimal 128000 or binary 131072 tokens |
| cohere/command-r-plus-08-2024 | max_output_tokens | AMBIGUOUS | stored value 4000 only matches ambiguous quote unit(s): 4k can mean decimal 4000 or binary 4096 tokens |
| cohere/tiny-aya-global | context_window_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| cohere/tiny-aya-global | max_output_tokens | AMBIGUOUS | stored value 8000 only matches ambiguous quote unit(s): 8k can mean decimal 8000 or binary 8192 tokens; 8k can mean decimal 8000 or binary 8192 tokens |
| deepseek/deepseek-v4-flash | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| deepseek/deepseek-v4-flash | max_output_tokens | AMBIGUOUS | stored value 384000 only matches ambiguous quote unit(s): 384K can mean decimal 384000 or binary 393216 tokens |
| deepseek/deepseek-v4-pro | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| deepseek/deepseek-v4-pro | max_output_tokens | AMBIGUOUS | stored value 384000 only matches ambiguous quote unit(s): 384K can mean decimal 384000 or binary 393216 tokens |
| moonshot/kimi-k2.5 | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens |
| moonshot/kimi-k2.6 | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens |
| moonshot/kimi-k2.7-code | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens |
| perplexity/sonar-pro | context_window_tokens | AMBIGUOUS | stored value 200000 only matches ambiguous quote unit(s): 200K can mean decimal 200000 or binary 204800 tokens |
| perplexity/sonar-reasoning-pro | context_window_tokens | AMBIGUOUS | stored value 128000 only matches ambiguous quote unit(s): 128K can mean decimal 128000 or binary 131072 tokens |
| together/Qwen/Qwen2.5-7B-Instruct-Turbo | context_window_tokens | AMBIGUOUS | stored value 32768 only matches ambiguous quote unit(s): 32K can mean decimal 32000 or binary 32768 tokens |
| xai/grok-4.20-0309-non-reasoning | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| xai/grok-4.20-0309-reasoning | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| xai/grok-4.20-multi-agent-0309 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| xai/grok-4.3 | context_window_tokens | AMBIGUOUS | stored value 1000000 only matches ambiguous quote unit(s): 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens; 1M can mean decimal 1000000 or binary 1048576 tokens |
| xai/grok-build-0.1 | context_window_tokens | AMBIGUOUS | stored value 256000 only matches ambiguous quote unit(s): 256k can mean decimal 256000 or binary 262144 tokens |
| alibaba/qwen3-max | context_window_tokens | CRITICAL | source assigned to field has numeric value(s) 0, 1 million, 128K, 2, 32K, 4 but none match stored value 256000 |
| alibaba/qwen3-max-2026-01-23 | context_window_tokens | CRITICAL | source assigned to field has numeric value(s) 0, 1 million, 128K, 2, 32K, 4 but none match stored value 256000 |
| alibaba/qwen3.6-max-preview | status | CRITICAL | quote status language implies preview, not stored status ga |
| alibaba/qwen3.7-max | status | CRITICAL | quote status language implies preview, not stored status ga |
| alibaba/qwen3.7-max-2026-05-17 | status | CRITICAL | quote status language implies preview, not stored status ga |
| alibaba/qwen3.7-max-2026-05-20 | status | CRITICAL | quote status language implies preview, not stored status ga |
| alibaba/qwen3.7-max-preview | status | CRITICAL | quote status language implies preview, not stored status ga |
| anthropic/claude-opus-4-6 | status | CRITICAL | quote status language implies preview, not stored status ga |
| anthropic/claude-opus-4-7 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/deepseek-v4-flash | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/deepseek-v4-pro | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/glm-5.1 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/glm-5.1-fast | pricing.cached_input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.74 do not match stored value 0.52 |
| fireworks/glm-5.1-fast | pricing.input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 2.8 |
| fireworks/glm-5.1-fast | pricing.output_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 8.8 |
| fireworks/glm-5.1-fast | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/glm-5.2 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/glm-5.2-fast | pricing.cached_input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.74 do not match stored value 0.21 |
| fireworks/glm-5.2-fast | pricing.input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 2.1 |
| fireworks/glm-5.2-fast | pricing.output_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 6.6 |
| fireworks/glm-5.2-fast | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/kimi-k2.6 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/kimi-k2.6-fast | pricing.input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 2.0 |
| fireworks/kimi-k2.6-fast | pricing.output_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 8.0 |
| fireworks/kimi-k2.6-fast | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/kimi-k2.7-code | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/kimi-k2.7-code-fast | pricing.cached_input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.74 do not match stored value 0.38 |
| fireworks/kimi-k2.7-code-fast | pricing.input_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 1.9 |
| fireworks/kimi-k2.7-code-fast | pricing.output_per_mtok | CRITICAL | field-labeled quote value(s) $0.028, $0.14, $0.145, $0.16, $0.19, $0.28, $0.95, $1.40 do not match stored value 8.0 |
| fireworks/kimi-k2.7-code-fast | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/minimax-m2.7 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/minimax-m3 | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/openai-gpt-oss-120b | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/openai-gpt-oss-20b | status | CRITICAL | quote status language implies preview, not stored status ga |
| fireworks/qwen-3.7-plus | status | CRITICAL | quote status language implies preview, not stored status ga |
| minimax/minimax-m2 | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| minimax/minimax-m2.1 | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| minimax/minimax-m2.5 | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| minimax/minimax-m2.7 | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| minimax/minimax-m3 | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| perplexity/sonar-reasoning-pro | status | CRITICAL | quote status language implies deprecated, not stored status ga |
| alibaba/qwen3.7-max <> together/qwen3.7-max | pricing.input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 2.5 vs 1.25 |
| alibaba/qwen3.7-max <> together/qwen3.7-max | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 7.5 vs 3.75 |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.cached_input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 0.52 vs 0.26 |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 2.8 vs 1.4 |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 8.8 vs 4.4 |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.cached_input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 0.52 vs 0.26 |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 2.8 vs 1.4 |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 8.8 vs 4.4 |
| fireworks/kimi-k2.6-fast <> moonshot/kimi-k2.6 | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 8.0 vs 4.0 |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.cached_input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 0.38 vs 0.19 |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 1.9 vs 0.95 |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 8.0 vs 4.0 |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.cached_input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 0.38 vs 0.19 |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.input_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 1.9 vs 0.95 |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.output_per_mtok | RULE-4 | same canonical model prices are exact 2x/10x ratio: 8.0 vs 4.0 |
| minimax/minimax-m2 | status | RULE-5 | active status but source 0 contains inactive language: Legacy |
| minimax/minimax-m2.1 | status | RULE-5 | active status but source 0 contains inactive language: Legacy |
| minimax/minimax-m2.5 | status | RULE-5 | active status but source 0 contains inactive language: Legacy |
| minimax/minimax-m2.7 | status | RULE-5 | active status but source 0 contains inactive language: Legacy |
| minimax/minimax-m3 | status | RULE-5 | active status but source 0 contains inactive language: Legacy |
| perplexity/sonar-reasoning-pro | status | RULE-5 | active status but source 1 contains inactive language: deprecated |
| alibaba/qwen3-max | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3-max | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3-max-2026-01-23 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3-max-2026-01-23 | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.6-flash | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.6-flash-2026-04-16 | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.6-max-preview | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3.6-plus | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.6-plus-2026-04-02 | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.7-max | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3.7-max-2026-05-17 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3.7-max-2026-05-20 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3.7-max-preview | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| alibaba/qwen3.7-plus | status | UNSUPPORTED | no stored quote entails status ga |
| alibaba/qwen3.7-plus-2026-05-26 | status | UNSUPPORTED | no stored quote entails status ga |
| amazon/amazon.nova-lite-v1:0 | status | UNSUPPORTED | no stored quote entails status ga |
| amazon/amazon.nova-micro-v1:0 | status | UNSUPPORTED | no stored quote entails status ga |
| amazon/amazon.nova-premier-v1:0 | status | UNSUPPORTED | no stored quote entails status ga |
| amazon/amazon.nova-pro-v1:0 | status | UNSUPPORTED | no stored quote entails status ga |
| amazon/anthropic.claude-3-5-sonnet-20241022-v2:0 | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| anthropic/claude-fable-5 | status | UNSUPPORTED | no stored quote entails status ga |
| anthropic/claude-haiku-4-5-20251001 | status | UNSUPPORTED | no stored quote entails status ga |
| anthropic/claude-opus-4-8 | status | UNSUPPORTED | no stored quote entails status ga |
| anthropic/claude-sonnet-5 | status | UNSUPPORTED | no stored quote entails status ga |
| cohere/command-a-plus-05-2026 | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| cohere/command-a-vision-07-2025 | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| cohere/command-r7b-12-2024 | status | UNSUPPORTED | no stored quote entails status ga |
| deepseek/deepseek-v4-flash | status | UNSUPPORTED | no stored quote entails status ga |
| deepseek/deepseek-v4-pro | status | UNSUPPORTED | no stored quote entails status ga |
| fireworks/llama-v3p3-70b-instruct | status | UNSUPPORTED | no stored quote entails status ga |
| fireworks/qwen2p5-vl-32b-instruct | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| fireworks/qwen2p5-vl-32b-instruct | status | UNSUPPORTED | no stored quote entails status ga |
| google/gemini-2.5-flash | status | UNSUPPORTED | no stored quote entails status ga |
| google/gemini-2.5-flash-lite | status | UNSUPPORTED | no stored quote entails status ga |
| google/gemini-2.5-pro | status | UNSUPPORTED | no stored quote entails status ga |
| google/gemini-3.1-flash-lite | status | UNSUPPORTED | no stored quote entails status ga |
| google/gemini-3.1-pro-preview | modalities | UNSUPPORTED | no stored quote entails input=['audio', 'image', 'text', 'video'] and output=['text'] |
| groq/llama-3.1-8b-instant | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| groq/llama-3.1-8b-instant | status | UNSUPPORTED | no stored quote entails status ga |
| groq/llama-3.3-70b-versatile | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| groq/llama-3.3-70b-versatile | status | UNSUPPORTED | no stored quote entails status ga |
| groq/openai/gpt-oss-120b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| groq/openai/gpt-oss-120b | status | UNSUPPORTED | no stored quote entails status ga |
| groq/openai/gpt-oss-20b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| groq/openai/gpt-oss-20b | status | UNSUPPORTED | no stored quote entails status ga |
| minimax/minimax-m2 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| minimax/minimax-m2.1 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| minimax/minimax-m2.5 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| minimax/minimax-m2.7 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| minimax/minimax-m3 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| mistral/codestral-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/devstral-medium-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/devstral-small-latest | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| mistral/devstral-small-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/magistral-medium-latest | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| mistral/magistral-medium-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/mistral-large-latest | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| mistral/mistral-large-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/mistral-medium-latest | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| mistral/mistral-medium-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/mistral-small-latest | modalities | UNSUPPORTED | no stored quote entails input=['image', 'text'] and output=['text'] |
| mistral/mistral-small-latest | status | UNSUPPORTED | no stored quote entails status ga |
| mistral/voxtral-small-latest | status | UNSUPPORTED | no stored quote entails status ga |
| moonshot/kimi-k2.5 | status | UNSUPPORTED | no stored quote entails status ga |
| moonshot/kimi-k2.6 | status | UNSUPPORTED | no stored quote entails status ga |
| moonshot/kimi-k2.7-code | status | UNSUPPORTED | no stored quote entails status ga |
| openai/gpt-5.4 | status | UNSUPPORTED | no stored quote entails status ga |
| openai/gpt-5.5 | status | UNSUPPORTED | no stored quote entails status ga |
| openai/gpt-5.5-pro | status | UNSUPPORTED | no stored quote entails status ga |
| perplexity/perplexity/sonar | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| perplexity/perplexity/sonar | pricing.cached_input_per_mtok | UNSUPPORTED | no stored quote contains numeric evidence for stored value 0.0625 |
| perplexity/perplexity/sonar | pricing.input_per_mtok | UNSUPPORTED | no stored quote contains numeric evidence for stored value 0.25 |
| perplexity/perplexity/sonar | pricing.output_per_mtok | UNSUPPORTED | no stored quote contains numeric evidence for stored value 2.5 |
| perplexity/perplexity/sonar | status | UNSUPPORTED | no stored quote entails status ga |
| perplexity/sonar-pro | pricing.input_per_mtok | UNSUPPORTED | tiered pricing quote has multiple values (10, 14, 15, 2, 3, 6) but notes do not document the chosen tier |
| perplexity/sonar-pro | pricing.output_per_mtok | UNSUPPORTED | tiered pricing quote has multiple values (10, 14, 15, 2, 3, 6) but notes do not document the chosen tier |
| perplexity/sonar-pro | status | UNSUPPORTED | no stored quote entails status ga |
| perplexity/sonar-reasoning-pro | pricing.input_per_mtok | UNSUPPORTED | tiered pricing quote has multiple values (10, 14, 15, 2, 3, 6) but notes do not document the chosen tier |
| perplexity/sonar-reasoning-pro | pricing.output_per_mtok | UNSUPPORTED | tiered pricing quote has multiple values (10, 14, 15, 2, 3, 6) but notes do not document the chosen tier |
| together/Qwen/Qwen2.5-7B-Instruct-Turbo | status | UNSUPPORTED | no stored quote entails status ga |
| together/cogito-v2.1-671b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/cogito-v2.1-671b | status | UNSUPPORTED | no stored quote entails status ga |
| together/deepseek-v4-pro | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/deepseek-v4-pro | status | UNSUPPORTED | no stored quote entails status ga |
| together/gemma-3n-e4b-instruct | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/gemma-3n-e4b-instruct | status | UNSUPPORTED | no stored quote entails status ga |
| together/gemma-4-31b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/gemma-4-31b | status | UNSUPPORTED | no stored quote entails status ga |
| together/gemma-4-31b-it-pearl | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/gemma-4-31b-it-pearl | status | UNSUPPORTED | no stored quote entails status ga |
| together/glm-5.1 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/glm-5.1 | status | UNSUPPORTED | no stored quote entails status ga |
| together/glm-5.2 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/glm-5.2 | status | UNSUPPORTED | no stored quote entails status ga |
| together/gpt-oss-120b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/gpt-oss-120b | status | UNSUPPORTED | no stored quote entails status ga |
| together/gpt-oss-20b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/gpt-oss-20b | status | UNSUPPORTED | no stored quote entails status ga |
| together/kimi-k2.6 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/kimi-k2.6 | status | UNSUPPORTED | no stored quote entails status ga |
| together/kimi-k2.7-code | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/kimi-k2.7-code | status | UNSUPPORTED | no stored quote entails status ga |
| together/lfm2-24b-a2b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/lfm2-24b-a2b | status | UNSUPPORTED | no stored quote entails status ga |
| together/llama-3.3-70b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/llama-3.3-70b | status | UNSUPPORTED | no stored quote entails status ga |
| together/minimax-m2.5 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/minimax-m2.5 | status | UNSUPPORTED | no stored quote entails status ga |
| together/minimax-m2.7 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/minimax-m2.7 | status | UNSUPPORTED | no stored quote entails status ga |
| together/minimax-m3 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/minimax-m3 | status | UNSUPPORTED | no stored quote entails status ga |
| together/nvidia-nemotron-3-ultra | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/nvidia-nemotron-3-ultra | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3-235b-a22b-fp8-throughput | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3-235b-a22b-fp8-throughput | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3.5-397b-a17b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3.5-397b-a17b | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3.5-9b | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3.5-9b | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3.6-plus | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3.6-plus | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3.7-max | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3.7-max | status | UNSUPPORTED | no stored quote entails status ga |
| together/qwen3.7-plus | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/qwen3.7-plus | status | UNSUPPORTED | no stored quote entails status ga |
| together/rnj-1-instruct | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| together/rnj-1-instruct | status | UNSUPPORTED | no stored quote entails status ga |
| xai/grok-4.20-0309-non-reasoning | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| xai/grok-4.20-0309-non-reasoning | status | UNSUPPORTED | no stored quote entails status ga |
| xai/grok-4.20-0309-reasoning | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| xai/grok-4.20-0309-reasoning | status | UNSUPPORTED | no stored quote entails status ga |
| xai/grok-4.20-multi-agent-0309 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| xai/grok-4.20-multi-agent-0309 | status | UNSUPPORTED | no stored quote entails status ga |
| xai/grok-4.3 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| xai/grok-4.3 | status | UNSUPPORTED | no stored quote entails status ga |
| xai/grok-build-0.1 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| xai/grok-build-0.1 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4-32b-0414-128k | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4-32b-0414-128k | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.5 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.5 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.5-air | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.5-air | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.5-airx | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.5-airx | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.5-x | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.5-x | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.6 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.6 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.7 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.7 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-4.7-flashx | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-4.7-flashx | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-5 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-5 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-5-turbo | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-5-turbo | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-5.1 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-5.1 | status | UNSUPPORTED | no stored quote entails status ga |
| zhipu/glm-5.2 | modalities | UNSUPPORTED | no stored quote entails input=['text'] and output=['text'] |
| zhipu/glm-5.2 | status | UNSUPPORTED | no stored quote entails status ga |

## Judgment

- Re-collection from live sources: 47 findings. This includes CRITICAL conflicts, stale/future timestamps, and high-signal invariant failures.
- Documentation or quote/note fixes: 233 findings. This includes unsupported or ambiguous quote entailment where the stored value may still be correct but the stored evidence is inadequate.
- Manual review before deciding: 15 findings. This mainly covers cross-provider same-model comparisons and exact-ratio price checks.

| Entry | Field | Class | Judgment |
| --- | --- | --- | --- |
| alibaba/qwen3.6-flash | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.6-flash-2026-04-16 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.6-max-preview | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.6-plus | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.6-plus-2026-04-02 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-max | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-max-2026-05-17 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-max-2026-05-20 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-max-preview | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-plus | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3.7-plus-2026-05-26 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-lite-v1:0 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-lite-v1:0 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-micro-v1:0 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-micro-v1:0 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-premier-v1:0 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-premier-v1:0 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-pro-v1:0 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/amazon.nova-pro-v1:0 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| amazon/anthropic.claude-3-5-sonnet-20241022-v2:0 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-fable-5 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-fable-5 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-haiku-4-5-20251001 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-haiku-4-5-20251001 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-opus-4-6 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-opus-4-7 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-opus-4-8 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-opus-4-8 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-sonnet-5 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| anthropic/claude-sonnet-5 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/c4ai-aya-expanse-32b | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/c4ai-aya-expanse-32b | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-03-2025 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-03-2025 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-plus-05-2026 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-plus-05-2026 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-reasoning-08-2025 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-reasoning-08-2025 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-translate-08-2025 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-translate-08-2025 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-vision-07-2025 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-a-vision-07-2025 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-light | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-light | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-03-2024 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-03-2024 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-08-2024 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-08-2024 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-plus-04-2024 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-plus-04-2024 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-plus-08-2024 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/command-r-plus-08-2024 | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/tiny-aya-global | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| cohere/tiny-aya-global | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| deepseek/deepseek-v4-flash | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| deepseek/deepseek-v4-flash | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| deepseek/deepseek-v4-pro | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| deepseek/deepseek-v4-pro | max_output_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| moonshot/kimi-k2.5 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| moonshot/kimi-k2.6 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| moonshot/kimi-k2.7-code | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| perplexity/sonar-pro | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| perplexity/sonar-reasoning-pro | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| together/Qwen/Qwen2.5-7B-Instruct-Turbo | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| xai/grok-4.20-0309-non-reasoning | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| xai/grok-4.20-0309-reasoning | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| xai/grok-4.20-multi-agent-0309 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| xai/grok-4.3 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| xai/grok-build-0.1 | context_window_tokens | AMBIGUOUS | Documentation fix if the value is correct: add an unambiguous quote or note the decimal/binary convention. |
| alibaba/qwen3-max | context_window_tokens | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3-max-2026-01-23 | context_window_tokens | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.6-max-preview | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.7-max | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.7-max-2026-05-17 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.7-max-2026-05-20 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.7-max-preview | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| anthropic/claude-opus-4-6 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| anthropic/claude-opus-4-7 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/deepseek-v4-flash | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/deepseek-v4-pro | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.1 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.1-fast | pricing.cached_input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.1-fast | pricing.input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.1-fast | pricing.output_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.1-fast | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.2 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.2-fast | pricing.cached_input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.2-fast | pricing.input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.2-fast | pricing.output_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/glm-5.2-fast | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.6 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.6-fast | pricing.input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.6-fast | pricing.output_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.6-fast | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.7-code | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.7-code-fast | pricing.cached_input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.7-code-fast | pricing.input_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.7-code-fast | pricing.output_per_mtok | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/kimi-k2.7-code-fast | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/minimax-m2.7 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/minimax-m3 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/openai-gpt-oss-120b | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/openai-gpt-oss-20b | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| fireworks/qwen-3.7-plus | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| minimax/minimax-m2 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| minimax/minimax-m2.1 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| minimax/minimax-m2.5 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| minimax/minimax-m2.7 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| minimax/minimax-m3 | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| perplexity/sonar-reasoning-pro | status | CRITICAL | Re-collect from live source; stored value and cited evidence conflict. |
| alibaba/qwen3.7-max <> together/qwen3.7-max | pricing.input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| alibaba/qwen3.7-max <> together/qwen3.7-max | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.cached_input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> together/glm-5.1 | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.cached_input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/glm-5.1-fast <> zhipu/glm-5.1 | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.6-fast <> moonshot/kimi-k2.6 | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.cached_input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> moonshot/kimi-k2.7-code | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.cached_input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.input_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| fireworks/kimi-k2.7-code-fast <> together/kimi-k2.7-code | pricing.output_per_mtok | RULE-4 | Manual review; likely re-collect or document provider-specific serving/pricing differences. |
| minimax/minimax-m2 | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| minimax/minimax-m2.1 | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| minimax/minimax-m2.5 | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| minimax/minimax-m2.7 | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| minimax/minimax-m3 | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| perplexity/sonar-reasoning-pro | status | RULE-5 | Re-collect from live source; this violates a high-signal sanity invariant. |
| alibaba/qwen3-max | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3-max | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3-max-2026-01-23 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3-max-2026-01-23 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.6-flash | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.6-flash-2026-04-16 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.6-max-preview | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.6-plus | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.6-plus-2026-04-02 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-max | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-max-2026-05-17 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-max-2026-05-20 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-max-preview | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-plus | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| alibaba/qwen3.7-plus-2026-05-26 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| amazon/amazon.nova-lite-v1:0 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| amazon/amazon.nova-micro-v1:0 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| amazon/amazon.nova-premier-v1:0 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| amazon/amazon.nova-pro-v1:0 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| amazon/anthropic.claude-3-5-sonnet-20241022-v2:0 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| anthropic/claude-fable-5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| anthropic/claude-haiku-4-5-20251001 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| anthropic/claude-opus-4-8 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| anthropic/claude-sonnet-5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| cohere/command-a-plus-05-2026 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| cohere/command-a-vision-07-2025 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| cohere/command-r7b-12-2024 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| deepseek/deepseek-v4-flash | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| deepseek/deepseek-v4-pro | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| fireworks/llama-v3p3-70b-instruct | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| fireworks/qwen2p5-vl-32b-instruct | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| fireworks/qwen2p5-vl-32b-instruct | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| google/gemini-2.5-flash | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| google/gemini-2.5-flash-lite | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| google/gemini-2.5-pro | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| google/gemini-3.1-flash-lite | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| google/gemini-3.1-pro-preview | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/llama-3.1-8b-instant | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/llama-3.1-8b-instant | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/llama-3.3-70b-versatile | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/llama-3.3-70b-versatile | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/openai/gpt-oss-120b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/openai/gpt-oss-120b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/openai/gpt-oss-20b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| groq/openai/gpt-oss-20b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| minimax/minimax-m2 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| minimax/minimax-m2.1 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| minimax/minimax-m2.5 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| minimax/minimax-m2.7 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| minimax/minimax-m3 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/codestral-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/devstral-medium-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/devstral-small-latest | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/devstral-small-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/magistral-medium-latest | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/magistral-medium-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-large-latest | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-large-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-medium-latest | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-medium-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-small-latest | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/mistral-small-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| mistral/voxtral-small-latest | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| moonshot/kimi-k2.5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| moonshot/kimi-k2.6 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| moonshot/kimi-k2.7-code | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| openai/gpt-5.4 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| openai/gpt-5.5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| openai/gpt-5.5-pro | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/perplexity/sonar | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/perplexity/sonar | pricing.cached_input_per_mtok | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/perplexity/sonar | pricing.input_per_mtok | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/perplexity/sonar | pricing.output_per_mtok | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/perplexity/sonar | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/sonar-pro | pricing.input_per_mtok | UNSUPPORTED | Documentation fix: note the selected pricing tier, or re-collect if the tier choice is uncertain. |
| perplexity/sonar-pro | pricing.output_per_mtok | UNSUPPORTED | Documentation fix: note the selected pricing tier, or re-collect if the tier choice is uncertain. |
| perplexity/sonar-pro | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| perplexity/sonar-reasoning-pro | pricing.input_per_mtok | UNSUPPORTED | Documentation fix: note the selected pricing tier, or re-collect if the tier choice is uncertain. |
| perplexity/sonar-reasoning-pro | pricing.output_per_mtok | UNSUPPORTED | Documentation fix: note the selected pricing tier, or re-collect if the tier choice is uncertain. |
| together/Qwen/Qwen2.5-7B-Instruct-Turbo | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/cogito-v2.1-671b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/cogito-v2.1-671b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/deepseek-v4-pro | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/deepseek-v4-pro | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-3n-e4b-instruct | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-3n-e4b-instruct | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-4-31b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-4-31b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-4-31b-it-pearl | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gemma-4-31b-it-pearl | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/glm-5.1 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/glm-5.1 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/glm-5.2 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/glm-5.2 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gpt-oss-120b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gpt-oss-120b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gpt-oss-20b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/gpt-oss-20b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/kimi-k2.6 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/kimi-k2.6 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/kimi-k2.7-code | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/kimi-k2.7-code | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/lfm2-24b-a2b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/lfm2-24b-a2b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/llama-3.3-70b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/llama-3.3-70b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m2.5 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m2.5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m2.7 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m2.7 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m3 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/minimax-m3 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/nvidia-nemotron-3-ultra | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/nvidia-nemotron-3-ultra | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3-235b-a22b-fp8-throughput | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3-235b-a22b-fp8-throughput | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.5-397b-a17b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.5-397b-a17b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.5-9b | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.5-9b | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.6-plus | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.6-plus | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.7-max | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.7-max | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.7-plus | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/qwen3.7-plus | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/rnj-1-instruct | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| together/rnj-1-instruct | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-0309-non-reasoning | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-0309-non-reasoning | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-0309-reasoning | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-0309-reasoning | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-multi-agent-0309 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.20-multi-agent-0309 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.3 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-4.3 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-build-0.1 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| xai/grok-build-0.1 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4-32b-0414-128k | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4-32b-0414-128k | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-air | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-air | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-airx | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-airx | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-x | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.5-x | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.6 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.6 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.7 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.7 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.7-flashx | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-4.7-flashx | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5-turbo | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5-turbo | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5.1 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5.1 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5.2 | modalities | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
| zhipu/glm-5.2 | status | UNSUPPORTED | Documentation fix if the stored value is correct; otherwise re-collect the missing evidence. |
