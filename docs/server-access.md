# Server Access Guide

This guide covers accessing the Lunaverse server via SSH, including LAN and Tailscale options.

---

## SSH Access Methods

### Standard SSH (LAN)

If the server is accessible on your local network:

```bash
ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
```

### SSH via Tailscale

If using Tailscale VPN, use the Tailscale hostname:

```bash
ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_SSH_TAILSCALE_HOST}
```

---

## Authentication

### Recommended: SSH Key Authentication

1. Generate an SSH key pair (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copy your public key to the server:
   ```bash
   ssh-copy-id -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
   ```

3. Test key-based authentication:
   ```bash
   ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
   ```

### Alternative: Password Authentication

If password authentication is required (less secure):

```bash
ssh -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
# Enter password when prompted
```

**Note:** The password is stored in `LUNAVERSE_SSH_PASSWORD` env var, but SSH key authentication is strongly recommended.

---

## Cockpit Web Interface

If Cockpit is installed and configured:

1. Open your browser and navigate to:
   ```
   ${COCKPIT_URL}
   ```

2. Log in with your server credentials

Cockpit provides a web-based interface for:
- System monitoring
- Service management
- Container management
- Network configuration
- And more

---

## Port Forwarding Example

To forward a local port to a remote service:

```bash
ssh -L 8080:localhost:8080 -p ${LUNAVERSE_SSH_PORT:-22} ${LUNAVERSE_SSH_USER}@${LUNAVERSE_HOST}
```

Then access the service at `http://localhost:8080` on your local machine.

---

## Troubleshooting

### Connection Refused

- Verify `LUNAVERSE_HOST` and `LUNAVERSE_SSH_PORT` are correct
- Check firewall rules on the server
- Ensure SSH service is running: `sudo systemctl status ssh`

### Permission Denied

- Verify `LUNAVERSE_SSH_USER` is correct
- Check SSH key permissions: `chmod 600 ~/.ssh/id_ed25519`
- Verify public key is in `~/.ssh/authorized_keys` on the server

### Tailscale Not Working

- Ensure Tailscale is running on both client and server
- Verify Tailscale hostname matches `LUNAVERSE_SSH_TAILSCALE_HOST`
- Check Tailscale status: `tailscale status`

---

## Security Best Practices

1. **Use SSH keys instead of passwords** - More secure and convenient
2. **Disable password authentication** on the server (if possible)
3. **Use Tailscale** for secure remote access without exposing ports
4. **Keep SSH keys secure** - Never share private keys
5. **Rotate keys periodically** - Especially if compromised

---

## Environment Variables Required

For server operations, ensure these are set:

- `LUNAVERSE_HOST` (required)
- `LUNAVERSE_SSH_USER` (required)
- `LUNAVERSE_SSH_PORT` (required)
- `LUNAVERSE_SSH_TAILSCALE_HOST` (optional, for Tailscale)
- `LUNAVERSE_SSH_PASSWORD` (optional, prefer SSH keys)
- `COCKPIT_URL` (optional, if Cockpit is available)

Validate with:
```bash
make env-check-server-ops
```

