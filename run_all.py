import os
import sys
import subprocess
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent
SONG_LYRICS = ROOT / "song_lyrics.csv"
SPOTIFY_WITH_LYRICS = ROOT / "spotify_with_lyrics.csv"
SPOTIFY_WITH_SENT = ROOT / "spotify_with_lyrics_and_sentiment.csv"

def run_step(name: str, cmd: list[str]) -> None:
    """Run a shell command as one pipeline step."""
    print(f"\n========== {name} ==========")
    print("Command:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"\n[ERROR] Step '{name}' failed with code {result.returncode}.")
        sys.exit(result.returncode)
    print(f"[OK] {name} completed.\n")

def main() -> None:
    # 0. Basic checks
    print("Running full pipeline from project root:", ROOT)

    if not SONG_LYRICS.exists():
        print(
            "\n[ERROR] song_lyrics.csv not found at:\n"
            f"    {SONG_LYRICS}\n\n"
            "Download it from Kaggle / Box and place it in the project root "
            "before running the pipeline."
        )
        sys.exit(1)

    # 1. Collect + clean + integrate
    run_step(
        "Step 1: Collect & clean data (Spotify + lyrics)",
        [sys.executable, "collect_and_clean_dataset.py"],
    )

    if not SPOTIFY_WITH_LYRICS.exists():
        print(
            "\n[ERROR] Expected output spotify_with_lyrics.csv not found at:\n"
            f"    {SPOTIFY_WITH_LYRICS}\n"
            "Check collect_and_clean_dataset.py for errors."
        )
        sys.exit(1)

    # 2. Sentiment analysis
    run_step(
        "Step 2: Sentiment analysis",
        [sys.executable, "sentiment_analysis.py"],
    )

    if not SPOTIFY_WITH_SENT.exists():
        print(
            "\n[ERROR] Expected output spotify_with_lyrics_and_sentiment.csv "
            "not found at:\n"
            f"    {SPOTIFY_WITH_SENT}\n"
            "Check sentiment_analysis.py for errors."
        )
        sys.exit(1)

    # 3. Gendered language analysis
    run_step(
        "Step 3: Gendered language analysis",
        [sys.executable, "gendered_language_analysis.py"],
    )

    print("\n🎉 Pipeline finished successfully! All datasets and plots should be updated.\n")

if __name__ == "__main__":
    main()
