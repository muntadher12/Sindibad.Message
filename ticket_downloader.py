orders = [
    266496, 266499, 266527, 266657, 266726, 266735, 266801, 266845, 266854,
    266862, 266937, 267076, 267130, 267214, 267279, 267294, 267293, 267312,
    267320, 267326, 267331, 267336, 267374, 267391, 267437, 267447, 267460,
    267662, 267663, 267726, 267734, 267773, 267735, 267807, 267846, 267866,
    268077, 268075, 268171, 268168, 268219, 268222, 268235, 268238, 268326,
    268335, 268388, 268501, 268538, 268570, 268608, 268621, 268680, 268724,
    268786, 268824, 268917, 268962, 268996, 268990, 269120, 269159, 266669,
    266830, 268143, 268971
]

import subprocess
import os
import time
import json

# Complete headers that bypass Cloudflare protection
HEADERS = """  -H 'ab-channel: backoffice' \
  -H 'accept: application/pdf' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'accept-token: 8SYakWxkhK5sGAg3ypEt5' \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1lZC5hQHNpbmRpYmFkLmlxIiwianRpIjoiMmQzNzE3YmEtZmRiMC00NTk1LWE5MTYtMTNlZWIwZWU4ZDAzIiwiaWF0IjoxNzUyMTMwOTExLCJyb2wiOiJhcGlfYWNjZXNzIiwiaWQiOiJlMmM2ODhiZi01NDZjLTQ3MTgtODI1ZC1hNTRkYzMwYTg4MTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6ImUyYzY4OGJmLTU0NmMtNDcxOC04MjVkLWE1NGRjMzBhODgxNCIsInVzZXJfdW5pcXVlX251bWJlciI6IjgzMDU4OSIsInByZWZlcnJlZF91c2VybmFtZSI6ImFobWVkLmFAc2luZGliYWQuaXEiLCJsb2dpbl90eXBlIjoiRW1haWwiLCJwaG9uZV9udW1iZXIiOiIrOTY0NzcwOTQyNDM3MSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6WyJ1c2Vyc0Nhbk1lbnRpb24iLCJhY2NvdW50aW5nIiwicGFuZWxVc2VyIl0sIm5iZiI6MTc1MjEzMDkxMCwiZXhwIjoxNzUyNzM1NzEwLCJpc3MiOiJ3ZWJBcGkiLCJhdWQiOiJodHRwOi8vYXV0aGVudGljYXRpb24tc2VydmljZS5zaW5kaWJhZC5hcHAvIn0.YdX4lXSR9ttXuTakHmIAL8F3jvC8Ybrk-oGV5voq348' \
  -H 'cache-control: no-cache' \
  -H 'device: web' \
  -H 'language: en' \
  -H 'origin: https://panel.sindibad.iq' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://panel.sindibad.iq/' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'timezone: Asia/Baghdad' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'"""

ORDER_HEADERS = """  -H 'ab-channel: backoffice' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'accept-token: 8SYakWxkhK5sGAg3ypEt5' \
  -H 'authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhaG1lZC5hQHNpbmRpYmFkLmlxIiwianRpIjoiMmQzNzE3YmEtZmRiMC00NTk1LWE5MTYtMTNlZWIwZWU4ZDAzIiwiaWF0IjoxNzUyMTMwOTExLCJyb2wiOiJhcGlfYWNjZXNzIiwiaWQiOiJlMmM2ODhiZi01NDZjLTQ3MTgtODI1ZC1hNTRkYzMwYTg4MTQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6ImUyYzY4OGJmLTU0NmMtNDcxOC04MjVkLWE1NGRjMzBhODgxNCIsInVzZXJfdW5pcXVlX251bWJlciI6IjgzMDU4OSIsInByZWZlcnJlZF91c2VybmFtZSI6ImFobWVkLmFAc2luZGliYWQuaXEiLCJsb2dpbl90eXBlIjoiRW1haWwiLCJwaG9uZV9udW1iZXIiOiIrOTY0NzcwOTQyNDM3MSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6WyJ1c2Vyc0Nhbk1lbnRpb24iLCJhY2NvdW50aW5nIiwicGFuZWxVc2VyIl0sIm5iZiI6MTc1MjEzMDkxMCwiZXhwIjoxNzUyNzM1NzEwLCJpc3MiOiJ3ZWJBcGkiLCJhdWQiOiJodHRwOi8vYXV0aGVudGljYXRpb24tc2VydmljZS5zaW5kaWJhZC5hcHAvIn0.YdX4lXSR9ttXuTakHmIAL8F3jvC8Ybrk-oGV5voq348' \
  -H 'cache-control: no-cache' \
  -H 'device: web' \
  -H 'language: en' \
  -H 'origin: https://panel.sindibad.iq' \
  -H 'pragma: no-cache' \
  -H 'priority: u=1, i' \
  -H 'referer: https://panel.sindibad.iq/' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'timezone: Asia/Baghdad' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'"""

