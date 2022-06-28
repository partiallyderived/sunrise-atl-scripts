# Source this file to use repo scripts.

activate() {
  # Note: use "deactivate" to deactivate venv.
  source venv/bin/activate
}

venv_make() {(
  rm -rf venv
  python3 -m venv venv || (rm -rf venv && exit 1)
  venv_update || (rm -rf venv && exit 1)
)}

venv_update() {(
  activate || exit 1
  python3 -m pip install -r requirements.txt
)}
