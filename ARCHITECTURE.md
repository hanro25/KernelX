# KernelX — SysMedic Architecture

## Product
KernelX — SysMedic

## Frontend
Streamlit (initial prototype)

## Backend
Python

## AI Engine
Replaceable AI inference service

## Initial AI strategy
Use a replaceable model provider during development.
No OpenAI dependency.

## Long-term AI strategy
Self-host open-weight models on dedicated cloud infrastructure.

## Core capabilities
1. Linux log analysis
2. Error diagnosis
3. Root-cause investigation
4. Diagnostic command recommendations
5. Risk classification
6. Safe remediation guidance

## Security
- Never execute commands automatically.
- Never request passwords or private keys.
- Redact sensitive customer information.
- Treat uploaded logs as untrusted input.

## Development environment
Windows 10
Python 3.13.6
VS Code 1.104.1
4 GB RAM