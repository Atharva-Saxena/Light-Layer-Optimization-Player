def handle_request(prompt, session):
    clean_prompt = sanitize(prompt)
    intent, c = classify_intent(clean_prompt)
    clarity = compute_clarity(clean_prompt, intent, c)
    sim_result = semantic_retriever(clean_prompt)
    if sim_result.similarity > 0.92:
        return sim_result.answer, "cached"
    if clarity < 0.6:
        clar_q = generate_clarifier(clean_prompt, intent)
        return {"action":"clarify","question":clar_q}
    est_cost = estimate_complexity(clean_prompt, intent)
    if clarity > 0.8 and est_cost < LIGHT_THRESHOLD:
        ans = light_resolver(clean_prompt, intent)
        if ans.confident: return ans, "light"
    enriched = enrich_prompt(clean_prompt, session, top_k_context)
    response = heavy_llm_generate(enriched)
    verified = verifier(response)
    if not verified.ok:
        return {"action":"clarify","question":"I need a bit more info to be sure..."}
    return response, "heavy"
