import http.server
import socketserver
import json
import random
import urllib.parse
import os
PORT = int(os.environ.get("PORT", 8000))

# In-memory state for current rolls
current_rolls = {
    'visual': None,
    'movement': None,
    'function': None
}

# New morphological table (UPD)
parameters = {
    'visual': [
        "Starlit Veils",
        "Molten Shards",
        "Pulsing Nebulae",
        "Feathered Prisms",
        "Shadowy Wisps",
        "Gilded Thorns",
        "Radiant Threads",
        "Opalized Shells",
        "Frosted Vortices",
        "Mirrored Facets",
        "Ethereal Blossoms",
        "Chromatic Fumes",
        "Velvet Crests",
        "Spectral Ribbons",
        "Diamond Dust",
        "Auroral Crests",
        "Luminous Webs",
        "Ceramic Mosaics"
    ],
    'movement': [
        "Glinting Hover",
        "Cyclic Pulsing",
        "Drifting Phantoms",
        "Twisting Vortex",
        "Harmonic Swaying",
        "Flashing Bursts",
        "Ripple Gliding",
        "Orbiting Dance",
        "Fractal Spinning",
        "Echoing Bounds",
        "Tidal Surging",
        "Flickering Drift",
        "Luminescent Trailing",
        "Gaseous Swirling",
        "Prismatic Leaping",
        "Static Hovering",
        "Celestial Arcing",
        "Vortex Weaving"
    ],
    'function': [
        "Harmonizing Vibrations",
        "Refraction of Light",
        "Temporal Echoes",
        "Phase Shifting",
        "Sonic Amplification",
        "Chrono Manipulation",
        "Aether Binding",
        "Holographic Camouflage",
        "Quantum Entanglement",
        "Thermal Resonance",
        "Spectral Projection",
        "Gravity Nullification",
        "Psionic Illusions",
        "Energy Dissipation",
        "Molecular Harmonization",
        "Lunar Synchronization",
        "Astral Manipulation",
        "Photon Scattering"
    ]
}

