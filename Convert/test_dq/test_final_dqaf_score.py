import pandas as pd

from Convert.rules.calculate_dqaf_scores import calculate_dqaf_scores
from Convert.test_data_generation.data_generation_dqaf_scoring_test import generate_full_dqaf_test_data

def test_final_dqaf_score_from_excel():
    """
    This function does three things:
    1. Reads scoring weights from an Excel file.
    2. Creates test data (3 observations).
    3. Calculates DQAF score and prints result table + FFP class for each observation.
    """

    # Step 1: Read Excel file to get weights for each outcome
    df = pd.read_excel("assertions_score_weighting_definition.xlsx")  # File must be in same folder
    weights_dict = {
        str(row['Data quality assertion']).strip(): float(row['BDR_General_Weight'])
        for _, row in df.iterrows()
        if pd.notna(row['Data quality assertion']) and pd.notna(row['BDR_General_Weight'])
    }

    # Step 2: Generate test results (obs1, obs2, obs3 with many outcomes)
    rdf_data = generate_full_dqaf_test_data()

    # Step 3: Apply scoring logic using the weight file
    scores = calculate_dqaf_scores(rdf_data, weights_dict)

    # Step 4: Make result table
    df_out = pd.DataFrame(scores)

    # Print full table with all info
    print("\n=== Full Scoring Results ===")
    print(df_out)

    # Print just FFP class per observation
    print("\n=== FFP Category Summary ===")
    for _, row in df_out.iterrows():
        print(f"{row['Observation']}: {row['FFP Category']}")

    return df_out

# Run this file directly
if __name__ == "__main__":
    test_final_dqaf_score_from_excel()
