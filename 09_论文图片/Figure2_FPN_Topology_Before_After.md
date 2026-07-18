# Figure 2: FPN Topology Before and After Entropy-Guided Pruning

```mermaid
flowchart LR
    subgraph B["(a) Baseline FPN Fusion"]
        B9["Layer 9<br/>SPPF<br/>256 × 20 × 20"]
        B10["Layer 10<br/>Upsample<br/>256 × 40 × 40"]
        B6["Layer 6<br/>Backbone Skip Feature<br/>128 × 40 × 40"]
        B11["Layer 11<br/>Concat<br/>384 × 40 × 40"]
        B12["Layer 12<br/>C2f Fusion<br/>128 × 40 × 40"]

        B9 --> B10
        B10 --> B11
        B6 -->|"Long skip branch"| B11
        B11 --> B12
    end

    subgraph P["(b) Entropy-Guided Pruned FPN"]
        P9["Layer 9<br/>SPPF<br/>256 × 20 × 20"]
        P10["Layer 10<br/>Upsample<br/>256 × 40 × 40"]
        P6["Layer 6<br/>Removed Skip Feature<br/>128 × 40 × 40"]
        P11["Layer 11<br/>Single-Input Pass-Through<br/>256 × 40 × 40"]
        P12["Layer 12<br/>Reconfigured C2f<br/>128 × 40 × 40"]

        P9 --> P10
        P10 --> P11
        P6 -.->|"Pruned"| P11
        P11 --> P12
    end

    style B6 fill:#D6EAF8,stroke:#2874A6
    style B11 fill:#FDEBD0,stroke:#CA6F1E
    style P6 fill:#FADBD8,stroke:#C0392B,stroke-dasharray:5 5
    style P11 fill:#D5F5E3,stroke:#239B56
```

**Figure 2. FPN topology before and after entropy-guided branch pruning.** The baseline model concatenates the Layer 6 backbone feature with the upsampled Layer 9 feature at Layer 11. The proposed configuration removes the Layer 6-to-Layer 11 skip branch and reconfigures the subsequent C2f block for the reduced input-channel dimension.
