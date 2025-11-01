
import os
import sys
import time
import subprocess
import requests
from pathlib import Path

# Ensure SECRET_KEY is set for the server process
os.environ.setdefault("SECRET_KEY", "test-secret")


def run_uvicorn_in_subprocess(port: int = 8000):
    """Start a uvicorn server for the backend in a subprocess.

    Returns the Popen object. Caller is responsible for terminating it.
    """
    # Run using the module so the environment is consistent
    cmd = [sys.executable, "-m", "uvicorn", "backend.main:app", "--port", str(port)]
    env = os.environ.copy()
    # start the server
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    # wait a short time for startup
    time.sleep(1.0)
    return proc


def wait_for_server(url: str, timeout: float = 5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=0.5)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def setup_db():
    # If running server in subprocess, the auth module will create db file; ensure path
    backend_dir = Path(__file__).resolve().parents[1]
    db = backend_dir / "db" / "auth.db"
    if db.exists():
        print(f"Removing existing DB at {db}")
        db.unlink()
    # don't init here; server will initialize on startup


def teardown_db():
    backend_dir = Path(__file__).resolve().parents[1]
    db = backend_dir / "db" / "auth.db"
    if db.exists():
        print(f"Removing DB at {db}")
        db.unlink()


def run_flow():
    # Start server in subprocess
    port = 8000
    base = f"http://127.0.0.1:{port}"
    proc = run_uvicorn_in_subprocess(port=port)
    try:
        if not wait_for_server(base + "/"):
            print("Server did not start in time")
            proc.kill()
            teardown_db()
            return 2

        sess = requests.Session()

        print("1) Registering user 'alice'...")
        r = sess.post(base + "/register", json={"username": "alice", "password": "s3cret"})
        print("   status:", r.status_code, "body:", r.text)
        if r.status_code != 200:
            print("Register failed")
            return 1

        print("2) Requesting token for 'alice' (form-encoded)...")
        r2 = sess.post(base + "/token", data={"username": "alice", "password": "s3cret"})
        print("   status:", r2.status_code, "body:", r2.text)
        if r2.status_code != 200:
            print("Token request failed")
            return 2

        # Check Set-Cookie header or session cookies
        cookies = r2.cookies
        print("   cookies returned:", cookies.get_dict())
        # Expect a cookie named 'session'
        session_cookie = cookies.get("session")
        if not session_cookie:
            # sometimes Set-Cookie is present but requests doesn't expose it on r2.cookies due to domain/path
            sc = r2.headers.get("set-cookie")
            print("   set-cookie header:", sc)
            if not sc or "session=" not in sc:
                print("No session cookie returned")
                return 3

        print("3) Calling protected /me with cookie (session)...")
        r3 = sess.get(base + "/me")
        print("   status:", r3.status_code, "body:", r3.text)
        if r3.status_code != 200:
            print("Protected endpoint failed")
            return 4

        print("Flow succeeded. /me returned:", r3.json())
        return 0
    finally:
        try:
            proc.terminate()
        except Exception:
            pass
        teardown_db()


if __name__ == "__main__":
    try:
        exit_code = run_flow()
    except Exception as e:
        print("Error during test run:", e)
        teardown_db()
        exit_code = 10
    sys.exit(exit_code)
