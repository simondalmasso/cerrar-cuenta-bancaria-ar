# Security / Safety Model

## Scope boundary

This repository is deliberately **read-only with respect to banking**.

The skill must never:
- request or store online-banking passwords, PINs, CVVs, OTPs, tokens or security answers;
- log into a bank;
- control the user's browser or banking app;
- transfer or withdraw funds;
- pay balances;
- accept commercial offers;
- close products;
- submit complaints or forms on behalf of the user.

It may:
- read evidence voluntarily supplied by the user;
- research public sources;
- explain rules;
- reconcile amounts;
- draft text;
- organize evidence;
- tell the human what to do next.

## Reporting a security issue

Do not open a public issue containing financial credentials, account numbers, identity documents or private evidence.

Report only reproducible problems in the repository itself and redact all personal/banking data.

## Third-party integrations

MCP/API integrations listed here are research accelerators, not trusted banking operators. Their terms, licenses, availability and security posture can change. No third-party integration is a hard dependency.

A connector that asks for bank credentials is outside the architecture of this project.
