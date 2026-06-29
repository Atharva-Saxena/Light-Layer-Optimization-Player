def triage(prompt):
    prompt = sanitize(prompt)
    intent, c_intent = intent_classify(prompt)
    clarity = clarity_score(prompt, intent, c_intent)
    complexity = complexity_estimate(prompt, intent)

    if clarity > 0.8 and complexity < LIGHT_THRESHOLD:
        # light resolve so use cached answer or small model
        answer = light_resolver(prompt, intent)
        if answer.confident: return answer
    if clarity < CLARITY_ASK_THRESHOLD:
        # Ask one clarifying question (checked by micro-LLM or template idk)
        question = generate_clarifying_question(prompt, intent)
        return Clarify(question)
    if intent == 'code' and code_sanity_fails(prompt):
        # ask the user what they want. full implementation or pseudocode
        return Clarify("Do you want full runnable code or pseudocode and explanation?")
    # else enrich and escalate
    enriched_prompt = enrich_prompt(prompt, intent, context_snippets)
    return EscalateToLLM(enriched_prompt)
