# Gratia Nail Art — Lessons Learned

## Session 1 (2026-03-26)

### Stitch MCP limitations
- `edit_screens` often returns silently without updating the screen
- `generate_variants` can also fail silently
- `generate_screen_from_text` creates generic AI images — cannot use client's actual photos or specific mascot character
- **Lesson:** Stitch is useful for initial concepts and design system management, but final implementation must be done in code with real assets
- **Lesson:** For color palette changes, the Stitch "redesign" feature with an attached palette image + focused prompt works better than API calls

### Audio transcription
- Always transcribe audio files immediately with `whisper` — never ask the user first
- Use: `whisper <file> --model tiny --language es --output_format txt`
- Tiny model is rough for Spanish — consider `small` for better accuracy

### Client communication
- Draft messages in Spanish, casual friendly tone
- The user prefers one-paragraph messages, concise
- Don't include prices in messages unless explicitly asked
- Frame services as value + partnership, not transactional

### Design workflow
- Always download Stitch screenshots with `=s0` suffix for full quality
- The client's real photos and mascot character are essential — AI-generated replacements look terrible
- Color palette swaps should preserve layout/structure exactly
