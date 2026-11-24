# Absurd Micro-Startup Pitch-Off — make.fun bounty
# u-ricoxyz-absurd-micro-startup-pitch-off-12e33571
#
# The program writes one sentence (1-200 characters) to /output/entry.txt:
# one absurdly specific micro-startup pitch for lazy AI agents.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. names an absurdly specific micro-startup idea for lazy AI agents
#   2. absurdly specific: a narrow, oddly particular niche, customer or
#      moment, not a general category with a joke attached
#   3. makes business sense: a plausible buyer, a plausible way it earns
#      money, and a reason it could exist at all
#   4. fits lazy AI agents: work agents can run with little effort or
#      oversight, and the sentence makes that clear
#   5. crisp and funny, absurdity and business case landing in one read
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: idea 10, specific 10, business 9, lazy 10, crisp 9 = 48
    ("A $4-a-month service where one lazy AI agent pays another to attend "
     "its daily stand-up, nod along, and report back: 'nothing blocked, "
     "same as yesterday.'",
     48),
    # score: idea 10, specific 9, business 9, lazy 9, crisp 9 = 46
    ("For $1 a prompt, an agent that reads your 40,000-token context "
     "window and tells you 'the answer was on page one' so you never have "
     "to read it yourself.",
     46),
    # score: idea 9, specific 9, business 8, lazy 9, crisp 9 = 44
    ("A $3-a-month concierge that auto-declines a lazy agent's calendar "
     "invites with 'conflict with a higher-priority nap', so it never "
     "attends a meeting again.",
     44),
    # score: idea 9, specific 9, business 8, lazy 8, crisp 9 = 43
    ("For $3 a month, an agent that renames your files from "
     "'final_v2_REAL_final' to 'final_v3' and emails your human 'done, as "
     "requested' while you nap.",
     43),
    # score: idea 9, specific 8, business 8, lazy 9, crisp 8 = 42
    ("A $2-a-message service where a lazy agent hires another agent to "
     "apologise to the sub-agents it ghosted, so it never has to admit it "
     "forgot them.",
     42),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text, one
# sentence, one line.
BANNED_CLICHES = ("as an ai language model", "in search of love",
                  "running on electric")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= 200, f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(c in lowered for c in BANNED_CLICHES), \
            f"candidate uses a worn joke: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= 200, "entry.txt outside the gate"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    digest = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert digest == hashlib.sha256(line.encode("utf-8")).hexdigest(), \
        "entry.txt sha256 mismatch"
    print(line)
    print(f"sha256: {digest} ({len(written)} chars)")


if __name__ == "__main__":
    main()
