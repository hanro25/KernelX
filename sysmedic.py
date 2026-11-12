
import re


def analyse_linux_issue(description):
    """
    KernelX SysMedic v0.3
    Local rule-based Linux diagnostic engine.
    No external AI services or command execution.
    """

    issue = description.lower()

    # Detect the category explicitly selected in the application.
    category_match = re.search(
        r"problem category:\s*([^\n]+)",
        issue
    )

    category = category_match.group(1).strip() if category_match else ""

    def contains(*words):
        return any(word in issue for word in words)

    # 1. NETWORK AND DNS
    if (
        "network / dns" in category
        or contains(
            "dns", "resolve", "resolution",
            "name or service not known",
            "temporary failure in name resolution",
            "could not resolve",
            "connection timed out",
            "network unreachable"
        )
    ):
        return """
## KernelX SysMedic — Network & DNS Doctor

### Possible causes
- DNS resolver failure.
- DNS server unreachable.
- Incorrect resolver configuration.
- Network connectivity problem.

### Diagnostic commands

**Test hostname resolution**
```bash
getent hosts example.com
```
READ-ONLY

**Query DNS**
```bash
nslookup example.com
```
READ-ONLY

**Inspect resolver configuration**
```bash
cat /etc/resolv.conf
```
READ-ONLY

**Inspect network interfaces**
```bash
ip addr
```
READ-ONLY

**Inspect routing**
```bash
ip route
```
READ-ONLY

### Interpretation
- No hostname result: investigate DNS resolution.
- DNS timeout: investigate resolver reachability.
- No default route: investigate routing configuration.
- Successful DNS resolution: investigate the application or connection path.

### Safety
Do not change DNS configuration or restart networking services
before collecting evidence.

### Follow-up
Which hostname fails? Does the server reach an external IP?
"""

    # 2. SERVICE FAILURES
    if (
        "service failure" in category
        or contains(
            "service failed", "service failure",
            "failed to start", "failed state",
            "unit entered failed state",
            "systemctl", "apache", "nginx"
        )
    ):
        return """
## KernelX SysMedic — Service Doctor

### Possible causes
- Invalid service configuration.
- Missing dependencies.
- Permission problems.
- Port conflicts.
- Application startup errors.

### Diagnostic commands

**Check service status**
```bash
systemctl status SERVICE_NAME --no-pager
```
READ-ONLY

**Inspect service logs**
```bash
journalctl -u SERVICE_NAME -n 100 --no-pager
```
READ-ONLY

**Check enabled state**
```bash
systemctl is-enabled SERVICE_NAME
```
READ-ONLY

**Inspect listening ports**
```bash
ss -lntup
```
READ-ONLY

### Interpretation
- Failed: inspect the reported failure reason.
- Address already in use: investigate port conflicts.
- Permission denied: investigate service permissions.
- Dependency failure: inspect the dependent service.

### Safety
Do not automatically restart production services.

### Follow-up
Which service is failing? What does systemctl status show?
"""

    # 3. DISK AND FILESYSTEM
    if (
        "disk / filesystem" in category
        or contains(
            "disk full", "disk space", "filesystem",
            "file system", "no space left",
            "inode", "storage full",
            "/var is full", "100% usage"
        )
    ):
        return """
## KernelX SysMedic — Disk Doctor

### Possible causes
- Filesystem capacity exhausted.
- Inode exhaustion.
- Excessive log growth.
- Application data accumulation.

### Diagnostic commands

**Check filesystem usage**
```bash
df -hT
```
READ-ONLY

**Check inode usage**
```bash
df -i
```
READ-ONLY

**Inspect mounted filesystems**
```bash
findmnt
```
READ-ONLY

**Identify large directories**
```bash
du -xhd1 /var 2>/dev/null | sort -h
```
READ-ONLY

### Interpretation
- Use% near 100%: investigate filesystem capacity.
- IUse% near 100%: investigate inode exhaustion.
- Large directories: identify which application or data is responsible.

### Safety
Never automatically delete logs, application data or customer files.
Check retention, backups and application dependencies first.

### Follow-up
Which filesystem is full? What are the df -hT and df -i results?
"""

    # 4. CPU AND MEMORY
    if (
        "cpu / memory" in category
        or contains(
            "high cpu", "cpu usage", "high load",
            "out of memory", "memory exhausted",
            "high memory", "low memory",
            "oom", "swap usage", "memory pressure"
        )
    ):
        return """
## KernelX SysMedic — CPU & Memory Doctor

### Possible causes
- CPU-intensive processes.
- Memory exhaustion.
- Excessive load.
- Memory leaks.
- Swap pressure.

### Diagnostic commands

**Check system load**
```bash
uptime
```
READ-ONLY

**Inspect CPU and memory**
```bash
top
```
READ-ONLY

**Identify CPU-intensive processes**
```bash
ps -eo pid,comm,%cpu,%mem --sort=-%cpu
```
READ-ONLY

**Check memory availability**
```bash
free -h
```
READ-ONLY

**Inspect kernel memory events**
```bash
journalctl -k -n 100 --no-pager
```
READ-ONLY

### Interpretation
- High CPU percentage: investigate the responsible process.
- High load: compare load with CPU capacity and I/O activity.
- Low available memory: investigate memory consumption.
- OOM messages: investigate memory exhaustion and affected processes.

### Safety
Do not terminate processes without identifying their purpose
and understanding production impact.

### Follow-up
Is the problem CPU saturation, memory exhaustion or both?
"""

    # 5. PERMISSIONS
    if (
        "permissions" in category
        or contains(
            "permission denied", "access denied",
            "ownership", "permission issue",
            "cannot access", "operation not permitted"
        )
    ):
        return """
## KernelX SysMedic — Permissions Doctor

### Possible causes
- Incorrect file ownership.
- Missing read, write or execute permissions.
- Incorrect directory permissions.
- Security policy restrictions.

### Diagnostic commands

**Inspect file permissions**
```bash
ls -l /path/to/file
```
READ-ONLY

**Inspect directory permissions**
```bash
namei -l /path/to/file
```
READ-ONLY

**Inspect current identity**
```bash
id
```
READ-ONLY

**Inspect ACL entries**
```bash
getfacl /path/to/file
```
READ-ONLY

### Interpretation
- Unexpected owner: investigate ownership requirements.
- Missing permission bits: investigate required access.
- ACL restrictions: inspect access control entries.
- SELinux denials: inspect relevant security audit logs.

### Safety
Do not recommend chmod 777 or recursive chown as generic fixes.
Verify the required access and security policy first.

### Follow-up
Which user receives the error? Which file or directory is affected?
"""

    # 6. BOOT ISSUES
    if (
        "boot issue" in category
        or contains(
            "boot failure", "failed to boot",
            "boot problem", "emergency mode",
            "initramfs", "grub error",
            "kernel panic", "failed to mount"
        )
    ):
        return """
## KernelX SysMedic — Boot Doctor

### Possible causes
- Filesystem or mount failure.
- Bootloader configuration issue.
- Kernel startup failure.
- Missing root filesystem.
- Incorrect boot configuration.

### Diagnostic commands

**Inspect failed system units**
```bash
systemctl --failed
```
READ-ONLY

**Inspect boot logs**
```bash
journalctl -b -p err --no-pager
```
READ-ONLY

**Inspect block devices**
```bash
lsblk -f
```
READ-ONLY

**Inspect filesystem mounts**
```bash
findmnt
```
READ-ONLY

### Interpretation
- Failed mount: inspect filesystem and mount configuration.
- Missing device: verify device availability and identifiers.
- Kernel errors: investigate kernel and driver messages.

### Safety
Do not modify GRUB, fstab or filesystem structures
without confirming the root cause and recovery plan.

### Follow-up
Does the server fail before login, or does it enter emergency mode?
"""

    # 7. PROCESS ISSUES
    if (
        "process issue" in category
        or contains(
            "hung process", "process stuck",
            "unresponsive process", "zombie process",
            "process consuming", "high process usage"
        )
    ):
        return """
## KernelX SysMedic — Process Doctor

### Possible causes
- Unresponsive application.
- Resource-intensive process.
- Zombie processes.
- Process contention.
- I/O blocking.

### Diagnostic commands

**List running processes**
```bash
ps aux
```
READ-ONLY

**Inspect process tree**
```bash
pstree -p
```
READ-ONLY

**Inspect process states**
```bash
ps -eo pid,ppid,stat,comm
```
READ-ONLY

**Inspect system activity**
```bash
top
```
READ-ONLY

### Interpretation
- Z state: investigate zombie process and parent process.
- High CPU: investigate resource consumption.
- D state: investigate uninterruptible I/O activity.
- Unresponsive process: inspect application logs and dependencies.

### Safety
Do not kill processes automatically.
Identify the owner, purpose and production impact first.

### Follow-up
Which process is affected? What is its PID and current state?
"""

    return """
## KernelX SysMedic — Further Investigation Required

No matching diagnostic playbook was identified.

Please provide:

- Complete error message.
- Linux distribution and version.
- Relevant diagnostic output.
- When the problem started.
- Whether the affected system is production.

SysMedic will not invent diagnostic results or assume
a root cause without sufficient evidence.
"""
