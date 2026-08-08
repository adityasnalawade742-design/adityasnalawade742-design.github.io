import shutil
from pathlib import Path

repo_cand = Path('scratch/B0BPM41R5C_candidates')
art_cand = Path(r'C:\Users\adity\.gemini\antigravity-cli\brain\663690f5-e7a9-486f-8df0-99811c14b2b0\scratch\B0BPM41R5C_candidates')
art_cand.mkdir(parents=True, exist_ok=True)

files = list(repo_cand.glob('*.jpg'))
for f in files:
    shutil.copy(f, art_cand / f.name)

print(f"Synced {len(files)} candidate photos to artifact directory.")
