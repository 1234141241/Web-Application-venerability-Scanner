import requests
from bs4 import BeautifulSoup


def scan_sql_injection(url, param):
    payload = "' OR '1'='1"  # Basic SQL Injection Payload
    test_url = f"{url}?{param}={payload}"
    response = requests.get(test_url)
    if "error" in response.text.lower() or "mysql" in response.text.lower():
        print(f"[!] SQL Injection vulnerability detected in parameter: {param}")
    else:
        print(f"[-] No SQL Injection vulnerability detected in parameter: {param}")


def scan_xss(url, param):
    payload = "<script>alert('XSS')</script>"
    test_url = f"{url}?{param}={payload}"
    response = requests.get(test_url)
    if payload in response.text:
        print(f"[!] XSS vulnerability detected in parameter: {param}")
    else:
        print(f"[-] No XSS vulnerability detected in parameter: {param}")


def extract_forms(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')
    return forms


def scan_forms(url):
    forms = extract_forms(url)
    for form in forms:
        action = form.get('action')
        method = form.get('method', 'get').lower()
        inputs = form.find_all('input')
        for input_tag in inputs:
            input_name = input_tag.get('name')
            if input_name:
                scan_sql_injection(url, input_name)
                scan_xss(url, input_name)


def main():
    target_url = input("Enter the target URL: ")
    scan_sql_injection(target_url, "test")
    scan_xss(target_url, "test")
    scan_forms(target_url)


if __name__ == "__main__":
    main()
