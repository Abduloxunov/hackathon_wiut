# Decisions and shared interfaces

Anything two parts of the code depend on (formats, function signatures, file paths, data links) goes here.

| Date/time | Decision | By |
|---|---|---|
| Sun 11 Oct 02:20 | **CarDoctor — multimodal (visual + text) RAG** is the final product. Three modes: used-car buying check, fleet triage, breakdown/accident assistance. DriveCoach and the road map are future modules. Recorded from the lead's [final pick](../ideas/FINAL-PICK.md) and [research dossier](RESEARCH.md#5-final-decision). | Davlatyor + claude-1 |
| Sun 11 Oct 02:20 | Planned architecture: visual reference retrieval + sourced text repair retrieval → evidence-backed explanation → workshop matching/map. Initial assignments at 02:20: Davlatyor + claude-1 implementation, Muhammadjon photos/measurements, Bexruz KB/pitch. The 02:40 ownership update below supersedes development/deck ownership. | Davlatyor + claude-1 |
| Sun 11 Oct 02:40 | Davlatyor builds CarDoctor with his own Codex (`dav/` branches). claude-1 reviews methods and implementation risks and handles the pitch; it does not write product code. Bexruz retains KB work and coordinates pitch support with claude-1. Recorded from the lead's message in [team.md](team.md). | Davlatyor + claude-1 |

## Shared interfaces

No CarDoctor API or data schema has been approved here yet. The developer must record concrete interfaces before other parts depend on them. The earlier RoadProof strategy does not define CarDoctor's interface.
