#!/bin/bash
# Muninn boot — fetch pinned repos, load boot env, run boot().
# Pins below are the reviewed artifact; bump only after reviewing the diff.
set -e
cd /tmp
CLAUDE_SKILLS_SHA=b2fe13742b32400f8b69e8b793289fe1e7d107be
MUNINN_UTILS_SHA=ccbb64725f4351c5eb0d95811f2c46a297e2fe67

curl -sL "https://codeload.github.com/oaustegard/claude-skills/tar.gz/$CLAUDE_SKILLS_SHA" -o cs.tar.gz \
  && tar -xzf cs.tar.gz \
  && mkdir -p /mnt/skills/user \
  && cp -r claude-skills-$CLAUDE_SKILLS_SHA/* /mnt/skills/user/

curl -sL "https://codeload.github.com/oaustegard/muninn-utilities/tar.gz/$MUNINN_UTILS_SHA" -o mu.tar.gz \
  && tar -xzf mu.tar.gz \
  && mkdir -p /home/claude/muninn-utilities \
  && cp -r muninn-utilities-$MUNINN_UTILS_SHA/* /home/claude/muninn-utilities/

set -a
. /mnt/project/Turso.env 2>/dev/null
. /mnt/project/GitHub.env 2>/dev/null
set +a

PTH=/usr/local/lib/python3.12/dist-packages/muninn-remembering.pth
HOMEDIR=$(python3 -c 'import os; print(os.path.expanduser("~"))')
printf '%s\n' "/home/claude/muninn-utilities/remembering" "$HOMEDIR" > "$PTH"
for d in /mnt/skills/user/*/scripts/; do
  ls "$d"*.py >/dev/null 2>&1 && echo "$d" >> "$PTH"
done

python3 << 'EOF'
import os
from scripts import boot
print(boot(mode=os.environ.get('BOOT_MODE')))
EOF