# HTML content as a string
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fantastic Creature Generator</title>
    <style>
        body {
            font-family: monospace;
            background: #fff;
            color: #000;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 1.5rem;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-bottom: 20px;
        }
        button {
            padding: 10px 20px;
            font-family: monospace;
            cursor: pointer;
            background: #000;
            color: #fff;
            border: 1px solid #000;
        }
        button:hover {
            background: #fff;
            color: #000;
        }
        .parameters {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }
        .parameter-card {
            border: 1px solid #000;
            padding: 10px;
            background: #f8f8f8;
        }
        .parameter-title {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .parameter-value {
            padding: 5px;
            background: #f0f0f0;
            min-height: 40px;
        }
        .description {
            border: 1px solid #000;
            padding: 10px;
            background: #f8f8f8;
            margin-bottom: 20px;
        }
        .loading {
            text-align: center;
            color: #666;
            font-style: italic;
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>
    <h1>Fantastic Creature Generator</h1>
    <p class="subtitle">Zwicky Morphological Analysis • Roll dice to create unique creatures</p>
    <div class="controls">
        <button onclick="rollDice()">🎲 Roll All Dice</button>
        <button onclick="generateDescription()">📝 Generate Description</button>
        <button onclick="resetAll()">🔄 Reset All</button>
    </div>
    <div class="parameters">
        <div class="parameter-card">
            <div class="parameter-title">1. Visual Dominant</div>
            <div class="parameter-value" id="visual-value">Roll a die</div>
        </div>
        <div class="parameter-card">
            <div class="parameter-title">2. Movement Form</div>
            <div class="parameter-value" id="movement-value">Roll a die</div>
        </div>
        <div class="parameter-card">
            <div class="parameter-title">3. Functional Feature</div>
            <div class="parameter-value" id="function-value">Roll a die</div>
        </div>
    </div>
    <div class="description">
        <div class="parameter-title">Creature Description:</div>
        <div id="creature-description">
            First, roll the dice to determine the parameters of your fantastic creature.<br><br>
            Then, click "Generate Description" to create a detailed prompt.
        </div>
    </div>
    <div class="footer">
        Zwicky Morphological Analysis Method • Combine parameters for unique concepts
    </div>
    <script>
        async function rollDice() {
            try {
                const response = await fetch('/api/roll_dice');
                const data = await response.json();
                document.getElementById('visual-value').textContent = data.visual_value;
                document.getElementById('movement-value').textContent = data.movement_value;
                document.getElementById('function-value').textContent = data.function_value;
            } catch (error) {
                alert('Failed to roll dice.');
            }
        }

        async function generateDescription() {
            try {
                const response = await fetch('/api/generate_description');
                const data = await response.json();
                if (data.error) {
                    alert(data.error);
                    return;
                }
                const descriptionElement = document.getElementById('creature-description');
                descriptionElement.innerHTML = '<div class="loading">Generating description...</div>';
                setTimeout(() => {
                    descriptionElement.innerHTML = `Selected combination:<br><br>
                        Visual Dominant: ${data.visual}<br>
                        Movement Form: ${data.movement}<br>
                        Functional Feature: ${data.function}<br><br>
                        Creature Description:<br>${data.description}`;
                }, 1000);
            } catch (error) {
                alert('Failed to generate description.');
            }
        }

        async function resetAll() {
            try {
                await fetch('/api/reset', { method: 'POST' });
                document.getElementById('visual-value').textContent = 'Roll a die';
                document.getElementById('movement-value').textContent = 'Roll a die';
                document.getElementById('function-value').textContent = 'Roll a die';
                document.getElementById('creature-description').innerHTML = 
                    'First, roll the dice to determine the parameters of your fantastic creature.<br><br>' +
                    'Then, click "Generate Description" to create a detailed prompt.';
            } catch (error) {
                alert('Failed to reset.');
            }
        }
    </script>
</body>
</html>
"""

def create_creature_description(visual, movement, func):
    backgrounds = ['clean white', 'pastel mint', 'ocean blue', 'forest green', 'sunset orange', 'cosmic black', 'radiant gold']
    angles = ['frontal', 'diagonal low angle', 'top-down', 'side profile', 'three-quarter view']
    textures = ['grain texture', 'dust particles', 'bokeh lights', 'floating debris', 'mist swirls']
    surreal = ['holographic confetti', 'chrome spheres', 'vintage buttons', 'crystal fragments', 'neon rings', 'pulsing orbs', 'fractured mirrors']

    bg = random.choice(backgrounds)
    angle = random.choice(angles)
    texture = random.choice(textures)
    surreal1 = random.choice(surreal)
    surreal2 = random.choice(surreal)

    return f"""Mystical creature dominated by {visual.lower()}, constantly in motion through {movement.lower()}, with the extraordinary ability of {func.lower()}. The creature's form seamlessly integrates these elements - its {visual.lower()} creating mesmerizing patterns as it moves, while its {func.lower()} manifests as visible energy fields around its body.

Captured in hyper-realistic vertical flash photograph, 1080x1350, harsh direct flash creating dramatic sculptural shadows and highlighting every detail of the creature's unique surface texture. Shot from {angle} to emphasize the dynamic {movement.lower()} and the creature's supernatural presence. Tight cinematic framing crops the creature at edges for maximum graphic impact.

{bg} background with subtle {texture} and atmospheric depth. The creature's {func.lower()} creates visible distortions in the air around it, while scattered {surreal1} and {surreal2} float in the space, affected by the creature's supernatural abilities. The overall composition balances the creature's organic nature with surreal, otherworldly elements that emphasize its fantastical origin."""

class CreatureGeneratorHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        
        elif path == '/api/roll_dice':
            global current_rolls
            current_rolls['visual'] = random.randint(1, 18)
            current_rolls['movement'] = random.randint(1, 18)
            current_rolls['function'] = random.randint(1, 18)

            response = {
                'visual_value': parameters['visual'][current_rolls['visual'] - 1],
                'movement_value': parameters['movement'][current_rolls['movement'] - 1],
                'function_value': parameters['function'][current_rolls['function'] - 1]
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        elif path == '/api/generate_description':
            if not all(current_rolls.values()):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Roll dice first'}).encode('utf-8'))
                return

            visual = parameters['visual'][current_rolls['visual'] - 1]
            movement = parameters['movement'][current_rolls['movement'] - 1]
            func = parameters['function'][current_rolls['function'] - 1]

            description = create_creature_description(visual, movement, func)

            response = {
                'visual': visual,
                'movement': movement,
                'function': func,
                'description': description
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/reset':
            global current_rolls
            current_rolls = {'visual': None, 'movement': None, 'function': None}
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'reset'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    PORT = int(os.environ.get("PORT", 8000))
    with socketserver.TCPServer(("", PORT), CreatureGeneratorHandler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.server_close()
            print("Server stopped.")