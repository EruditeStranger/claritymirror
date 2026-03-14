import json
import os
from http.server import BaseHTTPRequestHandler

from openai import OpenAI

client = OpenAI()  # reads OPENAI_API_KEY from environment

PROMPT_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs', 'system-prompt.md')
with open(PROMPT_PATH) as f:
    SYSTEM_PROMPT = f.read()


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length))

            intentions = body.get("intentions", [])
            vulnerabilities = body.get("vulnerabilities", [])
            brokers = body.get("brokers", [])

            user_message = build_user_message(intentions, vulnerabilities, brokers)

            response = client.chat.completions.create(
                model="gpt-5-nano",
                max_tokens=600,
                store=False,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_message},
                ],
            )

            reflection_text = response.choices[0].message.content

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"reflection": reflection_text}).encode())

        except Exception:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": "reflection_unavailable"}).encode()
            )


def build_user_message(intentions, vulnerabilities, brokers):
    lines = []

    if intentions:
        lines.append("The user's stated intentions:")
        for i in intentions:
            lines.append(f"  - {i}")

    if vulnerabilities:
        lines.append("\nVulnerability profile:")
        for v in vulnerabilities:
            lines.append(f"  - {v['category']} ({v['level']}): {v['whatTheySee']}")

    if brokers:
        lines.append(f"\nData sources in profile: {', '.join(brokers)}")

    return "\n".join(lines)
