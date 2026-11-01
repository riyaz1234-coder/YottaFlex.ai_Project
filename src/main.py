from generate_data import generate_synthetic_data
from pipeline import execute_pipeline

if __name__ == "__main__":
    print("--- Step 1: Generating Data ---")
    generate_synthetic_data()
    print("\n--- Step 2: Executing Pipeline ---")
    execute_pipeline()