Local development

# Setup

Use a domain e.g. webbhook.hyteck.de and configure nginx as 
reverse proxy for port 4242 for this domain.

# Connect

Run the local server and connect via (5000 is the local flask port)
`ssh -N -R 4242:localhost:5000 s`

