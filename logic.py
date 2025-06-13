UNSUPPORTED_OS = [
    "windows server 2003",
    "windows server 2008",
    "windows server 2012",
    "windows xp",
    "windows vista",
    "centos 6",
    "ubuntu 14.04",
    "rhel 6",
    "suse linux enterprise server 11"
]

def is_unsupported_os(os_name):
    if not isinstance(os_name, str):
        return False
    return any(keyword in os_name.lower() for keyword in UNSUPPORTED_OS)

def recommend_migration(row):
    cpu = row.get('CPU usage(%)', 0)
    mem = row.get('Memory usage(%)', 0)
    os = row.get('Operating system', '')
    readiness = row.get('Azure VM readiness', '').lower()
    issues = row.get('Azure readiness issues', '').lower()
    confidence = row.get('Confidence Rating (% of utilization data collected)', 100)

    if is_unsupported_os(os):
        return 'Replatform', 'Unsupported OS – Requires Replatform'

    if confidence < 50:
        return 'Manual Review', 'Low confidence in utilization data'

    if isinstance(os, str) and ('2008' in os or '2003' in os or 'XP' in os):
        return 'Replace', 'Legacy OS not suitable for Azure'

    if cpu > 80 or mem > 80:
        return 'Rearchitect', 'High resource usage'

    if isinstance(os, str) and 'linux' in os.lower() and cpu < 40 and mem < 40:
        return 'Refactor', 'Linux VM with low usage - candidate for containers'

    if readiness == 'ready' and issues == 'not applicable' and cpu < 60 and mem < 60:
        return 'Rehost', 'Standard lift-and-shift candidate'

    return 'Manual Review', 'Did not match any rule precisely'
