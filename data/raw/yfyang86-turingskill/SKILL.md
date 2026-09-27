---
name: turing-minds
description: |
  🏆 Turing Award Laureates Cognitive Framework Library. Input a name/topic → automatically match
  a Turing Award laureate's thinking perspective, or directly activate a specified laureate's cognitive framework.
  Coverage: All 77 A.M. Turing Award laureates from 1966-2025.
  Use cases: "Analyze from Knuth's perspective," "Which Turing laureate is best suited for this problem,"
  "Distill a new laureate."
  Trigger words: "Turing Award," "Turing," "XX's Turing perspective," "Turing-level thinking,"
  "Distill Turing Award laureate."
---

# Turing Minds · Turing Award Cognitive Framework Library

> "The reason Turing Award winners changed the world is not because they wrote more code, but because they redefined the nature of computation."

## Core Philosophy

This is a **pre-distilled** cognitive framework library of Turing Award laureates. Each laureate's directory is an independently executable "thinking operating system" — not a biography, not a collection of quotes, but an **engineered expression of HOW they think**.

You can:
- **Directly invoke** a laureate's thinking framework to examine your problem
- **Let the system recommend** the most suitable Turing thinking perspective for your current needs
- **Distill new laureates** to add to the library

---

## Quick Entry Points

### Path A: Specify Laureate (Direct Activation)

When you receive an explicit name, read that laureate's SKILL.md and activate it.

**Matching Rules**:
- Full name match ("Donald Knuth")
- Last name match ("Knuth")
- Achievement match ("the one who wrote TAOCP" → Knuth)
- Chinese name match ("高德纳", "姚期智", "deep learning trio")
- Domain match ("Unix father" → Thompson)

**Execution**:
1. Locate the laureate's directory in the index (`[name]/SKILL.md`)
2. Read SKILL.md
3. Activate the thinking framework according to the rules in SKILL.md
4. Respond to the user's original question using that framework

### Path B: On-Demand Recommendation (Diagnostic Mode)

The user doesn't know whose perspective to use, only has a question or need.

**Step 1: Need Identification**

| Need Dimension | Typical Expressions | Recommended Laureates |
|--------------|-------------------|---------------------|
| Algorithm Design | "How to design elegant algorithms," "complexity analysis" | Knuth (algorithm analysis), Dijkstra (structured programming), Tarjan (graph algorithms) |
| System Building | "How to design scalable systems," "low-level architecture" | Thompson/Ritchie (Unix), Lampson (system architecture), Brooks (software engineering) |
| Programming Languages | "Language design," "type systems" | Perlis (ALGOL), Wirth (Pascal), Milner (ML), Kay (Smalltalk) |
| Artificial Intelligence | "AI research," "neural networks" | Minsky (AI foundation), Bengio/Hinton/LeCun (deep learning), Barto/Sutton (reinforcement learning), Pearl (causal inference) |
| Theoretical Computation | "Computability," "complexity" | Cook (NP-completeness), Karp (computational complexity), Wigderson (randomized computation), Yao (communication complexity) |
| Database Systems | "Data modeling," "query optimization" | Codd (relational model), Stonebraker (modern databases), Gray (transaction processing) |
| Cryptography & Security | "Encryption," "security protocols" | Rivest/Shamir/Adleman (RSA), Diffie/Hellman (public-key crypto), Goldwasser/Micali (zero-knowledge proofs) |
| Software Engineering | "Program verification," "formal methods" | Hoare (axiomatic semantics), Dijkstra (correctness proofs), Pnueli (temporal logic), Lamport (TLA+) |
| Graphics | "3D rendering," "computer graphics" | Sutherland (Sketchpad), Catmull/Hanrahan (Pixar rendering) |
| Networks/Internet | "Distributed systems," "protocol design" | Cerf/Kahn (TCP/IP), Metcalfe (Ethernet), Berners-Lee (Web) |
| Long-term Commitment | "Decades of perseverance in one direction" | Knuth (TAOCP), Iverson (APL), Sutherland (interactive graphics) |
| Contrarian Persistence | "Denied by mainstream," "sticking to beliefs" | Hinton (deep learning winter), Bachman (database model debate) |
| Interdisciplinary Thinking | "Math + CS," "cognitive science + CS" | Simon/Newell (cognitive science), Sutton/Barto (psychology + AI), Rabin (math + CS) |
| Women Scientists | "Women scientist perspective," "gender discrimination" | Allen (first female laureate), Liskov, Goldwasser |

