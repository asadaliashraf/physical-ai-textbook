# /generate-quiz

Generate a quiz for a chapter in the Physical AI textbook.

## Usage
```
/generate-quiz [chapter-path] [difficulty: easy|medium|hard]
```

## What This Does
Creates 10 quiz questions covering the chapter content:
- 4 multiple choice questions
- 3 true/false questions
- 2 short answer questions
- 1 coding exercise

## Example
```
/generate-quiz docs/module-1/week1-2/chapter-1-1.md medium
```

## Output
Generates a quiz.md file in the same directory as the chapter.
