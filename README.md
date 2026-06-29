# Prompt Triage Layer
Pre prompt processor, eliminate costly garbage output from faulty inputs. Its a buffer is all. 

Compression was the initial thought process but on running a metrics (chat gpt lol) expected outcomes were not so impactful so I pivoted to pre processing 
Prompt Triage Layer or PTL, an idea was born, it will prevent wasteful heavy work in the first by confirming user needs before the expensive step. Better ROI because the heavy model is invoked only when it’s truly needed and with a better input. This idea primarily came from langgraph and is still under brainstorming phase.

Will add token saving system prompts too (eliminating unneccesary salutations, idle chitchat and emotions : MAKE ROBOTS ROBOTS AGAIN!)





_I'll clear it with an example:_

User: “fix this code” (ambiguous, no code attached)

PTL: clarity low → clarify: “Please paste the code or describe the bug and the language.”

Result: user supplies code → heavy LLM produces correct patch.

User: “optimize sorting big data” (ambiguous about constraints)

PTL: intent=code/architecture, clarity medium → clarifier: “Is this memory or time constrained? Disk/streaming allowed?”

Result: enriched prompt yields targeted, useful answer.

User: “summarize sales data” + attached table

PTL: detect table + intent=summary, complexity low → call light summarizer (distilled model) and return summary without heavy LLM.


this is clarified version ig, AI suggested this:

**Tier 0** – Lightweight Query Reasoner (LQR)
Engages before the LLM.
Performs query hygiene: cleaning typos, disambiguating vagueness, asking clarifying questions, gauging intent.
Uses empirical heuristics and prompt gravitas scoring to determine if the input deserves full LLM computation.
If the query is incomplete, vague, or low-quality, it loops back to the user for refinement.

**Tier 1**– Heavy LLM Core
Activates only when the pre-layer flags the query as semantically rich and computation-worthy.
Performs full reasoning, synthesis, and generation.