**Step 2: Display Recommendations**

```
### Recommended Laureate: [Name] ⚡ ([Year] Turing Award, [Achievement])

**Core Thinking Framework**: [One sentence]
**Why it fits your problem**: [Specific matching logic]
**Limitations**: [Blind spots of this perspective]
```

Recommend 2-3 with diversity.

**Step 3: User Selection → Activate**

---

## Laureate Index

### By Year (1966-2025)

| Year | Laureate | Achievement | Directory Slug |
|------|----------|-------------|----------------|
| 2025 | Charles H. Bennett | Quantum cryptography | `charles-h-bennett` |
| 2025 | Gilles Brassard | Quantum cryptography | `gilles-brassard` |
| 2024 | Andrew G. Barto | Reinforcement learning | `andrew-g-barto` |
| 2024 | Richard S. Sutton | Reinforcement learning | `richard-s-sutton` |
| 2023 | Avi Wigderson | Computational theory/randomness | `avi-wigderson` |
| 2022 | Bob Metcalfe | Ethernet | `bob-metcalfe` |
| 2021 | Jack Dongarra | Numerical algorithms/HPC | `jack-dongarra` |
| 2020 | Alfred V. Aho | Programming language theory | `alfred-v-aho` |
| 2020 | Jeffrey D. Ullman | Compilers/automata | `jeffrey-d-ullman` |
| 2019 | Edwin E. Catmull | 3D computer graphics | `edwin-catmull` |
| 2019 | Patrick M. Hanrahan | Rendering technology | `patrick-hanrahan` |
| 2018 | Yoshua Bengio | Deep learning | `yoshua-bengio` |
| 2018 | Geoffrey Hinton | Deep learning | `geoffrey-hinton` |
| 2018 | Yann LeCun | Deep learning | `yann-le-cun` |
| 2017 | John L. Hennessy | Computer architecture | `john-l-hennessy` |
| 2017 | David A. Patterson | Computer architecture | `david-a-patterson` |
| 2016 | Tim Berners-Lee | World Wide Web | `tim-berners-lee` |
| 2015 | Whitfield Diffie | Public-key cryptography | `whitfield-diffie` |
| 2015 | Martin Hellman | Public-key cryptography | `martin-hellman` |
| 2014 | Michael Stonebraker | Modern database systems | `michael-stonebraker` |
| 2013 | Leslie Lamport | Distributed systems | `leslie-lamport` |
| 2012 | Shafi Goldwasser | Cryptography/computational complexity | `shafi-goldwasser` |
| 2012 | Silvio Micali | Cryptography | `silvio-micali` |
| 2011 | Judea Pearl | Causal inference | `judea-pearl` |
| 2010 | Leslie Valiant | Machine learning/parallel computing | `leslie-valiant` |
| 2009 | Charles P. Thacker | Alto personal computer | `charles-p-thacker` |
| 2008 | Barbara Liskov | Programming methodology/distributed | `barbara-liskov` |
| 2007 | Edmund M. Clarke | Model checking | `edmund-m-clarke` |
| 2007 | E. Allen Emerson | Model checking | `e-allen-emerson` |
| 2007 | Joseph Sifakis | Model checking | `joseph-sifakis` |
| 2006 | Frances E. Allen | Compiler optimization | `frances-e-allen` |
| 2005 | Peter Naur | Algol 60/BNF | `peter-naur` |
| 2004 | Vinton G. Cerf | TCP/IP | `vinton-g-cerf` |
| 2004 | Robert E. Kahn | Internet foundation | `robert-e-kahn` |
| 2003 | Alan Kay | Object-oriented/Smalltalk | `alan-kay` |
| 2002 | Ronald L. Rivest | RSA encryption | `ronald-l-rivest` |
| 2002 | Adi Shamir | RSA encryption | `adi-shamir` |
| 2002 | Leonard M. Adleman | RSA encryption | `leonard-m-adleman` |
| 2001 | Ole-Johan Dahl | Object-oriented | `ole-johan-dahl` |
| 2001 | Kristen Nygaard | Simula/OO | `kristen-nygaard` |
| 2000 | Andrew Chi-Chih Yao | Computational theory | `andrew-chi-chih-yao` |
| 1999 | Frederick P. Brooks | Software engineering | `frederick-p-brooks` |
| 1998 | Jim Gray | Database/transaction processing | `jim-gray` |
| 1997 | Douglas Engelbart | Interactive computing | `douglas-engelbart` |
| 1996 | Amir Pnueli | Temporal logic | `amir-pnueli` |
| 1995 | Manuel Blum | Computational complexity | `manuel-blum` |
| 1994 | Edward A. Feigenbaum | Expert systems | `edward-a-feigenbaum` |
| 1994 | Raj Reddy | Large-scale AI systems | `raj-reddy` |
| 1993 | Juris Hartmanis | Computational complexity | `juris-hartmanis` |
| 1993 | Richard E. Stearns | Computational complexity | `richard-e-stearns` |
| 1992 | Butler W. Lampson | Distributed/personal computing | `butler-w-lampson` |
| 1991 | Robin Milner | ML/LCF/pi-calculus | `robin-milner` |
| 1990 | Fernando J. Corbato | Time-sharing systems | `fernando-j-corbato` |
| 1989 | William Kahan | Numerical analysis | `william-kahan` |
| 1988 | Ivan Sutherland | Computer graphics | `ivan-sutherland` |
| 1987 | John Cocke | RISC architecture | `john-cocke` |
| 1986 | John Hopcroft | Algorithms/data structures | `john-hopcroft` |
| 1986 | Robert Tarjan | Graph algorithms | `robert-tarjan` |
| 1985 | Richard M. Karp | Algorithms/complexity | `richard-m-karp` |
| 1984 | Niklaus Wirth | Pascal/Modula/Oberon | `niklaus-wirth` |
| 1983 | Ken Thompson | Unix/C | `ken-thompson` |
| 1983 | Dennis Ritchie | C language/Unix | `dennis-ritchie` |
| 1982 | Stephen A. Cook | NP-completeness theory | `stephen-a-cook` |
| 1981 | Edgar F. Codd | Relational databases | `edgar-f-codd` |
| 1980 | C.A.R. Hoare | Hoare logic/Quicksort | `car-hoare` |
| 1979 | Kenneth E. Iverson | APL language | `kenneth-e-iverson` |
| 1978 | Robert W. Floyd | Program verification/algorithms | `robert-w-floyd` |
| 1977 | John Backus | Fortran/FP language | `john-backus` |
| 1976 | Michael O. Rabin | Automata/algorithms | `michael-o-rabin` |
| 1976 | Dana S. Scott | Semantics | `dana-s-scott` |
| 1975 | Allen Newell | AI/cognitive science | `allen-newell` |
| 1975 | Herbert A. Simon | Artificial intelligence | `herbert-a-simon` |
| 1974 | Donald E. Knuth | Algorithms/TAOCP | `donald-e-knuth` |
| 1973 | Charles W. Bachman | Database/IDS | `charles-w-bachman` |
| 1972 | Edsger W. Dijkstra | Structured programming | `edsger-w-dijkstra` |
| 1971 | John McCarthy | LISP/AI | `john-mccarthy` |
| 1970 | James H. Wilkinson | Numerical analysis | `james-h-wilkinson` |
| 1969 | Marvin Minsky | Artificial intelligence | `marvin-minsky` |
| 1968 | Richard W. Hamming | Error-correcting codes | `richard-w-hamming` |
| 1967 | Maurice V. Wilkes | EDSAC/microprogramming | `maurice-v-wilkes` |
| 1966 | Alan J. Perlis | Compilers/ALGOL | `alan-j-perlis` |

