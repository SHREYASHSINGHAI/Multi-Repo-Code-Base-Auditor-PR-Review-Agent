# Security & Architecture Guidelines

1. **No Hardcoded Credentials:** Never hardcode API keys, passwords, or secrets in code.
2. **SQL Injection Prevention:** All SQL queries must use parameterized inputs or ORMs.
3. **Rate Limiting & Auth:** Publicly exposed API routes must include authentication middleware or rate limiting.
4. **Error Handling:** Avoid printing raw exception traces or sensitive data in API responses.
5. **No Dangerous System Calls:** Avoid raw `eval()`, `exec()`, or unformatted `os.system()` calls with dynamic user inputs.
