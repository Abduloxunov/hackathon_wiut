# Vector retrieval development results — 11 October 2026

These are 20 hand-authored development queries against the same 28 known KB records. They are not held-out cases, mechanic-reviewed diagnoses or an estimate of real-world accuracy. Expected IDs express a candidate we intended to retrieve; an ID appearing in the first three does not establish diagnosis or top-1 correctness. Uzbek/Russian wording needs native review.

The actual pinned multilingual E5 model and persistent local Qdrant store were used, on CPU. Synthetic-vector engineering tests are documented separately.

## Actual index

```json
{
  "collection": "cardoctor_text_e5_small_v1",
  "model_id": "intfloat/multilingual-e5-small",
  "revision": "614241f622f53c4eeff9890bdc4f31cfecc418b3",
  "dimension": 384,
  "content_hash": "1b7dd4008462ddd63f87ec6c14beeb11e07854bb29dbd53d199efd77e4498738",
  "record_count": 28,
  "inserted": 0,
  "updated": 28,
  "removed": 0,
  "max_passage_tokens": 269,
  "ingest_seconds": 4.364,
  "device": "cpu"
}
```

## Development query comparison

| Case | Keyword candidates | Semantic candidates | Hybrid candidates | Hybrid status | Expected candidate/status check |
|---|---|---|---|---|---|
| Tyre outward bubble | K012, K014 | K012, K013 | K012, K014, K013 | candidates_found | Matched |
| Tyre inward dip | K013, K009 | K013, K012, K014 | K013, K012, K014 | candidates_found | Matched |
| Front glass chip | K006 | K006 | K006 | candidates_found | Matched |
| Nail in tread | K010 | K010 | K010 | candidates_found | Matched |
| Misty headlight | K027, K028 | K028 | K028 | candidates_found | Matched |
| Paint scratch with unknown depth | K002 | K002, K001 | K002, K001 | candidates_found | Matched |
| Split bumper | K003, K004 | K004, K003 | K004, K003 | candidates_found | Matched |
| Green puddle | K017 | K017 | K017 | candidates_found | Matched |
| Flooded EV | K019, K020 | K020 | K020, K019 | candidates_found | Matched |
| Confirmed Cobalt running-engine warning | K021 | K021 | K021 | candidates_found | Matched |
| Russian tyre protrusion | None | None | None | no_evidence | Needs review |
| Uzbek tyre protrusion | K011, K012 | None | K012, K011 | candidates_found | Matched |
| Russian lamp mist | K027, K028 | None | K028, K027 | candidates_found | Matched |
| Unrelated licensing question | None | None | None | no_evidence | Matched |
| Unrelated nonsense | None | None | None | no_evidence | Matched |
| Crack with no component | None | None | None | needs_context | Matched |
| Cobalt key-on photo only | None | None | None | needs_context | Matched |
| Lacetti parking-brake context missing | None | None | None | needs_context | Matched |
| Gentra is not Lacetti | None | None | None | no_evidence | Matched |
| Unknown BYD propulsion | None | None | None | needs_context | Matched |

## Repeat ingestion

```json
{
  "collection": "cardoctor_text_e5_small_v1",
  "model_id": "intfloat/multilingual-e5-small",
  "revision": "614241f622f53c4eeff9890bdc4f31cfecc418b3",
  "dimension": 384,
  "content_hash": "1b7dd4008462ddd63f87ec6c14beeb11e07854bb29dbd53d199efd77e4498738",
  "record_count": 28,
  "inserted": 0,
  "updated": 28,
  "removed": 0,
  "max_passage_tokens": 269,
  "ingest_seconds": 4.175,
  "device": "cpu"
}
```

## Installed versions

```json
{
  "qdrant-client": "1.19.1",
  "sentence-transformers": "6.1.0",
  "transformers": "5.19.0",
  "huggingface-hub": "1.33.0",
  "numpy": "2.5.2",
  "torch": "2.14.0+cpu",
  "scipy": "1.18.1",
  "scikit-learn": "1.9.1",
  "tokenizers": "0.23.3"
}
```

## Full probe inputs and scores

