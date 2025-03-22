from datetime import timedelta

def hrb(value, digits=2, delim="", postfix=""):
    """Return a human-readable file size."""
    if value is None:
        return None
    
    if value < 0:
        return "0 B"  # Handling negative values

    # Initialize with bytes
    chosen_unit = "B"

    # Loop through the units until the value is less than 1024
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value >= 1024:
            value /= 1024
            chosen_unit = unit
        else:
            break

    # Return formatted string with specified digits, delimiter, and postfix
    return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"

def hrt(seconds, precision=0):
    """Return a human-readable time delta as a string."""
    pieces = []
    value = timedelta(seconds=seconds)

    # Add days if present
    if value.days:
        pieces.append(f"{value.days}d")

    # Calculate hours, minutes, and seconds from remaining seconds
    seconds = value.seconds
    if seconds >= 3600:
        hours = seconds // 3600
        pieces.append(f"{hours}h")
        seconds %= 3600

    if seconds >= 60:
        minutes = seconds // 60
        pieces.append(f"{minutes}m")
        seconds %= 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    # Return the formatted string based on precision
    if precision:
        return "".join(pieces[:precision])
    
    return "".join(pieces)

# Example usage
print(hrb(123456789))  # Outputs: "117.74 MiB"
print(hrt(3661))       # Outputs: "1h1m1s"



