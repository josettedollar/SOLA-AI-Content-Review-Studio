
# ☀️ SOLA | AI Content Review Studio

SOLA is an AI-assisted marketing content review application built with Python, Streamlit, and the OpenAI API.

## The Problem

Marketing teams need to evaluate content for clarity, brand consistency, audience relevance, and accuracy before publication.

AI writing tools can improve copy, but they can also introduce unsupported product claims or unnecessary revisions.

## The Solution

SOLA helps marketers review Instagram captions and marketing emails through five evaluation categories:

- Brand Voice
- Message Clarity
- Claims & Accuracy
- Call to Action
- Audience Relevance

The application provides structured feedback, suggested revisions when appropriate, and an independent AI check for potentially unsupported claims in revised content.

## Features

- Optional brand voice, audience, and verified product information
- Five-category content review
- Color-coded review findings
- AI-generated suggested revisions
- Independent revision claim checker
- Editable, copyable revisions
- Rule-based warnings for selected high-risk phrases
- Clear human-review disclaimers

## Development Process

I defined the marketing review criteria, designed the workflow, and used ChatGPT to assist with Python implementation and troubleshooting.

I tested the application using fictional marketing scenarios, evaluated its outputs, and refined the review instructions based on observed behavior.

Testing revealed that AI-generated revisions could introduce unsupported claims despite explicit instructions. I addressed this limitation by adding a separate AI-based revision safety check.

## Technology

- Python
- Streamlit
- OpenAI API
- JSON
- Streamlit theme configuration

## Limitations

SOLA provides advisory feedback rather than verified marketing or legal approval.

The independent AI checker can miss unsupported claims or flag acceptable language. Users must review generated suggestions before publishing.

The application currently supports Instagram captions and marketing emails.

## Testing

See [TESTING.md](TESTING.md) for documented test scenarios, observations, improvements, and known limitations.
