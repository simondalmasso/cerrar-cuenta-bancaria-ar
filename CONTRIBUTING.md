# Contributing

## Goal

Improve the skill without turning it into a bank-operating bot.

## Source policy

For legal/procedural changes:
1. prefer current BCRA text ordered / official communication;
2. then Argentina.gob.ar;
3. then official bank documentation;
4. use SAIJ/CSJN/official courts for jurisprudence;
5. secondary services are discovery only.

Every time-sensitive change should include:
- source URL;
- verification date;
- product/account type;
- reason the source applies.

## Pull requests

Before opening a PR:

```bash
python scripts/validate_repo.py
```

Add or update an eval when changing behavior.

## Privacy

Never commit real:
- DNI/CUIL/CUIT of a private person;
- CBU/CVU/account/card numbers;
- phone/email from a user's case;
- passwords/tokens/OTP;
- bank statements or screenshots with unredacted personal data.

Examples must be synthetic or anonymized.
