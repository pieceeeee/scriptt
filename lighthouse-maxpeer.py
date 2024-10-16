import subprocess

def run_command_and_get_output(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def count_occurrences(output, search_string):
    return output.count(search_string)

def main():
    command = "lsof -i -n -P | grep lighthous"
    output = run_command_and_get_output(command)

    with open("lsof_output.log", "w") as logfile:
        logfile.write(output)

    with open("lsof_output.log", "r") as logfile:
        log_data = logfile.read()

    total_connections = count_occurrences(log_data, "ESTABLISHED")
    incoming_connections = count_occurrences(log_data, "154.92.22.203:9000")
    outgoing_connections = total_connections - incoming_connections

    print(f"Total connections: {total_connections}")
    print(f"Incoming connections: {incoming_connections}")
    print(f"Outgoing connections: {outgoing_connections}")

if __name__ == "__main__":
    main()
