# Proxy Checker

This script is a proxy checker that verifies the availability and type of proxies. It distinguishes between working HTTP/HTTPS proxies, SOCKS4 proxies, and SOCKS5 proxies. Below is a detailed explanation of the script's components:

1. Importing Libraries

* urllib2: Used for handling network requests (in Python 2; this would be replaced by urllib.request in Python 3).
* threading: Provides multithreading capabilities to perform concurrent proxy checks.
* socket: Used for low-level network operations, such as connecting to a proxy server.
* sys: Provides system-level operations like exiting the script.
* time: Adds delays between actions or measures elapsed time.
* os: Used for file operations, like checking if an output file already exists.

2. Logging Functions

These provide color-coded messages for different log levels:

* error(msg): Logs error messages.
* alert(msg): Logs informational messages.
* action(msg): Logs success or progress messages.
* errorExit(msg): Exits the program with a fatal error message.

3. Proxy Type Check

* isSocks(host, port, soc):
Determines whether the proxy supports SOCKS4 or SOCKS5 protocols.
* Calls socks4 or socks5 for detailed checks.
* socks4(host, port, soc):
Sends a SOCKS4 handshake packet to the proxy server and checks the response.
* socks5(host, port, soc):
Sends a SOCKS5 handshake packet and verifies the proxy's response.
If the proxy is not SOCKS4/5, it may still be a functional HTTP/HTTPS proxy.

4. Proxy Alive Check
* isAlive(pip, timeout):
Tests if an HTTP/HTTPS proxy is functional by sending a request to Google.
If the proxy responds within the timeout, it is considered working.

5. Multithreaded Proxy Checking
checkProxies():
Runs in each thread to process proxies from the toCheck list.
For each proxy:
Extracts the host and port.
Validates the port range (0–65535).
Checks if it is a SOCKS proxy (isSocks).
If not, checks if it is a working HTTP/HTTPS proxy (isAlive).
Saves working proxies to the output file.

6. Main Script Logic
User Inputs:

Proxy list: A file containing proxies in IP:PORT format.
Output file: A file to save verified working proxies.
Number of threads: Specifies how many threads to run for parallel checks.
Timeout: Time (in seconds) to wait for a proxy's response.
Proxy Initialization:

Reads the proxy list and adds proxies to the toCheck list.
Checks if the output file exists and confirms overwriting if necessary.
Thread Management:

Creates a number of threads (threadsnum), each running checkProxies.
Threads are started with a small delay to avoid overwhelming resources.
Monitoring Progress:

Periodically checks the status of active threads, remaining proxies, and counts of verified proxies.

7. Outputs

* The script logs progress to the console and saves verified proxies to the output file. It categorizes:
* HTTP/HTTPS Proxies: Verified through isAlive.
* SOCKS4/5 Proxies: Verified through socks4 and socks5.

8. Limitations

* Python 2: The script uses Python 2, which is outdated. Modifications are needed to make it compatible with Python 3.
* Error Handling: Limited handling of edge cases like malformed proxy entries.
* Performance: Large proxy lists may still cause delays if not optimized further.

What the Script Does

* Loads a list of proxies from a file.
* Checks each proxy's type and availability using multiple threads.
* Saves working proxies to an output file.
* Provides real-time updates about progress and results.
