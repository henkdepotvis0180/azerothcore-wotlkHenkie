# Funserver workflow for Codex

Repository: henkdepotvis0180/azerothcore-wotlkHenkie
Core branch: Playerbot (fork of mod-playerbots/azerothcore-wotlk)
Goal: WotLK 3.3.5a solo funserver, AI playerbots and custom content.

## When the user asks "add module X"

1. Read the root AGENTS.md and obey existing AzerothCore engineering rules.
2. Find the exact upstream module repository and read its installation guide, license, dependencies, supported core versions and known conflicts. Do not guess a repository name.
3. Confirm it can reasonably target the Playerbot branch. If it depends on a different core fork or incompatible patch, report the issue instead of silently forcing it.
4. Edit funserver/modules.json: add or change one entry with safe module folder name, GitHub owner/repo and a full 40-character tested/selected commit SHA. Never use a moving branch name or an unpinned commit.
5. Check incompatibilities, particularly mutually exclusive difficulty scalers (AutoBalance, SoloCraft, Dungeon Scale), Lua engine differences (ALE vs Eluna), SQL conflicts and client-side patch requirements.
6. Update funserver/MODULES-NL.md with new module, why it was selected, upstream link, commit, installation notes, SQL/config steps, integration risks and validation status.
7. Run "python scripts/funserver_modules.py validate". If your environment supports network, run "python scripts/funserver_modules.py sync" and applicable focused checks; keep explicit track of what actually ran.
8. Open a pull request to Playerbot that changes the manifest/docs and any necessary custom module sources. The repository's Windows build workflow pulls the exact pinned modules and compiles the server through CMake automatically. Never claim a successful build without a green workflow run.
9. Never alter existing AzerothCore/gameplay core files only to accommodate a third-party module without a documented reason and separate review. Keep local custom work in a dedicated module when possible.
10. Do not invent success of in-game tests: full runtime checks still require a configured database, server assets and a WotLK client.

## CMake automation

A C++ server or C++ module change REQUIRES recompilation. The user should not have to type CMake commands: CI performs the compilation automatically. The scripts here only synchronize source modules; they are NOT an executable server and do not deploy a running server. Lua scripts and some SQL/config changes can often be reloaded, but do not assume hot reload is always possible.

## Security / stability

- Do not force-push, automatically merge or modify production data.
- Treat any new upstream GitHub module as untrusted executable code. Review changes and never run unknown install scripts blindly.
- Never commit credentials, game assets, database dumps or generated binaries.
- Back up authentication, characters, world and playerbots databases before migrations.
- Preserve original module licenses and attribution.
- For larger changes: keep separate test branches; include a rollback plan.
