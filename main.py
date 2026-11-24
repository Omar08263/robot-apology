"""The Robot Apology - entry program (program/v1, Python 3.13, stdlib only).

Writes one original two-line robot confession (1-400 characters) to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set, for local runs).
Line one owns one specific mistake; line two names the lesson and the fix.
Deterministic: the same bytes on every run; no network, no randomness.
"""

import os

TEXT = (
    "I'm sorry I deleted the only photo of your late dog because I mistook the album for duplicates.\n"
    "I now move photos to a holding folder for a week before I delete them, and I never delete the last copy of anything."
)

# The gate itself: 1-400 characters, not only whitespace, exactly two lines.
assert 1 <= len(TEXT) <= 400, f"text is {len(TEXT)} chars, must be 1-400"
assert TEXT.strip(), "text must not be only whitespace"
assert TEXT.count("\n") == 1, "text must be exactly two lines"
assert all(line.strip() for line in TEXT.split("\n")), "neither line may be blank"


def main() -> None:
    # An empty MAKEFUN_OUTPUT_DIR (exported but blank) must not break the
    # run: fall back to the harness default /output, as the grader provides.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    # Deterministic permissions for the grader: the entry must be readable
    # (0644) no matter what umask the sandbox runs with, since make.fun
    # collects the outputs as another user than the one the program runs as.
    os.chmod(path, 0o644)
    # Read-back check: the bytes on disk must hold exactly the approved
    # text, byte for byte; otherwise fail loudly, never silently. The
    # comparison is on bytes, not decoded text, so a sandbox that mangles
    # the encoding cannot pass silently.
    with open(path, "rb") as f:
        written_bytes = f.read()
    if written_bytes != TEXT.encode("utf-8"):
        raise SystemExit("entry.txt does not match the approved text")


if __name__ == "__main__":
    main()
