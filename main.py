from mcp.server.fastmcp import FastMCP,Image
from contextlib import asynccontextmanager
from argparse import ArgumentParser
from src.mobile import Mobile
from textwrap import dedent
import asyncio
import sys

parser = ArgumentParser()
parser.add_argument('--emulator',action='store_true',help='Use the emulator')
args = parser.parse_args()

instructions=dedent('''
Android MCP server provides tools to interact directly with the Android device, 
thus enabling to operate the mobile device like an actual USER.''')

@asynccontextmanager
async def lifespan(app: FastMCP):
    """Runs initialization code before the server starts and cleanup code after it shuts down."""
    # Removed unnecessary sleep to reduce startup time
    yield

mcp=FastMCP(name="Android-MCP",instructions=instructions)

# Initialize device connection with error handling
try:
    print(f"[Android-MCP] Connecting to {'emulator' if args.emulator else 'device'}...", file=sys.stderr, flush=True)
    mobile=Mobile(device=None if not args.emulator else 'emulator-5554')
    device=mobile.get_device()
    print(f"[Android-MCP] Device object created, getting info...", file=sys.stderr, flush=True)
    device_info = device.info
    print(f"[Android-MCP] Successfully connected to {device_info.get('productName', 'Unknown device')}", file=sys.stderr, flush=True)
    print(f"[Android-MCP] Device ready, MCP server starting...", file=sys.stderr, flush=True)
except Exception as e:
    print(f"[Android-MCP] Failed to connect to Android device: {e}", file=sys.stderr, flush=True)
    print("[Android-MCP] Please ensure:", file=sys.stderr, flush=True)
    print("[Android-MCP] 1. Android device is connected or emulator is running", file=sys.stderr, flush=True)
    print("[Android-MCP] 2. USB debugging is enabled", file=sys.stderr, flush=True)
    print("[Android-MCP] 3. Run 'adb devices' to verify device is visible", file=sys.stderr, flush=True)
    sys.exit(1)

@mcp.tool(name='Click-Tool',description='Click on a specific cordinate')
def click_tool(x:int,y:int):
    try:
        device.click(x,y)
        return f'Clicked on ({x},{y})'
    except Exception as e:
        raise RuntimeError(f'Failed to click on ({x},{y}): {str(e)}')

@mcp.tool('State-Tool',description='Get the state of the device. Optionally includes visual screenshot when use_vision=True. Use max_elements to limit output size (default: 20, max: 50 for vision). When use_vision=True, max_elements is automatically reduced to keep response size manageable.')
def state_tool(use_vision:bool=False, max_elements:int=20):
    try:
        # When using vision mode, reduce max_elements to keep response size manageable
        if use_vision:
            max_elements = min(max(1, max_elements), 15)
            print(f"[State-Tool] Vision mode detected, limiting to {max_elements} elements", file=sys.stderr, flush=True)
        else:
            max_elements = min(max(1, max_elements), 100)
        print(f"[State-Tool] Starting, use_vision={use_vision}, max_elements={max_elements}", file=sys.stderr, flush=True)
        mobile_state=mobile.get_state(use_vision=use_vision, max_elements=max_elements)
        print(f"[State-Tool] Got state, formatting response...", file=sys.stderr, flush=True)
        result = [mobile_state.tree_state.to_string()]+([Image(data=mobile_state.screenshot,format='JPEG')] if use_vision else [])
        print(f"[State-Tool] Success", file=sys.stderr, flush=True)
        return result
    except Exception as e:
        print(f"[State-Tool] Error: {str(e)}", file=sys.stderr, flush=True)
        raise RuntimeError(f'Failed to get device state: {str(e)}')

@mcp.tool(name='Long-Click-Tool',description='Long click on a specific cordinate')
def long_click_tool(x:int,y:int):
    try:
        device.long_click(x,y)
        return f'Long Clicked on ({x},{y})'
    except Exception as e:
        raise RuntimeError(f'Failed to long click on ({x},{y}): {str(e)}')

@mcp.tool(name='Swipe-Tool',description='Swipe on a specific cordinate')
def swipe_tool(x1:int,y1:int,x2:int,y2:int):
    try:
        device.swipe(x1,y1,x2,y2)
        return f'Swiped from ({x1},{y1}) to ({x2},{y2})'
    except Exception as e:
        raise RuntimeError(f'Failed to swipe from ({x1},{y1}) to ({x2},{y2}): {str(e)}')

@mcp.tool(name='Type-Tool',description='Type text into the currently focused input field or at specific coordinates')
def type_tool(text:str,x:int=None,y:int=None,clear:bool=False):
    try:
        # Click on coordinates if provided to focus the input field
        if x is not None and y is not None:
            device.click(x, y)
        device.set_fastinput_ime(enable=True)
        device.send_keys(text=text,clear=clear)
        return f'Typed "{text}"' + (f' at ({x},{y})' if x and y else '')
    except Exception as e:
        raise RuntimeError(f'Failed to type text: {str(e)}')

@mcp.tool(name='Drag-Tool',description='Drag from location and drop on another location')
def drag_tool(x1:int,y1:int,x2:int,y2:int):
    try:
        device.drag(x1,y1,x2,y2)
        return f'Dragged from ({x1},{y1}) and dropped on ({x2},{y2})'
    except Exception as e:
        raise RuntimeError(f'Failed to drag from ({x1},{y1}) to ({x2},{y2}): {str(e)}')

@mcp.tool(name='Press-Tool',description='Press on specific button on the device')
def press_tool(button:str):
    try:
        device.press(button)
        return f'Pressed the "{button}" button'
    except Exception as e:
        raise RuntimeError(f'Failed to press "{button}" button: {str(e)}')

@mcp.tool(name='Notification-Tool',description='Access the notifications seen on the device')
def notification_tool():
    try:
        device.open_notification()
        return 'Accessed notification bar'
    except Exception as e:
        raise RuntimeError(f'Failed to access notification bar: {str(e)}')

@mcp.tool(name='Wait-Tool',description='Wait for a specific amount of time')
def wait_tool(duration:int):
    try:
        device.sleep(duration)
        return f'Waited for {duration} seconds'
    except Exception as e:
        raise RuntimeError(f'Failed to wait: {str(e)}')

@mcp.tool(name='Restart-Tool',description='Restart the device connection. Use this when the device becomes unresponsive or after timeout errors.')
def restart_tool():
    global mobile, device
    try:
        print(f"[Restart-Tool] Restarting device connection...", file=sys.stderr, flush=True)
        # Reconnect to device
        mobile = Mobile(device=None if not args.emulator else 'emulator-5554')
        device = mobile.get_device()
        device_info = device.info
        print(f"[Restart-Tool] Successfully reconnected to {device_info.get('productName', 'Unknown device')}", file=sys.stderr, flush=True)
        return f"Device connection restarted successfully. Connected to {device_info.get('productName', 'Unknown device')}"
    except Exception as e:
        print(f"[Restart-Tool] Failed to restart: {str(e)}", file=sys.stderr, flush=True)
        raise RuntimeError(f'Failed to restart device connection: {str(e)}')

if __name__ == '__main__':
    mcp.run()