# Developed on Python 3.12.0
# Requires the following packages:
# pip install prompt-toolkit

import threading
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.patch_stdout import patch_stdout
import network_monitoring_functions
import datetime
import tcp_server
import tcp_client


# Worker thread function
def ping(stop_event: threading.Event, service_targets, targets_intervals) -> None:
    while not stop_event.is_set():
        ping_addr, ping_time = network_monitoring_functions.ping(service_targets[0])
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if ping_addr is None or ping_time is None:
            print(f"{timestamp} FAIL - PING: target ({service_targets[0]}): Request timed out or no reply received")
        print(f"{timestamp} SUCCESS - PING: target ({service_targets[0]}): {ping_addr[0]} - {ping_time:.2f} ms")
        time.sleep(targets_intervals[0])


def traceroute(stop_event: threading.Event, service_targets, targets_intervals) -> None:
    while not stop_event.is_set():
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"{timestamp} TRACEROUTE: target ({service_targets[1]}) " +
              network_monitoring_functions.traceroute(service_targets[1]))
        time.sleep(targets_intervals[1])


def http(stop_event: threading.Event, service_targets, targets_intervals) -> None:
    while not stop_event.is_set():
        http_server_status, http_server_response_code = \
            network_monitoring_functions.check_server_http(service_targets[2])
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if http_server_status is False:
            print(f"{timestamp} FAIL - HTTP: target ({service_targets[2]}): HTTP server status: {http_server_status}, "
                  f"Status Code: {http_server_status}")
        else:
            print(f"{timestamp} SUCCESS - HTTP: target ({service_targets[2]}): HTTP server status: "
                  f"{http_server_status}, Status Code: {http_server_status}")
        time.sleep(targets_intervals[2])


def https(stop_event: threading.Event, service_targets, targets_intervals) -> None:
    while not stop_event.is_set():
        https_server_status, https_server_response_code, description = network_monitoring_functions.check_server_https(
            service_targets[2])
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if https_server_status is False:
            print(f"{timestamp} FAIL - HTTPS: target ({service_targets[3]}): Description: {description}")
        else:
            print(f"{timestamp} SUCCESS - HTTPS: target ({service_targets[3]}): HTTP server status: "
                  f"{https_server_status}, Status Code: {https_server_status}")
        time.sleep(targets_intervals[3])


def ntp(stop_event: threading.Event, service_targets, targets_intervals) -> None:
    while not stop_event.is_set():
        ntp_server_status, ntp_server_time = network_monitoring_functions.check_ntp_server(service_targets[4])
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if ntp_server_status is False:
            print(f"{timestamp} FAIL - NTP: target ({service_targets[4]}): Server is down")
        else:
            print(f"{timestamp} SUCCESS - NTP: target ({service_targets[4]}): Time: {ntp_server_time}")
        time.sleep(targets_intervals[4])


def dns(stop_event: threading.Event, service_targets, targets_intervals, dns_query) -> None:
    dns_queries = [
        (dns_query, 'A'),
        (dns_query, 'MX'),
        (dns_query, 'AAAA'),
        (dns_query, 'CNAME')
    ]
    while not stop_event.is_set():
        for dns_query, dns_record_type in dns_queries:
            dns_server_status, dns_query_results = \
                network_monitoring_functions.check_dns_server_status(service_targets[5], dns_query, dns_record_type)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            if dns_server_status is False:
                print(f"{timestamp} FAIL - DNS: target ({service_targets[5]}), Status: {dns_server_status}, "
                      f"{dns_record_type} Records Results: {dns_query_results}")
            else:
                print(f"{timestamp} SUCCESS - DNS: target ({service_targets[5]}), Status: {dns_server_status}, "
                      f"{dns_record_type} Records Results: {dns_query_results}")
        time.sleep(targets_intervals[5])


def tcp(stop_event: threading.Event, service_targets, targets_intervals, tcp_port) -> None:
    while not stop_event.is_set():
        tcp_port_status, tcp_port_description = network_monitoring_functions.check_tcp_port(service_targets[6],
                                                                                            tcp_port)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if tcp_port_status is False:
            print(f"{timestamp} FAIL - TCP: target ({service_targets[6]}): TCP Port: {tcp_port}, TCP Port Status: "
                  f"{tcp_port_status}, Description: {tcp_port_description}")
        else:
            print(f"{timestamp} SUCCESS - TCP: target ({service_targets[6]}): TCP Port: {tcp_port}, TCP Port Status: "
                  f"{tcp_port_status}, Description: {tcp_port_description}")
        time.sleep(targets_intervals[6])


def udp(stop_event: threading.Event, service_targets, targets_intervals, udp_port) -> None:
    while not stop_event.is_set():
        udp_port_status, udp_port_description = network_monitoring_functions.check_udp_port(service_targets[7],
                                                                                            udp_port)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        if udp_port_status is False:
            print(
                f"{timestamp} FAIL - UDP: target ({service_targets[7]}): UDP Port: {udp_port}, UDP Port Status: "
                f"{udp_port_status}, Description: {udp_port_description}")
        else:
            print(f"{timestamp} SUCCESS - UDP: target ({service_targets[7]}): UDP Port: {udp_port}, UDP Port Status: "
                  f"{udp_port_status}, Description: {udp_port_description}")
        time.sleep(targets_intervals[7])


def tcp_s() -> None:
    tcp_server.tcp_server()