Cosine and BM25/RRF scores are retrieval signals, not diagnostic probabilities. The default cosine gate is an initial heuristic, not a validated threshold. Hybrid retrieval may retain a candidate with lexical support even below that gate.

### Tyre outward bubble

```json
{
  "title": "Tyre outward bubble",
  "query": "There is a bubble sticking out of the rubber near the wheel.",
  "context": {
    "part": "tire"
  },
  "expected": [
    "K012"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K012",
    "K014"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K012",
      "K013"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 26.9661,
    "scores": [
      {
        "record_id": "K012",
        "cosine": 0.82246,
        "bm25": 1.75089,
        "rank_score": 0.822456,
        "scope_allowed": true
      },
      {
        "record_id": "K013",
        "cosine": 0.80067,
        "bm25": 0,
        "rank_score": 0.800675,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K012",
      "K014",
      "K013"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0617,
    "scores": [
      {
        "record_id": "K012",
        "cosine": 0.82246,
        "bm25": 1.75089,
        "rank_score": 0.032787,
        "scope_allowed": true
      },
      {
        "record_id": "K014",
        "cosine": 0.7988,
        "bm25": 1.75089,
        "rank_score": 0.032002,
        "scope_allowed": true
      },
      {
        "record_id": "K013",
        "cosine": 0.80067,
        "bm25": 0,
        "rank_score": 0.016129,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Tyre inward dip

```json
{
  "title": "Tyre inward dip",
  "query": "There is a hollow inward dip in the side of the tyre.",
  "context": {
    "part": "tire"
  },
  "expected": [
    "K013"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K013",
    "K009"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K013",
      "K012",
      "K014"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0562,
    "scores": [
      {
        "record_id": "K013",
        "cosine": 0.8373,
        "bm25": 2.74915,
        "rank_score": 0.837296,
        "scope_allowed": true
      },
      {
        "record_id": "K012",
        "cosine": 0.82512,
        "bm25": 0,
        "rank_score": 0.825125,
        "scope_allowed": true
      },
      {
        "record_id": "K014",
        "cosine": 0.81099,
        "bm25": 0,
        "rank_score": 0.810986,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K013",
      "K012",
      "K014"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0536,
    "scores": [
      {
        "record_id": "K013",
        "cosine": 0.8373,
        "bm25": 2.74915,
        "rank_score": 0.032787,
        "scope_allowed": true
      },
      {
        "record_id": "K012",
        "cosine": 0.82512,
        "bm25": 0,
        "rank_score": 0.016129,
        "scope_allowed": true
      },
      {
        "record_id": "K014",
        "cosine": 0.81099,
        "bm25": 0,
        "rank_score": 0.015873,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Front glass chip

```json
{
  "title": "Front glass chip",
  "query": "A stone left a small chip in the front glass.",
  "context": {
    "part": "windshield"
  },
  "expected": [
    "K006"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K006"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K006"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0515,
    "scores": [
      {
        "record_id": "K006",
        "cosine": 0.81107,
        "bm25": 3.15653,
        "rank_score": 0.811067,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K006"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0525,
    "scores": [
      {
        "record_id": "K006",
        "cosine": 0.81107,
        "bm25": 3.15653,
        "rank_score": 0.032787,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Nail in tread

```json
{
  "title": "Nail in tread",
  "query": "A nail is stuck in the tread.",
  "context": {
    "part": "tire"
  },
  "expected": [
    "K010"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K010"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K010"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0525,
    "scores": [
      {
        "record_id": "K010",
        "cosine": 0.81933,
        "bm25": 3.94664,
        "rank_score": 0.819326,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K010"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0487,
    "scores": [
      {
        "record_id": "K010",
        "cosine": 0.81933,
        "bm25": 3.94664,
        "rank_score": 0.032787,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Misty headlight

```json
{
  "title": "Misty headlight",
  "query": "The headlight looks misty inside after rain.",
  "context": {
    "part": "lamp"
  },
  "expected": [
    "K028"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K027",
    "K028"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K028"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0506,
    "scores": [
      {
        "record_id": "K028",
        "cosine": 0.8076,
        "bm25": 0,
        "rank_score": 0.807596,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K028"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0491,
    "scores": [
      {
        "record_id": "K028",
        "cosine": 0.8076,
        "bm25": 0,
        "rank_score": 0.016393,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Paint scratch with unknown depth

```json
{
  "title": "Paint scratch with unknown depth",
  "query": "Paint has a thin scratch on the door.",
  "context": {
    "part": "body"
  },
  "expected": [
    "K001",
    "K002"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K002"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K002",
      "K001"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.046,
    "scores": [
      {
        "record_id": "K002",
        "cosine": 0.83553,
        "bm25": 3.19153,
        "rank_score": 0.835534,
        "scope_allowed": true
      },
      {
        "record_id": "K001",
        "cosine": 0.81995,
        "bm25": 1.38927,
        "rank_score": 0.819951,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K002",
      "K001"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0443,
    "scores": [
      {
        "record_id": "K002",
        "cosine": 0.83553,
        "bm25": 3.19153,
        "rank_score": 0.032787,
        "scope_allowed": true
      },
      {
        "record_id": "K001",
        "cosine": 0.81995,
        "bm25": 1.38927,
        "rank_score": 0.032258,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Split bumper

```json
{
  "title": "Split bumper",
  "query": "The plastic bumper is split.",
  "context": {
    "part": "body"
  },
  "expected": [
    "K004"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K003",
    "K004"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K004",
      "K003"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0444,
    "scores": [
      {
        "record_id": "K004",
        "cosine": 0.84327,
        "bm25": 2.46935,
        "rank_score": 0.843271,
        "scope_allowed": true
      },
      {
        "record_id": "K003",
        "cosine": 0.8406,
        "bm25": 2.55104,
        "rank_score": 0.840596,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K004",
      "K003"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0442,
    "scores": [
      {
        "record_id": "K004",
        "cosine": 0.84327,
        "bm25": 2.46935,
        "rank_score": 0.032522,
        "scope_allowed": true
      },
      {
        "record_id": "K003",
        "cosine": 0.8406,
        "bm25": 2.55104,
        "rank_score": 0.032522,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Green puddle

```json
{
  "title": "Green puddle",
  "query": "A green puddle is under my car.",
  "context": {
    "part": "fluid"
  },
  "expected": [
    "K017"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K017"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K017"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0472,
    "scores": [
      {
        "record_id": "K017",
        "cosine": 0.80042,
        "bm25": 1.95204,
        "rank_score": 0.800424,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K017"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0486,
    "scores": [
      {
        "record_id": "K017",
        "cosine": 0.80042,
        "bm25": 1.95204,
        "rank_score": 0.032787,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Flooded EV

```json
{
  "title": "Flooded EV",
  "query": "The electric car was partly underwater.",
  "context": {
    "part": "ev",
    "propulsion": "ev"
  },
  "expected": [
    "K020"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K019",
    "K020"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K020"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.046,
    "scores": [
      {
        "record_id": "K020",
        "cosine": 0.80297,
        "bm25": 0.19457,
        "rank_score": 0.802966,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K020",
      "K019"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0452,
    "scores": [
      {
        "record_id": "K020",
        "cosine": 0.80297,
        "bm25": 0.19457,
        "rank_score": 0.032787,
        "scope_allowed": true
      },
      {
        "record_id": "K019",
        "cosine": 0.7617,
        "bm25": 0.17153,
        "rank_score": 0.032258,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Confirmed Cobalt running-engine warning

```json
{
  "title": "Confirmed Cobalt running-engine warning",
  "query": "The oil pressure light stays on after the motor starts.",
  "context": {
    "part": "dashboard",
    "vehicle": "Cobalt",
    "confirmed_manual": "S11",
    "context": {
      "engine_running": true
    }
  },
  "expected": [
    "K021"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K021"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "candidates_found",
    "ids": [
      "K021"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0476,
    "scores": [
      {
        "record_id": "K021",
        "cosine": 0.84664,
        "bm25": 0.88241,
        "rank_score": 0.84664,
        "scope_allowed": true
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K021"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0514,
    "scores": [
      {
        "record_id": "K021",
        "cosine": 0.84664,
        "bm25": 0.88241,
        "rank_score": 0.032787,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Russian tyre protrusion

```json
{
  "title": "Russian tyre protrusion",
  "query": "На боковине шины появилась выпуклая шишка.",
  "context": {
    "part": "tire"
  },
  "expected": [
    "K012"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [],
  "keyword_status": "no_evidence",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": false,
    "seconds": 0.0537,
    "scores": [
      {
        "record_id": "K011",
        "cosine": 0.78909,
        "accepted": false
      },
      {
        "record_id": "K012",
        "cosine": 0.78324,
        "accepted": false
      },
      {
        "record_id": "K009",
        "cosine": 0.77834,
        "accepted": false
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": false,
    "seconds": 0.0538,
    "scores": [
      {
        "record_id": "K011",
        "cosine": 0.78909,
        "accepted": false
      },
      {
        "record_id": "K012",
        "cosine": 0.78324,
        "accepted": false
      },
      {
        "record_id": "K009",
        "cosine": 0.77834,
        "accepted": false
      }
    ],
    "questions": []
  }
}
```

### Uzbek tyre protrusion

```json
{
  "title": "Uzbek tyre protrusion",
  "query": "Shinaning yon tomonida tashqariga shish chiqdi.",
  "context": {
    "part": "tire"
  },
  "expected": [
    "K012"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K011",
    "K012"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": false,
    "seconds": 0.0507,
    "scores": [
      {
        "record_id": "K009",
        "cosine": 0.75733,
        "accepted": false
      },
      {
        "record_id": "K013",
        "cosine": 0.75684,
        "accepted": false
      },
      {
        "record_id": "K012",
        "cosine": 0.75613,
        "accepted": false
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K012",
      "K011"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0503,
    "scores": [
      {
        "record_id": "K012",
        "cosine": 0.75613,
        "bm25": 1.75089,
        "rank_score": 0.032522,
        "scope_allowed": true
      },
      {
        "record_id": "K011",
        "cosine": 0.73969,
        "bm25": 1.86326,
        "rank_score": 0.032522,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Russian lamp mist

```json
{
  "title": "Russian lamp mist",
  "query": "Фара запотевает изнутри после дождя.",
  "context": {
    "part": "lamp"
  },
  "expected": [
    "K028"
  ],
  "expected_status": "candidates_found",
  "keyword_ids": [
    "K027",
    "K028"
  ],
  "keyword_status": "evidence_found",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": false,
    "seconds": 0.0443,
    "scores": [
      {
        "record_id": "K028",
        "cosine": 0.78755,
        "accepted": false
      },
      {
        "record_id": "K027",
        "cosine": 0.76354,
        "accepted": false
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "candidates_found",
    "ids": [
      "K028",
      "K027"
    ],
    "expected_candidate_in_top3": true,
    "seconds": 0.0477,
    "scores": [
      {
        "record_id": "K028",
        "cosine": 0.78755,
        "bm25": 0.17914,
        "rank_score": 0.032522,
        "scope_allowed": true
      },
      {
        "record_id": "K027",
        "cosine": 0.76354,
        "bm25": 0.18562,
        "rank_score": 0.032522,
        "scope_allowed": true
      }
    ],
    "questions": []
  }
}
```

### Unrelated licensing question

```json
{
  "title": "Unrelated licensing question",
  "query": "How do I renew my driving licence?",
  "context": {
    "part": "body"
  },
  "expected": [],
  "expected_status": "no_evidence",
  "keyword_ids": [],
  "keyword_status": "no_evidence",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0414,
    "scores": [
      {
        "record_id": "K005",
        "cosine": 0.78942,
        "accepted": false
      },
      {
        "record_id": "K002",
        "cosine": 0.7784,
        "accepted": false
      },
      {
        "record_id": "K001",
        "cosine": 0.77801,
        "accepted": false
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.043,
    "scores": [
      {
        "record_id": "K005",
        "cosine": 0.78942,
        "accepted": false
      },
      {
        "record_id": "K002",
        "cosine": 0.7784,
        "accepted": false
      },
      {
        "record_id": "K001",
        "cosine": 0.77801,
        "accepted": false
      }
    ],
    "questions": []
  }
}
```

### Unrelated nonsense

```json
{
  "title": "Unrelated nonsense",
  "query": "quantum banana spaceship",
  "context": {
    "part": "body"
  },
  "expected": [],
  "expected_status": "no_evidence",
  "keyword_ids": [],
  "keyword_status": "no_evidence",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0494,
    "scores": [
      {
        "record_id": "K003",
        "cosine": 0.75321,
        "accepted": false
      },
      {
        "record_id": "K001",
        "cosine": 0.74565,
        "accepted": false
      },
      {
        "record_id": "K005",
        "cosine": 0.73822,
        "accepted": false
      }
    ],
    "questions": []
  },
  "hybrid": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0485,
    "scores": [
      {
        "record_id": "K003",
        "cosine": 0.75321,
        "accepted": false
      },
      {
        "record_id": "K001",
        "cosine": 0.74565,
        "accepted": false
      },
      {
        "record_id": "K005",
        "cosine": 0.73822,
        "accepted": false
      }
    ],
    "questions": []
  }
}
```

### Crack with no component

```json
{
  "title": "Crack with no component",
  "query": "crack",
  "context": {},
  "expected": [],
  "expected_status": "needs_context",
  "keyword_ids": [],
  "keyword_status": "needs_context",
  "semantic": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": null,
    "scores": [],
    "questions": [
      "Which component is affected? Confirm it before component-specific retrieval."
    ]
  },
  "hybrid": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": null,
    "scores": [],
    "questions": [
      "Which component is affected? Confirm it before component-specific retrieval."
    ]
  }
}
```

### Cobalt key-on photo only

```json
{
  "title": "Cobalt key-on photo only",
  "query": "oil pressure warning",
  "context": {
    "part": "dashboard",
    "vehicle": "Cobalt",
    "confirmed_manual": "S11",
    "context": {
      "engine_running": false
    }
  },
  "expected": [],
  "expected_status": "needs_context",
  "keyword_ids": [],
  "keyword_status": "needs_context",
  "semantic": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0498,
    "scores": [
      {
        "record_id": "K021",
        "cosine": 0.89871,
        "bm25": 1.33448,
        "rank_score": 0.89871,
        "scope_allowed": false
      }
    ],
    "questions": [
      "Is the warning still present with the engine running? A key-on lamp check alone does not establish a fault."
    ]
  },
  "hybrid": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.045,
    "scores": [
      {
        "record_id": "K021",
        "cosine": 0.89871,
        "bm25": 1.33448,
        "rank_score": 0.032787,
        "scope_allowed": false
      }
    ],
    "questions": [
      "Is the warning still present with the engine running? A key-on lamp check alone does not establish a fault."
    ]
  }
}
```

### Lacetti parking-brake context missing

```json
{
  "title": "Lacetti parking-brake context missing",
  "query": "brake warning",
  "context": {
    "part": "dashboard",
    "vehicle": "Lacetti",
    "confirmed_manual": "S14",
    "context": {
      "engine_running": true
    }
  },
  "expected": [],
  "expected_status": "needs_context",
  "keyword_ids": [],
  "keyword_status": "needs_context",
  "semantic": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0402,
    "scores": [
      {
        "record_id": "K023",
        "cosine": 0.88539,
        "bm25": 1.54114,
        "rank_score": 0.885393,
        "scope_allowed": false
      },
      {
        "record_id": "K024",
        "cosine": 0.8402,
        "bm25": 0.29113,
        "rank_score": 0.840202,
        "scope_allowed": true
      }
    ],
    "questions": [
      "Is the parking brake fully released and the warning still present?"
    ]
  },
  "hybrid": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0441,
    "scores": [
      {
        "record_id": "K023",
        "cosine": 0.88539,
        "bm25": 1.54114,
        "rank_score": 0.032787,
        "scope_allowed": false
      },
      {
        "record_id": "K024",
        "cosine": 0.8402,
        "bm25": 0.29113,
        "rank_score": 0.032258,
        "scope_allowed": true
      }
    ],
    "questions": [
      "Is the parking brake fully released and the warning still present?"
    ]
  }
}
```

### Gentra is not Lacetti

```json
{
  "title": "Gentra is not Lacetti",
  "query": "brake warning",
  "context": {
    "part": "dashboard",
    "vehicle": "Gentra",
    "confirmed_manual": "S14",
    "context": {
      "engine_running": true,
      "parking_brake_released": true
    }
  },
  "expected": [],
  "expected_status": "no_evidence",
  "keyword_ids": [],
  "keyword_status": "no_evidence",
  "semantic": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": null,
    "scores": [],
    "questions": []
  },
  "hybrid": {
    "status": "no_evidence",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": null,
    "scores": [],
    "questions": []
  }
}
```

### Unknown BYD propulsion

```json
{
  "title": "Unknown BYD propulsion",
  "query": "battery crash",
  "context": {
    "part": "ev",
    "vehicle": "BYD Song"
  },
  "expected": [],
  "expected_status": "needs_context",
  "keyword_ids": [],
  "keyword_status": "needs_context",
  "semantic": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0424,
    "scores": [
      {
        "record_id": "K019",
        "cosine": 0.87161,
        "bm25": 1.08508,
        "rank_score": 0.871613,
        "scope_allowed": false
      },
      {
        "record_id": "K020",
        "cosine": 0.85371,
        "bm25": 0.19457,
        "rank_score": 0.853714,
        "scope_allowed": false
      }
    ],
    "questions": [
      "Is the vehicle EV, PHEV, HEV or combustion-only? Confirm the exact variant."
    ]
  },
  "hybrid": {
    "status": "needs_context",
    "ids": [],
    "expected_candidate_in_top3": true,
    "seconds": 0.0397,
    "scores": [
      {
        "record_id": "K019",
        "cosine": 0.87161,
        "bm25": 1.08508,
        "rank_score": 0.032787,
        "scope_allowed": false
      },
      {
        "record_id": "K020",
        "cosine": 0.85371,
        "bm25": 0.19457,
        "rank_score": 0.032258,
        "scope_allowed": false
      }
    ],
    "questions": [
      "Is the vehicle EV, PHEV, HEV or combustion-only? Confirm the exact variant."
    ]
  }
}
```

## Findings and limits

The English misty-headlight paraphrase retrieved K028 through embeddings when the original title/search-term keyword baseline found no record. Different outward-bubble and inward-dip descriptions retrieved different leading semantic candidates. This demonstrates behaviour on these known records, not diagnostic accuracy.

The Russian tyre-protrusion query was missed at the default threshold. The Uzbek tyre query and Russian lamp-mist query needed lexical support to include the expected candidate; semantic-only searches returned no candidate at that threshold. Lowering the threshold without separate evaluation can also accept unrelated queries.

An initial rank-fusion probe produced exact ties whose record-ID fallback put cosmetic bumper damage above split/crack damage. Equal fused ranks now preserve semantic ordering before lexical ordering and stable IDs. This engineering rule fixes the arbitrary ID preference; it is not a trained or validated reranker.

The depth-unknown paint query retains both scratch-depth records. Other candidate lists also include alternatives requiring follow-up rather than a single inferred repair recommendation. Native-language review, query rewriting and reranking should be tested on separate cases.

No LLM rewriting, LLM answer generation, automotive training, mechanic review or held-out accuracy evaluation was run.

## Reproduce

```powershell
D:\hakathon_wiut\.venv\Scripts\python.exe -B kb/probe_vector.py
```

This overwrites this development report and its ignored runtime audit file. No LLM, cloud database, paid compute or automotive training is used.

## Development timing context

In this recorded CPU probe process, the first timed query took **26.9661 seconds**, including model/index startup. The median of the remaining **35 timed query calls** was **0.0485 seconds** with the model reused in memory. These are local development timings on this machine, not a production latency benchmark; early-return cases without a recorded time are excluded. Repeated standalone CLI invocations pay startup costs again. A future product adapter should keep one store/model instance open.
