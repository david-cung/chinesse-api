# master_seed.py
import subprocess
import sys
import os

def run_script(script_path):
    print(f"\n" + "="*80)
    print(f"RUNNING: {script_path}")
    print("="*80)
    try:
        # Add current directory to PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd() + ":" + env.get("PYTHONPATH", "")
        
        # Use sys.executable to ensure we use the same python interpreter (venv)
        result = subprocess.run([sys.executable, script_path], check=True, text=True, env=env)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}: {e}")
        return False

def main():
    scripts = [
        "seed/seed_data.py",                # Basic setup + Lesson 1
        "seed/seed_hsk1_new_lessons.py",    # 10 more HSK 1 lessons
        "seed/seed_hsk234_lessons.py",      # Initial HSK 2-4 lesson shells
        "seed/seed_hsk_all_levels.py",      # HSK 2-5 lessons (14 per level)
        "seed/seed_self_introduction.py",   # Detailed Lesson 2
        "seed/seed_numbers_counting.py",    # Detailed Lesson 3
        "seed/seed_family_members.py",      # Detailed Lesson 4
        "seed/seed_hsk2_all_details.py",    # Full details for HSK 2
        "seed/seed_vocabulary_examples.py"  # General enrichment
    ]

    for script in scripts:
        if not os.path.exists(script):
            print(f"⚠️ Warning: {script} not found, skipping...")
            continue
            
        success = run_script(script)
        if not success:
            print(f"🛑 Mission aborted due to failure in {script}")
            sys.exit(1)

    print("\n" + "="*80)
    print("✨ ALL SEEDING SCRIPTS COMPLETED SUCCESSFULLY! ✨")
    print("="*80)

if __name__ == "__main__":
    main()