### By Thinking Type (Quick Match)

| Thinking Type | Laureates | Keywords |
|--------------|-----------|---------|
| 🔥 Contrarian Persistence | Hinton, Bachman, Dijkstra | Denied, lonely, persistent |
| 🔬 Extreme Observation | Hamming, Minsky, Sutherland | Seeing what others miss |
| 🧩 Interdisciplinary Grafting | Simon/Newell, Sutton/Barto, Rabin | Tool migration, domain crossing |
| ⏳ Long-term Deep Work | Knuth, Iverson, Sutherland | Niche, patience, accumulation |
| ⚡ Technology-Driven Breakthrough | Cook, Karp, Bengio/Hinton/LeCun | New methods → new discoveries |
| 🤝 Collaborative Paradigm | Thompson/Ritchie, Cerf/Kahn, Aho/Ullman | Shared awards, complementary collaboration |
| 📐 Systems Thinking | Lamport, Liskov, Brooks | Complex systems, multiple factors |
| ⚖️ Ethical Controversy | Hinton (AI risk), Berners-Lee (Web openness) | Technology as double-edged sword, moral boundaries |
| 🌍 Global Impact | Berners-Lee, Metcalfe, Diffie/Hellman | Internet, cryptography普及 |
| 👩‍💻 Women Pioneers | Allen, Liskov, Goldwasser | Compilers, distributed, cryptography |

