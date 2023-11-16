def seconds_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds

# Example usage:
total_seconds = 3665  # Replace this with the number of seconds you want to convert
hours, minutes, seconds = seconds_to_time(total_seconds)
print(f"{hours} hours, {minutes} minutes, {seconds} seconds")

#==============================================================================#