# Loop through each coreOrderId and download the combined ticket PDF
for core_order_id in orders:
    print(f"\n--- Processing coreOrderId {core_order_id} ---")
    
    # Step 1: Get order data to extract order info and passengers
    order_data_command = f"curl -s 'https://api.sindibad.iq/api/v1/international-flight/order/{core_order_id}' \\\n{ORDER_HEADERS}"
    
    try:
        print(f"🔍 Fetching order data for coreOrderId {core_order_id}...")
        order_result = subprocess.run(order_data_command, shell=True, capture_output=True, text=True)
        
        if order_result.returncode != 0:
            print(f"✗ Failed to fetch order data: {order_result.stderr}")
            continue
            
        # Parse the JSON response
        try:
            order_data = json.loads(order_result.stdout)
            
            if not order_data.get('success', False):
                print(f"✗ API returned error: {order_data.get('error', 'Unknown error')}")
                continue
                
            # Extract order info
            order_id = order_data['result']['id']
            status = order_data['result'].get('status', 'Unknown')
            passengers = order_data['result'].get('passengers', [])
            
            print(f"✓ Order ID: {order_id}, Status: {status}, Passengers: {len(passengers)}")
            
            # Show passenger info for verification
            passenger_names = []
            total_tickets = 0
            for passenger in passengers:
                passenger_name = f"{passenger.get('firstname', '')} {passenger.get('surname', '')}"
                passenger_names.append(passenger_name)
                tickets = passenger.get('tickets', [])
                total_tickets += len(tickets)
                for ticket in tickets:
                    ticket_number = ticket.get('ticketNumber', 'N/A')
                    ticket_status = ticket.get('ticketStatus', 'Unknown')
                    print(f"  Passenger: {passenger_name} | Ticket: {ticket_number} | Status: {ticket_status}")
            
            if total_tickets == 0:
                print(f"✗ No tickets found in order {core_order_id}")
                continue
                
        except json.JSONDecodeError:
            print(f"✗ Failed to parse order data JSON")
            print(f"Response: {order_result.stdout[:200]}...")
            continue
        except KeyError as e:
            print(f"✗ Missing expected field in order data: {e}")
            continue
    
    except Exception as e:
        print(f"✗ Exception while fetching order data: {str(e)}")
        continue
    
    # Step 2: Download the combined ticket PDF using ORDER ID (not individual ticket IDs)
    print(f"\n📥 Downloading combined tickets for order {order_id} (coreOrderId: {core_order_id})")
    print(f"    Expected passengers: {', '.join(passenger_names)}")
    
    # Create filename with simple format
    filename = f"orderID_{core_order_id}.pdf"
    
    # Download using ORDER ID (this was the key fix!)
    curl_command = f"curl -s 'https://api.sindibad.iq/api/v1/international-flight/order/ticket/download/{order_id}' \\\n{HEADERS} \\\n  --output {filename}"
    
    try:
        # Execute the curl command
        result = subprocess.run(curl_command, shell=True, capture_output=True, text=True)
        
        # Check if file was created and its size
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            
            if file_size > 0:
                print(f"✓ Successfully downloaded {filename} ({file_size} bytes)")
                
                # Quick check if it's actually a PDF
                with open(filename, 'rb') as f:
                    first_bytes = f.read(10)
                    if first_bytes.startswith(b'%PDF'):
                        print("✓ File appears to be a valid PDF")
                        print(f"✓ This should contain tickets for: {', '.join(passenger_names)}")
                    else:
                        print("⚠ File doesn't start with PDF header, might be an error page")
                        # Let's see what the content actually is
                        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                            content_preview = f.read(500)
                            print(f"Content preview: {content_preview[:200]}...")
            else:
                print(f"✗ File {filename} was created but is empty (0 bytes)")
                # Remove empty file
                os.remove(filename)
        else:
            print(f"✗ No file was created for order {core_order_id}")
            
        if result.returncode != 0:
            print(f"✗ Curl returned error code {result.returncode}")
            if result.stderr:
                print(f"Error details: {result.stderr}")
    
    except Exception as e:
        print(f"✗ Exception occurred during download: {str(e)}")
    
    # Delay between orders
    print(f"\nCompleted processing order {core_order_id}. Waiting 3 seconds before next order...")
    time.sleep(1)

print("\n🎉 All downloads completed!")