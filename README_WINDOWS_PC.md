# Phase 0 on a Windows PC — Install List

Install in this order. Everything in the main README assumes a Linux-style
terminal, so on Windows the cleanest setup is WSL2 (Ubuntu inside Windows).
With WSL2, every command in `README_PHASE0.md` works exactly as written.

## 1. WSL2 + Ubuntu (do this first)
- Open PowerShell **as Administrator** and run: `wsl --install -d Ubuntu-24.04`
- Reboot when prompted, then open Ubuntu once and set your Linux username/password
- From now on, do all project work in the Ubuntu terminal, and keep project
  files inside the Linux filesystem (`~/projects/...`), not on `C:\`
- Verify: `wsl --version` in PowerShell, `lsb_release -a` in Ubuntu

## 2. Docker Desktop for Windows
- Download from docker.com and install
- During install, keep **"Use WSL 2 based engine"** checked
- After install: Settings → Resources → WSL Integration → turn on **Ubuntu-24.04**
- Verify in Ubuntu: `docker --version` and `docker compose version`
- If Docker won't start, virtualization is usually off in BIOS — enable
  Intel VT-x / AMD SVM, then retry

## 3. Visual Studio Code (Windows)
- Install VS Code on Windows (not inside Ubuntu)
- Extensions: **WSL**, **Python**, **Docker**, **GitHub Pull Requests**
- To open the project: in Ubuntu run `code .` from the project folder — VS Code
  opens on Windows but runs the code inside WSL

## 4. Git
- In Ubuntu: `sudo apt update && sudo apt install -y git`
- Configure once:
  - `git config --global user.name "Jeremy Yuan"`
  - `git config --global user.email "<your GitHub email>"`
- Optional: Git for Windows on the Windows side (gives you Git Bash) and the
  GitHub CLI (`gh`) for creating the repo from the terminal
- Verify: `git --version`

## 5. Python 3.12 (inside Ubuntu)
Ubuntu 24.04 ships Python 3.12. Install the venv/pip pieces:
- `sudo apt install -y python3 python3-venv python3-pip`
- Verify: `python3 --version` → 3.12.x
- Optional but recommended: `uv` (faster venv + installs):
  `curl -LsSf https://astral.sh/uv/install.sh | sh`

Then the starter kit itself, in Ubuntu:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q        # expect: 2 passed
```

> Windows-native note: if you skip WSL and use PowerShell, the activate
> command changes to `.venv\Scripts\Activate.ps1` and `cp` becomes `Copy-Item`.
> The kit works, but Docker/pgvector and deployment behave better under WSL2.

## Troubleshooting: "Virtual Machine Platform is not enabled"
Docker Desktop shows this when WSL2 hasn't been installed yet. Fix it
*before* installing Docker:
1. Close the Docker installer
2. Open PowerShell **as Administrator** (right-click Start → Terminal (Admin))
3. Run: `wsl --install -d Ubuntu-24.04`
4. **Restart the PC**, then open Ubuntu once to set your username/password
5. Re-run the Docker Desktop installer — the per-user install is fine now
6. Verify: `wsl -l -v` shows Ubuntu with VERSION 2

If you have no admin rights at all (e.g. a work-managed PC), skip Docker for
Phase 0: run the app directly in the venv (`uvicorn app.main:app --reload`,
`pytest -q`) and deploy via Render from GitHub — Render builds the Dockerfile
for you. You only truly need local Docker in Week 3.

## Troubleshooting: `python3-venv` / `python3-pip` has no installation candidate
This means the `universe` package source is not enabled (common on a fresh
WSL Ubuntu). Fix in Ubuntu:
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y universe
sudo apt update
sudo apt install -y python3-venv python3-pip
```
If it still fails, bypass apt for Python tooling entirely and use `uv`
(it installs its own Python and creates the venv itself):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# close and reopen the Ubuntu terminal
uv venv                        # creates .venv
uv pip install -r requirements.txt
.venv/bin/pytest -q            # expect: 2 passed
```

## Do NOT install
- **PostgreSQL locally** — `docker-compose.yml` already provides Postgres + pgvector
- **Anaconda / Miniconda** — conflicts with the venv workflow this kit uses
- **Node.js** — not needed until much later in the plan (and may never be)
- **PyCharm** — VS Code covers everything in this program

## Final check — all of these should respond
```bash
git --version
python3 --version     # 3.12.x
docker --version
docker compose version
code --version        # from Ubuntu, after VS Code + WSL extension
```
