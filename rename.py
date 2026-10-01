import os
from pathlib import Path

def rename_qmd_files(start_dir=".", dry_run=True):
    """
    Find .qmd files case-insensitively and rename them to lowercase with hyphens.
    Works reliably on Windows.
    """
    start_path = Path(start_dir).resolve()

    print(f"📁 Starting from: {start_path}")
    if not start_path.exists():
        print(f"❌ Directory not found: {start_path}")
        return

    # Define lowercase extension set
    valid_extensions = {".qmd", ".QMD", ".Qmd", ".qMd", ".QmD"}  # All possible cases

    # Find all files with .qmd extension (case-insensitive)
    all_files = list(start_path.rglob("*"))
    qmd_files = [f for f in all_files if f.is_file() and f.suffix in valid_extensions]

    if not qmd_files:
        print("📭 No .qmd files found.")
        # Optional: list all files to debug
        sample = list(start_path.rglob("*"))[:10]
        print("📌 Sample of files in project:")
        for f in sample:
            print(f"  {f.relative_to(start_path)}")
        return

    print(f"🔍 Found {len(qmd_files)} .qmd file(s):\n")
    for f in qmd_files:
        print(f"📄 {f.relative_to(start_path)}")

    changes = []

    for file_path in qmd_files:
        old_name = file_path.name
        # Convert to desired format
        new_name = (
            old_name
            .lower()           # to lowercase
            .replace('_', '-') # underscores → hyphens
            .replace(' ', '-') # spaces → hyphens
            .strip('-')        # no leading/trailing hyphens
        )

        # Skip if already matches
        if old_name == new_name:
            continue

        new_path = file_path.parent / new_name

        # Handle conflicts
        suffix = 1
        temp_new_path = new_path
        while temp_new_path.exists():
            base, ext = new_name.rsplit('.', 1)
            temp_new_path = file_path.parent / f"{base}-copy{suffix}.{ext}"
            suffix += 1
        new_path = temp_new_path

        changes.append((file_path, new_path))
        print(f"🔄 Would rename: '{old_name}' → '{new_path.name}'")

    print(f"\n📋 Total renames planned: {len(changes)}\n")

    if len(changes) == 0:
        print("🎉 All filenames already match the target format!")
        return

    if dry_run:
        print("✅ This was a dry run. No files were changed.")
        print("To apply changes, set dry_run=False.")
        return

    # --- Perform renames ---
    print("🚀 Performing renames...\n")
    for old_path, new_path in changes:
        try:
            old_path.rename(new_path)
            print(f"✅ Renamed: '{old_path.name}' → '{new_path.name}'")
        except Exception as e:
            print(f"❌ Failed to rename '{old_path.name}': {e}")

    print(f"\n🎉 Done! {len(changes)} file(s) renamed successfully.")


# ===================================================
# 🔘 CONTROL: Set dry_run=False to apply changes
# ===================================================
if __name__ == "__main__":
    rename_qmd_files(start_dir=".", dry_run=False)  # ← Change to False when ready