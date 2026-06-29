# Refactor Candidates

After the TDD cycle, look for scoped refactors in touched code or code that must change for the tested behavior. Do not introduce broader architecture changes unless the prompt or planning task requires them.

- **Duplication** -> Extract function/class
- **Long methods** -> Break into private helpers (keep tests on public interface)
- **Shallow modules** -> Combine or deepen
- **Feature envy** -> Move logic to where data lives
- **Primitive obsession** -> Introduce value objects
- **Existing code** the new code reveals as problematic