def print_configurations(service_targets, dns_query, targets_intervals, tcp_port, udp_port):
    print(f"\n1 Ping target: {service_targets[0]}, interval: {targets_intervals[0]} seconds\n"
          f"2 Traceroute target: {service_targets[1]}, interval: {targets_intervals[1]} seconds\n"
          f"3 HTTP target: {service_targets[2]}, interval: {targets_intervals[2]} seconds\n"
          f"4 HTTPS target: {service_targets[3]}, interval: {targets_intervals[3]} seconds\n"
          f"5 NTP target: {service_targets[4]}, interval: {targets_intervals[4]} seconds\n"
          f"6 DNS target: {service_targets[5]}, domain name: {dns_query}, interval: "
          f"{targets_intervals[5]} seconds\n"
          f"7 TCP target: {service_targets[6]} on Port: {tcp_port}, interval: {targets_intervals[6]} seconds\n"
          f"8 UDP target: {service_targets[7]} on Port: {udp_port}, interval: {targets_intervals[7]} seconds\n"
          f"\nEcho server available for use when running network monitoring\n")


# Main function
def main() -> None:
    """
    Main function to handle user input and manage threads.
    Uses prompt-toolkit for handling user input with auto-completion and ensures
    the prompt stays at the bottom of the terminal.
    """
    # Event to signal the worker thread to stop
    stop_event: threading.Event = threading.Event()

    # Command completer for auto-completion
    # This is where you will add new auto-complete commands
    command_completer: WordCompleter = WordCompleter(['exit'], ignore_case=True)
    command_completer: WordCompleter = WordCompleter(['echo'], ignore_case=True)

    # Create a prompt session
    session: PromptSession = PromptSession(completer=command_completer)

    # Variable to control the main loop
    is_running: bool = True

    try:
        with patch_stdout():
            service_targets = ["discord.com", "eecs.oregonstate.edu", "http://washington.edu", "https://microsoft.com",
                               "129.6.15.29", "8.8.8.8", "wikipedia.com", "github.com"]
            dns_query = "google.com"
            targets_intervals = [1, 10, 3, 3, 3, 15, 5, 5]
            tcp_port = 80
            udp_port = 53
            print_configurations(service_targets, dns_query, targets_intervals, tcp_port, udp_port)
            edit: str = "placeholder"
            while edit.lower() != "":
                edit: str = session.prompt("Press 'e' to configure targets, or press Enter to run network monitoring: ")
                if edit.lower() == "e":
                    target = 9
                    while target < 1 or target > 8:
                        target: int = session.prompt("Enter the number of the target you'd like to configure: ")
                        target = int(target)
                    target_name: str = session.prompt(f"Enter a new target, or press Enter to keep "
                                                      f"{service_targets[target - 1]} as target: ")
                    if target_name != "":
                        service_targets[target - 1] = str(target_name)
                    if target == 6:
                        new_domain: str = session.prompt(f"Enter a domain name, or press Enter to keep {dns_query}: ")
                        if new_domain != "":
                            dns_query = new_domain
                    interval: int = session.prompt(f"Enter an interval in seconds, or press Enter to keep "
                                                   f"{targets_intervals[target - 1]} as interval: ")
                    if interval != "":
                        targets_intervals[target - 1] = int(interval)
                    if 6 < target < 9:
                        port: int = session.prompt(f"Enter a port number, or press Enter to keep current port: ")
                        if port != "":
                            if target == 7:
                                tcp_port = int(port)
                            else:
                                udp_port = int(port)
                    print_configurations(service_targets, dns_query, targets_intervals, tcp_port, udp_port)
            ping_thread: threading.Thread = threading.Thread(target=ping, args=(stop_event, service_targets,
                                                                                targets_intervals))
            traceroute_thread: threading.Thread = threading.Thread(target=traceroute, args=(stop_event, service_targets,
                                                                                            targets_intervals))
            http_thread: threading.Thread = threading.Thread(target=http, args=(stop_event, service_targets,
                                                                                targets_intervals))
            https_thread: threading.Thread = threading.Thread(target=https, args=(stop_event, service_targets,
                                                                                  targets_intervals))
            ntp_thread: threading.Thread = threading.Thread(target=ntp, args=(stop_event, service_targets,
                                                                              targets_intervals))
            dns_thread: threading.Thread = threading.Thread(target=dns, args=(stop_event, service_targets,
                                                                              targets_intervals, dns_query))
            tcp_thread: threading.Thread = threading.Thread(target=tcp, args=(stop_event, service_targets,
                                                                              targets_intervals, tcp_port))
            udp_thread: threading.Thread = threading.Thread(target=udp, args=(stop_event, service_targets,
                                                                              targets_intervals, udp_port))
            tcp_server_thread: threading.Thread = threading.Thread(target=tcp_s, args=())
            server_open = True
            ping_thread.start()
            traceroute_thread.start()
            http_thread.start()
            https_thread.start()
            ntp_thread.start()
            dns_thread.start()
            tcp_thread.start()
            udp_thread.start()
            tcp_server_thread.start()
            while is_running:
                # Using prompt-toolkit for input with auto-completion
                user_input: str = session.prompt("\nType 'echo' to test the echo server, or exit to quit: ")

                # This is where you create the actions for your commands
                if user_input == "echo":
                    if not server_open:
                        print("You closed the server!")
                    else:
                        echo_message = session.prompt("\nEnter message to send to echo server. Send 'Goodbye' "
                                                      "to kill server: ")
                        tcp_client.tcp_client(echo_message)
                        if echo_message == "Goodbye":
                            server_open = False
                if user_input == "exit":
                    print("Preparing to exit application... Please be patient\n")
                    is_running = False

    finally:
        # Signal the worker thread to stop and wait for its completion
        stop_event.set()
        ping_thread.join()
        traceroute_thread.join()
        http_thread.join()
        https_thread.join()
        ntp_thread.join()
        dns_thread.join()
        tcp_thread.join()
        udp_thread.join()
        if server_open:
            tcp_client.tcp_client("Goodbye")
            tcp_server_thread.join()


if __name__ == "__main__":
    main()
