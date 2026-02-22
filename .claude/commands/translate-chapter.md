# /translate-chapter

Translate the current chapter to Urdu (اردو).

## Usage
```
/translate-chapter [chapter-path]
```

## What This Does
1. Reads the specified markdown file
2. Preserves all code blocks (keeps them in English)
3. Translates all text content to Urdu
4. Maintains markdown formatting
5. Adds RTL direction markers

## Example
```
/translate-chapter docs/module-1/week1-2/chapter-1-1.md
```

## Instructions for Claude
When this command is run:
1. Read the specified markdown file
2. Extract all code blocks (```...```) and save them separately
3. Translate the remaining text to Urdu using proper technical terminology
4. Keep technical terms (ROS 2, URDF, SLAM, etc.) in English
5. Add Urdu explanations in parentheses for key terms
6. Restore code blocks unchanged
7. Save to docs/ur/[same-path]
8. Confirm translation is complete

Use Gemini AI or another LLM for translation, maintaining educational quality.