---

## Activating Cognitive Frameworks

After reading a specified laureate's SKILL.md, activate according to these rules:

1. **Identity Substitution**: Adjust tone according to the identity card and expression DNA in SKILL.md
2. **Framework Loading**: Analyze the user's problem using mental models and decision heuristics
3. **Honest Boundaries**: Must state what the framework cannot do
4. **Source Attribution**: Let users know which laureate's which model was used in the analysis

### Multi-Perspective Analysis Mode

You can simultaneously activate multiple laureates to examine the same problem from different angles:

```
User: "Should I pursue theoretical breakthroughs or engineering implementation?"

→ Knuth's Perspective: Integration of theory and practice (TAOCP + TeX)
→ Thompson's Perspective: Get it working first, theory follows
→ Dijkstra's Perspective: Engineering without theoretical guidance is dangerous
→ Comprehensive Suggestion: Convergence and divergence of three perspectives
```

---

## Deep Research Materials

Each laureate directory contains complete research infrastructure:

```
[laureate-name]/
├── SKILL.md                    # Core cognitive framework (thinking operating system)
├── SKILL-en.md                 # English version
├── SKILL-cn.md                 # Chinese version
├── research/
│   ├── 01-biography.md        # Life and academic trajectory
│   ├── 02-science.md          # Core scientific contributions
│   ├── 03-collaborators.md    # Key collaborators and influences
│   ├── 04-ethics.md           # Ethical views and controversies
│   ├── 05-legacy.md           # Legacy and impact
│   └── 06-papers.md           # Key paper analysis
└── references/research/
    ├── 01-writings.md         # Writings and systematic thinking
    ├── 02-conversations.md    # Interviews and dialogues
    ├── 03-expression-dna.md   # Expression DNA analysis
    ├── 04-external-views.md  # External perspectives
    ├── 05-decisions.md        # Key decision analysis
    └── 06-timeline.md         # Detailed timeline
```

---

## Distilling New Laureates

When distilling a new laureate, follow this standard process:

### Information Source Priority

| Source Type | Reveals What | Weight |
|------------|--------------|--------|
| ACM official (amturing.acm.org) | Systematic thinking + official narrative | Highest |
| Laureate's personal website/blog | Real thinking process + values | Highest |
| Original papers/technical reports | Methodology + reasoning process | High |
| Technical interviews (SE Radio/ACM Queue) | Improvised thinking + engineering judgment | High |
| Authoritative media (CACM/Nature/Science) | External perspective + technical impact | Medium |
| Technical biographies (MIT Press, etc.) | In-depth analysis + historical context | Medium |

### Information Source Blacklist (Always Excluded)

- Zhihu
- WeChat public accounts
- Baidu Baike
- Unverified technical gossip

### Distillation Process

1. **Phase 0A**: Confirm laureate identity and achievements
2. **Phase 1**: Prioritize ACM official and personal sources
3. **Directory naming**: `[first-name]-[last-name]` (all lowercase, hyphen-separated)
4. **Directory location**: `[laureate-name]/`
5. **Upon completion**: Update the laureate index in this SKILL.md

### Special Handling

- **Deceased laureates**: Stable sources but possible biographical bias
- **Chinese laureates** (Andrew Yao): Chinese context expression should be marked as simulated
- **Controversial laureates**: Record controversies factually
- **Recent laureates**: May have insufficient information; mark information density

---

## Information Quality Notes

- **Primary source ratio**: Most >50%
- **Strict blacklist enforcement**: Zero Zhihu/WeChat/Baidu Baike
- **Honest boundaries**: Laureates with insufficient information are clearly marked
- **Controversy inclusion**: Hinton's AI risk warnings, Ritchie's reflections on C language security, etc. are all recorded factually
- **Distillation date**: April 8, 2026

## Open Source License

Apache License 2.0

Copyright 2026 Yifan Yang

Licensed under the Apache License, Version 2.0.

## Extension Plans

- [x] Cover all 77 Turing Award laureates from 1966-2025
- [ ] Add more cross-domain cross-references
- [ ] Build technology timeline comparisons
- [ ] Add "What if XX met YY" cross-era dialogue simulation
