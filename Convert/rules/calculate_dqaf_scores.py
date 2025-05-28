def calculate_dqaf_scores(rdf_results, weights_dict):
    """
    Calculate DQAF score and assign quality level (FFP) for each observation.

    - rdf_results: a list of (observation_id, function_name, result_label)
    - weights_dict: a dictionary like {"function:label": weight_value}

    Returns a list of dictionaries with score, quality level, FFP category, and details.
    """

    def classify(score):
        # Simple classification based on normalized score
        if score >= 0.8:
            return "High Quality", "FFP1"
        elif score >= 0.5:
            return "Medium Quality", "FFP2"
        else:
            return "Low Quality", "FFP3"

    # Step 1: Find the highest weight for each function (used to normalize scores)
    max_weights_per_function = {}
    for key, weight in weights_dict.items():
        func = key.split(":")[0]
        if func not in max_weights_per_function:
            max_weights_per_function[func] = weight
        else:
            max_weights_per_function[func] = max(max_weights_per_function[func], weight)

    # Step 2: Group each function:label pair by observation
    from collections import defaultdict
    grouped = defaultdict(list)
    for obs, func, outcome in rdf_results:
        key = f"{func}:{outcome}"
        grouped[obs].append((func, key))

    results = []
    # Step 3: For each observation, calculate score
    for obs_id, items in grouped.items():
        # Total of actual weights for this observation
        actual_score = sum(weights_dict.get(k, 0.0) for (_, k) in items)
        # Maximum possible weight for those functions
        max_score = sum(max_weights_per_function.get(f, 1.0) for (f, _) in items)
        # Normalize score (divide actual by max)
        normalized_score = actual_score / max_score if max_score > 0 else 0.0

        # Get quality level and FFP based on score
        quality, ffp = classify(normalized_score)

        results.append({
            "Observation": obs_id,
            "Score": round(normalized_score, 3),
            "Quality Level": quality,
            "FFP Category": ffp,
            "Details": ", ".join(k for (_, k) in items)
        })

    return results
