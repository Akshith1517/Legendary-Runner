import os

# Get the folder where this script is running
folder = os.path.dirname(__file__)

print("\n--- FILE DIAGNOSTIC TOOL ---")
print(f"Checking folder: {folder}")

# The files the game NEEDS to find
required_files = [
    "background.png", 
    "player_walk1.png", 
    "player_walk2.png",
    "enemy.png",
    "rock.png",
    "bird.png"
]

print("\n--- MISSING FILES ---")
missing_count = 0
for filename in required_files:
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        print(f"❌ MISSING: {filename}")
        missing_count += 1
    else:
        print(f"✅ FOUND:   {filename}")

if missing_count > 0:
    print("\n--- FOUND THESE SIMILAR FILES ---")
    # Show ALL files in the folder so we can spot the mistake
    all_files = os.listdir(folder)
    for f in all_files:
        if "back" in f or "player" in f or "bird" in f:
            print(f" - {f}")

print("\n----------------------------")